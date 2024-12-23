with open("input.txt","r") as input_file:
    input_data = input_file.read()

computer_connection_strings = [string.strip() for string in input_data.splitlines()]

computer_connections = {}
for connection_str in computer_connection_strings:
    com_1_str, div_str, com_2_str = connection_str.partition("-")
    computer_connections.setdefault(com_1_str, set()).add(com_2_str)
    computer_connections.setdefault(com_2_str, set()).add(com_1_str)

networks = {tuple(): set(computer_connections.keys())}
while computer_connections:
    comp, comp_conns = computer_connections.popitem()
    networks.update(
        {net+(comp,):net_conns&comp_conns for net,net_conns in networks.items() if comp in net_conns}
        )

lan_triples_with_t = sum(any(comp[0] == "t" for comp in net) for net in networks if len(net) == 3)
print(f"{'Three computer LANs with t_ computer:': <40}{lan_triples_with_t: >20}")    
print(f"{'LAN party password:': <20}{','.join(sorted(max(networks, key=len))): >40}")
