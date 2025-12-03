with open("input.txt","r") as input_file:
    input_data = [line.strip() for line in input_file.readlines()]

def getMaxJoltage (bank, digits):
    bank_joltage_digits = []
    prev_battery_pos = -1
    for joltage_dig in range(digits, 0, -1):
        max_joltage = 0
        new_battery_pos = 0
        bank_to_scan = bank[prev_battery_pos+1:(len(bank)+1-joltage_dig)]
        for battery_pos, battery_joltage in enumerate(bank_to_scan, prev_battery_pos+1):
            if int(battery_joltage) > max_joltage:
                max_joltage = int(battery_joltage)
                new_battery_pos = battery_pos

        bank_joltage_digits.append(bank[new_battery_pos])
        prev_battery_pos = new_battery_pos
    return int(''.join(bank_joltage_digits))

max_joltages_for_n_batteries = {2:[], 12:[]}
for n in max_joltages_for_n_batteries:
    for line in input_data:
        max_joltages_for_n_batteries[n].append(getMaxJoltage(bank=line, digits=n))

print(f"{'Total output joltage (2 batteries per bank):': <45}{sum(max_joltages_for_n_batteries[2]): >15}")
print(f"{'Total output joltage (12 batteries per bank):': <45}{sum(max_joltages_for_n_batteries[12]): >15}")