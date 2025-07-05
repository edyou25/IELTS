# Generate Balabolka-formatted text for 300 words with 5-second pause (using <silence msec="5000"/>)
import pandas as pd
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

random.shuffle(words)
print("words = [")
for i in range(0, len(words), 6):
    chunk = words[i : i + 6]
    line = ", ".join(f'"{w}"' for w in chunk)
    comma = "," if i + 6 < len(words) else ""
    print(f"    {line}{comma}")
print("]")

