from tqdm import tqdm


with open("input.txt","r") as input_file:
    input_data = input_file.readlines()

towels_available = [string.strip() for lst in 
                            [string.strip("\n").split(",") for string in input_data[:input_data.index("\n")]] 
                    for string in lst]
designs_required = [string.strip("\n").strip() for string in input_data[input_data.index("\n")+1:]]


memo = {}

def matchTowelDesign(design):
    combinations_found = 0
    for towel in towels_available:
        try:
            if towel == design[:len(towel)]:
                remaining_design = design[len(towel):]
                if towel == design:
                    combinations_found += 1
                else:
                    try:
                        combinations_found += memo[remaining_design]
                    except KeyError:
                        memo[remaining_design] = matchTowelDesign(remaining_design)
                        combinations_found += memo[remaining_design]
        except IndexError:
            continue
    return combinations_found

matched_designs = [matchTowelDesign(design) for design in tqdm(designs_required)]

print(f"{'Number of designs possible:': <30}{sum(1 if num else 0  for num in matched_designs): >20}")
print(f"{'Total ways of making designs:': <30}{sum(matched_designs): >20}")
