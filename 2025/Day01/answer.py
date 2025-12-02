with open("input.txt","r") as input_file:
    input_data = input_file.readlines()

dial_rotations = [(line[0], int(line[1:])) for line in input_data]

position = 50
count_zero_stops = 0
count_zero_passes = 0

for dir, num in dial_rotations:
    revolutions, remaining_clicks = divmod(num,100)
    count_zero_passes += revolutions

    start_at_zero = position == 0

    pass_zero, position = divmod(position + remaining_clicks * (-1 if dir == 'L' else 1),100)
    if (position == 0 or pass_zero) and not start_at_zero:
        count_zero_passes += 1

    if position == 0:
        count_zero_stops += 1

print(f"{'Tumbler stops at zero:': <25}{count_zero_stops: >15}")
print(f"{'Tumbler passes zero:': <25}{count_zero_passes: >15}")