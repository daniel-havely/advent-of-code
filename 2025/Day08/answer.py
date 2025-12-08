import math

with open("input.txt","r") as input_file:
    input_data = input_file.readlines()

junction_box_positions = [tuple(map(int,line.split(','))) for line in input_data]

connections = [
    (box_1, box_2)
    for index, box_1 in enumerate(junction_box_positions[:-1]) 
    for box_2 in junction_box_positions[index+1:]
]
connections.sort(key=lambda x: math.dist(*x))

circuits = [{box} for box in junction_box_positions]

for iteration, connection in enumerate(connections, start=1):
    new_circuit = set()
    for box in connection:
        for circ_ix, circ in enumerate(circuits):
            if box in circ:
                new_circuit.update(circ)
                del circuits[circ_ix]
                break
    circuits.append(new_circuit)
    if iteration == 1000:
        circuits.sort(key=len, reverse=True)
        circuits_after_1000_connections = circuits.copy()
    if len(circuits) <= 1:
        last_connection = connection
        break

answers = {
    'Product of the sizes of the three largest circuits?:': 
        math.prod([len(c) for c in circuits_after_1000_connections[:3]]), 
    'Product of the X coordinates of the last two junction boxes to connect?:': 
        last_connection[0][0] * last_connection[1][0]
}
max_len_quest = max(len(q) for q in answers.keys())
max_len_soln = max(len(str(s)) for s in answers.values())
for question, solution in answers.items():
    print(f"{question:<{max_len_quest+1}}{solution:>{max_len_soln}}")