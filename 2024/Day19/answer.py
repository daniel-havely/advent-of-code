from tqdm import tqdm

with open("input.txt","r") as input_file:
    input_data = input_file.read()

towel_string, div_string, design_string = input_data.partition("\n\n")
towels_available = [string.strip() for string in towel_string.split(",")]
designs_required = [string.strip() for string in design_string.splitlines()]

memo = {}

def matchTowelDesign(design):
    if design:
        try:
            return memo[design]
        except KeyError:
            memo[design] = sum(
                matchTowelDesign(design[:-len(towel)]) for towel in towels_available if design.endswith(towel)
                )
            return memo[design]
    else:
        return 1

matched_designs = [matchTowelDesign(design) for design in tqdm(designs_required)]

print(f"{'Number of designs possible:': <30}{sum(map(bool,matched_designs)): >20}")
print(f"{'Total ways of making designs:': <30}{sum(matched_designs): >20}")
