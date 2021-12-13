#!/usr/bin/env python3
import os

DIR_MAIN_FILE = os.path.dirname(os.path.abspath(__file__))
FILE_PUZZLE_INPUT = os.path.join(DIR_MAIN_FILE,'puzzle_input.txt')


def open_puzzle_input():
    puzzle_input = open(FILE_PUZZLE_INPUT)
    return puzzle_input


def create_list(string_in: str):
    return [f for f in string_in]

def return_highest_number(a: int, b:int):
    return ( a * (a > b) + b * (a <= b) )

def or_bool_value(bool_1, bool_2):
    a = ( 1 * ( int(bool_1) == 0 ) )
    b = ( 1 * ( int(bool_2) == 0 ) )
    return 1 - ( 1 * a ) * ( 1 * b )

def triple_or_bool_value(bool_1, bool_2, bool_3):
    a = ( 1 * ( int(bool_1) == 0 ) )
    b = ( 1 * ( int(bool_2) == 0 ) )
    c = ( 1 * ( int(bool_3) == 0 ) )
    return 1 - ( 1 * a ) * ( 1 * b ) * ( 1 * c )

def xor_bool_value(bool_1, bool_2):
    return ( 1 - ( int(bool_1) == int(bool_2) ) )

def bool_swap(binary):
    return ( 1 * (int(binary) == 0) )

def get_arr_len(coordinates: list):
    arr_len = 0
    for _ in coordinates:
        arr_len += 1
    return arr_len


def get_axis_increment_value(a: int,b: int):
    # returns either -1, 0 or +1
    # if a is greatest = -1
    # if b is greatest = +1
    # if equal = 0
    is_equal = 1 * ( a == b )
    a_is_higher = 1 * ( a > b )
    increment = 1 - is_equal - a_is_higher - a_is_higher
    return increment


def get_coordinates(puzzle_input: object):
    l = []
    line = puzzle_input.readline()
    while get_arr_len(line) > 0:
        # line = create_list(line) # list-ify it
        line = line[:-1] # [:-1] for skipping the new line character -> '\n'
        l.append(line)
        line = puzzle_input.readline()
    return l


def coordinate_formatting(coordinates: list):
    '''
        turns [
                ['105,697 -> 287,697'],
                ['705,62 -> 517,250'],
                ['531,627 -> 531,730']
              ]
        into  [
                [ ['105', '697'], ['287', '697'] ],
                [ ['705', '62'], ['517', '250'] ],
                [ ['531', '627'], ['531', '730'] ]
              ]
    '''
    formatted_array = []
    total_elements = get_arr_len(coordinates)
    current_arr_index = 0
    while current_arr_index < total_elements:
        string_element = coordinates[current_arr_index]
        total_characters = get_arr_len(string_element)

        _arr = {
                    0: { 0:'', 1:'', 2:'',3:'' },
                    1: { 0:'', 1:'', 2:'',3:'' }
                }
        current_character_index = 0
        index_move = 0 # when counted, move to next index in _arr
        while current_character_index < total_characters:
            current_character = string_element[current_character_index]

            is_comma = 1 * ( current_character == ',' )
            is_hyphen = 1 * ( current_character == '-' )
            is_whitespace = 1 * ( current_character == ' ' )
            is_gt = ( current_character == '>' )
            is_unwanted = triple_or_bool_value(is_hyphen, is_whitespace, is_gt)

            # based on conditions, we keep only characters we want
            not_keep = or_bool_value(is_comma, is_unwanted)
            keep = bool_swap(not_keep)

            # next index in the list for when going from x1 to y1 etc.
            index_move += or_bool_value(is_comma,is_gt)

            # based on the keep variable, our values resides in _arr[1]
            _arr[keep][index_move] += current_character
            current_character_index += 1

        # prepare the proper formatting before appending
        l = [ [ _arr[1][0], _arr[1][1] ], [ _arr[1][2], _arr[1][3] ] ]
        formatted_array.append(l)

        current_arr_index += 1

    return formatted_array


def split_diagonal_lines(coordinates: list):
    keys = { 0: 'diagonal', 1:'nodiagonal'}
    new_coordinates = { 'nodiagonal':[], 'diagonal':[] }
    for plots in coordinates:
        x_one = plots[0][0]
        y_one = plots[0][1]
        x_two = plots[1][0]
        y_two = plots[1][1]

        keep_x = ( x_one == x_two )
        keep_y = ( y_one == y_two )

        # if one of them is 1, it is a non diagonel
        not_diagonal = xor_bool_value(keep_x,keep_y)
        new_coordinates[ keys[not_diagonal] ].append(plots)

    return new_coordinates


