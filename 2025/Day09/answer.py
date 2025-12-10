import math
from tqdm import tqdm
import matplotlib.pyplot as plt

with open("input.txt","r") as input_file:
    input_data = input_file.readlines()


sign = lambda x: (x>0)-(x<0)

def getPointsBetween(point_1, point_2):
    (x1, y1), (x2, y2) = point_1, point_2
    x_inc = sign(x2-x1)
    y_inc = sign(y2-y1)
    return (
        x for x in zip(range(x1,x2,x_inc) if x_inc else [x1]*abs(y2-y1),range(y1,y2,y_inc) if y_inc else [y1]*abs(x2-x1))
    )
    
area = lambda a,b: math.prod(map(lambda x,y: abs(x-y)+1,a,b))

class Rectangle:
    def __init__(self, points):
        (x1, y1), (x2, y2) = points
        self.points = [(x1, y1), (x1, y2), (x2, y2) ,(x2, y1)]
        self.edges = [(a,b) for a,b in zip(self.points, self.points[1:]+self.points[:1])]
        # self.area = abs(((x2-x1)+1)*((y2-y1)+1))
        self.area = area(*points)
    
    def perimeter (self):
        for edge in self.edges:
            for point in getPointsBetween(*edge):
                yield point



red_tiles = [tuple(map(int,line.split(','))) for line in input_data]


rectangles = [
    Rectangle((tile_1, tile_2))
    for index, tile_1 in enumerate(red_tiles[:-1]) 
    for tile_2 in red_tiles[index+1:]
]

rectangles.sort(key=lambda x: x.area, reverse=True)

boundry_edges = [edge for edge in zip(red_tiles, red_tiles[1:]+red_tiles[:1])]

all_boundry_points = {
    point
    for p1, p2 in boundry_edges 
    for point in getPointsBetween(p1,p2) 
}

vertical_boundry_points = {
    point
    for (x1, y1), (x2, y2) in boundry_edges if x1 == x2
    for point in getPointsBetween(*sorted([(x1, y1), (x2, y2)], key=lambda x:x[1])) 
}

memo = dict.fromkeys(all_boundry_points, True)
def insideBoundry (point):
    try:
        return memo[point]
    except KeyError:
        x, y = point
        assert type(x) == int
        boundry_crosses = [
            p for p 
            in getPointsBetween(point, (-1, y))
            if p in vertical_boundry_points
        ]
        memo[point] = bool(len(boundry_crosses)%2)
        return memo[point]


def crossesEdge (rectangle, edge):
    if edge[0][0] == edge[1][0]:    # Vertical edge
        return (
            (
                rectangle[0][0] < edge[0][0] < rectangle[1][0]
                or
                rectangle[1][0] < edge[0][0] < rectangle[0][0]
            )
            and 
            (
                edge[0][1] < rectangle[0][1] < edge[1][1]
                or
                edge[1][1] < rectangle[0][1] < edge[0][1]
                or
                edge[0][1] < rectangle[1][1] < edge[1][1]
                or
                edge[1][1] < rectangle[1][1] < edge[0][1]
            )
        )
    else:                           # Horizontal edge
        return (
            (
                rectangle[0][1] < edge[0][1] < rectangle[1][1]
                or
                rectangle[1][1] < edge[0][1] < rectangle[0][1]
            )
            and 
            (
                edge[0][0] < rectangle[0][0] < edge[1][0]
                or
                edge[1][0] < rectangle[0][0] < edge[0][0]
                or
                edge[0][0] < rectangle[1][0] < edge[1][0]
                or
                edge[1][0] < rectangle[1][0] < edge[0][0]
            )
        )

# Not completely robust but works
for rectangle in tqdm(rectangles):
    for edge in boundry_edges:
        if crossesEdge((rectangle.points[0],rectangle.points[2]), edge): break
        if not insideBoundry(rectangle.points[1]): break
        if not insideBoundry(rectangle.points[3]): break
    else:
       largest_internal_rectangle = rectangle
       break

# plt.axis([90000, 100000, 65000, 70000])
# plt.axis([0, 10000, 65000, 70000])
# plt.axis([45000, 55000, 90000, 100000])
plt.axis([0, 100000, 30000, 100000])
for tile in red_tiles:
    plt.plot(*tile, '.', color='red')
for edge in boundry_edges:
    xs = (edge[0][0],edge[1][0])
    ys = (edge[0][1],edge[1][1])
    plt.plot(xs,ys, color='green')

for edge in largest_internal_rectangle.edges:
    xs = (edge[0][0],edge[1][0])
    ys = (edge[0][1],edge[1][1])
    plt.plot(xs,ys, color='blue')
plt.show()


answers = {
    'What is the largest area of any rectangle you can make?:': 
        rectangles[0].area, 
    'What is the largest area of any rectangle you can make using only red and green tiles?:': 
        largest_internal_rectangle.area
}
max_len_quest = max(len(q) for q in answers.keys())
max_len_soln = max(len(str(s)) for s in answers.values())
for question, solution in answers.items():
    print(f"{question:<{max_len_quest+1}}{solution:>{max_len_soln}}")