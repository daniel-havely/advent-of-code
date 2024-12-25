with open("input.txt","r") as input_file:
    input_data = input_file.read()

segments = input_data.split("\n\n")
key_silhouettes = [s.splitlines() for s in segments if s.splitlines()[0] == "....."]
lock_silhouettes = [s.splitlines() for s in segments if s.splitlines()[-1] == "....."]

key_heights = [[col.count("#") for col in zip(*key)] for key in key_silhouettes]
lock_heights = [[col.count("#") for col in zip(*lock)] for lock in lock_silhouettes]

print(sum(max(map(sum,zip(key,lock))) < 8 for key in key_heights for lock in lock_heights))
