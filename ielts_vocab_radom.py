# Generate Balabolka-formatted text for 300 words with 5-second pause (using <silence msec="5000"/>)
import pandas as pd
import random


# Load word list from user-provided data
words = [
    "accommodate",    "achievement",    "advanced course",    "air conditioner",    "allergy",    "alumni/alumnus",
    "anesthetist",    "apartment/flat",    "appetizer",    "application letter",    "appointment",    "assistance",
    "associate professor",    "attending/chief doctor",    "attitude",    "baby crib",    "bachelor",    "back issue",
    "balance",    "bankrupt",    "be addicted to the book",    "be involved in",    "beef steak",    "beverage",
    "bid",    "biography",    "bird flu",    "blaze a trail",    "book reservation",    "book review",
    "book the ticket",    "branch",    "breeze",    "broadcast",    "budget",    "buffet",
    "burglar",    "call on",    "campaign manager",    "candidate",    "catalogue",    "chain store",
    "chairman",    "change",    "check in",    "check out",    "circulation",    "client",
    "climate trend",    "climate variation",    "climate warming",    "climate watch",    "climate-sensitive activity",    "climatic anomaly",
    "clinic",    "closing time",    "collapse",    "commercial advertisement",    "complaint",    "compromise",
    "compulsory course",    "computer course",    "computer science",    "conductor",    "confident",    "conflict",
    "conservation area",    "consult",    "continuous exploration",    "contribution",    "convenience store",    "cooperation",
    "copier",    "counter",    "crack",    "credit",    "cupboard",    "current issue",
    "curriculum",    "customer",    "cutlery",    "cyberspace",    "date",    "dean",
    "decline",    "decoration",    "deflation",    "deforestation rate",    "deliver",    "dental decay",
    "department store",    "depression",    "dessert",    "determined",    "devote to",    "diabetes",
    "digital video camera",    "diligent",    "do odd jobs",    "doctoral candidate",    "documentary",    "done",
    "downpour",    "downtown",    "drop the course",    "drop-out",    "dwell",    "economic crisis",
    "economical",    "editorial",    "election campaign",    "elective/optional course",    "electric cooker",    "electronic product",    
    "enroll in",    "entertainment industry",    "epidemic",    "excursion",    "express train",    "expressway/freeway",
    "extra copy",    "family size",    "feel under the weather",    "ferry",    "financier",    "fine",
    "fire",    "fit as a fiddle",    "fix the dinner",    "flight number",    "forecast",    "forgetful",
    "fracture",    "freshman",    "full-time job",    "furnace",    "furnished",    "gardening",
    "get along with",    "get through a novel",    "go dutch aa",    "grocery store",    "gust",    "hacker",
    "hallway",    "hang on",    "hang up",    "hard-working",    "have a temperature",    "have no match for",
    "heater",    "high-speed train",    "hiking",    "hire",    "hitch-hike",    "hold on",
    "horror movie",    "hospitable",    "house-warming party",    "household expenses",    "housekeeper",    "housemaid",
    "housewife",    "housework",    "humidity",    "impression",    "in a fit state",    "in a mess",
    "in charge of",    "in good shape",    "in poor shape",    "in stock",    "index",    "inexperienced",
    "infectious illness",    "infirmary",    "inflation",    "inquiry",    "install",    "interview",
    "interviewee",    "interviewer",    "introductory course",    "iron",    "job hunting",    "job-hopping",
    "join for dinner",    "junior student",    "keep an eye on",    "keep contact",    "keep down the cost",    "keyword",
    "landlord/landlady",    "latest number",    "laundry",    "leak",    "lecturer",    "legend",
    "leisure time",    "librarian",    "library card",    "light bulb",    "live broadcast",    "loaf",
    "long-distance call",    "lose weight",    "luxurious items",    "magazine",    "maintenance",    "make a reservation",
    "makeup exam",    "mall",    "master",    "medium",    "menu",    "mineral bath",
    "monetary",    "motel",    "muggy",    "multimedia",    "multiple glazing",    "mutton",
    "napkin",    "neighbor-hood",    "novel",    "on business",    "on diet",    "on sale",
    "opening/vacancy",    "opportunity",    "out of print",    "out of shape",    "out of stock",    "outlet",
    "overdue",    "overweight",    "overwork",    "paperback edition",    "part-time job",    "participant",
    "past the prime",    "pay phone",    "performance",    "periodical",    "periodical room",    "perseverance",
    "personality",    "physical exercise",    "physician",    "physics",    "pioneer",    "pipe",
    "platform",    "plough through",    "plumber",    "pork",    "position",    "post doctorate",
    "potential",    "press",    "professor",    "proposal",    "prosperous",    "psychology course",
    "publication",    "publisher",    "put on reserve",    "put on weight",    "quarterly",    "rank",
    "raw",    "read extensively",    "read selectively",    "reading room",    "receipt",    "recession",
    "recognition",    "recruit",    "recyclable",    "recycled water",    "reference room",    "refrigerator/fridge",
    "register",    "regular dinner",    "renewable energy",    "residence",    "resort",    "resume",
    "return",    "roundtrip",    "run for",    "runny nose",    "sars",    "sell out",
    "seminar",    "senior student",    "server",    "sewage treatment",    "shelf",    "shopping list",
    "shuttle",    "sideboard",    "sign up for",    "sink",    "skiing",    "snack",
    "sneeze",    "sophomore",    "sore throat",    "spare room",    "speech contest",    "staple",
    "stationery",    "stomachache",    "strear",    "struggle",    "study lounge",    "suburb",
    "subway entrance",    "supermarket",    "supervisor",    "surgeon",    "surplus",    "syllabus",
    "symbol",    "symptom",    "take a message",    "take over",    "take the course",    "teaching assistant",
    "telephone booth",    "temperature",    "tenant",    "the stacks",    "the student",    "toothache",
    "transaction",    "transfer",    "transportation",    "travel agency",    "tribute",    "tube/underground",
    "turn down",    "tv channels",    "tv theater",    "unemployment",    "unfurnished",    "vacuum cleaner",
    "ventilation",    "violence movie",    "visa",    "volume",    "vote",    "wage",
    "waiter/waitress",    "want ads",    "washing machine",    "watch your diet",    "water and soil erosion",    "wear out",
    "workaholic",    "workload",    "writing permission"
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

