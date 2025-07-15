# Generate Balabolka-formatted text for 300 words with 5-second pause (using <silence msec="5000"/>)
import pandas as pd
import random


# Load word list from user-provided data
words = [
    "accountant",    "allergy",    "balcony",    "canteen",    "designer",    "experience",
    "extension",    "gymnasium",    "hostel",    "itinerary",    "mattress",    "pharmacist",
    "principal",    "reimbursement",    "sanitation",    "secretary",    "seminar",    "transportation",
    "welfare"
]
words = list(dict.fromkeys(words))

random.shuffle(words)
print("words = [")
for i in range(0, len(words), 6):
    chunk = words[i : i + 6]
    line = ", ".join(f'"{w}"' for w in chunk)
    comma = "," if i + 6 < len(words) else ""
    print(f"    {line}{comma}")
print("]")

print(f"\nTotal words: {len(words)}")

