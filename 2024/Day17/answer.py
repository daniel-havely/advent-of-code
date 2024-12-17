from tqdm import tqdm

with open("input.txt","r") as input_file:
    input_data = input_file.readlines()

stored_values = {k.strip():int(v) for k,v in [tuple(str.strip().split(":")) for str in input_data[:input_data.index("\n")]]}
program = [int(ch.strip()) for str in input_data[input_data.index("\n")+1:] for ch in str[str.find(":")+1:].split(",")]

class Elf_Machine:
    def __init__(self):
        self.register = {"A":0, "B":0, "C":0}
        self.instruction_pointer = 0
        self.output = []

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

    process = {
        0: adv,
        1: bxl,
        2: bst,
        3: jnz,
        4: bxc,
        5: out,
        6: bdv,
        7: cdv
    }
    
    def runProgram(self, program):
        self.instruction_pointer = 0
        while 0 <= self.instruction_pointer < len(program):
            opcode = program[self.instruction_pointer]
            self.instruction_pointer += 1
            operand = program[self.instruction_pointer]
            self.instruction_pointer += 1
            Elf_Machine.process[opcode](self,operand)
    
    def printOutput(self):
        print(",".join(str(num) for num in self.output))


machine = Elf_Machine()
machine.register["A"] = stored_values["Register A"]
machine.runProgram(program)
machine.printOutput()
print()

# Each output number is only affected by two co-efficients, the last only by one.
# So.. starting with the co-eff of the largest exponent and working backwards...
try_number = (
                    5*pow(8,15) + 3*pow(8,14) + 2*pow(8,13) + 5*pow(8,12) +
                    3*pow(8,11) + 7*pow(8,10) + 6*pow(8,9) + 6*pow(8,8) + 
                    4*pow(8,7) + 6*pow(8,6) + 2*pow( 8,5) + 3*pow(8,4) + 
                    6*pow(8,3) + 0*pow(8,2) + 1*pow(8,1) + 7*pow(8,0)
) #Yes! Worked out by hand changing one co-eff at a time:-(
new_machine = Elf_Machine()
new_machine.register["A"] = try_number
new_machine.runProgram(program)
new_machine.printOutput()
print(",".join(str(num) for num in program))
if new_machine.output == program:
    print(try_number)






