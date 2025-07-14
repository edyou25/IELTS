# Generate Balabolka-formatted text for 300 words with 5-second pause (using <silence msec="5000"/>)
import pandas as pd
import random


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

