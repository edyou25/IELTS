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

from words import words 

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