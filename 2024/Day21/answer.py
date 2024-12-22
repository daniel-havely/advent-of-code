with open("input.txt","r") as input_file:
    input_data = input_file.read()

key_sequences = [string.strip() for string in input_data.splitlines()]

direction_offsets = {
    "^": (-1,0),
    ">": (0,1),
    "v": (1,0),
    "<": (0,-1)
}

directions = ["^",">","v","<"]

pad_dir = [["","^","A"],
           ["<","v",">"]]

pad_num = [["7","8","9"],
           ["4","5","6"],
           ["1","2","3"],
           ["","0","A"]]

class Pad:
    def __init__(self, button_list):
        self.button_grid = [[Button(char, (row_ix, col_ix), self) if char else None
                   for col_ix, char in enumerate(row)] 
                   for row_ix, row in enumerate(button_list)]
        
        self.button = {}
        for row in self.button_grid:
            for but in row:
                if but is not None:
                    self.button[but.character] = but
                    but.buildConnections()

class Button:
    def __init__(self, character: str, location: tuple, pad: Pad):
        self.location = location
        self.character = character
        self.connection = dict.fromkeys(directions)
        self.pad = pad
        
    def buildConnections(self):
        for dir, offset in direction_offsets.items():
            row_ix, col_ix = tuple(map(sum,zip(self.location,offset)))
            if 0 <= row_ix < len(self.pad.button_grid) and 0 <= col_ix < len(self.pad.button_grid[row_ix]):
                if self.pad.button_grid[row_ix][col_ix] is not None:
                    self.connection[dir] = self.pad.button_grid[row_ix][col_ix]


directional_pad = Pad(pad_dir)

numerical_pad = Pad(pad_num)

def findPathStrings(current_button: Button, finish_button: Button, visited = set()):
    curr_visited = visited.copy()
    curr_visited.add(current_button)
    if current_button == finish_button:
        return ["A"]
    else:
        return [dir+s for dir in directions 
                if current_button.connection[dir] is not None and current_button.connection[dir] not in curr_visited
                for s in findPathStrings(current_button.connection[dir], finish_button, curr_visited) 
                if s.endswith("A")
                # for s in l
                ]

pad_map_dir_to_dir = {
    (st_ch,fi_ch):findPathStrings(st_but,fi_but) for st_ch, st_but in directional_pad.button.items() for fi_ch, fi_but in directional_pad.button.items()
}

pad_map_num_to_dir = {
    (st_ch,fi_ch):findPathStrings(st_but,fi_but) for st_ch, st_but in numerical_pad.button.items() for fi_ch, fi_but in numerical_pad.button.items()
}

memo = {}
def getStringLengthAterNthRobot(key_1, key_2, robots, start = True):
    try:
        return memo[(key_1, key_2, robots)]
    except KeyError:
        if robots:
            list_of_new_keys = pad_map_num_to_dir[(key_1, key_2)] if start else pad_map_dir_to_dir[(key_1, key_2)]
            memo[(key_1, key_2, robots)] = min(
                                    sum(
                                        getStringLengthAterNthRobot(k_1, k_2, robots-1, False)
                                        for k_1, k_2 in zip("A"+new_keys,new_keys)
                                    ) 
                                    for new_keys in list_of_new_keys)
            return memo[(key_1, key_2, robots)]
        else:
            return 1

def getComplexityScore(sequences, map_to_string_length ):
    return sum( 
        int(seq[:-1])*sum(
                map_to_string_length[(prev_key,key)] 
                for key, prev_key in zip(seq,"A"+seq)
                ) 
        for seq in sequences)

map_num_to_string_lengths_3_robots = {
    (k1,k2):getStringLengthAterNthRobot(k1,k2,3) for k1,k2 in pad_map_num_to_dir.keys()
}

map_num_to_string_lengths_26_robots = {
    (k1,k2):getStringLengthAterNthRobot(k1,k2,26) for k1,k2 in pad_map_num_to_dir.keys()
}

print(f"{'Complexity score with 3 robots:': <35}{getComplexityScore(key_sequences, map_num_to_string_lengths_3_robots): >15}")
print(f"{'Complexity score with 26 robots:': <35}{getComplexityScore(key_sequences, map_num_to_string_lengths_26_robots): >15}")
