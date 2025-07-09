# Generate Balabolka-formatted text for 300 words with 5-second pause (using <silence msec="5000"/>)
import pandas as pd
from googletrans import Translator
import asyncio
import random
import os

current_path = os.path.abspath(__file__)
current_dir = os.path.dirname(current_path)

# Load word list from user-provided data
words = [
    "expressway/freeway", "study lounge", "housemaid", "workaholic", "tenant", "collapse",
    "recession", "residence", "staple", "hospitable", "skiing", "pork", 
    "blaze a trail", "do odd jobs", "convenience store", "compromise", "editorial", "telephone booth",      
    "catalogue", "periodical room", "anesthetist", "overdue", "outlet", "department store",
    "symptom", "job-hopping", "put on reserve", "out of stock", "fit as a fiddle", "syllabus",
    "wage", "furnace", "spare room", "perseverance", "prosperous", "run for",
    "on business", "wear out", "infectious illness", "sophomore", "roundtrip", 
    "inflation",    "call on",    "hitch-hike",
    "baby crib",    "breeze",    "drop-out",    "mutton",    "stationery",    "sewage treatment",
    "infirmary",    "monetary",    "conductor",    "cutlery",    "deforestation rate",    "paperback edition",
    "in poor shape",    "sneeze",    "downpour",    "buffet",    "surplus",    "sideboard",
    "recruit",    "muggy",    "plough through",    "diabetes",    "have a temperature",    "fracture",
    "dwell",    "depression",    "check out", "hung up", 
    "call on", "hitch-hike", "baby crib",  "accommodate", "turn down", "epidemic",
    "resume", "crack", "in stock", "attending/chief doctor", "loaf", "bankrupt",
    "shelf", "appetizer", "fix the dinner", "ventilation", "speech contest", "dental decay",
    "shuttle", "past the prime", "diligent", "napkin", "multiple glazing", "gust",
    "hang up", "latest number", "periodical", "household expenses", "reference room", "bid",
    "tribute", "hacker", "inexperienced", "circulation", "forecast", "out of print"
]


vocabulary_name = "oit-1-363-1st108err"

md_name = vocabulary_name + ".md"
tts_name = vocabulary_name + ".txt"

cols = 2  # Number of columns in the markdown table

words = list(dict.fromkeys(words))



# Generate Balabolka-compatible input with 5s pause
balabolka_text = "\n".join([f"{word} {{{{pause:5000}}}}" for word in words])



# Save to text file for preview if needed
with open(os.path.join(current_dir + "//tts", tts_name), "w", encoding="utf-8") as f:

    f.write(balabolka_text)



async def fetch_translations(ts):
    tr = Translator()
    return await tr.translate(ts, src='en', dest='zh-cn')

trans = asyncio.run(fetch_translations(words))
meanings = [t.text for t in trans]

total_words = len(words)
rows_per_column = (total_words + 2) // cols

# 表头
if cols == 3:
    md_lines = ["| No. | Word | Chinese | No. | Word | Chinese | No. | Word | Chinese |", 
                "|-----|------|---------|-----|------|---------|-----|------|---------|"]
elif cols == 2:
    md_lines = ["| No. | Word | Chinese | No. | Word | Chinese |", 
                "|-----|------|---------|-----|------|---------|"]
elif cols == 1:
    md_lines = ["| No. | Word | Chinese |", 
                "|-----|------|---------|"]

for row in range(rows_per_column):
    line_parts = []
    for col in range(cols):
        idx = row + col * rows_per_column
        if idx < total_words:
            line_parts.append(f"| {idx+1} | {words[idx]} | {meanings[idx]} ")
        else:
            line_parts.append("| | | ")
    md_lines.append("".join(line_parts) + "|")

with open(os.path.join(current_dir + "//md", md_name), "w", encoding="utf-8") as f:
    f.write("\n".join(md_lines))

