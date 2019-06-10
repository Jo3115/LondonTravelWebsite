import requests


"""Places Module
Handles the API requests and information received for the Places Page.
"""


__version__ = '1.2'
__author__ = 'Joshua Mugglestone'


def find_place(input, input_type='textquery'):
    """Handles the Api call sending the users input and receiving a place
    with the closest matching name."""
    params = {'input': input,
              'inputtype': input_type,
              'fields': 'photos,formatted_address,name,rating,opening_hours,'
                        'geometry,place_id',
              'key': ''}
    return requests.get('https://maps.googleapis.com/maps/'
                        'api/place/findplacefromtext/json?', params).json()


def get_photo_request(photo_reference):
    try:
        params = ('photoreference=' + str(photo_reference) + '&maxheight=1600&'
                                                             'maxwidth=1600&'\
                                'key=')
        return 'https://maps.googleapis.com/maps/api/place/photo?' + params
    except IndexError:
        return


def get_locations(query, data):
    params = {'key':'',
              'location': str(data['candidates'][0]['geometry']['location']
                              ['lat']) + ',' +
                          str(data['candidates'][0]['geometry']['location']
                              ['lng']),
              'keyword': query,
              'rankby': 'distance'}
    data = requests.get('https://maps.googleapis.com/maps/api/'
                        'place/nearbysearch/json?', params).json()
    data = data['results']
    results = []
    for result in data:
        list=[]
        list.append(result)
        try:
            list.append(get_photo_request(result['photos'][0]
                                          ['photo_reference']))
        except KeyError:
            list.append(' ')
        results.append(list)
    return results
