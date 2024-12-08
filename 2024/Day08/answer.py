with open("input.txt","r") as input_file:
    input_data = [list(string) for string in input_file.read().split("\n") if string]

antennae = {}
for ix_row, row in enumerate(input_data):
    for ix_col, char in enumerate(row):
        antennae.setdefault(char,[]).append((ix_row,ix_col))
del antennae["."]

resonant_antinodes = set()
harmonic_antinodes = set()
antinodes = set()
for antenna_locations in antennae.values():
    for location_pair in [(i,j) for i in antenna_locations for j in antenna_locations if i != j]:
        x, y = location_pair
        vector_x_to_y = tuple(map(lambda co_ord:co_ord[1]-co_ord[0], zip(x,y)))
        on_map = True
        antinode_location = y
        distance = 0
        while on_map:
            if distance == 1: resonant_antinodes.add(antinode_location)
            harmonic_antinodes.add(antinode_location)

            antinode_location = tuple(map(sum, zip(antinode_location,vector_x_to_y)))
            distance += 1
            an_row, an_col = antinode_location
            if not (
                0 <= an_row < len(input_data)
                and
                0 <= an_col < len(input_data[an_row])
            ):
                on_map = False
            
print("Resonant antinodes", len(resonant_antinodes), sep="\t")
print("All harmonic antinodes", len(harmonic_antinodes), sep="\t")
        





