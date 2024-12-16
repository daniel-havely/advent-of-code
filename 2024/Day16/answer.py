with open("input.txt","r") as input_file:
    input_data = input_file.readlines()

reindeer_maze = [list(str.strip("\n")) for str in input_data]


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
        self.cost_to_reach = dict.fromkeys(directions)
        self.connection = dict.fromkeys(directions)
    
    def getMinimumCost(self):
        return min(val for val in self.cost_to_reach.values() if val is not None)
    
    def buildConnections(self):
        for dir, offset in direction_offsets.items():
            row_ix, col_ix = tuple(map(sum,zip(self.location,offset)))
            if cell_grid[row_ix][col_ix] is not None:
                self.connection[dir] = cell_grid[row_ix][col_ix]
    
    def updateCosts(self, cost_to_reach, direction):
        updated = False
        for dir_delta in range(-1,3):
            dir = directions[(directions.index(direction)+dir_delta)%4]
            new_cost = cost_to_reach + 1000*abs(dir_delta) + 1
            if (
                self.cost_to_reach[dir] is None
                or
                self.cost_to_reach[dir] > new_cost
            ):
                self.cost_to_reach[dir] = new_cost
                updated = True
        return updated
                
    
cell_grid = [
    [Cell(ch, (row_ix,col_ix)) if ch != "#" else None 
    for col_ix,ch in enumerate(row)] 
    for row_ix, row in enumerate(reindeer_maze)
    ]

for row in cell_grid:
    for cell in row:
        if cell is not None:
            cell.buildConnections()

start_cell = next(cell for row in cell_grid for cell in row if cell is not None and cell.character == "S")
start_direction = "E"
start_cell.updateCosts(-1, start_direction)
remaining = {start_cell}
while remaining:
    working_cell = remaining.pop()
    for dir in directions:
        connected_cell = working_cell.connection[dir]
        if connected_cell is not None:
            if connected_cell.updateCosts(working_cell.cost_to_reach[dir], dir):
                remaining.add(connected_cell)

finish_cell = next(cell for row in cell_grid for cell in row if cell is not None and cell.character == "E")

print(f"{'Minimum score to complete the maze:': <40}{finish_cell.getMinimumCost(): >6}")

path_cells = set()
finish_cell.path_direction = min(finish_cell.cost_to_reach, key=finish_cell.cost_to_reach.get)
remaining  = {finish_cell}
while remaining:
    working_cell = remaining.pop()
    path_cells.add(working_cell)
    for dir in directions:
        connected_cell = working_cell.connection[dir]
        if connected_cell is not None and connected_cell not in path_cells:
            dir_opp = directions[(directions.index(dir)+2)%4]
            for dir_delta in range(-1,3):
                dir_to_test = directions[(directions.index(dir_opp)+dir_delta)%4]
                if dir_to_test == working_cell.path_direction:
                    cost_to_test = connected_cell.cost_to_reach[dir_opp] + 1000*abs(dir_delta) + 1
                    if cost_to_test == working_cell.cost_to_reach[working_cell.path_direction]:
                        connected_cell.path_direction = dir_opp
                        remaining.add(connected_cell)

print(f"{'Tiles along best paths through maze:': <40}{len(path_cells): >6}")



