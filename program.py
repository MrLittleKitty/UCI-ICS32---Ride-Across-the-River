# Eric Wolfe 76946154 eawolfe@uci.edu
import outputs


def start_program() -> None:
    """
    The main entry point for the program.
    Runs the program.
    """
    numLocations = get_input_integer()
    locations = get_input_strings(numLocations)
    numOutputs = get_input_integer()
    outputStrings = get_input_strings(numOutputs)

    outputObjects = []
    for outputType in outputStrings:
        outputObjects.append(get_output_class(outputType))

    print('')
    for output in outputObjects:
        # Catch any errors that would be thrown from things like mapquest being down or not having internet
        try:
            output.print_output(locations)
        except:
            print('MAPQUEST ERROR')

        print('')

    print("Directions Courtesy of MapQuest; Map Data Copyright OpenStreetMap Contributors")


def get_output_class(type: str) -> object:
    """
    Creates an instance of the output class given the type string
    :param type: The type of output that is needed
    :return: An instance of an output class
    """
    if type.upper() == 'STEPS':
        return outputs.Steps()
    elif type.upper() == 'TOTALDISTANCE':
        return outputs.TotalDistance()
    elif type.upper() == 'TOTALTIME':
        return outputs.TotalTime()
    elif type.upper() == 'LATLONG':
        return outputs.LatLong()
    else:
        return outputs.Elevation()


def get_input_strings(number: int) -> [str]:
    """
    Gets a the given number of strings from the standard input and returns them as a list
    :param number: The number of strings to get from the input
    :return: A list of strings retrieved from the standard input
    """
    returnList = []
    for i in range(number):
        line = input().strip()
        returnList.append(line)
    return returnList


def get_input_integer() -> int:
    """
    Gets an integer from the standard input
    :return: The integer retrieved from the standard input
    """
    value = input().strip()
    return int(value)


if __name__ == '__main__':
    start_program()
