import asyncio
from googletrans import Translator
import signal
import sys
import time
import os
import json
from tqdm import tqdm

from words import words 

do_translate = True  # Set to True to enable translation
async def fetch_translation(text, src='en', dest='zh-cn'):
    tr = Translator()
    result = await tr.translate(text, src=src, dest=dest)
    return result.text

def signal_handler(sig, frame):
    print("\n\nCtrl+C detected, exiting...")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def load_translations_cache():
    """Load translations from cache file"""
    cache_file = os.path.join(os.path.dirname(__file__), 'translations_cache.json')
    if os.path.exists(cache_file):
        try:
            with open(cache_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Warning: Failed to load cache: {e}")
    return {}

def save_translations_cache(translations):
    """Save translations to cache file"""
    cache_file = os.path.join(os.path.dirname(__file__), 'translations_cache.json')
    try:
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(translations, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Warning: Failed to save cache: {e}")

async def speak_and_test(words):
    incorrect_words = []
    correct_count = 0
    
    # Load existing translations from cache
    print("📂 Loading translation cache...")
    translations = load_translations_cache()
    
    # Check which words need translation
    words_to_translate = [word for word in words if word not in translations]
    cached_count = len(words) - len(words_to_translate)
    
    if cached_count > 0:
        print(f"✅ Found {cached_count} cached translations")
    
    if words_to_translate:
        print(f"🔤 Translating {len(words_to_translate)} new words...")
        
        # Use tqdm progress bar for translation preparation
        with tqdm(total=len(words_to_translate), desc="Translating", 
                  bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]") as pbar:
            
            for word in words_to_translate:
                try:
                    translation = await fetch_translation(word, src='en', dest='zh-cn')
                    translations[word] = translation
                    pbar.set_postfix({"Current": word, "Translation": translation[:15] + "..." if len(translation) > 15 else translation})
                except Exception as e:
                    translations[word] = f"[Translation error: {e}]"
                    pbar.set_postfix({"Current": word, "Status": "Error"})
                
                pbar.update(1)
        
        # Save updated translations to cache
        print("💾 Saving translations to cache...")
        save_translations_cache(translations)
    else:
        print("✅ All translations loaded from cache!")
            
    print(f"🎯 Ready! {len(words)} words loaded.\n")
    
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