import re
import os
current_path = os.path.abspath(__file__)
current_dir = os.path.dirname(current_path)
with open(os.path.join(current_dir, "temp.txt"), "r", encoding="utf-8") as f:
    lines = f.readlines()

results = []
for line in lines:
    match = re.search(r"([A-Za-z][A-Za-z\s/\-'.]*[A-Za-z])", line)
    if match:
        phrase = match.group(1).strip()
        phrase = re.sub(r"\bsb\b|\bsth\b|etc|[^\w\s/\-']", "", phrase, flags=re.IGNORECASE)
        phrase = re.sub(r"\s{2,}", " ", phrase).strip()
        if phrase:
            results.append(phrase.lower())

results = sorted(set(results))

print("words = [")
for i, word in enumerate(results):
    end = "," if i < len(results) - 1 else ""
    sep = "\n" if (i + 1) % 6 == 0 else ""
    print(f'    "{word}"{end}{sep}', end="")
print("\n]")
print(f"\nTotal unique words: {len(results)}")