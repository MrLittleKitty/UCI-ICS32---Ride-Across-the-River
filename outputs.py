# Eric Wolfe 76946154 eawolfe@uci.edu
import network


class Steps:
    def print_output(self, locations: [str]) -> None:
        maneuvers = network.get_directions(locations)
        if len(maneuvers) == 0:
            return

        print('DIRECTIONS')
        for maneuver in maneuvers:
            print(maneuver)


class TotalDistance:
    def print_output(self, locations: [str]) -> None:
        distance = network.get_total_distance(locations)
        if distance == -1:
            return
        distance = int(round(distance, 0))
        print('TOTAL DISTANCE: ' + str(distance) + ' miles')


class TotalTime:
    def print_output(self, locations: [str]) -> None:
        totalTimeInSeconds = network.get_total_time(locations)
        if totalTimeInSeconds == -1:
            return
        totalTimeInMinutes = totalTimeInSeconds / 60
        totalTimeInMinutes = int(round(totalTimeInMinutes, 0))
        print('TOTAL TIME: ' + str(totalTimeInMinutes) + ' minutes')


class LatLong:
    def print_output(self, locations: [str]) -> None:
        latLongs = network.get_lats_longs(locations)
        if len(latLongs) == 0:
            return

        print('LATLONGS')
        for lat, long in latLongs:
            latString = '{:.2f}'.format(abs(lat))
            longString = '{:.2f}'.format(abs(long))
            if lat > 0:
                latString += 'N'
            else:
                latString += 'S'

            if long > 0:
                longString += 'E'
            else:
                longString += 'W'

            print(latString + ' ' + longString)


class Elevation:
    def print_output(self, locations: [str]) -> None:
        elevations = network.get_elevations(locations)
        if len(elevations) == 0:
            return

        print('ELEVATIONS')
        for elevation in elevations:
            print(str(int(round(elevation, 0))))
        return
