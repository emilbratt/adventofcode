#!/usr/bin/env python3

import os

DIR_MAIN_FILE = os.path.dirname( os.path.abspath(__file__) )
FILE_PUZZLE_INPUT = os.path.join(DIR_MAIN_FILE, 'puzzle_input.txt')


def open_puzzle_input():
    puzzle_input = open(FILE_PUZZLE_INPUT)
    return puzzle_input

def convert_puzzle_input_to_list(puzzle_input: object):
    binary_numbers = []
    for line in puzzle_input:
        l = list(line[:-1]) # [:-1] because we want to skip new line: '\n'
        binary_numbers.append(l)
    return binary_numbers


# make our own binary to decimal converter because we are awesome
def binary_to_decimal(binary: str):
    digit_count = len(binary);
    decimal = 0
    for i in range(digit_count, 0, -1):
        binary_digit = binary[digit_count - i] # starting from left
        exponent = i - 1 # i starts from 1 higher than total digits
        power_of_position = 2 ** exponent
        decimal += ( int(binary_digit) * power_of_position )
    return decimal


# for swapping binary digits: 1 to 0 or 0 to 1
def binary_swap(binary):
    return ( 1 - int(binary) )


# we still try to avoid if statements, so arithmetic is key
def sum_by_binary_position(diagnostic_report: list):
    sum_by_position = []

    # prepare the list appending a 0 for each binary digit
    for digit in diagnostic_report[0]:
        sum_by_position.append(0)

    # iterate through inpuut and summarize each designated position
    for line in diagnostic_report:
        position = 0

        for digit in line:
            float_val_ue = int(digit) - 0.5
            int_value = int(float_val_ue * 10) # evaluate to either -5 or +5
            sum_by_position[position] += int_value
            position += 1

    # convert negative and positive values to 0 and 1 respectively
    most_common_values = []
    for sum in sum_by_position:
        binary_value = ( 1 * (sum >= 0) )
        most_common_values.append(binary_value)
    return most_common_values


def extract_power_consumption(diagnostic_report: list):
    most_common_values = sum_by_binary_position(diagnostic_report)
    consumption_rating = { 'gamma': '', 'epsilon': '' }
    for value in most_common_values:
        consumption_rating['gamma'] += str(value)
        consumption_rating['epsilon'] += str(binary_swap(value))
    return consumption_rating


def report_by_both_criteria(diagnostic_report: list):
    ratings = { 0: [], 1: [] } # 0 = oxygen generate, 1 = carbon scrubbing
    for line in diagnostic_report:
        ratings[0].append(line)
        ratings[1].append(line)

    # iterate thrugh both arrays
    for rating_index in range(len(ratings)):

        # the position of the digit that we analyze
        position = 0

        while len(ratings[rating_index]) > 1:
            # keep tabs on indexes for lines we want to keep and not keep
            index_array = { 0: [], 1: [] } # 0 = remove, 1 = keep
            preserved_index_numbers = []
            most_common_values = sum_by_binary_position(ratings[rating_index])
            most_common_value = most_common_values[position]

            # this will swap to the least common value if rating_index = 1
            swap_value = 1 - ( 1 * (most_common_value == rating_index) )

            # append result (index numbers) for those numbers we want to keep
            for i in range(len(ratings[rating_index])):
                current_digit = int(ratings[rating_index][i][position])
                res = 1 * (current_digit == swap_value)
                index_array[res].append(i)

            # we extract the index numbers we want to keep
            for index in index_array[1]:
                preserved_index_numbers.append(ratings[rating_index][index])

            # then we overwrite the array with only the indexes we want to keep
            ratings[rating_index] = preserved_index_numbers

            # we move one digit to the right after first iteration
            position += 1

        # at this point there is only one list element left, we extract it
        rating = ratings[rating_index][0]

        # do additional steps to end up with a binary string
        result = ''
        for digit in rating:
            result += digit

        # finally, we overwrite the array with the new binary string
        ratings[rating_index] = result

    # add the designated ratings as key value and return
    result = { 'oxygen_generating':ratings[0], 'carbon_scrub':ratings[1] }
    return result



if __name__ == '__main__':
    puzzle_input_file = open_puzzle_input()
    diagnostic_report = convert_puzzle_input_to_list(puzzle_input_file)
    puzzle_input_file.close()

    # task 1
    consumption_rating = extract_power_consumption(diagnostic_report)
    gamma_rate_decimal = binary_to_decimal(consumption_rating['gamma'])
    epsilon_rate_decimal = binary_to_decimal(consumption_rating['epsilon'])
    power_consumption = ( gamma_rate_decimal * epsilon_rate_decimal )
    print('The power consumption of the submarine = '+ str(power_consumption))

    # task 2
    ratings = report_by_both_criteria(diagnostic_report)
    ox_gen_rating_decimal = binary_to_decimal(ratings['oxygen_generating'])
    co_scrub_rating_decimal = binary_to_decimal(ratings['carbon_scrub'])
    support_rating = ( ox_gen_rating_decimal * co_scrub_rating_decimal )
    print('The life support rating of the submarine = ' + str(support_rating))
