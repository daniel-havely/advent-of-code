import re
from tqdm import tqdm

with open("input.txt","r") as input_file:
    input_data = input_file.read()

regex_string = r'p=(\d+),(\d+) v=(-?\d+),(-?\d+)'

map_size = (101, 103)

class Robot:
    def __init__(self, loc_x, loc_y, vel_x, vel_y):
        self.location = (loc_x, loc_y)
        self.velocity = (vel_x, vel_y)
    
    def getFutureLocation(self, time_in_sec):
        return tuple(map(lambda z: (z[0]+time_in_sec*z[1])%z[2],zip(self.location,self.velocity,map_size)))


robots = [Robot(*map(int,prm)) for prm in re.findall(regex_string, input_data)]

def getSafetyFactor(list_of_robots, time_in_sec):
    qmap = lambda z: 0 if z[0] <z[1]//2 else 1 if z[0] > z[1]//2 else None

    quadrant_count = {}
    for rob in list_of_robots:
        q = tuple(map(qmap,zip(rob.getFutureLocation(time_in_sec),map_size)))
        if all(i is not None for i in q):
            quadrant_count[q] = quadrant_count.get(q,0)+1

    product = 1
    for v in quadrant_count.values():
        product *= v

    return product

print(f"{'Safety factor': <20}{getSafetyFactor(robots, 100)}")

safety_factors = []
for time in tqdm(range(10000)):
    sf = getSafetyFactor(robots, time)
    safety_factors.append(getSafetyFactor(robots, time))
    if sf < (sum(safety_factors)/len(safety_factors))/2: break


print(f"{'Minimum safety factor at': <30}{safety_factors.index(min(safety_factors))}{'s'}")

tile_map = [["."]*101 for _ in range(103)]

for rob in robots:
    x,y = rob.getFutureLocation(safety_factors.index(min(safety_factors)))
    tile_map[y][x] = "@"

for row in tile_map:
    print("".join(row))

