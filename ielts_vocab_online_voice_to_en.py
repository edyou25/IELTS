import asyncio
import edge_tts
import pygame
import time
import os
from googletrans import Translator
import signal
import sys
import tempfile
import threading
import queue

words = [
    "boarding pass", "business trip", "credit card", "customer service", "data analysis"
]

VOICE = "en-GB-RyanNeural"
# Valid Edge TTS voices (not related to googletrans)
VOICE = "en-US-AriaNeural"      # Female
# VOICE = "en-US-JennyNeural"     # Female
# VOICE = "en-US-GuyNeural"       # Male
# VOICE = "en-GB-SoniaNeural"     # Female British
# VOICE = "en-AU-NatashaNeural"   # Female Australian
give_chinese = True  # Set to True to give Chinese translation

# Initialize pygame properly for both audio and event handling
pygame.init()  # Initialize all pygame modules
pygame.mixer.init()  # Ensure mixer is initialized

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
    
    # Create a unique temp directory for this session
    temp_dir = tempfile.mkdtemp(prefix="ielts_audio_")
    
    # Track if the directory exists for later cleanup
    temp_dir_exists = True
    
    for idx, word in enumerate(words, 1):
        print(f"\n[{idx}/{len(words)}] 🔊 Please write the word/phrase you hear:")
        tts = edge_tts.Communicate(text=word, voice=VOICE)
        
        # Create unique filename for each word to avoid permission issues
        temp_file = os.path.join(temp_dir, f"word_{idx}_{int(time.time())}.mp3")
        await tts.save(temp_file)
        
        # Create a queue for replay commands
        replay_queue = queue.Queue()
        replay_stop = threading.Event()
        
        # Function to handle audio playback in background
        def audio_playback_thread():
            try:
                # Play the audio
                pygame.mixer.music.load(temp_file)
                pygame.mixer.music.set_volume(1.0)
                pygame.mixer.music.play()
                
                # Continue checking for replay requests while not stopped
                while not replay_stop.is_set():
                    # Check if there's a replay command in queue
                    try:
                        cmd = replay_queue.get(block=False)
                        if cmd == "replay":
                            pygame.mixer.music.play()
                    except queue.Empty:
                        pass
                    
                    time.sleep(0.1)
            except Exception as e:
                print(f"Audio playback error: {e}")
        
        # Start audio playback in background thread
        audio_thread = threading.Thread(target=audio_playback_thread)
        audio_thread.daemon = True
        audio_thread.start()
        
        # Start keyboard listener thread for replay ('r' key)
        def keyboard_listener():
            if not msvcrt_available:
                return
                
            while not replay_stop.is_set():
                try:
                    import msvcrt
                    if msvcrt.kbhit():
                        key = msvcrt.getch().decode('utf-8', errors='ignore').lower()
                        if key == 'r':
                            replay_queue.put("replay")
                            print("Replaying audio...")
                except:
                    pass
                time.sleep(0.1)
        
        kb_thread = threading.Thread(target=keyboard_listener)
        kb_thread.daemon = True
        kb_thread.start()
        
        # print("Type your answer (press 'r' to replay):")
        user_input = input("").strip().lower()
        correct = word.lower()
        
        # Signal threads to stop
        replay_stop.set()
        
        # Wait a moment to ensure threads have stopped using the file
        time.sleep(0.2)
        
        # Explicitly release the file from pygame
        pygame.mixer.music.unload()
        time.sleep(0.2)
        
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
        
        # Delete the temporary audio file immediately after use
        try:
            if os.path.exists(temp_file):
                os.remove(temp_file)
            # print("✓ Temp file deleted")
        except Exception as e:
            print(f"Could not delete temp file: {e}")
            # Add to global list only if immediate deletion failed
            temp_files.append(temp_file)
        
        time.sleep(1)

    # Try to remove the temp directory if it's empty
    try:
        if temp_dir_exists and os.path.exists(temp_dir):
            os.rmdir(temp_dir)
    except:
        pass
    
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
    # Check if msvcrt is available (Windows only)
    msvcrt_available = False
    try:
        import msvcrt
        msvcrt_available = True
    except ImportError:
        pass
        
    try:
        asyncio.run(speak_and_test(words))
    finally:
        cleanup()