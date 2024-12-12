with open("input.txt","r") as input_file:
    input_data = [list(string) for string in input_file.read().split("\n") if string]

directions = ["N","E","S","W"]
direction_offsets ={"N": (-1,0), "E": (0,1), "S": (1,0), "W": (0,-1)}

class Plot:
    def __init__(self, location, plant_type):
        self.location = location
        self.plant_type = plant_type
        self.connected_plots = {d:None for d in direction_offsets.keys()}
    
    def buildConnections(self):
        for dir, offset in direction_offsets.items():
            look_row_ix, look_col_ix = tuple(map(sum,zip(self.location,offset)))
            if (
                0 <= look_row_ix < len(plot_grid)
                and
                0 <= look_col_ix < len(plot_grid[look_row_ix])
                and
                plot_grid[look_row_ix][look_col_ix].plant_type == self.plant_type
            ):
                self.connected_plots[dir] = plot_grid[look_row_ix][look_col_ix]
        return self

class Region:
    def __init__(self, plot):
        self.plant_type = plot.plant_type
        self.plots = set()
        self.plots.add(plot)

        searched_plots = set()
        while unsearched_plots := self.plots - searched_plots:
            for search_plot in unsearched_plots:
                for connected_plot in search_plot.connected_plots.values():
                    if connected_plot is not None:
                        self.plots.add(connected_plot)
                searched_plots.add(search_plot)
    
    def getPerimeter(self):
        return sum(1 if con is None else 0 for plt in self.plots for con in plt.connected_plots.values())
    
    def getArea(self):
        return len(self.plots)
    
    def getSides(self):
        sides = []
        perimter_units = [(plt,dir) for plt in self.plots for dir, con in plt.connected_plots.items() if con is None]
        while perimter_units:
            new_side = []
            first_unit = perimter_units.pop()
            new_side.append(first_unit)
            facing = first_unit[1]
            for d in [1,-1]:
                con_dir = directions[(directions.index(facing)+d)%4]
                while (unit := (new_side[-1][0].connected_plots[con_dir],facing)) in perimter_units:
                    new_side.append(perimter_units.pop(perimter_units.index(unit)))
                new_side.reverse()
            sides.append(new_side)
        return len(sides)


plot_grid = [[Plot((row_ix,col_ix), char) for col_ix, char in enumerate(row)] for row_ix, row in enumerate(input_data)]

unallocated_plots = {plot.buildConnections() for row in plot_grid for plot in row}
regions = set()
while unallocated_plots:
    new_region = Region(unallocated_plots.pop())
    regions.add(new_region)
    unallocated_plots.difference_update(new_region.plots)

print(f"{'Total fencing price:': <30}{sum(reg.getPerimeter()*reg.getArea() for reg in regions): >10}")
print(f"{'Total bulk cost fencing price:': <30}{sum(reg.getSides()*reg.getArea() for reg in regions): >10}")




