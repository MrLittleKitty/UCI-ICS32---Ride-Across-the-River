# Eric Wolfe 76946154 eawolfe@uci.edu
import json
import urllib as lib

api_key = ""

with open("mapquest.key") as file:
    global api_key
    api_key = file.readline()


def get_directions(locations: [str]) -> [str]:
    # TODO----This isnt a real method its just a placeholder to show what we need in this class
    return
