from os import environ
import requests
import json

def main(args):
    command = args.get("cmd", "false")
    if command == "forecast":
        latlong = args.get("latlong", "false")
        if latlong != "false":
            period = args.get("period", "false")
            if period != "false":
                zone = GetNWSForecastZone(latlong)
                forecast = GetNWSForecast(zone)
                return {"body": OutputNWSForecast(int(period), forecast)}
                #return {"body": forecast}
            else:
                return {"body": "ERR: Bad Forecast Period"}
        else:
            return {"body": "ERR: Bad LatLong"}
    elif command == "alerts":
        latlong = args.get("latlong", "false")
        if latlong != "false":
            zone = GetNWSAlertZone(latlong)
            alerts = GetNWSAlerts(zone)
            return {"body": GetNWSAlertCount(alerts)}
    else:
        return {"body": "ERR: No command given."}


def GetNWSForecastZone(args):
    latlong = str(args)

    jsonraw = requests.get("https://api.weather.gov/zones?point=" + latlong)
    jsontext = jsonraw.text

    data = json.loads(jsontext)
    zone_data = data['features']

    for i in zone_data:
        if i['properties']['type'] == 'public':
            zone = i['properties']['id']
            return str(zone)

    return zone

def GetNWSAlertZone(args):
    latlong = str(args)

    jsonraw = requests.get("https://api.weather.gov/zones?point=" + latlong)
    jsontext = jsonraw.text

    data = json.loads(jsontext)
    zone_data = data['features']

    for i in zone_data:
        if i['properties']['type'] == 'county':
            zone = i['properties']['id']
            return str(zone)

    return zone

def GetNWSForecast(zone):
    zone = zone

    jsonraw = requests.get('https://api.weather.gov/zones/county/' + zone + '/forecast')
    jsontext = jsonraw.text

    data = json.loads(jsontext)
    forecast = data['properties']
    return forecast

def GetNWSAlerts(zone):
    zone = zone

    jsonraw = requests.get('https://api.weather.gov/alerts/active/zone/' + zone)
    jsontext = jsonraw.text

    data = json.loads(jsontext)
    alerts = data['features']
    return alerts

def GetNWSAlertCount(alerts):
    count = 0

    for i in alerts:
        count = count + 1
    return count

def OutputNWSForecast(period, forecast):
    forecast = forecast
    forecast_period = ""
    forecast_desc = ""

    for i in forecast["periods"]:
        if i["number"] == period:
            forecast_period = i["name"]
            forecast_desc = i["detailedForecast"]

    forecast_msg = forecast_period + ': ' + forecast_desc
    return str(forecast_msg)


if __name__=="__main__":
    main()