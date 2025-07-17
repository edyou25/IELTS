import asyncio
from googletrans import Translator
import signal
import sys
import time
import os

from temp import words 

do_translate = True  # Set to True to enable translation
async def fetch_translation(text, src='en', dest='zh-cn'):
    tr = Translator()
    result = await tr.translate(text, src=src, dest=dest)
    return result.text

def signal_handler(sig, frame):
    print("\n\nCtrl+C detected, exiting...")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

async def speak_and_test(words):
    incorrect_words = []
    correct_count = 0
    
    # First, get all Chinese translations ahead of time
    print("Preparing vocabulary translations...")
    translations = {}
    for word in words:
        try:
            translations[word] = await fetch_translation(word, src='en', dest='zh-cn')
        except Exception as e:
            translations[word] = f"[Translation error: {e}]"
            
    print(f"Ready! {len(words)} words loaded.\n")
    
    for idx, word in enumerate(words, 1):
        # Show Chinese translation and ask for English word
        chinese = translations[word]
        print(f"\n[{idx}/{len(words)}]🔊 Chinese: {chinese}")
        # print("Write the English word/phrase:")
        
        user_input = input("").strip().lower()
        correct = word.lower()
        
        if user_input == correct:
            print("✅ Correct!")
            correct_count += 1
        else:
            print(f"❌ Incorrect, should be: {word}")
            incorrect_words.append(word)
        
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
        pass  # No cleanup needed