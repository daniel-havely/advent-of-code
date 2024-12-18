with open("input.txt","r") as input_file:
    input_data = input_file.readlines()

stored_values = {k.strip():int(v) for k,v in [tuple(str.strip().split(":")) for str in input_data[:input_data.index("\n")]]}
program = [int(ch.strip()) for str in input_data[input_data.index("\n")+1:] for ch in str[str.find(":")+1:].split(",")]

class Elf_Machine:
    def __init__(self):
        self.register = {"A":0, "B":0, "C":0}
        self.instruction_pointer = 0
        self.output = []

        self.process = {
            0: self.adv,
            1: self.bxl,
            2: self.bst,
            3: self.jnz,
            4: self.bxc,
            5: self.out,
            6: self.bdv,
            7: self.cdv
        }

    def combo(self, operand):
        if operand < 4:
            return operand
        if operand == 4:
            return self.register["A"]
        if operand == 5:
            return self.register["B"]
        if operand == 6:
            return self.register["C"]
        if operand == 7:
            raise Exception("Machine error")

    def adv(self, operand):
        self.register["A"] = int(self.register["A"]/pow(2,self.combo(operand)))

    def bxl(self, operand):
        self.register["B"] = self.register["B"] ^ operand

    def bst(self, operand):
        self.register["B"] = self.combo(operand)%8

    def jnz(self, operand):
        if self.register["A"]: self.instruction_pointer = operand

    def bxc(self, operand):
        self.register["B"] = self.register["B"] ^ self.register["C"]

    def out(self, operand):
        self.output.append(self.combo(operand)%8)

    def bdv(self, operand):
        self.register["B"] = int(self.register["A"]/pow(2,self.combo(operand)))

    def cdv(self, operand):
        self.register["C"] = int(self.register["A"]/pow(2,self.combo(operand)))

    def runProgram(self, program):
        self.instruction_pointer = 0
        while 0 <= self.instruction_pointer < len(program):
            opcode = program[self.instruction_pointer]
            self.instruction_pointer += 1
            operand = program[self.instruction_pointer]
            self.instruction_pointer += 1
            self.process[opcode](operand)
    
    def printOutput(self):
        print(",".join(str(num) for num in self.output))


machine = Elf_Machine()
for k,v in stored_values.items():
    machine.register[k[-1]] = v
machine.runProgram(program)
print(f"{'Machine output:': <40}{','.join(str(num) for num in machine.output)}")


def findByteAt(position, running_value=0):
    for byte_value in range(8):
        test_value = running_value + byte_value*pow(8, position)
        machine = Elf_Machine()
        machine.register["A"] = test_value
        machine.runProgram(program)
        if machine.output[position:] == program[position:]:
            # print(f"{'pos:'}{pos}{'  byte:'}{byte}")
            if position:
                value = findByteAt(position-1, test_value)
                if value is not None: return value
            else:
                return test_value

print(f"{'Minimum value to replicate program:': <40}{findByteAt(len(program)-1)}")
        



