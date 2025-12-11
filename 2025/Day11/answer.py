import networkx as nx

with open("input.txt","r") as input_file:
    input_data =  input_file.readlines()

devices = [
    (name.strip(), map(str.strip, outputs.split())) 
    for name, outputs in [line.split(':') for line in input_data]
]

device_flow = nx.DiGraph()
device_flow.add_nodes_from([name for name, outputs in devices])
device_flow.add_edges_from(
    [(name, output_name) for name, outputs in devices for output_name in outputs]
)

assert nx.is_directed_acyclic_graph(device_flow)

paths_you_out = nx.all_simple_paths(G=device_flow, source='you', target='out')
paths_you_out_number = (sum(1 for path in paths_you_out))

nx.set_node_attributes(device_flow, 0, 'weight')
vital_nodes = {'dac', 'fft'}
for layer_nodes in nx.topological_generations(device_flow):
    vital_node_in_layer = set(layer_nodes) & vital_nodes
    if vital_node_in_layer: layer_nodes = vital_node_in_layer
    for node in layer_nodes:
        device_flow.nodes[node]['weight'] = 1 if node == 'svr' \
            else sum(device_flow.nodes[pr]['weight'] for pr in device_flow.predecessors(node))
paths_svr_fft_dac_out_number = device_flow.nodes['out']['weight']

answers = {
    'How many different paths lead from you to out?:': 
        paths_you_out_number
    ,
    'How many of those paths visit both dac and fft?:': 
        paths_svr_fft_dac_out_number
}
max_len_quest = max(len(q) for q in answers.keys())
max_len_soln = max(len(str(s)) for s in answers.values())
for question, solution in answers.items():
    print(f"{question:<{max_len_quest+1}}{solution:>{max_len_soln}}")




