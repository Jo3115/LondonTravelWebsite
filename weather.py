"""Weather Module
Handles the API requests and information received pertaining to the weather
using Open Weather API.
"""


__version__ = '1.0'
__author__ = 'Joshua Mugglestone'


import requests
import datetime
import pprint

def get_weather():
    """Gets the current weather according to Open Weather API"""
    response = requests.get('http://api.openweathermap.org/data/2.5/weather?'
                            'q=London,uk&'
                            'units=metric&'
                            'appid=')
    data = response.json()
    return data


def get_weather_forcast():
    """Gets the weather forecast according to Open Weather API"""
    response = requests.get('http://api.openweathermap.org/data/2.5/forecast?'
                            'q=London,uk&'
                            'units=metric&'
                            'appid=')
    data = response.json()
    return data


def interpret_weather_forcast():
    """interpretes the weather forecasted supplied by the API call and
    converts it into list format ordered in days and containing converted
    time values so they are more readible for the user.
    """
    data = (get_weather_forcast())
    forcast = []
    current_date = datetime.datetime.now()
    current_day = int(current_date.day)
    day = []
    for i in data['list']:
        date = datetime.datetime.fromtimestamp(i['dt']).strftime('%c')
        date_time = (date.split(" "))
        try:
            date = int(date_time[3])
            date_time.remove('')
        except ValueError:
            date = int(date_time[2])
        entry = [i['main'], i['weather'], i['wind'],date_time]
        if date == (current_day):
            day.append(entry)
        else:
            if day:
                forcast.append(day)
            day = []
            current_day += 1
            day.append(entry)
    forcast.append(day)
    return forcast


if __name__=='__main__':
    pprint.pprint(interpret_weather_forcast())
