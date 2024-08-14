import datetime as dt
import pkgutil

import pandas as pd

import quatex.market.assetinfo as ai
import quatex.market.marketcalender as mc
import quatex.market.providers.marketdataapp as mda
import quatex.utility.config as cfg

listing_data = pkgutil.get_data(__package__, 'data/listing_status.csv')
listing_dict = {}
for row in listing_data.decode("utf-8").splitlines():
    if row.startswith("symbol"):
        continue
    cols = row.split(",")
    listing_dict[cols[0].strip()] = cols[4].strip()


class MarketDataReader:
    def __init__(self, token: str):
        self.token = token

    def read(self, symbol: str, interval: str, start: str | dt.date = None, end: str | dt.date = None) -> pd.DataFrame:
        symbol_dir = cfg.get_hist_dir().joinpath(symbol.lower())
        data_file = symbol_dir.joinpath(symbol.lower() + "-" + interval + ".csv")
        meta_file = symbol_dir.joinpath("." + symbol.lower() + "-" + interval + ".csv.meta")
        columns = ["datetime", "open", "high", "low", "close", "volume"]

        # Format start and end and save to orig_start and orig_end
        orig_start = None
        if start is not None:
            orig_start = dt.date.fromisoformat(start) if isinstance(start, str) else start

        orig_end = None
        if end is not None:
            orig_end = dt.date.fromisoformat(end) if isinstance(end, str) else end

        fetch_start = self.__deduce_fetch_start(symbol, meta_file)
        fetch_end = self.__deduce_fetch_end(symbol, end)

        # Fetch delta data from remote if not up-to-date
        if fetch_start <= fetch_end:
            date_pairs = []
            if interval.endswith("m") or interval.endswith("H") or interval.endswith("h"):
                loop_start = fetch_start
                while True:
                    loop_next_year = dt.date(loop_start.year + 1, 1, 1)
                    loop_end = loop_next_year + dt.timedelta(days=-1)
                    loop_end = fetch_end if loop_end > fetch_end else loop_end
                    date_pairs.append([loop_start, loop_end])
                    if loop_end >= fetch_end:
                        break
                    loop_start = loop_next_year
            else:
                date_pairs.append([fetch_start, fetch_end])

            for date_pair in date_pairs:
                pair_start = date_pair[0]
                pair_end = date_pair[1]
                print(
                    "[{}-{}] Fetching data from remote service: start={}, end={}".format(
                        symbol, interval, pair_start, pair_end
                    )
                )

                rows = mda.get_candles(symbol, interval, pair_start, pair_end, self.token)

                # Ensure symbol directory and file exists
                if not symbol_dir.exists():
                    symbol_dir.mkdir(parents=True, exist_ok=True)

                if not data_file.exists():
                    data_file.write_text(",".join(columns) + "\n")

                # Append rows to local file
                with open(data_file, mode="a") as file:
                    for row in rows:
                        file.write(",".join([str(c) for c in row]) + "\n")

                if len(rows) > 0:
                    meta_file.write_text(rows[-1][0])

                print(
                    "[{}-{}] Data fetching completed: start={}, end={}, rows={}".format(
                        symbol, interval, pair_start, pair_end, len(rows)
                    )
                )

        # Read all from local file
        rows = []
        with open(data_file, "r") as file:
            while True:
                line = file.readline()

                if line.startswith("datetime"):
                    continue

                if len(line.strip()) == 0:
                    break

                line_cols = line.split(",")
                line_date = dt.datetime.fromisoformat(line_cols[0]).date()

                included = False
                if orig_start is None and orig_end is None:
                    included = True
                elif orig_start is None and orig_end is not None:
                    if line_date <= orig_end:
                        included = True
                elif orig_start is not None and orig_end is None:
                    if line_date >= orig_start:
                        included = True
                else:
                    if orig_start <= line_date <= orig_end:
                        included = True

                if included:
                    rows.append([
                        dt.datetime.fromisoformat(line_cols[0]),
                        float(line_cols[1]),
                        float(line_cols[2]),
                        float(line_cols[3]),
                        float(line_cols[4]),
                        float(line_cols[5]),
                    ])

        return pd.DataFrame(rows, columns=columns)

    def __deduce_fetch_start(self, symbol, meta_file):
        if not meta_file.exists():
            ipo_date = listing_dict.get(symbol)
            result = dt.date.fromisoformat(ipo_date) if ipo_date is not None else None
            if result is None:
                raise Exception("The list date of {} is null".format(symbol))
        else:
            last_date = dt.datetime.fromisoformat(meta_file.read_text()).date()
            result = last_date + dt.timedelta(days=1)

        while mc.is_holiday(result):
            result = result + dt.timedelta(days=1)

        return result

    def __deduce_fetch_end(self, symbol, end):
        if end is None:
            local_today = dt.datetime.now(tz=ai.get_time_zone(symbol)).date()
            result = local_today + dt.timedelta(days=-1)
        else:
            result = dt.date.fromisoformat(end) if isinstance(end, str) else end

        while mc.is_holiday(result):
            result = result + dt.timedelta(days=-1)
        return result
