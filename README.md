# Personal Care Product Analyzer

A Flask-based web application that evaluates personal care product ingredients and categorizes them as **Safe, Caution, or Harmful** based on predefined rules.

## Features
- Analyzes personal care product ingredients.
- Supports ingredient aliases and autocomplete.
- Allows users to select their skin type.
- Provides additional notes for sensitive skin.
- Uses a local SQLite database and works offline.

## Technologies
Python, Flask, SQLite, HTML, CSS, JavaScript, and Excel.

## Installation

1. Clone or download the project.
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Start the application:
   ```bash
   python app.py
   ```
5. Open `http://127.0.0.1:5001/` in your browser.

## Disclaimer
Ingredient classifications are based on the project's reference data and rules. They are for informational purposes only and do not replace professional medical or dermatological advice.
