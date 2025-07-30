import re
import os
current_path = os.path.abspath(__file__)
current_dir = os.path.dirname(current_path)
with open(os.path.join(current_dir, "temp.txt"), "r", encoding="utf-8") as f:
    lines = f.readlines()

results = []
# 只保留0 ，6， 12， 18
# for line in lines:
for i in range(0, len(lines), 1):
    line = lines[i].strip()
    if not line:
        continue
    
    # Check for "Incorrect, should be:" pattern
    incorrect_match = re.search(r"Incorrect, should be:(.*?)$", line)
    incorrect_match = re.search(r"(.*?) {{pause:5000}}", line)
    if incorrect_match:
        correction = incorrect_match.group(1).strip().lower()
        if correction:
            results.append(correction)
        continue
    

results = sorted(set(results))

print("words = [")
for i, word in enumerate(results):
    end = "," if i < len(results) - 1 else ""
    sep = "\n" if (i + 1) % 6 == 0 else ""
    print(f'    "{word}"{end}{sep}', end="")
print("\n]")
print(f"\nTotal unique words: {len(results)}")