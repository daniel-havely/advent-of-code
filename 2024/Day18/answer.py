from tqdm import tqdm

with open("input.txt","r") as input_file:
    input_data = input_file.readlines()

byte_falls = [tuple(map(int,str.strip("\n").split(","))) for str in input_data]

direction_offsets = {
    "N": (0,-1),
    "E": (1,0),
    "S": (0,1),
    "W": (-1,0)
}

directions = ["N","E","S","W"]

class Cell:
    def __init__(self, location):
        self.location = location
        self.cost_to_reach = None
        self.connection = dict.fromkeys(directions)
        
    def buildConnections(self):
        # print(self.location)
        for dir, offset in direction_offsets.items():
            col_ix, row_ix = tuple(map(sum,zip(self.location,offset)))
            if (0 <= row_ix < len(memory_space) and 0 <= col_ix < len(memory_space[row_ix])):
                if memory_space[row_ix][col_ix] is not None:
                    self.connection[dir] = memory_space[row_ix][col_ix]

    def deleteConnections(self):
        for dir, connected_cell in self.connection.items():
            if connected_cell is not None:
                dir_opp = directions[(directions.index(dir)+2)%4]
                self.connection[dir] = None
                connected_cell.connection[dir_opp] = None

    def updateCostToReach(self, updating_cell):
        update = (self.cost_to_reach is None 
            or self.cost_to_reach > updating_cell.cost_to_reach + 1)
        if update:
            self.cost_to_reach = updating_cell.cost_to_reach + 1
        return update


memory_space = [
    [Cell((col_ix,row_ix))
    for col_ix in range(71)] 
    for row_ix in range(71)
    ]

for i in range(1024):
    col_ix, row_ix = byte_falls[i]
    memory_space[row_ix][col_ix] = None

for row in memory_space:
    for cell in row:
        if cell is not None:
            cell.buildConnections()

start_cell = memory_space[0][0]
finish_cell = memory_space[70][70]

def fillCellGrid(first_cell, test_function):
    remaining = {first_cell}
    while remaining:
        working_cell = remaining.pop()
        for dir in directions:
            connected_cell = working_cell.connection[dir]
            if connected_cell is not None:
                if test_function(working_cell, connected_cell):
                    remaining.add(connected_cell)


start_cell.cost_to_reach = 0
fillCellGrid(start_cell, lambda a,b:b.updateCostToReach(a))

print(f"{'Shortest path to exit:': <30}{finish_cell.cost_to_reach: >6}")

touched = set()
def notTouched(cell):
    updated = cell not in touched
    touched.add(cell)
    return updated

for i in tqdm(range(1024,len(byte_falls))):
    col_ix, row_ix = byte_falls[i]
    memory_space[row_ix][col_ix].deleteConnections()
    memory_space[row_ix][col_ix] = None

    touched = set()
    fillCellGrid(start_cell, lambda a,b:notTouched(b))

    if finish_cell not in touched:
        final_byte = byte_falls[i]
        break

print(f"{'Last byte to fall:': <30}{','.join(map(str,final_byte)): >6}")