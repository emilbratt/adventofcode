#!/usr/bin/env python3
import os

DIR_MAIN_FILE = os.path.dirname(os.path.abspath(__file__))
FILE_PUZZLE_INPUT = os.path.join(DIR_MAIN_FILE,'puzzle_input.txt')


def open_puzzle_input():
    puzzle_input = open(FILE_PUZZLE_INPUT)
    return puzzle_input


def get_puzzle_input(puzzle_input: object):
    return puzzle_input.readline()


def create_list(string_in: str):
    return [f for f in string_in]


def get_arr_len(arr: list):
    arr_len = 0
    for _ in arr:
        arr_len += 1
    return arr_len


def get_highest_number(a: int, b:int):
    return ( a * (a > b) + b * (a <= b) )


def get_lowest_number(a: int, b:int):
    return ( a * (a < b) + b * (a >= b) )


def cast_arr_elements_to_int(arr: list):
    index = 0
    new_arr = []
    while index < get_arr_len(arr) > 0:
        new_arr.append( int(arr[index]) )
        index += 1
    return new_arr


def remove_array_delimitter(arr: list, delimitter: str):
    '''
        turns [
                ['4', '9', ',', '4', '8', ',', '9', '8']
              ]

        into  [
                ['4', '9'], ['4', '8'], ['9', '8']
              ]
        where delimitter = ","
    '''

    delimitter_count = 0
    is_delimitter = 0
    temp_number_register = { 0: [], 1: [], }
    key_register = { 0: [], 1: [], }
    arr_index = 0
    while ( arr_index + 1 ) < get_arr_len(arr):

        # store first character in the array
        arr_element = arr[arr_index]

        # if delimitter is found: is_delimitter = 1
        is_delimitter = 1 * ( arr_element == delimitter )

        # index based on how many delimitters we have counted
        delimitter_count += is_delimitter

        insert_dict = {delimitter_count:arr_element}
        temp_number_register[is_delimitter].append(insert_dict)
        key_register[is_delimitter].append(delimitter_count)

        arr_index += 1

    number_register_dict = {}
    key_register = key_register[0]
    arr = temp_number_register[0]

    # add designated key value that holds a list for each number
    for key in key_register:
        number_register_dict[key] = []

    # append each number as its own list into its correct key
    for dict in arr:
        for key in dict:
            # some keys are the same, this way we preserve the digits
            number_register_dict[key].append(dict[key])

    # finally push all the values into a 2 dimensional list
    final_list = []
    for key in number_register_dict:
        final_list.append(number_register_dict[key])

    return final_list


def one_dimesion_down_number_array(number_list: list):
    '''
        turns [
                [ ['1'], ['2'] ] , [ ['1'] ]
              ]

        into  [
                ['12'] , ['1']
              ]
    '''
    extracted_numbers = []
    main_index = 0
    while main_index < get_arr_len(number_list):
        current_number = number_list[main_index]
        sub_index = 0
        n = ''
        while get_arr_len(current_number) > sub_index:
            n += str(current_number[sub_index])
            sub_index += 1

        extracted_numbers.append(n)
        main_index += 1

    return extracted_numbers


def shell_sort(arr: list):
    index_count = get_arr_len(arr)
    gap_val = index_count // 2
    while gap_val > 0:
        i = gap_val
        while i < index_count:
            temp = arr[i]
            j = i
            while j >= gap_val and arr[j - gap_val] > temp:
                arr[j] = arr[j - gap_val]
                j -= gap_val

            arr[j] = temp
            i += 1

        # the new gap will be half of the existing gap and so on until gap = 0
        gap_val = gap_val // 2

    return arr


def get_highest_number_arr(arr: list):
    arr_length = get_arr_len(arr)
    index = 1
    highest_num = int(arr[0])
    while index < arr_length:
        highest_num = get_highest_number(int(arr[index]), highest_num)
        index += 1
    return highest_num


def get_lowest_number_arr(arr: list):
    arr_length = get_arr_len(arr)
    index = 1
    lowest_num = int(arr[0])
    while index < arr_length:
        lowest_num = get_lowest_number(int(arr[index]), lowest_num)
        index += 1
    return lowest_num


