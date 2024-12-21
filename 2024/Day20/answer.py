from tqdm import tqdm

with open("input.txt","r") as input_file:
    input_data = input_file.readlines()

race_track = [list(str.strip("\n")) for str in input_data]

direction_offsets = {
    "N": (-1,0),
    "E": (0,1),
    "S": (1,0),
    "W": (0,-1)
}

directions = ["N","E","S","W"]

class Cell:
    def __init__(self, character, location):
        self.location = location
        self.character = character
        self.cost_to_reach = None
        self.connection = dict.fromkeys(directions)
        self.cheats = {}
        
    def buildConnections(self):
        for dir, offset in direction_offsets.items():
            row_ix, col_ix = tuple(map(sum,zip(self.location,offset)))
            if cell_grid[row_ix][col_ix] is not None:
                self.connection[dir] = cell_grid[row_ix][col_ix]

    def updateCostToReach(self, updating_cell):
        update = (self.cost_to_reach is None 
            or self.cost_to_reach > updating_cell.cost_to_reach + 1)
        if update:
            self.cost_to_reach = updating_cell.cost_to_reach + 1
        return update
    
    def findCheats(self, picoseconds):
        row_ix, col_ix = self.location
        for row_offset in range(-picoseconds, picoseconds+1):
            for col_offset in range(-picoseconds+abs(row_offset), picoseconds+1-abs(row_offset)):
                look_row_ix = row_ix + row_offset
                look_col_ix = col_ix + col_offset
                if 0 <= look_row_ix < len(cell_grid) and 0 <= look_col_ix < len(cell_grid[look_row_ix]):
                    cheat_cell = cell_grid[look_row_ix][look_col_ix]
                    if cheat_cell is not None:
                        self.cheats[cheat_cell] = (
                            (cheat_cell.cost_to_reach - self.cost_to_reach)
                            - (abs(row_offset) + abs(col_offset))
                            )

    
cell_grid = [
    [Cell(ch, (row_ix,col_ix)) if ch != "#" else None 
    for col_ix,ch in enumerate(row)] 
    for row_ix, row in enumerate(race_track)
    ]

for row in cell_grid:
    for cell in row:
        if cell is not None:
            cell.buildConnections()

start_cell = next(cell for row in cell_grid for cell in row if cell is not None and cell.character == "S")
start_cell.cost_to_reach = 0
remaining = {start_cell}
track = []
while remaining:
    working_cell = remaining.pop()
    track.append(working_cell)
    for dir in directions:
        connected_cell = working_cell.connection[dir]
        if connected_cell is not None:
            if connected_cell.updateCostToReach(working_cell):
                remaining.add(connected_cell)

for cell in tqdm(track):
    cell.findCheats(2)

print(f"{'Cheats of 2ps saving >=100ps:': <45}{sum(cheat_gain >= 100 for cell in track for cheat_gain in cell.cheats.values()): >6}")

for cell in tqdm(track):
    cell.findCheats(20)

print(f"{'Cheats of up to 20ps saving >=100ps:': <45}{sum(cheat_gain >= 100 for cell in track for cheat_gain in cell.cheats.values()): >6}")