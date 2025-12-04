import networkx as nx

with open("input.txt","r") as input_file:
    input_data = input_file.readlines()

paper_rolls = nx.Graph()
for row_n, row in enumerate(input_data):
    for col_n, ch in enumerate(row.strip()):
        if ch == '@':
            paper_rolls.add_node((row_n, col_n))
            for row_off, col_off in [(0,-1),(-1,-1),(-1,-0),(-1,1)]:
                link_node = (row_n + row_off, col_n + col_off)
                if paper_rolls.has_node(link_node): 
                    paper_rolls.add_edge((row_n, col_n) , link_node)


rolls_accessible = [n[0] for n in paper_rolls.degree() if n[1] < 4]
number_of_rolls_removed = []
while rolls_accessible:
    number_of_rolls_removed.append(len(rolls_accessible))
    paper_rolls.remove_nodes_from(rolls_accessible)
    rolls_accessible = [n[0] for n in paper_rolls.degree() if n[1] < 4]

print(
f"{'Number of paper rolls initially accessible:': <45}\
{number_of_rolls_removed[0]: >10}"
)
print(
f"{'Total number of paper rolls removed:': <45}\
{sum(number_of_rolls_removed): >10}"
)
