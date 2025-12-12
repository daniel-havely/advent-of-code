import regex as re
import numpy as np
import itertools
from tqdm import tqdm
import math

with open("input.txt","r") as input_file:
    input_data =  input_file.read()

machine_data = [
    (
        light_str, 
        [tuple(map(int, but[1:-1].split(","))) for but in button_str.split()], 
        [int(jol) for jol in joltage_str.split(",")]
    ) 
    for light_str, button_str, joltage_str 
    in re.findall(r'\[(.*)\] (\(.*\)) \{(.*)\}', input_data)
]

def genCombo(but_ranges, but_jolts, total_jolts, base=True):
    if len(but_ranges) > 1: 
        but_ranges = but_ranges.copy()
        current_range = but_ranges.pop()
        but_jolts = but_jolts.copy()
        current_jolts = but_jolts.pop()
        
        return [
            ([*result, a], joltage + (a*current_jolts))
            for a in (tqdm(current_range) if base else current_range)
            for result, joltage in (genCombo(but_ranges, but_jolts, total_jolts, False ))
            if joltage < total_jolts
            ]
    else:
        return  (([r], r*but_jolts[0]) for r in but_ranges[0])

class Machine:
    def __init__(self, light_data, button_data, joltage_data):
        self.light_data = light_data
        self.button_data = button_data
        self.joltage_data = joltage_data
        
    def getButtonPushesForLights(self):
        target_vector = np.array([int(ch == '#') for ch in self.light_data])
        operator_matrix = np.array([
            [int(j in i) for j in range(len(target_vector))] for i in self.button_data
        ]).transpose()
        binary_format_str = '0'+str(len(self.button_data))+'b'
        input_vectors = np.array([
            [int(i) for i in format(j, binary_format_str)] for j in range(2**len(self.button_data))
        ])

        output_vectors = np.mod(operator_matrix @ input_vectors.transpose(), 2)
        correct_output = np.equal(output_vectors.transpose(), target_vector).all(axis=1)

        return (
            buttons
            for buttons, correct in zip(input_vectors, correct_output)
            if correct
        )
    
    def getButtonPushesForJoltages(self):
        if all(n == 0 for n in self.joltage_data):
            # print(self.light_data, 'Solution!')
            return [[0 for b in self.button_data],]
        else:
            # print(self.joltage_data)
            target_vector = np.array(list(map(lambda x: x%2, self.joltage_data)))
            operator_matrix = np.array([
                [int(j in i) for j in range(len(target_vector))] for i in self.button_data
            ]).transpose()
            binary_format_str = '0'+str(len(self.button_data))+'b'
            input_vectors = np.array([
                [int(i) for i in format(j, binary_format_str)] 
                for j in range(2**len(self.button_data))
            ])

            output_vectors = (operator_matrix @ input_vectors.transpose()).transpose()
            correct_output = np.equal(np.mod(output_vectors, 2), target_vector).all(axis=1)

            new_machine_data = [
                (input, [x-y for x,y in zip(self.joltage_data, output)])
                # (input, self.joltage_data, output)
                for input, output, correct in zip(input_vectors, output_vectors, correct_output)
                if correct
            ]

            # return new_machine_data

            return [
                [
                    x + (2 * y)
                    for x, y in zip(odd_buttons_pressed, even_buttons_pressed)
                ]
                for odd_buttons_pressed, new_joltage_data in new_machine_data
                if all([bool(n >= 0) for n in new_joltage_data])
                for even_buttons_pressed in Machine(
                            self.light_data, 
                            self.button_data, 
                            [int(x/2) for x in new_joltage_data]
                        ).getButtonPushesForJoltages()
            ]


machines = [Machine(*data) for data in machine_data]

# test = machines[29].getButtonPushesForJoltages()

answers = {
    'Fewest button presses required to configure the idicator lights on all of the machines?:': 
        sum(min(map(sum,mach.getButtonPushesForLights())) for mach in machines), 
    'Fewest button presses required to configure the joltage counters on all of the machines?:': 
        sum(min(map(sum,mach.getButtonPushesForJoltages())) for mach in tqdm(machines))
}
max_len_quest = max(len(q) for q in answers.keys())
max_len_soln = max(len(str(s)) for s in answers.values())
for question, solution in answers.items():
    print(f"{question:<{max_len_quest+1}}{solution:>{max_len_soln}}")