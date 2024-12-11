with open("input.txt","r") as input_file:
    input_data = input_file.read().split()

known_answers = {}
def countStonesAfterNthBlink(stone, number_of_blinks):
    if number_of_blinks == 1:
        return 1 if len(stone)%2 else 2
    else:
        try:
            return known_answers[(stone, number_of_blinks)]
        except:
            if stone == "0":
                resulting_number_of_stones = countStonesAfterNthBlink("1", number_of_blinks -1)
            elif len(stone)%2 == 0:
                resulting_number_of_stones = (
                    countStonesAfterNthBlink(stone[:len(stone)//2], number_of_blinks -1)
                    +
                    countStonesAfterNthBlink(stone[len(stone)//2:-1].lstrip("0")+stone[-1], number_of_blinks -1)
                )
            else:
                resulting_number_of_stones = countStonesAfterNthBlink(str(int(stone)*2024), number_of_blinks -1)
            
            known_answers[(stone, number_of_blinks)] = resulting_number_of_stones
            return resulting_number_of_stones
                
print("Stones after 25 blinks:", sum(countStonesAfterNthBlink(stone,25) for stone in input_data), sep="\t")
print("Stones after 75 blinks:", sum(countStonesAfterNthBlink(stone,75) for stone in input_data), sep="\t")


