from tqdm import tqdm

with open("input.txt","r") as input_file:
    input_data = [list(string) for string in input_file.read().split("\n") if string]

directions = {
    "^": (-1,0),
    ">": (0,1),
    "v": (1,0),
    "<": (0,-1)
}

dir_keys = list(directions.keys())

def traverseMap(elf_map, start_location, start_direction):
    loc = start_location
    dir = start_direction
    on_map = True
    in_loop = False
    locations_visited = []
    while on_map and not in_loop:
        locations_visited.append({"location": loc, "direction": dir})
        for attempt_direction in range(4):
            move_dir = dir_keys[(dir_keys.index(dir)+attempt_direction)%4]
            move_loc = tuple(map(sum, zip(loc, directions[move_dir])))
            move_row, move_col = move_loc
            if not (
                0 <= move_row < len(elf_map)
                and
                0 <= move_col < len(elf_map[move_row])
            ):
                on_map = False
                break
            else:
                if elf_map[move_row][move_col] not in {"#", "O"}:
                    if {"location": move_loc, "direction": move_dir} in locations_visited:
                        in_loop = True
                    else:
                        loc = move_loc
                        dir = move_dir
                    break
    return {"locations visited": locations_visited, "in loop": in_loop, "off map": not on_map}

start_parameters = next(
                {"start_location": (row_ix, col_ix), "start_direction": char}
                for row_ix, row in enumerate(input_data) 
                for col_ix, char in enumerate(row) if char in dir_keys
                )
            
original_journey = traverseMap(input_data,**start_parameters)["locations visited"]

loopy_journeys = []
tried_locations = set()
for start_loc, start_dir, obstr_loc in tqdm([
                        (start["location"],start["direction"],obstr["location"]) 
                        for start,obstr in zip(original_journey, original_journey[1:])
                        ]):
    if obstr_loc not in tried_locations:
        tried_locations.add(obstr_loc)
        obstr_row, obstr_col = obstr_loc
        new_map = [row.copy() for row in input_data]
        new_map[obstr_row][obstr_col] = "O"
        result_of_journey = traverseMap(new_map, start_loc, start_dir)
        if result_of_journey["in loop"]:
            loopy_journeys.append(result_of_journey["locations visited"])

print("Locations visited", len(set([loc["location"] for loc in original_journey])), sep="\t")
print("Obtruction locations" ,len(loopy_journeys), sep="\t")

