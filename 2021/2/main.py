#!/usr/bin/env python3

import os

DIR_MAIN_FILE = os.path.dirname(os.path.abspath(__file__))
FILE_PUZZLE_INPUT_1 = os.path.join(DIR_MAIN_FILE,'puzzle_input_1.txt')
FILE_PUZZLE_INPUT_2 = os.path.join(DIR_MAIN_FILE,'puzzle_input_2.txt')


def open_puzzle_input(FILE_PUZZLE_INPUT):
    puzzle_input = open(FILE_PUZZLE_INPUT)
    return puzzle_input

def convert_puzzle_input_to_list(puzzle_input):
    directions = []
    for line in puzzle_input:
        directions.append(line)
    return directions


# the two next functions uses key value store to handle different cases
# isntead of if blocks just for fun
def calculate_final_position_task_1(directions):
    position_data = { 'd':0, 'u':0, 'f':0 }
    for line in directions:
        key = line[0] # grab first character for each line
        n = int(line.split(' ')[1]) # each number comes after a space
        position_data[key] = position_data[key] + n

    return position_data['f'] * (position_data['d'] - position_data['u'])


def calculate_final_position_task_2(directions):
    position_data = { 'aim':0, 'depth':0, 'horizontal':0 }

    # create the 3 different functions needed for calculating position data
    def move_submarine(n):
        position_data['horizontal'] += n
        position_data['depth'] += (position_data['aim'] * n)

    def increase_aim(n):
        position_data['aim'] += n

    def decrease_aim(n):
        position_data['aim'] -= n

    # store the 3 functions in a dictionary so they get called based on input
    sub_functions = { 'u':decrease_aim, 'd':increase_aim, 'f':move_submarine }
    for line in directions:
        key = line[0]
        n = int(line.split(' ')[1])
        sub_functions[key](n)

    return position_data['depth'] * position_data['horizontal']



if __name__ == '__main__':
    puzzle_input = open_puzzle_input(FILE_PUZZLE_INPUT_1)
    directions = convert_puzzle_input_to_list(puzzle_input)
    final_answer = calculate_final_position_task_1(directions)
    print('Task 1: horizontal position times depth = ' + str(final_answer))

    puzzle_input = open_puzzle_input(FILE_PUZZLE_INPUT_2)
    directions = convert_puzzle_input_to_list(puzzle_input)
    final_answer = calculate_final_position_task_2(directions)
    print('Task 2: horizontal position times depth = ' + str(final_answer))
