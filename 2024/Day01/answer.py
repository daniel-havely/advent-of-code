with open("input.txt","r") as input_file:
    input_data = [[int(num) for num in number_string.split()] for number_string in input_file.read().split("\n") if number_string]

location_lists = list(map(list,zip(*input_data)))

for col in location_lists:
    col.sort()

distances = [abs(a-b) for a,b in zip(*location_lists)]

print("Total distance  ",sum(distances),sep="\t")

similarity_coeffs = [loc*location_lists[1].count(loc) for loc in location_lists[0]]

print("Total similarity",sum(similarity_coeffs),sep="\t")