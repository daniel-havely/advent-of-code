import math

a = (3,7)
b = (8,4)

area = lambda a,b: abs(math.prod(map(int.__sub__,a,b)))

sign = lambda x: (x>0)-(x<0)

def getPointsBetween(point_1, point_2):
    (x1, y1), (x2, y2) = point_1, point_2
    x_inc = sign(x2-x1)
    y_inc = sign(y2-y1)
    x, y = point_1
    while (x, y) != point_2:
        yield (x, y)
        x += x_inc
        y += y_inc


for i, p in enumerate(getPointsBetween((5,15),(17,15))):
    print(i,p)
    if i > 20: break
    