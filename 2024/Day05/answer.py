with open("input.txt","r") as input_file:
    input_data = input_file.readlines()

sort_orders = [tuple(str.strip().split("|")) for str in input_data[:input_data.index("\n")]]
page_lists = [str.strip().split(",") for str in input_data[input_data.index("\n")+1:]]

predecessors = {}
for bef,aft in sort_orders:
    predecessors.setdefault(aft,set()).add(bef)

ordered_lists = []
for lst in page_lists:
    correct_order = True
    for page_index,page in enumerate(lst):
        if predecessors[page] & set(lst[page_index:]):
            correct_order = False
            new_order = lst[:page_index]
            pages_to_sort = lst[page_index:]
            while pages_to_sort:
                found_pages = False
                for pg_index, pg in enumerate(pages_to_sort):
                    if not predecessors[pg] & set(pages_to_sort):
                        new_order.append(pages_to_sort.pop(pg_index))
                        found_pages = True
                if not found_pages: raise Exception("Sort failure")
            break
    ordered_lists.append({"initial correct order": correct_order, "page list": lst if correct_order else new_order})

getMiddle = lambda lst: lst[int((len(lst))/2)]

print(sum([int(getMiddle(lst["page list"])) for lst in ordered_lists if lst["initial correct order"]]))
print(sum([int(getMiddle(lst["page list"])) for lst in ordered_lists if not lst["initial correct order"]]))
