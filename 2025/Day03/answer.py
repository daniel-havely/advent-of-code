with open("input.txt","r") as input_file:
    input_data = [line.strip() for line in input_file.readlines()]

def getMaxJoltage (bank, batteries_on):
    bank_joltage_digits = []
    prev_battery_loc = -1
    for joltage_dig in range(batteries_on, 0, -1):
        max_joltage = 0
        selected_battery_loc = 0
        first_loc = prev_battery_loc + 1
        last_loc = len(bank) - joltage_dig + 1
        for batt_loc, batt_joltage in enumerate(bank[first_loc:last_loc],first_loc):
            if int(batt_joltage) > max_joltage:
                max_joltage = int(batt_joltage)
                selected_battery_loc = batt_loc
        bank_joltage_digits.append(bank[selected_battery_loc])
        prev_battery_loc = selected_battery_loc
    return int(''.join(bank_joltage_digits))

max_joltages_for_n_batteries = {2:[], 12:[]}
for n in max_joltages_for_n_batteries:
    for line in input_data:
        max_joltages_for_n_batteries[n].append(getMaxJoltage(bank=line, batteries_on=n))

print(f"{'Total output joltage (2 batteries per bank):': <45}{sum(max_joltages_for_n_batteries[2]): >15}")
print(f"{'Total output joltage (12 batteries per bank):': <45}{sum(max_joltages_for_n_batteries[12]): >15}")