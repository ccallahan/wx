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
                zone = GetNWSZone(latlong)
                forecast = GetNWSForecast(zone)
                return {"body": OutputNWSForecast(int(period), forecast)}
            else:
                return {"body": "ERR: Bad Forecast Period"}
        else:
            return {"body": "ERR: Bad LatLong"}
    else:
        return {"body": "ERR: No command given."}


def GetNWSZone(args):
    latlong = str(args)

    jsonraw = requests.get("https://api.weather.gov/zones?point=" + latlong)
    jsontext = jsonraw.text

    data = json.loads(jsontext)
    zone = data['features'][2]['properties']['id']
    return zone

def GetNWSForecast(zone):
    zone = zone

    jsonraw = requests.get('https://api.weather.gov/zones/county/' + zone + '/forecast')
    jsontext = jsonraw.text

    data = json.loads(jsontext)
    forecast = data['properties']
    return forecast

def OutputNWSForecast(period, forecast):
    forecast = forecast
    period = period - 1
    forecast_msg = forecast['periods'][period]['name'] + ': ' + forecast['periods'][period]['detailedForecast']
    return str(forecast_msg)



if __name__=="__main__":
    main()