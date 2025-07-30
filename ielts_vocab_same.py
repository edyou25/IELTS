from words import words, words2


words3 = []
for word in words2:
    if word not in words:
        words3.append(word)
print("words3 = [")
for i, word in enumerate(words3):
    end = "," if i < len(words3) - 1 else ""
    sep = "\n" if (i + 1) % 6 == 0 else ""
    print(f'    "{word}"{end}{sep}', end="")
print("]")
print(f"Total unique words: {len(words3)}")
print(f"id: {len(words)+1}-{len(words + words3)}")