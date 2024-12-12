with open("input.txt","r") as input_file:
    input_data = input_file.read().split()

def getStonesAfterBlink(stone):
        if stone == "0":
            return ["1"]
        elif len(stone)%2 == 0:
            return [stone[:len(stone)//2],stone[len(stone)//2:-1].lstrip("0")+stone[-1]]
        else:
            return [str(int(stone)*2024)]

known_answers = {}
def countStonesAfterNthBlink(stone, number_of_blinks):
    if number_of_blinks == 1:
        return 1 if len(stone)%2 else 2
    else:
        try:
            return known_answers[(stone, number_of_blinks)]
        except KeyError:
            resulting_number_of_stones = sum(
                countStonesAfterNthBlink(new_stone, number_of_blinks -1)
                for new_stone in getStonesAfterBlink(stone)
                )
            known_answers[(stone, number_of_blinks)] = resulting_number_of_stones
            return resulting_number_of_stones
                
print("Stones after 25 blinks:", sum(countStonesAfterNthBlink(stone,25) for stone in input_data), sep="\t")
print("Stones after 75 blinks:", sum(countStonesAfterNthBlink(stone,75) for stone in input_data), sep="\t")


