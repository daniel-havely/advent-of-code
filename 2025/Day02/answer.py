import re

with open("input.txt","r") as input_file:
    input_data = input_file.read()

id_ranges = [tuple(rng.split('-')) for rng in input_data.split(',')]

invalid_regex_string = r'^(\d+)\1$'
invalid_ids = []

silly_invalid_regex_string = r'^(\d+)\1+$'
silly_invalid_ids = []

for id_first, id_last in id_ranges:
    for id in range(int(id_first), int(id_last) + 1):
        id_str = str(id)
        if invalid_id_match := re.search(invalid_regex_string,id_str):
            invalid_ids.append(int(invalid_id_match.group()))
            silly_invalid_ids.append(int(invalid_id_match.group()))
        elif invalid_id_match := re.search(silly_invalid_regex_string,id_str):
            silly_invalid_ids.append(int(invalid_id_match.group()))
        
print(f"{'Sum of invalid IDs:': <25}{sum(invalid_ids): >15}")
print(f"{'Sum of silly invalid IDs:': <25}{sum(silly_invalid_ids): >15}")