import requests
import datetime


"""Transport Module
Controlls the Api Calls For The Transport pages (taxi, train, buss) and the 
information they return.
"""


__version__ = '1.1'
__author__ = 'Joshua Mugglestone'


def taxi():
    """Calls the Taxi API from TFL and Returns the Information """
    params = {'lat': '51.5074',
              'lon': '0.1278',
              'key': ''}
    return requests.get('https://api.tfl.gov.uk/Cabwise/search?',
                        params).json()


def get_train_stations():
    """Imports a List of Stations From A CSV file to be used as the station
    options in a drop down.
    """
    file = open('station_names.csv', 'r')
    list = []
    for i in file:
        name = i.split('\t')
        code = name[1].split('\n')[0]
        list.append(name[0] + ' ' + code)
    return list


def train_timetable(station, date='', time=''):
    """Calls the Transport Api Train API To Get a train time table and
    returns it
    """
    station = station.split(' ')[-1]
    params = {'app_id': 'af247995',
              'app_key': '',
              'train_status': 'passenger'}
    return requests.get(
        'https://transportapi.com/v3/uk/train/station/{0}/{1}/{2}/timetable.'
        'json?'.format(station, date, time), params).json()


def train_information(url):
    """Calls the Transport Api Train API to get more information on a specific
    train and Returns It.
    """
    url = url.split('?')[0]
    params = {'app_id': 'af247995',
              'app_key': ''}
    return requests.get(url, params).json()


def get_buss_stop_list():
    """Imports a List of Buss Stops From A CSV file to be used as the station
    options in a drop down.
    """
    file = open('bus_stops.csv', 'r')
    list = []
    for line in file:
        line = line.split(',')
        try:
            line_list = [line[2], line[3]]
            list.append(line_list)
        except IndexError:
            pass
    del list[0]
    return list


def get_buss_code(stop):
    """Checks the Users input against the list of Buss Stop Codes and Returns
    Them
    """
    list = get_buss_stop_list()
    for s in list:
        if s[1] == stop:
            return s[0]
    return False


def buss_timetable(stop, date='', time=''):
    """Calls the Transport Api Buss API To Get a Buss time table for a
    specific stop and returns it
    """
    code = get_buss_code(stop)
    if code is False:
        return False
    print(code)
    params = {'app_id': 'af247995',
              'app_key': '',
              'group': 'route'}
    return requests.get(
        'https://transportapi.com/v3/uk/bus/stop/{0}/{1}/{2}/timetable.json?'
            .format(code, date, time), params).json()


def convert_buss_timetable(timetable):
    """Gets the Buss Time Table And Orders It in Date Order."""
    entry_list = []
    for rout in timetable['departures']:
        for buss in (timetable['departures'][rout]):
            date = datetime.datetime.strptime(buss['aimed_departure_time'],
                                              '%H:%M')
            entry_list.append([date, buss])
    entry_list.sort(key=lambda r: r[0])
    return entry_list
