with open("input.txt","r") as input_file:
    input_data = input_file.read().strip()

disk_blocks = []
file_index = 0
contains_data = True
for ch in input_data:
    number_of_blocks = int(ch)
    disk_blocks.extend(([file_index] if contains_data else [None])*number_of_blocks)
    if contains_data: file_index += 1
    contains_data = not contains_data

disk_blocks_compacted = disk_blocks.copy()
for ix in range(len(disk_blocks_compacted)):
    if ix >= len(disk_blocks_compacted): break
    if disk_blocks_compacted[ix] is None:
        block_found = False
        while not block_found:
            block = disk_blocks_compacted.pop()
            if block is not None:
                try:
                    disk_blocks_compacted[ix] = block
                    block_found = True
                except IndexError:
                    disk_blocks_compacted.append(block)
                    break

disk_file_list = []
file_index = 0
contains_data = True
for ch in input_data:
    number_of_blocks = int(ch)
    disk_file_list.append({
        "file index": file_index if contains_data else None,
        "contains data": contains_data,
        "length": int(ch)})
    if contains_data: file_index += 1
    contains_data = not contains_data

for file_to_move in [file for file in reversed(disk_file_list.copy()) if file["contains data"]]:
    index_of_file_to_move = disk_file_list.index(file_to_move)
    file_to_replace = next(
        (file for file in disk_file_list[:index_of_file_to_move] 
        if not file["contains data"]
        and
        file["length"] >= file_to_move["length"])
        ,
        None
        )
    if file_to_replace is None: continue
    index_of_file_to_replace = disk_file_list.index(file_to_replace)

    file_to_replace["length"] -= file_to_move["length"] 
    disk_file_list.insert(index_of_file_to_move+1, {"file index": None, "contains data": False, "length": file_to_move["length"]})
    disk_file_list.insert(index_of_file_to_replace, disk_file_list.pop(index_of_file_to_move))

disk_blocks_defragmented = []
for file in disk_file_list:
    file_index = file["file index"]
    contains_data = file["contains data"]
    number_of_blocks = file["length"]
    disk_blocks_defragmented.extend(([file_index] if contains_data else [None])*number_of_blocks)

print("Compacted checksum",sum([ix*block_id for ix, block_id in enumerate(disk_blocks_compacted) if block_id is not None]), sep="\t")
print("Defragmented checksum",sum([ix*block_id for ix, block_id in enumerate(disk_blocks_defragmented) if block_id is not None]), sep="\t")


