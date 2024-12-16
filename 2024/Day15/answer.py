with open("input.txt","r") as input_file:
    input_data = input_file.readlines()

goods_map = [list(str.strip("\n")) for str in input_data[:input_data.index("\n")]]
robot_intructions = "".join(str.strip("\n") for str in input_data[input_data.index("\n")+1:])

directions = {
    "^": (-1,0),
    ">": (0,1),
    "v": (1,0),
    "<": (0,-1)
}

class Map:
    def __init__(self, input_map):
        self.grid = [row.copy() for row in input_map]
        self.robot_location = next(
                (row_ix, col_ix)
                for row_ix, row in enumerate(self.grid) 
                for col_ix, char in enumerate(row) if char == "@"
                )
    
    def __str__(self):
        return "\n".join("".join(line) for line in self.grid)
    
    def getMapLocation(self, location):
        row_ix, col_ix = location
        return self.grid[row_ix][col_ix]

    def setMapLocation(self, location, value):
        row_ix, col_ix = location
        self.grid[row_ix][col_ix] = value

    def getAdjacentR(self, location):
        return tuple(map(sum,zip(location, (0,1))))
    
    def getAdjacentL(self, location):
        return tuple(map(sum,zip(location, (0,-1))))

    def shiftBox(self, location, direction):
        wide_box = self.getMapLocation(location) in {"["}
        new_location = tuple(map(sum,zip(location, directions[direction])))
        if wide_box:
            self.setMapLocation(location, ".")
            self.setMapLocation(self.getAdjacentR(location), ".")
            self.setMapLocation(new_location, "[")
            self.setMapLocation(self.getAdjacentR(new_location), "]")
        else:
            self.setMapLocation(location, ".")
            self.setMapLocation(new_location, "O")
        
    def moveBoxes(self, location, direction):
        box_shifts_required = []
        if self.getMapLocation(location) == "]":
            location = self.getAdjacentL(location)
        wide_box = self.getMapLocation(location) in {"["}
        vertical =  direction in {"^","v"}
        next_location = tuple(map(sum,zip(location, directions[direction])))
        if wide_box and direction == ">": next_location = tuple(map(sum,zip(next_location, directions[direction])))
        if wide_box:
            if vertical:
                whats_infront = self.getMapLocation(next_location)+self.getMapLocation(self.getAdjacentR(next_location))
            elif direction == ">":
                whats_infront = self.getMapLocation(next_location)
            elif direction == "<":
                whats_infront = self.getMapLocation(next_location)
        else:
            whats_infront = self.getMapLocation(next_location)
        if all(ch == "." for ch in whats_infront):
            box_shifts_required.append(
                {"okay to move": True,
                 "location": location,
                 "direction": direction}
            )
        elif any(ch == "#" for ch in whats_infront):
            box_shifts_required.append(
                {"okay to move": False,
                 "location": location,
                 "direction": direction}
            )
        else:
            for l in (
                self.moveBoxes(loc, direction)
                for loc in 
                {self.getAdjacentR(next_location) if n else next_location for n, ch in enumerate(whats_infront) if ch in {"[", "O"}}
                |{next_location if n else self.getAdjacentL(next_location) for n, ch in enumerate(whats_infront) if ch in {"]"}}
            ):
                box_shifts_required.extend(l)
            box_shifts_required.append(
                {"okay to move": True,
                 "location": location,
                 "direction": direction}
            )
        return box_shifts_required

    def moveRobot(self, direction):
        move_location = tuple(map(sum,zip(self.robot_location, directions[direction])))
        if self.getMapLocation(move_location) == ".":
            self.setMapLocation(self.robot_location, ".")
            self.setMapLocation(move_location, "@")
            self.robot_location = move_location
        elif self.getMapLocation(move_location) in {"[", "]", "O"}:
            box_shifts = self.moveBoxes(move_location, direction)
            if all(shift["okay to move"] for shift in box_shifts):
                boxes_already_shifted = set()
                for shift in box_shifts:
                    if shift["location"] not in boxes_already_shifted:
                        self.shiftBox(shift["location"], shift["direction"])
                        boxes_already_shifted.add(shift["location"])
                self.setMapLocation(self.robot_location, ".")
                self.setMapLocation(move_location, "@")
                self.robot_location = move_location

    def getSumOfGPS(self):
        return sum(
                [100*row_ix + col_ix for row_ix, row in enumerate(self.grid) for col_ix, char in enumerate(row) if char in {"[", "O"}]
            )


wide_elements = {
    "#": "##",
    "O": "[]",
    ".": "..",
    "@": "@."
}

first_map = Map(goods_map)
second_map = Map([[c for ch in row for c in wide_elements[ch]] for row in goods_map])
for instr in robot_intructions:
    first_map.moveRobot(instr)
    second_map.moveRobot(instr)
    

print(f"{'Sum of GPS for original map': <30}{first_map.getSumOfGPS(): >10}")
print(f"{'Sum of GPS for widened map': <30}{second_map.getSumOfGPS(): >10}")
