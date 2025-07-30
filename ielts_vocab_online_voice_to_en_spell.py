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

from words import words
from configs.configs import VOICE

give_chinese = True  # Set to True to give Chinese translation
spell_letters = True  # Set to True to spell out letters after word

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

async def create_spelled_audio(word, temp_dir, idx):
    """创建拼写版本的音频文件"""
    # 创建拼写文本，在每个字母之间添加多个停顿
    letters = list(word.lower())
    spelled_parts = []
    for i, letter in enumerate(letters):
        spelled_parts.append(letter)
        if i < len(letters) - 1:  # 不在最后一个字母后添加停顿
            spelled_parts.append("...")  # 多个句号创建长停顿
    
    spelled_text = " ".join(spelled_parts)
    
    tts_spelled = edge_tts.Communicate(text=spelled_text, voice=VOICE)
    temp_spelled_file = os.path.join(temp_dir, f"spelled_{idx}_{int(time.time())}.mp3")
    await tts_spelled.save(temp_spelled_file)
    
    return temp_spelled_file

async def play_audio_with_control(audio_file, replay_queue, replay_stop):
    """播放音频并处理重播控制"""
    try:
        # Play the audio
        pygame.mixer.music.load(audio_file)
        pygame.mixer.music.set_volume(1.0)
        pygame.mixer.music.play()
        
        # Wait for audio to finish
        while pygame.mixer.music.get_busy():
            # Check if there's a replay command in queue
            try:
                cmd = replay_queue.get(block=False)
                if cmd == "replay":
                    pygame.mixer.music.play()
                    print("🔄 Replaying...")
            except queue.Empty:
                pass
            
            if replay_stop.is_set():
                break
                
            time.sleep(0.1)
            
    except Exception as e:
        print(f"Audio playback error: {e}")

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
        
        # Create normal audio
        tts = edge_tts.Communicate(text=word, voice=VOICE)
        temp_file = os.path.join(temp_dir, f"word_{idx}_{int(time.time())}.mp3")
        await tts.save(temp_file)
        
        # Create spelled audio if enabled
        spelled_file = None
        if spell_letters:
            spelled_file = await create_spelled_audio(word, temp_dir, idx)
        
        # Create a queue for replay commands
        replay_queue = queue.Queue()
        replay_stop = threading.Event()
        
        # Function to handle audio playback in background
        def audio_playback_thread():
            # First play the normal word
            asyncio.run(play_audio_with_control(temp_file, replay_queue, replay_stop))
            
            # Then play spelled version if enabled and not stopped
            if spell_letters and spelled_file and not replay_stop.is_set():
                time.sleep(0.5)  # Short pause between word and spelling
                asyncio.run(play_audio_with_control(spelled_file, replay_queue, replay_stop))
        
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
                except:
                    pass
                time.sleep(0.1)
        
        kb_thread = threading.Thread(target=keyboard_listener)
        kb_thread.daemon = True
        kb_thread.start()
        
        # Show what will be played
        # if spell_letters:
        #     letters_display = '-'.join(list(word.lower()))
        #     print(f"🔤 Playing: {word} → {letters_display}")
        
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
            # if spell_letters:
            #     letters_display = '-'.join(list(word.lower()))
            #     print(f"🔤 Spelling: {letters_display}")
            incorrect_words.append(word)
        
        try:
            if give_chinese:
                translation = await fetch_translation(word)
                print(f"📝 Chinese translation: {translation}")
        except Exception as e:
            print(f"Unable to get translation: {e}")
        
        # Delete the temporary audio files immediately after use
        for temp_audio_file in [temp_file, spelled_file]:
            if temp_audio_file:
                try:
                    if os.path.exists(temp_audio_file):
                        os.remove(temp_audio_file)
                except Exception as e:
                    print(f"Could not delete temp file: {e}")
                    # Add to global list only if immediate deletion failed
                    temp_files.append(temp_audio_file)
        
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