def get_next_target(fuel_map: dict, targets: dict):

    # if mid is closest
    fuel_l_tgt = fuel_map['low']
    fuel_m_tgt = fuel_map['mid']
    fuel_h_trgt = fuel_map['high']

    # if lowest target drops below 1, make sure it is at least 1
    is_zero = targets['low'] < 1
    targets['low'] += is_zero

    # this is where the new target is calculated based on the fuel consumption
    target_base_map = {
        'shrink_target_gap': {
            'closest_target':targets['mid'],
            'low':targets['mid'] - (targets['mid'] // targets['low']),
            'mid':targets['mid'],
            'high':targets['mid'] + (targets['high'] // targets['low']),
        },
        'move_target_down': {
            'closest_target':targets['low'],
            'low':targets['low'] - (targets['low'] // 2),
            'mid':targets['mid'] - (targets['mid'] // 2),
            'high':targets['high'] - (targets['high'] // 2),
        },
        'move_target_up': {
            'closest_target':targets['high'],
            'low':targets['low'] + (targets['low'] // 2),
            'mid':targets['mid'] + (targets['mid'] // 2),
            'high':targets['high'] + (targets['high'] // 2),
        },
    }

    # the target with lowest fuel count is the base for calculating new targets
    target_key_map = {
        0: 'shrink_target_gap', # if mid target has lowest fuel count
        1: 'move_target_down', # if low target has lowest fuel count
        2: 'move_target_up', # if high target has lowest fuel count
    }
    is_lowest = (fuel_l_tgt < fuel_m_tgt and fuel_l_tgt < fuel_h_trgt) * 1
    is_highest = (fuel_h_trgt < fuel_m_tgt and fuel_h_trgt < fuel_l_tgt) * 2
    target_key = target_key_map[(is_lowest + is_highest)]

    return target_base_map[target_key]


def run_fuel_calculation_constant(puzzle_input: list):
    input_arr_len = get_arr_len(puzzle_input)

    # we sort the array before splitting it by length index
    puzzle_input = shell_sort(puzzle_input)

    # then find the best target by using the middle number in the array
    target = puzzle_input[input_arr_len // 2]
    index = 0
    fuel = 0
    while index < input_arr_len:
        cur_pos = puzzle_input[index]
        index += 1
        top_n = get_highest_number(cur_pos, target)
        bottom_n = get_lowest_number(cur_pos, target)
        fuel += top_n - bottom_n

    return { 'target':target, 'fuel': fuel }


def get_fuel_inc_by_target(cur_pos: int, target: int):
    '''
        get the correct increase + 1 for each step
        using the "sum of the first n positive integers"
        1 step = 1
        2 steps = 3
        3 steps = 6
        4 steps = 10
        5 steps = 15
        6 steps = 21 and so forth
        read the over 1 decade old thread about this here:
        https://math.stackexchange.com/questions/2260/proof-1234-cdotsn-fracn-timesn12
    '''
    # get the N in the formula: N x (N +1) / 2
    top_n = get_highest_number(cur_pos, target)
    bottom_n = get_lowest_number(cur_pos, target)
    N = top_n - bottom_n

    # calculate the consumption with the formula
    fuel = ( N * (N + 1) ) / 2
    return fuel


def run_fuel_calculation_increase(puzzle_input: list):
    '''
        we start with dividing the highest found target creating a split value
        that will serve as the base forming new targets during iterations

        the target producing the lowest fuel consumption will be the new
        base for producing 3 new targets and so on
    '''

    # create base target positions that we use before calculating better targets
    highest_position = get_highest_number_arr(puzzle_input)
    split = highest_position // 2
    targets = {
        'low': split // 2,
        'mid': split,
        'high': split + (split // 2),
    }

    input_arr_len = get_arr_len(puzzle_input)
    end_loop = False
    while end_loop == False:
        fuel_map = {}
        fuel_map['low'] = 0
        fuel_map['mid'] = 0
        fuel_map['high'] = 0
        index = 0
        while index < input_arr_len:
            cur_pos = puzzle_input[index]
            index += 1
            fuel_map['low'] += get_fuel_inc_by_target(cur_pos,  targets['low'])
            fuel_map['mid'] += get_fuel_inc_by_target(cur_pos, targets['mid'])
            fuel_map['high'] += get_fuel_inc_by_target(cur_pos, targets['high'])


        # keep old targets to check if we need to jump out of loop
        old_low_target = targets['low']
        old_high_target = targets['high']
        old_mid_target = targets['mid']
        targets = get_next_target(fuel_map, targets)

        # check if at least 2 targets are the same
        same_low = (old_low_target == targets['low'])
        same_high = (old_high_target == targets['high'])
        same_mid = (old_mid_target == targets['mid'])
        same_targets = (same_low + same_high + same_mid) > 1

        # highest target should not exceeded the highest number
        exceeded_highest_position = (targets['high'] > highest_position)

        # no target should be the same
        found_target = (
                    targets['low'] == targets['mid'] or
                    targets['high'] == targets['mid'])

        # if any of the above conditions are true, jump out and go to next step
        end_loop = (same_targets + exceeded_highest_position + found_target)


    # this is the next step
    # most likely we have found a close target until now, lets find the exact
    # one to get the least amount of fuel for that target

    # get lowest fuel calculated so far
    fuel_arr = [fuel_map['low'], fuel_map['mid'],  fuel_map['high']]
    fuel = get_lowest_number_arr(fuel_arr)

    # get the best target we have so far
    target = targets['closest_target']

    # run the new algo to find the least expensive target and the fuel count
    result = calc_exact_target(puzzle_input, fuel, target)
    return result


def calc_exact_target(puzzle_input: list,fuel: int, target: int):
    input_arr_len = get_arr_len(puzzle_input)

    '''
        this iterates the targets by first subtracting then adding target

        subtracting 1 for each to check if that decreases the amount of fuel

        then adding 1 for each to check if that decreases the amount of fuel

        whichever makes the fuel consumption go down will affect the total fuel
    '''

    ### increasing the target
    fuel_has_decreased = True
    old_fuel = fuel
    fuel_map = {}
    while fuel_has_decreased:
        # keep old fuel and target
        fuel_map[target] = old_fuel
        target += 1
        index = 0
        new_fuel = 0
        while index < input_arr_len:
            cur_pos = puzzle_input[index]
            index += 1
            new_fuel += get_fuel_inc_by_target(cur_pos, target)
        fuel_map[target] = new_fuel
        fuel_has_decreased = (new_fuel < old_fuel)
        old_fuel = new_fuel
    # we subtract 1 to go back 1 step getting the correct value
    target = target - 1
    fuel = fuel_map[target]

    ### decreasing the target
    fuel_has_decreased = True
    old_fuel = fuel
    fuel_map = {}
    while fuel_has_decreased:
        fuel_map[target] = old_fuel
        target -= 1
        index = 0
        new_fuel = 0
        while index < input_arr_len:
            cur_pos = puzzle_input[index]
            index += 1
            new_fuel += get_fuel_inc_by_target(cur_pos, target)
        fuel_map[target] = new_fuel
        fuel_has_decreased = (new_fuel < old_fuel)
        old_fuel = new_fuel
    # we add 1 to go back 1 step getting the correct value
    target = target + 1
    fuel = fuel_map[target]

    return { 'target':target, 'fuel': fuel }



if __name__ == '__main__':

    '''
        align crabs (all on same number by moving (adding + or -))
        1. find lowest and highest number in array
        2. find most common number
    '''

    # fetch and format input data to a list
    puzzle_input_file = open_puzzle_input()
    puzzle_input = get_puzzle_input(puzzle_input_file)
    puzzle_input_file.close()
    puzzle_input = create_list(puzzle_input)

    # wash and prepare array
    puzzle_input = remove_array_delimitter(puzzle_input, ',')
    puzzle_input = one_dimesion_down_number_array(puzzle_input)

    # convert all values to int
    puzzle_input = cast_arr_elements_to_int(puzzle_input)


    # task 1: expected result: 337833
    print('Task 1')
    result = run_fuel_calculation_constant(puzzle_input)
    target = str(result['target'])
    value = str(result['fuel'])
    print('Most efficient target is ' + target + ' with fuel cost at ' + value)
    print()


    # task 1: expected result: 96678050
    print('Task 2')
    # result = calculate_fuel_increased_rate(puzzle_input)
    result = run_fuel_calculation_increase(puzzle_input)
    target = str(result['target'])
    value = str( int(result['fuel']) )
    print('Most efficient target is ' + target + ' with fuel cost at ' + value)
