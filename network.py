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
    params = [('key', _api_key), ('from', locations[0])]
    for index in range(1, len(locations)):
        params.append(('to', locations[index]))
    encodedParams = parse.urlencode(params)
    response = request.urlopen('http://open.mapquestapi.com/directions/v2/route?' + encodedParams)
    data = response.read()
    return json.loads(data)


def _get_lat_longs(jsonResponse: object) -> [(decimal, decimal)]:
    latLongs = []
    for index in range(len(jsonResponse['route']['locations'])):
        latLong = jsonResponse['route']['locations'][index]['latLng']
        lat = latLong['lat']
        lng = latLong['lng']
        latLongs.append((lat, lng))

    return latLongs


def _check_directions_status(json: object) -> bool:
    status = json['info']['statuscode']
    if status == 0:
        return True

    if (status >= 400 and status <= 403) or status == 500 or status == 600 or status == 601 or status == 602:
        print("MAPQUEST ERROR")
    else:
        print("NO ROUTE FOUND")

    return False


def get_elevations(locations: [str]) -> [decimal]:
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
    response = _get_directions_json(locations)
    if not _check_directions_status(response):
        return []
    return _get_lat_longs(response)


def get_total_time(locations: [str]) -> int:
    response = _get_directions_json(locations)
    if not _check_directions_status(response):
        return -1
    return response['route']['time']


def get_total_distance(locations: [str]) -> int:
    response = _get_directions_json(locations)
    if not _check_directions_status(response):
        return -1
    return response['route']['distance']
