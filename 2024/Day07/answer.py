from tqdm import tqdm

with open("input.txt","r") as input_file:
    input_data = input_file.readlines()

calibration_equations = [
        {
        "target": int(line.split(":")[0]),
        "operands": [int(num) for num in line.split(":")[1].strip().split() if num]
        }
    for line in input_data if ":" in line
    ]

def getPossibleResults(operands, operations):
    current_operand = operands.pop()
    return {opr(result,current_operand) for opr in operations
            for result in (getPossibleResults(operands.copy(), operations) if len(operands) > 1 else operands)}

def sumCorrectEquations(equation_list, operations):
    return sum(
        [
        eqation["target"] 
        for eqation in tqdm(equation_list)
        if eqation["target"] in getPossibleResults(eqation["operands"], operations)
        ]
    )

operators_to_use = [lambda x,y:x+y, lambda x,y:x*y]
print("Calibration result (part I)", sumCorrectEquations(calibration_equations, operators_to_use), sep="\t")

operators_to_use = [lambda x,y:x+y, lambda x,y:x*y, lambda x,y:int(str(x)+str(y))]
print("Calibration result (part II)", sumCorrectEquations(calibration_equations, operators_to_use), sep="\t")
