import asyncio
from googletrans import Translator
import signal
import sys
import time
import os
import edge_tts
import pygame
import tempfile
import threading
import queue

words = [
    "climate variation", "fine", "expressway/freeway", "economic crisis", "change", "hard-working",
    "mall", "study lounge", "in a fit state", "broadcast", "pipe", "housemaid",
    "workaholic", "register", "tenant", "collapse", "recession", "residence",
    "staple", "washing machine", "hospitable", "skiing", "rank", "fire",
    "hire", "on sale", "pork", "electric cooker", "subway entrance", "cyberspace",
    "want ads", "extra copy", "consult", "ferry", "neighbor-hood", "interviewer",
    "recycled water", "keep down the cost", "humidity", "shopping list", "cooperation", "multimedia",
    "housekeeper", "forgetful", "publisher", "surgeon", "blaze a trail", "enroll in",
    "do odd jobs", "convenience store", "light bulb", "reading room", "compromise", "computer science",
    "editorial", "telephone booth", "keep contact", "personality", "be involved in", "balance",
    "climate-sensitive activity", "in a mess", "vacuum cleaner", "read selectively", "sink", "take a message",
    "catalogue", "periodical room", "unfurnished", "apartment/flat", "appointment", "anesthetist",
    "job hunting", "writing permission", "overweight", "overdue", "makeup exam", "get through a novel",
    "outlet", "platform", "recognition", "documentary", "department store", "leak",
    "symptom", "iron", "job-hopping", "put on reserve", "advanced course", "counter",
    "assistance", "out of stock", "fit as a fiddle", "commercial advertisement", "drop the course", "compulsory course",
    "install", "cupboard", "client", "opening/vacancy", "interviewee", "legend",
    "credit", "syllabus", "determined", "wage", "book the ticket", "furnace",
    "novel", "watch your diet", "volume", "recyclable", "out of shape", "magazine",
    "downtown", "read extensively", "lose weight", "spare room", "air conditioner", "be addicted to the book",
    "copier", "hiking", "economical", "housework", "climate trend", "perseverance",
    "prosperous", "run for", "psychology course", "server", "on business", "wear out",
    "hallway", "infectious illness", "position", "sophomore", "leisure time", "water and soil erosion",
    "financier", "campaign manager", "physician", "book reservation", "climate watch", "maintenance",
    "refrigerator/fridge", "roundtrip", "strear", "master", "waiter/waitress", "book review",
    "inflation", "horror movie", "feel under the weather", "publication", "renewable energy", "call on",
    "the student", "date", "hitch-hike", "go dutch aa", "full-time job", "baby crib",
    "hold on", "breeze", "closing time", "drop-out", "mutton", "check in",
    "quarterly", "devote to", "associate professor", "introductory course", "stationery", "hang on",
    "sewage treatment", "application letter", "infirmary", "monetary", "teaching assistant", "conductor",
    "cutlery", "deforestation rate", "paperback edition", "violence movie", "excursion", "physics",
    "have no match for", "chairman", "achievement", "index", "press", "in poor shape",
    "tv channels", "sars", "sneeze", "runny nose", "in good shape", "stomachache",
    "library card", "downpour", "branch", "buffet", "gardening", "part-time job",
    "surplus", "sideboard", "take over", "recruit", "muggy", "workload",
    "climatic anomaly", "potential", "conservation area", "get along with", "resort", "plough through",
    "snack", "allergy", "diabetes", "electronic product", "high-speed train", "done",
    "on diet", "computer course", "chain store", "struggle", "elective/optional course", "deliver",
    "opportunity", "participant", "have a temperature", "fracture", "unemployment", "election campaign",
    "dwell", "depression", "flight number", "current issue", "housewife", "burglar",
    "luxurious items", "check out", "pay phone", "climate warming", "clinic", "back issue",
    "continuous exploration", "menu", "biography", "accommodate", "alumni/alumnus", "turn down",
    "decoration", "epidemic", "transportation", "transfer", "in charge of", "grocery store",
    "resume", "crack", "in stock", "attending/chief doctor", "attitude", "proposal",
    "loaf", "bankrupt", "shelf", "regular dinner", "symbol", "performance",
    "post doctorate", "return", "appetizer", "fix the dinner", "house-warming party", "professor",
    "bird flu", "ventilation", "take the course", "keyword", "speech contest", "supervisor",
    "dental decay", "shuttle", "past the prime", "inquiry", "diligent", "motel",
    "sign up for", "dean", "heater", "sell out", "seminar", "napkin",
    "plumber", "librarian", "multiple glazing", "conflict", "gust", "customer",
    "hang up", "curriculum", "tv theater", "bachelor", "transaction", "latest number",
    "deflation", "toothache", "visa", "beef steak", "dessert", "put on weight",
    "furnished", "entertainment industry", "pioneer", "freshman", "budget", "receipt",
    "temperature", "laundry", "suburb", "express train", "periodical", "keep an eye on",
    "lecturer", "family size", "household expenses", "reference room", "travel agency", "bid",
    "complaint", "tribute", "sore throat", "impression", "beverage", "decline",
    "mineral bath", "confident", "medium", "supermarket", "overwork", "vote",
    "hacker", "the stacks", "contribution", "join for dinner", "inexperienced", "doctoral candidate",
    "make a reservation", "physical exercise", "circulation", "forecast", "digital video camera", "out of print",
    "long-distance call", "landlord/landlady", "tube/underground", "interview", "senior student", "candidate",
    "raw", "junior student", "live broadcast"
]
do_translate = False  # Set to True to enable translation
read_vocabulary = False  # Set to True to read vocabulary aloud

