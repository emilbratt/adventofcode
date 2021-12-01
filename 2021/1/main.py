#!/usr/bin/env python3

import os

DIR_MAIN_FILE = os.path.dirname(os.path.abspath(__file__))
FILE_PUZZLE_INPUT = os.path.join(DIR_MAIN_FILE,'puzzle_input.txt')


def open_puzzle_input():
    puzzle_input = open(FILE_PUZZLE_INPUT)
    return puzzle_input

def convert_puzzle_input_to_list(puzzle_input):
    numbers = []
    for line in puzzle_input:
        numbers.append(int(line))
    return numbers

# the two next functions uses branchless method (no if`s) but instead adds the
# value of True / False which by default is evaluated as 1 and 0 respectively
def get_increase_count(depth_msr):
    increase_count = 0
    for i in range(1, len(depth_msr)):
        increase_count += (depth_msr[i] > depth_msr[i-1])
    return increase_count

def get_increase_count_from_window(depth_msr):
    increase_count = 0
    old_window = depth_msr[0] + depth_msr[1] + depth_msr[2]
    for i in range(3, len(depth_msr)):
        new_window = (depth_msr[i] + depth_msr[i-1] + depth_msr[i-2])
        increase_count += (new_window > old_window)
        old_window = (depth_msr[i] + depth_msr[i-1] + depth_msr[i-2])
    return increase_count



if __name__ == '__main__':
    puzzle_input = open_puzzle_input()
    depth_msr = convert_puzzle_input_to_list(puzzle_input)

    increase_count = get_increase_count(depth_msr)
    print(
        str(increase_count)
        + ' measurements are larger than the previous measurement')

    increase_count_window = get_increase_count_from_window(depth_msr)
    print(
        str(increase_count_window)
        + ' sums are larger than the previous sum')
