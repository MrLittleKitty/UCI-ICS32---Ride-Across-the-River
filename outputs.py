# Eric Wolfe 76946154 eawolfe@uci.edu
import network


class Steps:
    def print_output(self, locations: [str]) -> None:
        """
        Prints a detailed output of the maneuvers required to get to all the given locations
        :param locations: The locations to get detailed maneuver data for
        """
        maneuvers = network.get_directions(locations)
        if len(maneuvers) == 0:
            return

        print('DIRECTIONS')
        for maneuver in maneuvers:
            print(maneuver)


class TotalDistance:
    def print_output(self, locations: [str]) -> None:
        """
        Prints the total distance of the route to all the given locations
        :param locations: The locations to get the total route distance for
        """
        distance = network.get_total_distance(locations)
        if distance == -1:
            return
        distance = int(round(distance, 0))
        print('TOTAL DISTANCE: ' + str(distance) + ' miles')


class TotalTime:
    def print_output(self, locations: [str]) -> None:
        """
        Prints the total time of the route to all the given locations
        :param locations: The locations to get the total route time for
        """
        totalTimeInSeconds = network.get_total_time(locations)
        if totalTimeInSeconds == -1:
            return
        totalTimeInMinutes = totalTimeInSeconds / 60
        totalTimeInMinutes = int(round(totalTimeInMinutes, 0))
        print('TOTAL TIME: ' + str(totalTimeInMinutes) + ' minutes')


class LatLong:
    def print_output(self, locations: [str]) -> None:
        """
        Prints the latitude and longitude for each of the given locations
        :param locations: The locations to print the latitudes and longitudes for
        """
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
        """
        Prints the elevation for each each of the given locations
        :param locations: The locations to print the elevations for
        """
        elevations = network.get_elevations(locations)
        if len(elevations) == 0:
            return

        print('ELEVATIONS')
        for elevation in elevations:
            print(str(int(round(elevation, 0))))
        return
