# Declutter Droid

An AI-powered agent to clean up your Gmail inbox using Gemini and ADB.

## Prerequisites

- Python 3.9+
- Android device connected via ADB (Developer options enabled)
- Gemini API Key

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Configure environment:
   - Create a `.env` file from the template.
   - Add your `GEMINI_API_KEY`.

3. Connect your Android device via USB/Wireless debugging.
   ```bash
   adb devices
   ```

## Usage

Run the main script:
```bash
python main.py
```

The script will:
1. Open Gmail.
2. Scan for emails from Zomato, Swiggy, or Flipkart.
3. Long-press to select.
4. Move them to the "Marketing" label.
