import datetime as dt

import requests

import quatex.market.assetinfo as ai


def get_candles(symbol: str, interval: str, start: dt.date, end: dt.date, token: str):
    url = "https://api.marketdata.app/v1/stocks/candles/{resolution}/{symbol}"
    url = url.format(resolution=interval.replace("m", ""), symbol=symbol)
    response = requests.get(url, params={'from': start, 'to': end, 'adjustsplits': 'true'}, headers={
        'Authorization': 'Bearer ' + token
    })
    result = response.json()

    rows = []
    if result["s"].casefold() == "ok".casefold():
        for i in range(len(result["t"])):
            rows.append([
                dt.datetime.fromtimestamp(result["t"][i], tz=dt.timezone.utc).astimezone(
                    ai.get_time_zone(symbol)).isoformat(),
                result["o"][i],
                result["h"][i],
                result["l"][i],
                result["c"][i],
                result["v"][i],
            ])
    return rows
