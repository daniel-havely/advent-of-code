from tqdm import tqdm

with open("input.txt","r") as input_file:
    input_data = input_file.read()

initial_numbers = [int(string.strip()) for string in input_data.splitlines()]

def nextSecretNumber(secret_number: int):
    num_1 = ((secret_number*64) ^ secret_number) % 16777216
    num_2 = ((num_1//32) ^ num_1) % 16777216
    num_3 = ((num_2*2048) ^ num_2) % 16777216
    return num_3

buyer_secret_numbers =[]
for buyer, secret_number in tqdm(enumerate(initial_numbers)):
    buyer_secret_numbers.append([secret_number])
    for i in range (2000):
        secret_number = nextSecretNumber(secret_number)
        buyer_secret_numbers[buyer].append(secret_number)

buyer_prices = [[int(str(num)[-1]) for num in buyer] for buyer in buyer_secret_numbers]

buyer_sequence_price = []
for buyer_number, buyer in tqdm(enumerate(buyer_prices)):
    buyer_sequence_price.append({})
    for i in range(len(buyer)-6):
        sequence = tuple(map(lambda t:t[1]-t[0],zip(buyer[i:i+4],buyer[i+1:i+5])))
        buyer_sequence_price[buyer_number][sequence] = buyer_sequence_price[buyer_number].get(sequence,buyer[i+4])

sequence_total_bananas = {}
for buyer in buyer_sequence_price:
    for seq, pri in buyer.items():
        sequence_total_bananas[seq] = sequence_total_bananas.get(seq,0) + pri

print(f"{'Sum of final secret numbers:': <35}{sum(b[-1] for b in buyer_secret_numbers): >15}")
print(f"{'Total bananas:': <35}{max(sequence_total_bananas.values()): >15}")
