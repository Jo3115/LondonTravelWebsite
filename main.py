from flask import Flask, render_template, url_for, request, redirect
import os
import pprint
import weather
import places
import news
import transport


"""Main Module For Flask Web App
Creates and runs the app and contains all of the appropriate app routes
"""


__version__ = '1.1'
__author__ = 'Joshua Mugglestone'


app = Flask(__name__)


@app.route('/')
def home_page():
    """Displays The Homepage"""
    return render_template('home.html',
                           weather_icon=weather.get_weather(),
                           news=news.short_list_news())


@app.route('/weather')
def weather_page():
    """Displays The Weather Page"""
    try:
        day_number = int(request.args.get('day'))
    except TypeError:
        day_number = 0
    return render_template('weather.html',
                           title='weather',
                           weather_data=weather.interpret_weather_forcast(),
                           day_number=day_number,
                           weather_icon=weather.get_weather())


@app.route('/taxi')
def taxi_page():
    """Displays The Taxi Page"""
    return render_template('taxi.html',
                           title='taxi',
                           weather_icon=weather.get_weather(),
                           taxi=transport.taxi()['Operators']['OperatorList'])


@app.route('/train', methods=['GET', 'POST'])
def train_page():
    """Displays The Train Page"""
    timetable = ''
    if request.method == 'POST':
        station = request.form.get('station')
        date = request.form.get('date')
        time = request.form.get('time')
        timetable = transport.train_timetable(station, date, time)
    return render_template('train.html',
                           title='train',
                           weather_icon=weather.get_weather(),
                           train_stations=transport.get_train_stations(),
                           timetable=timetable)


@app.route('/train/info', methods=['GET', 'POST'])
def train_page_info():
    """Displays More Information For The Train Page"""
    url = request.args.get('url')
    if url:
        print(url)
        information = transport.train_information(url)
        pprint.pprint(information)
        return render_template('train_info.html',
                               title='train',
                               weather_icon=weather.get_weather(),
                               train_stations=transport.get_train_stations(),
                               information=information)
    return redirect(url_for('train_page'))


@app.route('/buss', methods=['GET', 'POST'])
def buss_page():
    """Displays The Buss Page"""
    timetable = ''
    error = ''
    if request.method == 'POST':
        stop = request.form.get('buss')
        date = request.form.get('date')
        time = request.form.get('time')
        timetable = transport.buss_timetable(stop, date, time)
        if timetable is False:
            error = 'Invalid Data Entry Please Try Again'
            timetable = ''
        else:
            timetable = transport.convert_buss_timetable(timetable)
    return render_template('buss.html',
                           title='buss',
                           weather_icon=weather.get_weather(),
                           buss_stop=transport.get_buss_stop_list(),
                           timetable=timetable,
                           error=error)


@app.route('/map')
def map_page():
    """Displays the map page. The map page shows a
    standard map centered on London by default however changes to show
    directions if start and end point parameters are passed in.
    """
    start = request.args.get('start')
    end = request.args.get('end')
    if start is None:
        url = 'https://www.google.com/maps/embed/v1/place?' \
              'key=' \
              '&q=London'
    else:
        url = 'https://www.google.com/maps/embed/v1/directions?'\
              'origin=place_id:' + start + '&destination=place_id:' + end + \
              '&mode=walking&key='
    return render_template('map.html',
                           title='Map',
                           url=url,
                           weather_icon=weather.get_weather())


@app.route('/place', methods=['GET', 'POST'])
def place():
    """Displays The place page defaulting in GET to ask the user for input
    then swapping to post to display the required information.
    """
    data = ''
    image = ''
    error = ''
    if request.method == 'POST':
        place = request.form.get('place_name')
        data = places.find_place(place)
        try:
            image = places.get_photo_request(data['candidates'][0]['photos'][0]
                                             ['photo_reference'])
        except IndexError:
            pass
        if image:
            pass
        else:
            data = ''
            image = ''
            error = 'Place Not Found Try Again'
    return render_template('place.html',
                           title='Places',
                           data=data,
                           image=image,
                           weather_icon=weather.get_weather(),
                           error=error)


@app.route('/place/found')
def place_found():
    """Displays the Place Found page"""
    starting_place_data = places.find_place(request.args.get('place'))
    starting_place_picture = places.get_photo_request(
        starting_place_data['candidates'][0]['photos'][0]['photo_reference'])
    locations = places.get_locations(request.args.get('query'),
                                     starting_place_data)
    return render_template('place found.html',
                           title='Places',
                           starting_place_data=starting_place_data,
                           starting_place_picture=starting_place_picture,
                           weather_icon=weather.get_weather(),
                           locations=locations)


if __name__ == '__main__':
    app.run(debug=True)
