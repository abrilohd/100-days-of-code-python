# Day 31 – Flash Card Project

A simple **Tkinter-based flash card app** to help learn French words with English translations.

## Features
- Random French word display
- Auto flip to English after 3 seconds
- Mark words as known or unknown
- Saves progress using CSV files
- Persistent learning state (`words_to_learn.csv`)

## Project Structure
Day_31_flash-card-project/
│
├── main.py
├── data/
│ ├── french_words.csv
│ └── words_to_learn.csv
└── images/
├── card_front.png
├── card_back.png
├── right.png
└── wrong.png


## How It Works
- Unknown  → next word
- Known  → word removed and saved
- App remembers remaining words between runs

## Requirements
- Python 3
- pandas
- tkinter (built-in)

## Run
```bash
python main.py
