with open("input.txt","r") as input_file:
    input_data = input_file.readlines()

sort_orders = [tuple(str.strip().split("|")) for str in input_data[:input_data.index("\n")]]
page_lists = [str.strip().split(",") for str in input_data[input_data.index("\n")+1:]]

predecessors = {}
for bef,aft in sort_orders:
    predecessors.setdefault(aft,set()).add(bef)

processed_page_lists = []
for page_list in page_lists:
    correct_order = True
    pages_to_sort = page_list.copy()
    sorted_page_list = []
    while pages_to_sort:
        found_pages = False
        for pg in pages_to_sort.copy():
            if predecessors[pg] & set(pages_to_sort):
                correct_order = False
            else:
                sorted_page_list.append(pages_to_sort.pop(pages_to_sort.index(pg)))
                found_pages = True
        if not found_pages: raise Exception("Sort failure")
    processed_page_lists.append({"initially correct": correct_order, "page list": sorted_page_list})

getMiddle = lambda lst: lst[int((len(lst))/2)]

print(
    "Sum for ordered page-lists",
    sum([int(getMiddle(lst["page list"])) for lst in processed_page_lists if lst["initially correct"]]),
    sep="\t"
    )
print(
    "Sum for fixed page-lists",
    sum([int(getMiddle(lst["page list"])) for lst in processed_page_lists if not lst["initially correct"]]),
    sep="\t"
    )
