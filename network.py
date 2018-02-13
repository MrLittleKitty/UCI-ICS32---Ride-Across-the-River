# Eric Wolfe 76946154 eawolfe@uci.edu
import urllib.parse as parse
import urllib.request as request
import decimal
import json

_api_key = ""

# TODO---This needs to be removed before submitting the final project. Replace with hardcoded api key field
with open("mapquest.key") as file:
    _api_key = file.readline()


def _get_directions_json(locations: [str]) -> object:
    """
    Makes an HTTP request to mapquest directions API for a route and then returns a json object for the response
    :param locations: The locations to get directions for
    :return: A json object that is the response from the mapquest directions API
    """
    params = [('key', _api_key), ('from', locations[0])]
    for index in range(1, len(locations)):
        params.append(('to', locations[index]))
    encodedParams = parse.urlencode(params)
    response = request.urlopen('http://open.mapquestapi.com/directions/v2/route?' + encodedParams)
    data = response.read()
    return json.loads(data)


def _get_lat_longs(jsonResponse: object) -> [(decimal, decimal)]:
    """
    Gets the latitude and longitude for each location in the given json response
    :param jsonResponse: The json response object from the mapquest directions API
    :return: A list of tuples where each tuple is the latitude and the longitude for a location
    """
    latLongs = []
    for index in range(len(jsonResponse['route']['locations'])):
        latLong = jsonResponse['route']['locations'][index]['latLng']
        lat = latLong['lat']
        lng = latLong['lng']
        latLongs.append((lat, lng))

    return latLongs


def _check_directions_status(json: object) -> bool:
    """
    Checks the status code of the json object from the mapquest directions API and prints an error if necessary
    :param json: The json response object from the mapquest directions API
    :return: True if the json response is normal. False if there is an error and a message has been output
    """
    status = json['info']['statuscode']
    if status == 0:
        return True

    if (status >= 400 and status <= 403) or status == 500 or status == 600 or status == 601 or status == 602:
        print("MAPQUEST ERROR")
    else:
        print("NO ROUTE FOUND")

    return False


def get_elevations(locations: [str]) -> [decimal]:
    """
    Gets the elevation for each of the given locations
    :param locations: The locations to get the elevations for
    :return: A list of decimals where each decimal is the elevation of the corresponding location
    """
    directionsResponse = _get_directions_json(locations)
    if not _check_directions_status(directionsResponse):
        return None

    latLongs = _get_lat_longs(directionsResponse)
    elevations = []

    for lat, long in latLongs:
        params = [('key', _api_key), ('inFormat', 'kvp'), ('outFormat', 'json'), ('unit', 'f'), ('shapeFormat', 'raw'),
                  ('latLngCollection', str(lat) + ',' + str(long))]
        encodedParams = parse.urlencode(params)
        url = 'http://open.mapquestapi.com/elevation/v1/profile?' + encodedParams
        response = request.urlopen(url)
        data = response.read()
        jsonResponse = json.loads(data)
        elevations.append(jsonResponse['elevationProfile'][0]['height'])

    return elevations


def get_directions(locations: [str]) -> [str]:
    """
    Gets the detailed maneuvers for getting to each of the given locations
    :param locations: The locations to get directions for
    :return: A list of strings where each string is a maneuver to take to get to the given locations
    """
    response = _get_directions_json(locations)
    if not _check_directions_status(response):
        return []
    returnList = []
    for legIndex in range(len(response['route']['legs'])):
        leg = response['route']['legs'][legIndex]
        for maneuverIndex in range(len(leg['maneuvers'])):
            maneuver = leg['maneuvers'][maneuverIndex]
            returnList.append(maneuver['narrative'])

    return returnList


def get_lats_longs(locations: [str]) -> [(decimal, decimal)]:
    """
    Gets the latitude and longitude for each of the given locations
    :param locations: The locations to get the latitudes and longitudes for
    :return: A list of tuples where each tuple is the latitude and longitude of the corresponding location
    """
    response = _get_directions_json(locations)
    if not _check_directions_status(response):
        return []
    return _get_lat_longs(response)


def get_total_time(locations: [str]) -> int:
    """
    Gets the total time required on a trip to all of the given locations
    :param locations: The locations to get the total trip time for
    :return: An integer that is the number of minutes required to travel to all the given locations
    """
    response = _get_directions_json(locations)
    if not _check_directions_status(response):
        return -1
    return response['route']['time']


def get_total_distance(locations: [str]) -> decimal:
    """
    Gets the total distance that would be travelled on a trip to all the given locations
    :param locations: The locations to get the total trip distance for
    :return: A decimal that is the number of miles that would be travelled on a trip to all the given locations
    """
    response = _get_directions_json(locations)
    if not _check_directions_status(response):
        return -1
    return response['route']['distance']
