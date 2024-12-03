import re

with open("input.txt","r") as input_file:
    input_data = input_file.read()

enabled = True
products = {"enabled":[],"disabled":[]}

for multiply,num_str_1,num_str_2,cmd_enable,cmd_disable in re.findall(r'(mul)\((\d+),(\d+)\)|(do)\(\)|(don\'t)\(\)', input_data):
    if multiply:
        products["enabled" if enabled else "disabled"].append(int(num_str_1)*int(num_str_2))
    elif cmd_enable:
        enabled = True
    elif cmd_disable:
        enabled = False

print("Sum of all products",sum(products["enabled"]+products["disabled"]), sep="\t")
print("Sum of enabled products",sum(products["enabled"]), sep="\t")