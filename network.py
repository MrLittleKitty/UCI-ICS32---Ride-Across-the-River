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


def _check_directions_status(json: object) -> bool:
    status = json['info']['statuscode']
    if status == 0:
        return True

    if (status >= 400 and status <= 403) or status == 500 or status == 600 or status == 601 or status == 602:
        print("MAPQUEST ERROR")
    else:
        print("NO ROUTE FOUND")

    return False


def get_lats_longs(locations: [str]) -> [(decimal, decimal)]:
    response = _get_directions_json(locations)
    if not _check_directions_status(response):
        return []
    returnList = []
    for index in range(len(locations)):
        latLong = response['route']['locations'][index]['latLng']
        lat = latLong['lat']
        lng = latLong['lng']
        returnList.append((lat, lng))

    return returnList


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
