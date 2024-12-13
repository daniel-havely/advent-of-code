import re

with open("input.txt","r") as input_file:
    input_data = input_file.read()

regex_string = r'Button A: X\+(\d+), Y\+(\d+)\nButton B: X\+(\d+), Y\+(\d+)\nPrize: X=(\d+), Y=(\d+)'

tokens_required = 0
corrected_tokens_required = 0
for params in re.findall(regex_string, input_data):
    a_x, a_y, b_x, b_y, p_x, p_y = map(int,params)

    det = a_x*b_y - a_y*b_x
 
    a = (p_x*b_y - p_y*b_x)/det
    b = (p_y*a_x - p_x*a_y)/det

    tokens_required += 3*int(a)+int(b) if a.is_integer() and b.is_integer() else 0
    
    p_x += 10000000000000
    p_y += 10000000000000
 
    a = (p_x*b_y - p_y*b_x)/det
    b = (p_y*a_x - p_x*a_y)/det

    corrected_tokens_required += 3*int(a)+int(b) if a.is_integer() and b.is_integer() else 0

print(f"{'Tokens required': <35}{tokens_required: >20}")
print(f"{'Tokens required after correction': <35}{corrected_tokens_required: >20}")