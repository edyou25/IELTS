import os


current_path = os.path.abspath(__file__)
current_dir = os.path.dirname(current_path)
with open(os.path.join(current_dir, "temp.txt"), "r", encoding="utf-8") as f:    
    lines = [line.strip() for line in f if line.strip()]

results = []
i = 0
while i < len(lines) - 1:
    line = lines[i]
    next_line = lines[i + 1]
    if line.startswith("[") and "]" in line:
        word = line.split("]")[-1].strip()
        if next_line.startswith('n'):
            print(f"Skipping {word} due to next line starting with 'n'")
            results.append(word)
    i += 1

print("words = [")
for i, word in enumerate(results):
    end = "," if i < len(results) - 1 else ""
    sep = "\n" if (i + 1) % 6 == 0 else ""
    print(f'    "{word}"{end}{sep}', end="")
print("\n]")