async def fetch_translation(text, src='en', dest='zh-cn'):
    tr = Translator()
    result = await tr.translate(text, src=src, dest=dest)
    return result.text

# Initialize pygame for audio playback
pygame.init()
pygame.mixer.init()

# Track temporary files for cleanup
temp_files = []

def cleanup():
    for file in temp_files:
        try:
            if os.path.exists(file):
                pygame.mixer.quit()
                pygame.mixer.init()
                time.sleep(0.5)
                os.remove(file)
        except Exception as e:
            print(f"Failed to clean up {file}: {e}")
            try:
                if os.name == 'nt':
                    import ctypes
                    MOVEFILE_DELAY_UNTIL_REBOOT = 4
                    ctypes.windll.kernel32.MoveFileExW(file, None, MOVEFILE_DELAY_UNTIL_REBOOT)
            except:
                pass

def signal_handler(sig, frame):
    print("\n\nCtrl+C detected, exiting...")
    cleanup()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

async def speak_and_test(words):
    incorrect_words = []
    correct_count = 0
    previous_word = None
    previous_known = False
    
    # Create a unique temp directory for audio files
    temp_dir = tempfile.mkdtemp(prefix="ielts_audio_")
    translations = {}
    # First, get all Chinese translations ahead of time
    if do_translate:
        print("Preparing vocabulary translations...")
        for word in words:
            try:
                translations[word] = await fetch_translation(word, src='en', dest='zh-cn')
            except Exception as e:
                translations[word] = f"[Translation error: {e}]"
            
    print(f"Ready! {len(words)} words loaded.\n")
    print("For each word, type 'y' if you know it, 'n' if you don't\n")
    
    for idx, word in enumerate(words, 1):
        # Show English word first
        print(f"\n[{idx}/{len(words)}] {word}")
        
        # Start preparing audio file in background
        if read_vocabulary:
            temp_file = os.path.join(temp_dir, f"word_{idx}_{int(time.time())}.mp3")
            temp_files.append(temp_file)
            
            # Generate audio file and play it immediately
            tts = edge_tts.Communicate(text=word, voice="en-US-AriaNeural")
            await tts.save(temp_file)
            
            # Play audio automatically
            try:
                pygame.mixer.music.load(temp_file)
                pygame.mixer.music.set_volume(1.0)
                pygame.mixer.music.play()
                
                # Wait for audio to finish with replay option
                try:
                    import msvcrt
                    while pygame.mixer.music.get_busy():
                        if msvcrt.kbhit():
                            key = msvcrt.getch().decode('utf-8', errors='ignore').lower()
                            if key == 'r':
                                pygame.mixer.music.play()
                        time.sleep(0.1)
                except ImportError:
                    # If msvcrt not available, just wait for audio to finish
                    while pygame.mixer.music.get_busy():
                        time.sleep(0.1)
            except Exception as e:
                print(f"Audio error: {e}")
        
        # Now wait for user input after audio played
        user_input = input("").strip().lower()
        
        # Handle 'b' input to mark previous word as incorrect
        if user_input == 'b':
            if previous_word and previous_known:
                # Remove from correct count and add to incorrect list
                correct_count -= 1
                if previous_word not in incorrect_words:
                    incorrect_words.append(previous_word)
                print(f"✓ Marked previous word '{previous_word}' as unknown.")
                
                # Still need to handle the current word
                print(f"\n[{idx}/{len(words)}] {word}")
                user_input = input("Know this word? (y/n): ").strip().lower()
            else:
                print("⚠️ No previous known word to mark as unknown.")
                user_input = input("Know this word? (y/n): ").strip().lower()
        
        # Show Chinese translation after user response
        if do_translate:
            chinese = translations[word]
            print(f"{chinese}")
        
        # Clean up audio resources
        try:
            pygame.mixer.music.unload()
            os.remove(temp_file)
            temp_files.remove(temp_file)
        except:
            pass
        
        # Store current word before moving on
        previous_word = word
        
        if user_input == 'n':
            incorrect_words.append(word)
            previous_known = False
        else:
            correct_count += 1
            previous_known = True
        
        # time.sleep(1)

    print("\n" + "="*50)
    known_percent = correct_count / len(words) * 100
    print(f"📊 Vocabulary Results: Total {len(words)} words")
    print(f"✅ Known: {correct_count} ({known_percent:.1f}%)")
    print(f"❌ Unknown: {len(words) - correct_count} ({100 - known_percent:.1f}%)")
    
    if incorrect_words:
        print("\n❌ Words to review:")
        print("words = [")
        chunks = [incorrect_words[i:i+6] for i in range(0, len(incorrect_words), 6)]
        for i, chunk in enumerate(chunks):
            formatted = ", ".join(f'"{w}"' for w in chunk)
            ending = "," if i < len(chunks) - 1 else ""
            print(f"    {formatted}{ending}")
        print("]")

if __name__ == "__main__":
    try:
        asyncio.run(speak_and_test(words))
    finally:
        cleanup()