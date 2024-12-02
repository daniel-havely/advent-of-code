with open("input.txt","r") as input_file:
    # input_data = [list(map(int,number_string.split())) for number_string in input_file.read().split("\n") if number_string]
    input_data = [[int(x) for x in number_string.split()] for number_string in input_file.read().split("\n") if number_string]

def getSafetyCriteria(record):
    level_changes = [level2-level1 for level1,level2 in zip(record,record[1:])]
    return {
    "level_changes_inbounds": [0 < abs(change) <=3 for change in level_changes],
    "level_changes_samedirection": [(change_1 ^ change_2) >= 0  for change_1, change_2 in zip(level_changes,level_changes[1:])]
    }

def testSafety(record):
     safety_criteria = getSafetyCriteria(record)
     return all(safety_criteria["level_changes_inbounds"]) and all(safety_criteria["level_changes_samedirection"])

count_safe = 0
count_fixable = 0

for index, record in enumerate(input_data):
    safe, fixable = False, False
    safety = getSafetyCriteria(record)
    if all(safety["level_changes_inbounds"]) and all(safety["level_changes_samedirection"]):
        safe = True
    elif 0 < sum(map(lambda x: not x,safety["level_changes_inbounds"])) <= 2:
        index_first_change_outofbounds = safety["level_changes_inbounds"].index(False)
        for index_to_omit in range(index_first_change_outofbounds, index_first_change_outofbounds+1+1):
            if testSafety(record[:index_to_omit]+record[index_to_omit+1:]):
                fixable =True
                break
    elif 0 < sum(map(lambda x: not x,safety["level_changes_samedirection"])) <= 2:
        index_first_change_notsamedirection = safety["level_changes_samedirection"].index(False)
        for index_to_omit in range(index_first_change_notsamedirection, index_first_change_notsamedirection+2+1):
            if testSafety(record[:index_to_omit]+record[index_to_omit+1:]):
                fixable =True
                break
    if safe:
        count_safe += 1
    elif fixable:
        count_fixable +=1
    # print(index, str(record).ljust(40), safe, fixable)

print("Safe",count_safe, sep="\t")
print("Fixable",count_fixable, sep="\t")
print("Total",count_safe+count_fixable, sep="\t")