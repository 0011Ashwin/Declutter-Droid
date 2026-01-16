import os
import io
import time
import json
import logging
import subprocess
import datetime
from dotenv import load_dotenv

import google.generativeai as genai
from PIL import Image

import utils
import prompts

# --- SETUP ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

# Create output folder for screenshots
OUTPUT_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Agent-output")
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

load_dotenv()
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    logger.error("❌ GEMINI_API_KEY missing!")
    exit(1)

genai.configure(api_key=GEMINI_API_KEY)
MODEL_NAME = "gemini-2.0-flash-exp" 

def get_screenshot_in_memory():
    """Captures screenshot to RAM."""
    try:
        result = subprocess.run(
            ["adb", "exec-out", "screencap", "-p"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        if result.returncode != 0: return None
        image_data = io.BytesIO(result.stdout)
        img = Image.open(image_data)
        
        ts = datetime.datetime.now().strftime("%H-%M-%S")
        img.save(os.path.join(OUTPUT_FOLDER, f"debug_view_{ts}.png"))
        return img
    except: return None

def ask_gemini(pil_image, prompt):
    """Robust Gemini Call handling Lists and Dicts."""
    model = genai.GenerativeModel(MODEL_NAME)
    for attempt in range(3):
        try:
            response = model.generate_content(
                [prompt, pil_image],
                generation_config={"response_mime_type": "application/json"}
            )
            data = json.loads(response.text)
            if isinstance(data, list):
                return data[0] if data else {"action": "none"}
            return data
        except Exception as e:
            if "429" in str(e):
                time.sleep(5)
            else:
                return {"action": "none"}
    return {"action": "none"}

def clean_inbox():
    logger.info("🚀 Declutter Droid 4.0 (Label Mode) Starting...")
    device = utils.get_device()
    if not device: return

    logger.info(f"📱 Connected: {device.serial}")
    utils.launch_app(device, "com.google.android.gm")

    for i in range(2): # Run 2 loops
        logger.info(f"\n--- Scan {i+1} ---")
        img = get_screenshot_in_memory()
        if not img: continue

        # 1. FIND EMAIL
        resp = ask_gemini(img, prompts.SYSTEM_INSTRUCTION)
        
        if resp.get("action") == "long_press":
            x, y = resp["location"]
            safe_x = x + 100 # Shift right to hit body
            logger.info(f"📍 Long Pressing at {safe_x}, {y}")
            utils.input_swipe(device, safe_x, y, safe_x, y, 1000)
            time.sleep(2)
            
            perform_cleanup(device)
        else:
            logger.info("⬇️ No target found. Scrolling...")
            utils.input_swipe(device, 500, 1500, 500, 500, 300)
            time.sleep(2)

def perform_cleanup(device):
    """
    SAMSUNG M11 FLOW:
    Three Dots -> Label as -> Marketing -> OK
    """
    logger.info("🧹 Labeling Sequence...")
    
    # 1. CLICK THREE DOTS (Top Right)
    # Hardcoded fallback for M11: x=660, y=140
    img = get_screenshot_in_memory()
    resp = ask_gemini(img, prompts.CLEANUP_STEP_1)
    point = resp.get("point")
    
    if point and point[1] < 300: # Valid top click
        utils.input_tap(device, point[0], point[1])
    else:
        logger.warning("⚠️ Using M11 Fallback for Menu")
        utils.input_tap(device, 660, 140)
    
    time.sleep(1.5)

    # 2. CLICK 'LABEL AS'
    logger.info("👀 Looking for 'Label as'...")
    img2 = get_screenshot_in_memory()
    resp2 = ask_gemini(img2, prompts.CLEANUP_STEP_2)
    p2 = resp2.get("point")
    
    if p2:
        utils.input_tap(device, p2[0], p2[1])
    else:
        # Fallback: 'Label as' is usually the 3rd item down
        logger.warning("⚠️ Blind tapping 3rd menu item")
        utils.input_tap(device, 450, 350) 
    
    time.sleep(1.5)

    # 3. SELECT 'MARKETING'
    logger.info("🏷️ Selecting 'Marketing' checkbox...")
    img3 = get_screenshot_in_memory()
    resp3 = ask_gemini(img3, prompts.CLEANUP_STEP_3)
    p3 = resp3.get("point")
    
    if p3:
        utils.input_tap(device, p3[0], p3[1])
    else:
        logger.warning("⚠️ Blind tapping Marketing (Approx location)")
        utils.input_tap(device, 360, 600) # Middle screen guess
    
    time.sleep(1.0)

    # 4. CLICK 'OK'
    logger.info("✅ Confirming (OK)...")
    img4 = get_screenshot_in_memory()
    resp4 = ask_gemini(img4, prompts.CLEANUP_STEP_4)
    p4 = resp4.get("point")
    
    if p4:
        utils.input_tap(device, p4[0], p4[1])
    else:
        # Fallback OK button usually bottom right of dialog
        utils.input_tap(device, 600, 900)
    
    logger.info("🎉 DONE!")
    time.sleep(2)

if __name__ == "__main__":
    clean_inbox()