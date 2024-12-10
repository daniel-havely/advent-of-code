with open("input.txt","r") as input_file:
    input_data = [[int(x) for x in list(number_string)] for number_string in input_file.read().split("\n") if number_string]

search_directions = [(0,1),(0,-1),(1,0),(-1,0)]

class TrailHead:
    def __init__(self, location, trails):
        self.location = location
        self.trails = trails
    
    def getScore(self):
        return len({route[-1] for route in self.trails})
    
    def getRating(self):
        return len(self.trails)


def findTrails(reindeer_map, route):
    start_location = route[-1]
    start_row_index, start_col_index = start_location
    hiking_trails = list()
    for row_index, col_index in [tuple(map(sum,zip(start_location,offset))) for offset in search_directions]:
        try:
            if row_index < 0: raise IndexError
            if col_index < 0: raise IndexError
            if reindeer_map[row_index][col_index] ==  reindeer_map[start_row_index][start_col_index] + 1:
                route_branch = route + [(row_index, col_index)]
                if reindeer_map[row_index][col_index] == 9:
                    hiking_trails.append(route_branch)
                else:
                    hiking_trails.extend(findTrails(reindeer_map, route_branch))
        except IndexError:
            continue
    return hiking_trails

trail_heads = {
    TrailHead((row_index,col_index), findTrails(input_data, [(row_index,col_index)]))
    for row_index, row in enumerate(input_data)
    for col_index, val in enumerate(row)
    if val == 0
}

print("Sum of trailhead scores:", sum(th.getScore() for th in trail_heads), sep="\t")
print("Sum of trailhead ratings:", sum(th.getRating() for th in trail_heads), sep="\t")