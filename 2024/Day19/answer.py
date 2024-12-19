from tqdm import tqdm

with open("input.txt","r") as input_file:
    input_data = input_file.read()

towel_string, div_string, design_string = input_data.partition("\n\n")
towels_available = [string.strip() for string in towel_string.split(",")]
designs_required = [string.strip() for string in design_string.splitlines()]

memo = {}

def matchTowelDesign(design):
    combinations_found = 0
    for towel in towels_available:
        try:
            if towel == design[:len(towel)]:
                remaining_design = design[len(towel):]
                if not remaining_design:
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

print(f"{'Number of designs possible:': <30}{sum(map(bool,matched_designs)): >20}")
print(f"{'Total ways of making designs:': <30}{sum(matched_designs): >20}")
