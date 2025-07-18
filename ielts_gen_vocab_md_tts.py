# Generate Balabolka-formatted text for 300 words with 5-second pause (using <silence msec="5000"/>)
import pandas as pd
from googletrans import Translator
import asyncio
import random
import os
import time
from tqdm import tqdm

current_path = os.path.abspath(__file__)
current_dir = os.path.dirname(current_path)

# Load word list from user-provided data
from configs.configs import vocabulary_name, cols
from words import words

md_name = vocabulary_name + ".md"
tts_name = vocabulary_name + ".txt"

words = list(dict.fromkeys(words))

# Generate Balabolka-compatible input with 5s pause
balabolka_text = "\n".join([f"{word} {{{{pause:5000}}}}" for word in words])

# Save to text file for preview if needed
with open(os.path.join(current_dir + "//tts", tts_name), "w", encoding="utf-8") as f:
    f.write(balabolka_text)

async def fetch_translations_with_progress(word_list):
    """Fetch translations with progress bar"""
    tr = Translator()
    meanings = []
    
    print(f"Translating {len(word_list)} words...")
    
    # Create progress bar
    with tqdm(total=len(word_list), desc="Translation Progress", 
              bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]") as pbar:
        
        for i, word in enumerate(word_list):
            try:
                # Translate individual word
                result = await tr.translate(word, src='en', dest='zh-cn')
                meanings.append(result.text)
                
                # Update progress bar
                pbar.set_postfix({"Current": word, "Translation": result.text})
                pbar.update(1)
                
                # Small delay to avoid rate limiting
                # await asyncio.sleep(0.1)
                
            except Exception as e:
                # print(f"\n❌ Error translating '{word}': {e}")
                meanings.append(word)  # Fallback to original word
                pbar.update(1)
    
    return meanings

# Fetch translations with progress bar
meanings = asyncio.run(fetch_translations_with_progress(words))

total_words = len(words)
rows_per_column = (total_words + 2) // cols

# 表头
if cols == 3:
    md_lines = ["| No. | Word | Chinese | No. | Word | Chinese | No. | Word | Chinese |", 
                "|-----|------|---------|-----|------|---------|-----|------|---------|"]
elif cols == 2:
    md_lines = ["| No. | Word | Chinese | No. | Word | Chinese |", 
                "|-----|------|---------|-----|------|---------|"]
elif cols == 1:
    md_lines = ["| No. | Word | Chinese |", 
                "|-----|------|---------|"]

for row in range(rows_per_column):
    line_parts = []
    for col in range(cols):
        idx = row + col * rows_per_column
        if idx < total_words:
            line_parts.append(f"| {idx+1} | {words[idx]} | {meanings[idx]} ")
        else:
            line_parts.append("| | | ")
    md_lines.append("".join(line_parts) + "|")

with open(os.path.join(current_dir + "//md", md_name), "w", encoding="utf-8") as f:
    f.write(f"### {vocabulary_name}\n\n")
    f.write("\n".join(md_lines))