def get_dimensions(coordinates: list):
    dimension = { 0:{'x':0, 'y':0}, 1:{'x':0, 'y':0} }

    for plots in coordinates:
        highest_x = dimension[1]['x']
        highest_y = dimension[1]['y']

        x_one = int(plots[0][0])
        y_one = int(plots[0][1])
        x_two = int(plots[1][0])
        y_two = int(plots[1][1])

        x = return_highest_number(x_one,x_two)
        y = return_highest_number(y_one,y_two)

        keep_x = 1 * ( x > highest_x )
        keep_y = 1 * ( y > highest_y )

        dimension[keep_x]['x'] = x
        dimension[keep_y]['y'] = y


    highest = [dimension[1]['x'], dimension[1]['y']]
    return highest


def create_hydrothermal_plane(dimension: list):
    x_plane = dimension[0]
    y_plane = dimension[1]
    x = 0
    plane = []
    while x < ( x_plane + 1 ):
        l = []
        y = 0

        while y < ( y_plane + 1 ):
            l.append(0)
            y += 1
        x += 1
        plane.append(l)

    return plane


def get_overlap_count(hydroplane: list):
    row_count = get_arr_len(hydroplane)
    row = 0
    overlap_count = 0
    col_count = get_arr_len(hydroplane[row])
    while row < row_count:

        col = 0
        while col < col_count:
            val = hydroplane[row][col]
            is_overlap = 1 * ( val >= 2 )
            overlap_count += is_overlap
            col += 1

        row += 1

    return overlap_count


def update_hydroplane(coordinates: list, hydroplane: list):
    total_plot_count = get_arr_len(coordinates)
    plot_count = 0
    while total_plot_count > plot_count:
        plots = coordinates[plot_count]
        x_one = int(plots[0][0])
        y_one = int(plots[0][1])
        x_two = int(plots[1][0])
        y_two = int(plots[1][1])

        # this gives us the increment value (0, -1 or +1) for each axis
        # which in turn makes it possible to run both diagonal and
        # non diagonal plots in this very same while loop
        x_steps = get_axis_increment_value(x_one,x_two)
        y_steps = get_axis_increment_value(y_one,y_two)

        # # this gives us the "range" that the line will span
        x_positive_steps = ( (x_one > x_two) * (x_one - x_two) )
        x_negative_steps = ( (x_two > x_one) * (x_two - x_one) )
        x_range = x_positive_steps + x_negative_steps
        y_positive_steps = ( (y_one > y_two) * (y_one - y_two) )
        y_negative_steps = ( (y_two > y_one) * (y_two - y_one) )
        y_range = y_positive_steps + y_negative_steps

        # we might have a none diagnoal, which means we need the none zero value
        axis_range = return_highest_number(x_range, y_range)

        step = 0 # iterate until we reach the range + 1 (for last plot)
        while step < ( axis_range + 1 ):
            hydroplane[y_one][x_one] += 1
            x_one += x_steps
            y_one += y_steps
            # increments with either 0, +1 or -1 based on steps contidion

            step += 1

        plot_count += 1

    return hydroplane


if __name__ == '__main__':

    # fetch raw input data
    puzzle_input_file = open_puzzle_input()
    coordinates = get_coordinates(puzzle_input_file)
    puzzle_input_file.close()

    # prepare data structure for coordinates
    coordinates = coordinate_formatting(coordinates)

    # get the width and length of the illustrated field
    dimension = get_dimensions(coordinates)

    # split our coordinates into lists of diagonal and non diagonal
    split_c = split_diagonal_lines(coordinates)
    non_diagonal_coordinates = split_c['nodiagonal']
    diagonal_coordinates = split_c['diagonal']

    # this is the illustrated field of hydrothermal vents
    hydroplane = create_hydrothermal_plane(dimension)

    # task 1 wants all non diagonal
    hydroplane = update_hydroplane(non_diagonal_coordinates, hydroplane)
    task_1_result = get_overlap_count(hydroplane)
    print('Task 1: counting only vertical and horizontal lines')
    print('Lines overlap ' + str(task_1_result) + ' times')

    # task 2 wants both diagonal and non diagonal, lets update again
    hydroplane = update_hydroplane(diagonal_coordinates, hydroplane)
    task_2_result = get_overlap_count(hydroplane)
    print('Task 2: including diagonal ines')
    print('Lines overlap ' + str(task_2_result) + ' times')
