import asyncio
import edge_tts
import pygame
import time
import os
from googletrans import Translator
import signal
import sys

words = [
    "boarding pass", "credit card", "student discount", "entry fee", "group booking",
    "customer service", "library card", "parking permit", "mobile phone", "return ticket"
]

VOICE = "en-GB-RyanNeural"
# Valid Edge TTS voices (not related to googletrans)
VOICE = "en-US-AriaNeural"      # Female
# VOICE = "en-US-JennyNeural"     # Female
# VOICE = "en-US-GuyNeural"       # Male
# VOICE = "en-GB-SoniaNeural"     # Female British
# VOICE = "en-AU-NatashaNeural"   # Female Australian
give_chinese = True  # Set to True to give Chinese translation

pygame.mixer.init()

async def fetch_translation(text):
    tr = Translator()
    result = await tr.translate(text, src='en', dest='zh-cn')
    return result.text

temp_files = []

def cleanup():
    for file in temp_files:
        try:
            if os.path.exists(file):
                # Force pygame to stop using any audio files before attempting deletion
                pygame.mixer.quit()
                pygame.mixer.init()
                time.sleep(0.5)  # Give more time for resources to be released
                os.remove(file)
        except Exception as e:
            print(f"Failed to clean up {file}: {e}")
            # If we can't delete now, mark for deletion on Windows reboot
            try:
                if os.name == 'nt':  # Windows
                    import ctypes
                    MOVEFILE_DELAY_UNTIL_REBOOT = 4
                    ctypes.windll.kernel32.MoveFileExW(file, None, MOVEFILE_DELAY_UNTIL_REBOOT)
                    print(f"File {file} will be deleted on next reboot")
            except:
                pass

def signal_handler(sig, frame):
    print("\n\nCtrl+C detected, exiting...")
    cleanup()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

async def speak_and_test(words):
    base_dir = os.path.abspath(os.path.dirname(__file__))
    incorrect_words = []
    correct_count = 0
    
    for idx, word in enumerate(words, 1):
        temp_file = os.path.join(base_dir, f"temp_{idx}_{int(time.time())}.mp3")
        temp_files.append(temp_file)
        print(f"\n[{idx}/{len(words)}] 🔊 Please write the word/phrase you hear:")
        tts = edge_tts.Communicate(text=word, voice=VOICE)
        await tts.save(temp_file)
        
        try:
            pygame.mixer.music.load(temp_file)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
            pygame.mixer.music.unload()
            pygame.mixer.music.set_volume(0)  # Help release resources
            time.sleep(0.5)  # Increase delay to ensure file is released
        except Exception as e:
            print(f"Error: {e}")
        
        time.sleep(0.5)
        
        user_input = input("").strip().lower()
        correct = word.lower()
        
        if user_input == correct:
            print("✅ Correct!")
            correct_count += 1
        else:
            print(f"❌ Incorrect, should be: {word}")
            incorrect_words.append(word)
        
        try:
            if give_chinese:
                translation = await fetch_translation(word)
            print(f"📝 Chinese translation: {translation}")
        except Exception as e:
            print(f"Unable to get translation: {e}")
        
        try:
            if os.path.exists(temp_file):
                os.remove(temp_file)
        except PermissionError:
            print(f"Cannot delete temp file, it will be cleaned up when program ends")
        
        time.sleep(1)

    print("\n" + "="*50)
    accuracy = correct_count / len(words) * 100
    print(f"📊 Test Results: Total {len(words)} words, {correct_count} correct, Accuracy {accuracy:.1f}%")
    
    if incorrect_words:
        print("\n❌ Incorrect words list:")
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