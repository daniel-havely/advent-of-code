from tqdm import tqdm


with open("input.txt","r") as input_file:
    input_data = input_file.read()

input_wire_string, div_string, gate_string = input_data.partition("\n\n")
wire_values = {k:int(v.strip()) for k,v in (tuple(string.split(":")) for string in input_wire_string.splitlines())}
gate_data = [tuple(string.split()) for string in gate_string.splitlines()]

class LogicGate:
    def __init__(self, input_1, input_2, output, operator):
        self.input_1 = input_1
        self.input_2 = input_2
        self.output = output
        self.operator = operator 
    
    operators = {
        "AND": lambda x,y: x&y,
        "OR": lambda x,y: x|y,
        "XOR": lambda x,y: x^y
    }

    def setOutputValue(self):
        if self.output in wire_values: return False
        try:
            wire_values[self.output] = LogicGate.operators[self.operator](wire_values[self.input_1], wire_values[self.input_2])
            return True
        except KeyError:
            return False


logic_gates = {LogicGate(input_1, input_2, output, operator)
               for input_1, operator, input_2, p, output in gate_data}

def processLogicGates():
    update = True
    while update:
        update = any(gate.setOutputValue() for gate in logic_gates)

processLogicGates()

print(sum(
    v*pow(2,n) for n,v in enumerate(v for k,v in sorted(wire_values.items()) if k.startswith("z"))
))

wrongish_gates = []
for gate in logic_gates:
    if (
        (gate.operator == "XOR" and gate.input_1[0] in {"x","y"} and gate.output not in (inp for gate in logic_gates for inp in (gate.input_1, gate.input_2) if gate.operator == "AND"))
        or
        (gate.operator == "XOR" and gate.input_1[0] not in {"x","y"} and gate.output[0] != "z")
        or
        (gate.operator == "AND" and gate.input_1[0] in {"x","y"} and gate.output not in (inp for gate in logic_gates for inp in (gate.input_1, gate.input_2) if gate.operator == "OR"))
        or
        (gate.operator == "AND" and gate.input_1[0] not in {"x","y"} and gate.output not in (inp for gate in logic_gates for inp in (gate.input_1, gate.input_2) if gate.operator == "OR"))
        or
        (gate.operator == "OR" and gate.output not in (inp for gate in logic_gates for inp in (gate.input_1, gate.input_2) if gate.operator == "AND")) 
    ):
        wrongish_gates.append(gate)

def swapGateOutputs(gate_1: LogicGate, gate_2: LogicGate):
    temp_gate_output = gate_1.output+""
    gate_1.output = gate_2.output+""
    gate_2.output = temp_gate_output+""

swapped_outputs = []
clear = False
while not clear:
    clear = True
    for bit in range(45):
        for g_1, g_2 in [(a,b) for a in wrongish_gates for b in wrongish_gates]:
            swapGateOutputs(g_1,g_2)
            for x_bit, y_bit, carry_bit, bit_def in ((x,y,c,d) for x in {0,1} for y in {0,1} for c in ({0,1} if bit else {0}) for d in {0,1}):
                wire_values.clear()
                wire_values = dict.fromkeys((l+str(n).zfill(2) for l in ["x","y"] for n in range(45)),bit_def)
                wire_values["x"+str(bit).zfill(2)] = x_bit
                wire_values["y"+str(bit).zfill(2)] = y_bit
                if bit:
                    wire_values["x"+str(bit-1).zfill(2)] = carry_bit
                    wire_values["y"+str(bit-1).zfill(2)] = carry_bit
                processLogicGates()
                try:
                    if (
                        wire_values["z"+str(bit).zfill(2)] != (x_bit + y_bit + carry_bit)%2
                        # or
                        # wire_values["z"+str(bit+1).zfill(2)] != (x_bit + y_bit + carry_bit)//2
                    ):
                        swapGateOutputs(g_1,g_2)
                        break
                except KeyError:
                    swapGateOutputs(g_1,g_2)
                    break
            else:
                if g_1 == g_2:
                    print("Bit ",bit," OK")
                else:
                    print("Bit ",bit," Fixed")
                    swapped_outputs.append((g_1.output,g_2.output))
                    clear = False
                break
        else:
            print("Bit ",bit," Failed to fix")
            clear = False
            continue

print(",".join(sorted({g for s in swapped_outputs for g in s})))