#!/usr/bin/env python3
from time import sleep
import os

DIR_MAIN_FILE = os.path.dirname(os.path.abspath(__file__))
FILE_PUZZLE_INPUT = os.path.join(DIR_MAIN_FILE,'puzzle_input.txt')


def open_puzzle_input():
    puzzle_input = open(FILE_PUZZLE_INPUT)
    return puzzle_input

def convert_puzzle_input_to_list(puzzle_input: object):
    binary_numbers = []
    for line in puzzle_input:
        l = list(line[:-1]) # [:-1] because we need to skip new line: '\n'
        binary_numbers.append(l)
    return binary_numbers


# make our own binary to decimal converter because we are awesome
def binary_to_decimal(binary: str):
    digit_count = len(binary);
    decimal = 0
    for i in range(digit_count, 0, -1):
        binary_digit = binary[digit_count - i] # starting from left
        exponent = i - 1 # i starts from 1 higher than total digits
        power_of_position = 2**(exponent)
        decimal += ( int(binary_digit) * power_of_position)
    return decimal


def binary_swap(binary):
    return ( 1 * (int(binary) == 0) )


# we still avoid if statements, so arithmetic is key
def sum_by_binary_position(diagnostic_report: list):
    sum_by_position = []

    # prepare the list with the an element per binary digit
    for digit in diagnostic_report[0]:
        sum_by_position.append(0)

    # iterate through inpuut and summarize each designated position
    for line in diagnostic_report:
        position = 0

        for digit in line:
            '''
                1. we subtract 0.5 so that we can use arithmetic to calculate
                   the most common digit
                   this gives us a float: 0.5 or -0.5

                2. then multiply with 10 so that we have an integer resulting
                   in either 5 or -5

                3. then we summarize the total resulting in:
                     if a positive number, 1 is most common
                     if a negative number, 0 is most common
                     if 0, both 0 and 1 is mutually common
            '''
            float_val_ue = int(digit) - 0.5
            int_value = int(float_val_ue * 10) # evaluate to either -5 or +5
            sum_by_position[position] += int_value
            position += 1


    most_common_values = []
    for sum in sum_by_position:
        binary_value = ( 1 * (sum >= 0) )
        most_common_values.append(binary_value)

    return most_common_values

def extract_power_ratings(most_common_values):
    pass


def extract_gamma_rating_binary(most_common_values: list):
    gamma_rate = ''
    for value in most_common_values:
        gamma_rate += str(value)
    return gamma_rate


def extract_epsilon_rating_binary(most_common_values: list):
    epsilon_rate = ''
    for value in most_common_values:
        epsilon_rate += str(binary_swap(value))
    return epsilon_rate



def report_by_both_criteria(diagnostic_report: list):
    '''
        oxygen generator rating
            determine the most common value (0 or 1) in current bit position
            and keep only numbers with that bit in that position.
            If 0 and 1 are equally common,
            keep values with a 1 in the position being considered.

        carbon scrubber rating
            determine the least common value (0 or 1) in current bit position
            and keep only numbers with that bit in that position.
            If 0 and 1 are equally common,
            keep values with a 0 in the position being considered
    '''

    ratings = { 0: [], 1: [] } # 0 = oxygen generate, 1 = carbon scrubbing
    for line in diagnostic_report:
        ratings[0].append(line)
        ratings[1].append(line)


    for rating_index in range(len(ratings)):
        position_iter = 0
        # ratings[rating_index] = ratings[rating_index]
        while len(ratings[rating_index]) > 1:
            # keep tabs on indexes for lines we want to keep until one remains
            index_array = { 0: [], 1: []} # 0 = remove, 1 = keep
            numbers_keep = []
            most_common = sum_by_binary_position(ratings[rating_index])
            # most_common = most_common_by_position(sum_by_position)
            most_common_number = most_common[position_iter]

            # our special ingredient, swap to least common if rating_index = 1
            swap_value = 1 - ( 1 * (most_common_number == rating_index) )

            # append reulst (index number) for those numbers we want to keep
            for i in range(len(ratings[rating_index])):
                current_digit = int(ratings[rating_index][i][position_iter])
                res = 1 * (current_digit == swap_value)
                index_array[res].append(i)

            for index in index_array[1]:
                numbers_keep.append(ratings[rating_index][index])

            ratings[rating_index] = numbers_keep
            position_iter += 1

        result = ''.join(ratings[rating_index][0])
        ratings[rating_index] = result

    result = {'ox_gen_rating':ratings[0], 'co_scrub_rating':ratings[1]}
    return result


def report_by_bit_criteria_carbon(diagnostic_report: list):
    pass
    # for line in diagnostic_report:
    #     position = 0
    #
    #     for digit in line[:-1]: # [:-1] is used because we want to skip new line




if __name__ == '__main__':
    puzzle_input_file = open_puzzle_input()
    diagnostic_report = convert_puzzle_input_to_list(puzzle_input_file)
    puzzle_input_file.close()
    most_common_values = sum_by_binary_position(diagnostic_report)


    # task 1
    ratings = extract_power_ratings(most_common_values)

    gamma_rate_binary = extract_gamma_rating_binary(most_common_values)
    epsilon_rate_binary = extract_epsilon_rating_binary(most_common_values)
    gamma_rate_decimal = binary_to_decimal(gamma_rate_binary)
    epsilon_rate_decimal = binary_to_decimal(epsilon_rate_binary)
    power_consumption = ( gamma_rate_decimal * epsilon_rate_decimal )
    print('The power consumption of the submarine = '+ str(power_consumption))

    # task 2
    ratings = report_by_both_criteria(diagnostic_report)
    ratings['ox_gen_rating'] = binary_to_decimal(ratings['ox_gen_rating'])
    ratings['co_scrub_rating'] = binary_to_decimal(ratings['co_scrub_rating'])
    support_rating = ( ratings['ox_gen_rating'] * ratings['co_scrub_rating'] )
    print('The life support rating of the submarine = ' + str(support_rating))
