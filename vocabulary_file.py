# Generate Balabolka-formatted text for 300 words with 5-second pause (using <silence msec="5000"/>)
import pandas as pd
from googletrans import Translator
import asyncio
import random

# Load word list from user-provided data
words = [
    "zone", "resident", "reservation", "ambulance", "device", "politician",
    "nutrition", "calendar", "appointment", "hostel", "diploma", "satisfaction",
    "gymnasium", "boarding pass", "tourism", "clerk", "auditor", "essay",
    "dancer", "deadline", "arrival", "actor", "tablet", "builder",
    "physician", "plumber", "responsibility", "banker", "interview", "heater",
    "intersection", "campus", "scientist", "commute", "withdrawal", "teacher",
    "reception", "curriculum", "internship", "experience", "welfare", "telephone",
    "workshop", "ferry", "police officer", "gas", "requirement", "colleague",
    "schedule", "transportation", "dormitory", "departure", "venue", "receipt",
    "pedestrian", "gym", "museum", "upload", "canteen", "consultant",
    "enquiry", "warehouse", "illness", "invoice", "lecture", "client",
    "basement", "university", "analyst", "translator", "vegetarian", "scholarship",
    "surcharge", "charger", "tutor", "rent", "employer", "blanket",
    "thesis", "transit", "password", "pillow", "professor", "catering",
    "tourist", "storage", "library", "cancellation", "attendance", "mattress",
    "luggage", "discount", "allergy", "baggage", "equipment", "electrician",
    "feedback", "budget", "citizen", "deposit", "gender", "motorcycle",
    "baker", "payment", "ingredient", "insurance", "nurse", "receptionist",
    "complaint", "update", "headache", "smartphone", "fitness", "cleaner",
    "photographer", "photography", "electricity", "tenant", "beverage", "souvenir",
    "interpreter", "surgeon", "editor", "mechanic", "specialist", "credit card",
    "theater", "monitor", "extension", "cabin", "architect", "tour guide",
    "address", "nationality", "accountant", "platform", "driver", "kettle",
    "voucher", "gardener", "cash", "pharmacy", "pharmacist", "youth",
    "car park", "aisle", "facility", "account", "reimbursement", "musician",
    "assessment", "waiter", "emergency", "visa", "calorie", "sculpture",
    "timetable", "producer", "instructor", "register", "room rate", "postage",
    "backpack", "painting", "retail", "email", "cashier", "terminal",
    "pilot", "lawyer", "roommate", "microwave", "certificate", "technician",
    "volunteer", "qualification", "owner", "designer", "farmer", "maintenance",
    "assistant", "accommodation", "utilities", "chef", "fire exit", "lecturer",
    "librarian", "rehearsal", "plumbing", "secretary", "destination", "check-in",
    "heating", "keyboard", "estate", "medication", "undergraduate", "brochure",
    "sponsorship", "broker", "sailor", "nursery", "cabin crew", "poet",
    "transfer", "manager", "supervisor", "employee", "laundry", "judge",
    "lounge", "lease", "passport", "guidebook", "speaker", "apartment",
    "faculty", "subsidy", "economist", "laboratory", "headphone", "vaccination",
    "tuition", "currency", "customer", "painter", "researcher", "access",
    "engineer", "airline", "surrounding", "carpenter", "stomachache", "cinema",
    "repair", "expense", "income", "surveillance", "training", "adapter",
    "waitress", "director", "vehicle", "wheelchair", "injury", "soldier",
    "residence", "priority", "neighbor", "overtime", "balcony", "roundabout",
    "token", "postgraduate", "download", "principal", "attachment", "assignment",
    "postcode", "visitor", "transaction", "seminar", "refund", "landlord",
    "examination", "avenue", "dentist", "psychologist", "novelist", "surname",
    "suburb", "student", "hallway", "opportunity", "cruise", "passenger",
    "revision", "corridor", "prescription", "diplomat", "salary", "butcher",
    "journalist", "suitcase", "cafeteria", "dessert", "sanitation", "bicycle",
    "fridge", "occupation", "sightseeing", "curtain", "website", "exhibition",
    "counselor", "itinerary", "gallery", "resume", "firefighter", "battery"
]

words = list(dict.fromkeys(words))



# Generate Balabolka-compatible input with 5s pause
balabolka_text = "\n".join([f"{word} {{{{pause:5000}}}}" for word in words])



# Save to text file for preview if needed
output_path = "tts_input.txt"
with open(output_path, "w") as f:
    f.write(balabolka_text)

output_path

async def fetch_translations(ts):
    tr = Translator()
    return await tr.translate(ts, src='en', dest='zh-cn')

trans = asyncio.run(fetch_translations(words))
meanings = [t.text for t in trans]

total_words = len(words)
rows_per_column = (total_words + 2) // 3

# 表头
md_lines = ["| No. | Word | Chinese | No. | Word | Chinese | No. | Word | Chinese |", 
            "|-----|------|---------|-----|------|---------|-----|------|---------|"]

for row in range(rows_per_column):
    line_parts = []
    for col in range(3):
        idx = row + col * rows_per_column
        if idx < total_words:
            line_parts.append(f"| {idx+1} | {words[idx]} | {meanings[idx]} ")
        else:
            line_parts.append("| | | ")
    md_lines.append("".join(line_parts) + "|")

with open(r"c:\Users\85244\OneDrive\Desktop\IELTS\vocabulary.md", "w", encoding="utf-8") as f:
    f.write("\n".join(md_lines))

