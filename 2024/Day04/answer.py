with open("input.txt","r") as input_file:
    input_data = [list(string) for string in input_file.read().split("\n") if string]

words_to_search = ["XMAS","MAS"]

search_directions = {
    "Straight_Left_Right":           (0,1),
    "Diagonal_TopLeft_BottomRight":  (1,1),
    "Straight_Top_Bottom":           (1,0),
    "Diagonal_opRight_BottomLeft":   (1,-1),
    "Straight_Right_Left":           (0,-1),
    "Diagonal_BottomRight_TopLeft":  (-1,-1),
    "Straight_Bottom_Top":           (-1,0),
    "Diagonal_BottomLeft_TopRight":  (-1,1)
}

words_found = []
for ix_row, row in enumerate(input_data):
    for ix_col, col in enumerate(row): 
        for dir_name, dir_offset in search_directions.items():
            for search_word in words_to_search:
                for char_num, char in enumerate(search_word):
                    if (
                        0 <= (target_row := ix_row+char_num*dir_offset[0]) < len(input_data) 
                        and 
                        0 <= (target_col := ix_col+char_num*dir_offset[1]) < len(input_data[target_row])
                        and
                        input_data[target_row][target_col] == char
                    ):
                        match_found = True
                    else:
                        match_found = False
                        break
                if match_found:
                    words_found.append({"word": search_word, "location": (ix_row,ix_col), "direction": dir_name})

print("XMAS count", len(list(filter(lambda found: found["word"] == "XMAS", words_found))), sep="\t")

mas_locations_centered_on_a = [
    tuple([sum(tup) for tup in zip(found["location"],search_directions[found["direction"]])]) #re-centre location on the A
    for found in words_found 
    if found["word"] == "MAS" and found["direction"][:8] == "Diagonal"
    ]

count_diag_mas_at_location = {}
for loc in mas_locations_centered_on_a:
    count_diag_mas_at_location[loc] = count_diag_mas_at_location.get(loc,0) + 1

print("x-MAS count", len({loc: count for loc, count in count_diag_mas_at_location.items() if count == 2}), sep="\t")
