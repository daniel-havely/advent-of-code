import re
import numpy as np
import itertools

# t_str = '[##...###.#] (0,1,5,6,7,8,9) (4,5) (1,2,3,5,6) (0,3) (8,9) (0,3,5,6,7,8,9) (0,1,4,6,7,9) (1,2) (5,8) {51,38,12,25,9,52,42,42,58,49}'

# example = r'(mul)\((\d+),(\d+)\)|(do)\(\)|(don\'t)\(\)'

# r_str = r'\[(.*)\] (\(.*\)) \{(.*)\}'

# se = re.search(r_str, t_str)
# ma = re.match(r_str, t_str)
# fi = re.findall(r_str, t_str)

# print(se.group())
# print(ma.group())
# print(fi)


# with open("input.txt","r") as input_file:
#     input_data =  input_file.read()


# fin = [(x,y,z) for x,y,z in re.findall(r_str, input_data)]
# print(fin)
# print(fin[0])

t_str = '[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}'

# r_str = r'\[(.*)\] (\(.*\)) \{(.*)\}'

data = [
    (
        light_str, 
        [tuple(map(int, but[1:-1].split(","))) for but in button_str.split()], 
        [int(jol) for jol in joltage_str.split(",")]
    ) 
    for light_str, button_str, joltage_str 
    in re.findall(r'\[(.*)\] (\(.*\)) \{(.*)\}', t_str)
]

def genCombo(but_ranges, but_jolts, total_jolts):
    if len(but_ranges) > 1: 
        but_ranges = but_ranges.copy()
        current_range = but_ranges.pop()
        but_jolts = but_jolts.copy()
        current_jolts = but_jolts.pop()
        
        return [
            ([*result, a], joltage + (a*current_jolts))
            for a in current_range 
            for result, joltage in (genCombo(but_ranges, but_jolts, total_jolts ))
            if joltage <= total_jolts
            ]
    else:
        return  (([r], r*but_jolts[0]) for r in but_ranges[0])


# def genFromRanges(but_ranges):
#     if len(but_ranges) > 1: 
#         but_ranges = but_ranges.copy()
#         current_range = but_ranges.pop()
#         return [
#             [*result, a]
#             for a in current_range 
#             for result in (genFromRanges(but_ranges))
#             if a + sum(result) < 110
#             ]
#     else:
#         return  ([r] for r in but_ranges[0])
        





tgt_data, opr_data, jol_data = data[0]


# print(jol_data)
# print(opr_data)

# tgt = np.array([int(ch == '#') for ch in tgt_data])
tgt = np.array(jol_data)

# opr = np.array([[int(j in i) for j in range(len(tgt))] for i in opr_data])
opr = np.array([[int(j in i) for j in range(len(tgt))] for i in opr_data])

# fmt = '0'+str(len(opr_data))+'b'
# inp = np.array([[int(i) for i in format(j, fmt)] for j in range(2**len(opr_data))])
tot = sum(jol_data)
lens = [len(but) for but in opr_data]
# rngs = [list(range(int(tot/n)+1)) for n in lens]
rngs = [list(range(min([jol_data[i]for i in ixs])+1)) for ixs in opr_data]
# comb = itertools.product(*rngs)
comb = list(genCombo(rngs, lens, tot))
inp = np.array([c for c, j in comb])
# inp = np.array([c for c in comb if np.dot(c,lens) == tot])

# out = opr.transpose() @ inp.transpose()
# out2 = np.mod(out, 2)
out = opr.transpose() @ inp.transpose()

# corr = np.equal(out2.transpose(), tgt)
# corr2 = corr.all(axis=1)
corr = np.equal(out.transpose(), tgt).all(axis=1)

# results = [t for t in zip(inp, corr2)]
# for presses, correct in results:
#     if correct: print(presses)
results = [t for t in zip(inp, corr)]
for presses, correct in results:
    if correct: print(presses)
