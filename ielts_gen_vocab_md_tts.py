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
    "abruptly",    "absorbed",    "abusively",    "accordance",    "adequate",    "advocates",
    "agendas",    "altitude",    "anticipate",    "anticipating",    "aqueducts",    "archipelago",
    "arson",    "artistic",    "ascent",    "augmented",    "avail",    "ballet",
    "bank",    "banquet",    "beads",    "bedsit",    "begs",    "bizarre",
    "blend",    "bolstered",    "canoe",    "carnival",    "catered",    "ceramics",
    "charcoal",    "chronological",    "clarinet",    "clay",    "coating",    "comets",
    "commissioned",    "complicated",    "composition",    "comprehend",    "compromised",    "compulsory",
    "concentrate",    "connotative",    "consultation",    "consumption",    "contagious",    "contradictory",
    "coordination",    "cope",    "counteract",    "dementia",    "destruction",    "deterioration",
    "diary",    "diminishing",    "distinct",    "distinction",    "diversify",    "drawing",
    "drummer",    "eerie",    "ethical",    "exacerbated",    "expertise",    "explicit",
    "exploitation",    "exponentially",    "feminine",    "figures",    "filth",    "flirtation",
    "flute",    "fraud",    "genuine",    "glazes",    "glitch",    "hierarchies",
    "hills",    "hut",    "illustrator",    "implicit",    "inferior",    "infuse",
    "ingredient",    "initiative",    "insulating",    "intimate",    "lace",    "lap",
    "latter",    "lauded",    "lime",    "literacy",    "lucrative",    "maladies",
    "marble",    "masculine",    "medicals",    "minded",    "morale",    "necessarily",
    "niece",    "nutrients",    "obscure",    "october",    "odd",    "omit",
    "opposite",    "outmoded",    "overrun",    "past",    "pattern",    "peasants",
    "percussion",    "persuasive",    "pharmacy",    "playwrights",    "predators",    "preserve",
    "priority",    "prominent",    "prone",    "proportion",    "publicised",    "radical",
    "ramp",    "rather",    "reaffirm",    "reduction",    "rehearse",    "remuneration",
    "renowned",    "repatriation",    "resemble",    "reservations",    "respiratory",    "ribbons",
    "scraper",    "second",    "sector",    "shipwrecked",    "shoulder",    "solitary",
    "souvenirs",    "sphere",    "stamp",    "striking",    "submission",    "summit",
    "superior",    "swiss",    "synthetic",    "taxation",    "tedious",    "terrace",
    "textiles",    "thermometer",    "thorough",    "thrive",    "thrived",    "tidy",
    "traits",    "transcend",    "transparency",    "trivial",    "undermines",    "underpinnings",
    "vaccinations",    "vibrant",    "vitamins",    "wardens",    "warehouse",    "weight",
    "whereas",    "yacht"
]


vocabulary_name = "ielts-bro-1-176"

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

