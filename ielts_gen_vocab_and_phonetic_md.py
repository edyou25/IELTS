# Generate Balabolka-formatted text for 300 words with 5-second pause (using <silence msec="5000"/>)
import pandas as pd
from googletrans import Translator
import asyncio
import random
import os
import requests
import json
import nltk
from nltk.corpus import cmudict

current_path = os.path.abspath(__file__)
current_dir = os.path.dirname(current_path)

# Download CMU dictionary if not already present
try:
    d = cmudict.dict()
except LookupError:
    nltk.download('cmudict')
    d = cmudict.dict()

# Load word list from user-provided data
from temp import words
vocabulary_name = "ielts-bro-test"

md_name = vocabulary_name + ".md"

cols = 2  # Number of columns in the markdown table

words = list(dict.fromkeys(words))

def arpabet_to_ipa(arpabet):
    """Convert ARPABET to IPA (Standard British English style)"""
    conversion_map = {
        'AA': 'ɑː', 'AE': 'æ', 'AH': 'ʌ', 'AO': 'ɔː', 'AW': 'aʊ', 'AY': 'aɪ',
        'B': 'b', 'CH': 'tʃ', 'D': 'd', 'DH': 'ð', 'EH': 'e', 'ER': 'ə',
        'EY': 'eɪ', 'F': 'f', 'G': 'g', 'HH': 'h', 'IH': 'ɪ', 'IY': 'iː',
        'JH': 'dʒ', 'K': 'k', 'L': 'l', 'M': 'm', 'N': 'n', 'NG': 'ŋ',
        'OW': 'əʊ', 'OY': 'ɔɪ', 'P': 'p', 'R': 'r', 'S': 's', 'SH': 'ʃ',
        'T': 't', 'TH': 'θ', 'UH': 'ʊ', 'UW': 'uː', 'V': 'v', 'W': 'w',
        'Y': 'j', 'Z': 'z', 'ZH': 'ʒ'
    }
    
    ipa_sounds = []
    for sound in arpabet:
        # Remove stress markers (numbers)
        clean_sound = ''.join([c for c in sound if not c.isdigit()])
        if clean_sound in conversion_map:
            ipa_sounds.append(conversion_map[clean_sound])
        else:
            ipa_sounds.append(clean_sound.lower())
    
    result = ''.join(ipa_sounds)
    
    # Post-processing: fix common patterns
    result = result.replace('ər', 'ə')  # Remove r-coloring
    result = result.replace('θə', 'θɜː')  # thorough pattern
    result = result.replace('ɑr', 'ɑː')  # car pattern
    result = result.replace('ɔr', 'ɔː')  # for pattern
    
    return result

def get_phonetic(word):
    """Get phonetic transcription using CMU dictionary"""
    word_lower = word.lower()
    if word_lower in d:
        # Get the first pronunciation
        arpabet = d[word_lower][0]
        ipa = arpabet_to_ipa(arpabet)
        return f"/{ipa}/"
    else:
        print(f"Word '{word}' not found in CMU dictionary")
        return f"/{word}/"

# Get phonetic transcriptions
print("Fetching phonetic transcriptions from CMU dictionary...")
phonetics = []
for i, word in enumerate(words):
    print(f"Processing {i+1}/{len(words)}: {word}")
    phonetic = get_phonetic(word)
    phonetics.append(phonetic)

async def fetch_translations(ts):
    tr = Translator()
    return await tr.translate(ts, src='en', dest='zh-cn')

trans = asyncio.run(fetch_translations(words))
meanings = [t.text for t in trans]

total_words = len(words)
rows_per_column = (total_words + 2) // cols

# 表头
if cols == 3:
    md_lines = ["| No. | Word | Phonetic | Chinese | No. | Word | Phonetic | Chinese | No. | Word | Phonetic | Chinese |", 
                "|-----|------|----------|---------|-----|------|----------|---------|-----|------|----------|---------|"]
elif cols == 2:
    md_lines = ["| No. | Word | Phonetic | Chinese | No. | Word | Phonetic | Chinese |", 
                "|-----|------|----------|---------|-----|------|----------|---------|"]
elif cols == 1:
    md_lines = ["| No. | Word | Phonetic | Chinese |", 
                "|-----|------|----------|---------|"]

for row in range(rows_per_column):
    line_parts = []
    for col in range(cols):
        idx = row + col * rows_per_column
        if idx < total_words:
            line_parts.append(f"| {idx+1} | {words[idx]} | {phonetics[idx]} | {meanings[idx]} ")
        else:
            line_parts.append("| | | | ")
    md_lines.append("".join(line_parts) + "|")

with open(os.path.join(current_dir + "//md", md_name), "w", encoding="utf-8") as f:
    f.write("\n".join(md_lines))

print(f"Generated file: {md_name}")