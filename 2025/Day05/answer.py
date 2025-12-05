with open("input.txt","r") as input_file:
    input_data = input_file.readlines()

fresh_ingredient_id_ranges = [tuple(map(int, rng.split("-"))) for rng in input_data[:input_data.index("\n")]]
available_ingredient_ids = [int(id) for id in input_data[input_data.index("\n")+1:]]

fresh_ingredient_id_ranges.sort()
def isFresh(id):
    for first_id, last_id in fresh_ingredient_id_ranges:
        if id > last_id: continue
        fresh = (id >= first_id)
        break
    else:
        fresh = False
    return fresh

fresh_ingredient_ids = [id for id in available_ingredient_ids if isFresh(id)]

count_fresh_ingredient_ids = 0
current_id = 0
for first_id, last_id in fresh_ingredient_id_ranges:
    if current_id >= last_id: continue
    if current_id >= first_id: first_id = current_id + 1
    count_fresh_ingredient_ids += (last_id - first_id) + 1
    current_id = last_id

answers = {}
answers['How many of the available ingredient IDs are fresh?:'] = len(fresh_ingredient_ids)
answers['How many of all the ingredient IDs are fresh?:'] = count_fresh_ingredient_ids

for question, solution in answers.items():
    print(f"{question:<55}{solution:>15}")