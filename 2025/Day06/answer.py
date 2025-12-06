import math

with open("input.txt","r") as input_file:
    input_data =  input_file.readlines()


operation = lambda x: math.prod if x == '*' else sum

problems = [st for st in zip(*map(lambda x: x.split(),input_data))]
solutions = [operation(y[-1])(list(map(int,y[:-1])))  for y in problems]

problems_cephalopod_form = []
input_data_columns = [y for y in zip(*input_data)]
while input_data_columns:
    column = input_data_columns.pop()
    if ''.join(column).strip() == '':
        problems_cephalopod_form.append(list())
    else:
        problems_cephalopod_form[-1].append(''.join(column[:-1]))
        if column[-1] != ' ': problems_cephalopod_form[-1].append(column[-1])
solutions_cephalopod_form = \
    [operation(y[-1])(list(map(int,y[:-1])))  for y in problems_cephalopod_form]

answers = {
    'What is the grand total of all of the answers?:': 
        sum(solutions), 
    'What is the grand total of all of the answers using cephalopod logic?:': 
        sum(solutions_cephalopod_form)
}
max_len_quest = max(len(q) for q in answers.keys())
max_len_soln = max(len(str(s)) for s in answers.values())
for question, solution in answers.items():
    print(f"{question:<{max_len_quest+1}}{solution:>{max_len_soln}}")