import networkx as nx

with open("input.txt","r") as input_file:
    input_data =  input_file.readlines()

tachyon_flow = nx.DiGraph()
tachyon_beam_in_column = [set() for i in range(len(input_data[0].strip()))]
for row_n, row in enumerate(input_data):
    for col_n, ch in enumerate(row.strip()):
        current_posiition = (row_n, col_n)
        if ch == '.':
            continue
        elif ch == 'S':
            tachyon_flow.add_node(current_posiition, node_type="Source", paths=1)
            tachyon_beam_in_column[col_n].add(current_posiition)
        elif ch == '^':
            tachyon_flow.add_node(current_posiition, node_type="Splitter", paths=0)
            current_node = tachyon_flow.nodes[current_posiition]
            if tachyon_beam_in_column[col_n]:
                for beam_source in tachyon_beam_in_column[col_n]:
                    tachyon_flow.add_edge(beam_source, current_posiition)
                    current_node['paths'] += tachyon_flow.nodes[beam_source]['paths']
                tachyon_beam_in_column[col_n].clear()
                if col_n > 0:
                    tachyon_beam_in_column[col_n-1].add(current_posiition)
                if col_n < len(row)-1:
                    tachyon_beam_in_column[col_n+1].add(current_posiition)
        else:
            raise Exception("Unexpected character in input")
    # print(''.join(['|' if x else ' ' for x in tachyon_beam_in_column]))
for col_n, column in enumerate(tachyon_beam_in_column):
    if bool(column):
        current_posiition = (len(input_data), col_n)
        tachyon_flow.add_node(current_posiition, node_type="Output", paths=0)
        current_node = tachyon_flow.nodes[current_posiition]
        for beam_source in column:
            tachyon_flow.add_edge(beam_source, current_posiition)
            current_node['paths'] += tachyon_flow.nodes[beam_source]['paths']

beam_splits = [
    tachyon_flow.in_degree(nod) > 0 
    for nod, att in tachyon_flow.nodes(data=True)
    if att['node_type']=='Splitter' 
]
output_paths = [
    att['paths'] 
    for nod, att in tachyon_flow.nodes(data=True)
    if att['node_type']=='Output'
]

answers = {
    'How many times will the beam be split?:': 
        sum(beam_splits), 
    'On how many different timelines would a single tachyon particle end up?:': 
        sum(output_paths)
}
max_len_quest = max(len(q) for q in answers.keys())
max_len_soln = max(len(str(s)) for s in answers.values())
for question, solution in answers.items():
    print(f"{question:<{max_len_quest+1}}{solution:>{max_len_soln}}")