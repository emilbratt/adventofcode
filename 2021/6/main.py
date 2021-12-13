#!/usr/bin/env python3
import os

DIR_MAIN_FILE = os.path.dirname(os.path.abspath(__file__))
FILE_PUZZLE_INPUT = os.path.join(DIR_MAIN_FILE,'puzzle_input.txt')


def open_puzzle_input():
    puzzle_input = open(FILE_PUZZLE_INPUT)
    return puzzle_input


def get_puzzle_input(puzzle_input: object):
    return puzzle_input.readline()


def get_arr_len(coordinates: list):
    arr_len = 0
    for _ in coordinates:
        arr_len += 1
    return arr_len


def create_empty_key_arr(N: int):
    arr = {}
    key = -1
    while key < N:
        key += 1
        arr[key] = 0
    return arr


def create_list_from_fish_numbers(fish_numbers: str):
    # remove unwanted characters
    temp_arr = { 0:[], 1:[] }
    for _ in fish_numbers:
        key_index = 1 - ( _ != ',' )
        key_index += 1 - ( _ != '\n' )
        temp_arr[key_index].append(_)
    # cast numbers to int and append to empty array
    fish_numbers = []
    for n in temp_arr[0]:
        fish_numbers.append(int(n))

    return fish_numbers


def total_slow_alg(fish_numbers: list, DAYS: int, max_age: int, reset_age: int):
    '''
        slow algorithm:
            the array extends for each new fish making every new
            fish impact the rate in which we calculate the total
            number of fish slow down exponentially
    '''
    day = 0
    while day < DAYS:

        new_fish = 0
        fish_count = get_arr_len(fish_numbers)
        index = 0
        while index < fish_count:
            fish_age = fish_numbers[index]

            # if new fish if current fish has age 0
            is_zero = 1 * ( fish_age == 0 )

            # either minus 1 from old age or if 0 -> back to reset age
            fish_age = ( fish_age - ( 1 - is_zero ) ) + ( reset_age * is_zero )

            # insert the subtracted fish age back into its same index in array
            fish_numbers[index] = fish_age

            # if the current fish was age zero, add +1 to new_fish
            new_fish += is_zero

            index += 1

        # append the new born fish to the array with highest age
        while new_fish != 0:
            fish_numbers.append(max_age)
            new_fish -= 1

        day += 1

    return get_arr_len(fish_numbers)


def convert_to_key_val_array(fish_numbers: list, max_age: int):
    new_fish_counter = create_empty_key_arr(max_age)
    arr_length = get_arr_len(fish_numbers)
    index = 0
    while index < arr_length:
        fish_age = fish_numbers[index]
        new_fish_counter[fish_age] += 1
        index += 1

    return new_fish_counter


def total_fast_alg(fish_counter: dict, DAYS: int, max_age: int, reset_age: int):
    '''
        fast algorithm:
            instead of the array extending for each fish, we keep the
            number of fish stored as a key value pair where the key
            represents the age and value represents the total number
    '''
    day = 0
    while day < DAYS:

        # preserve fish with "zero days left" for the reset_age key
        fish_reset = fish_counter[0]
        age = 0
        while age < max_age:
            # start from 1 (0 is already preserved, we can ignore the overwrite)
            age += 1
            # swap over to new age but this age is minus 1
            fish_counter[age - 1] = fish_counter[age]

        # add back the new fish as well as the new born fish from age 0
        fish_counter[reset_age] += fish_reset
        fish_counter[max_age] = fish_reset

        day += 1

    # count (summarize) the total fish and add to the total result
    result = 0
    age = -1
    while age < max_age:
        age += 1
        result += fish_counter[age]

    return result



if __name__ == '__main__':

    # fetch and format input data to a list
    puzzle_input_file = open_puzzle_input()
    input_fish_numbers = get_puzzle_input(puzzle_input_file)
    puzzle_input_file.close()

    # constants that does not change
    MAX_AGE = 8 # amount of days until a this fish creates a new fish
    RESET_AGE = 6 # when fish spawns new, reset current fish to X days


    # task 1 (expected answer: 390011)
    print('Working on Task 1')
    DAYS = 80 # record window for new fish for task 1
    fish_arr = create_list_from_fish_numbers(input_fish_numbers)
    result = total_slow_alg(fish_arr, DAYS, MAX_AGE, RESET_AGE)
    print('There are '
        + str(result)
        + ' lanternfish after '
        + str(DAYS)
        + ' days')


    # task 2 (expected answer: 1746710169834)
    '''
        NOTE:
            while 80 days is fine with a growing array of new fish,
            256 days is to much for the exponential growth..

            task 2 demands a new way of structuring the data so that it is
            possible to calculate the total lanternfish for 256 iterations
            in less than 4 years
    '''
    print('Working on Task 2')
    DAYS = 256 # record window for new fish for task 2
    fish_arr = create_list_from_fish_numbers(input_fish_numbers)
    fish_k_v_arr = convert_to_key_val_array(fish_arr, MAX_AGE)
    result = total_fast_alg(fish_k_v_arr, DAYS, MAX_AGE, RESET_AGE)
    print('There are '
        + str(result)
        + ' lanternfish after '
        + str(DAYS)
        + ' days')
