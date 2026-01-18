# main.py
# ============================================
# DECLUTTER DROID - AI-POWERED DIGITAL JANITOR
# Pure AI Vision - No Hardcoded Fallbacks
# Gemini + Groq Llama 4 Scout Vision
# ============================================

import os
import io
import time
import json
import logging
import subprocess
import datetime
import base64
from dotenv import load_dotenv

import google.generativeai as genai
from PIL import Image

# Groq import
try:
    from groq import Groq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False

import utils

# --- SETUP ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

OUTPUT_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Agent-output")
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

load_dotenv()

# ============================================
# API CONFIGURATION
# ============================================
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    logger.info("✅ Gemini API configured")
else:
    logger.warning("⚠️ GEMINI_API_KEY missing")

GEMINI_MODEL = "gemini-2.0-flash-exp"

# Groq Setup with Llama 4 Scout (Vision model)
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
groq_client = None
if GROQ_API_KEY and GROQ_AVAILABLE:
    groq_client = Groq(api_key=GROQ_API_KEY)
    logger.info("✅ Groq API configured (Llama 4 Scout Vision)")
else:
    logger.warning("⚠️ GROQ_API_KEY missing or groq not installed")

# Working Groq Vision Models (Jan 2026)
GROQ_VISION_MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"
GROQ_VISION_BACKUP = "meta-llama/llama-4-maverick-17b-128e-instruct"

# ============================================
# DEVICE CONFIG - Samsung M11 (720x1600)
# ============================================
SCREEN_WIDTH = 720
SCREEN_HEIGHT = 1600

# ============================================
# SMART PROMPTS - AI THINKING
# ============================================
ANALYZE_SCREEN_PROMPT = """
You are analyzing a mobile phone screenshot. The screen is 720x1600 pixels.

TASK: Identify what app/screen is currently visible.

Look for:
1. App header/toolbar at top
2. Navigation elements (hamburger menu, back arrow)
3. Content type (email list, email content, browser, menu)

Return JSON:
{
    "app": "Gmail" or "Browser" or "Unknown",
    "screen_type": "inbox_list" or "email_open" or "side_menu" or "browser_page" or "other",
    "has_hamburger_menu": true/false,
    "hamburger_position": [x, y] or null,
    "folder_name": "Primary" or "Promotions" or "Social" or null,
    "thinking": "brief explanation of what you see"
}
"""

FIND_MENU_PROMPT = """
You are analyzing a Gmail mobile screenshot (720x1600 pixels).

TASK: Find the hamburger menu icon (☰ three horizontal lines).

It is typically:
- In the top-left corner of the screen
- Part of the app bar/toolbar
- A small icon with 3 horizontal lines

Return JSON:
{
    "found": true/false,
    "point": [x, y],
    "confidence": "high" or "medium" or "low",
    "thinking": "I see the hamburger menu at top-left..."
}
"""

FIND_FOLDER_PROMPT = """
You are analyzing Gmail's side navigation menu (720x1600 pixels).

TASK: Find the "Promotions" folder in the menu list.

Look for:
- Text saying "Promotions" with a tag/label icon
- It's usually below Primary, Social in the folder list
- May have an icon next to it

Return JSON:
{
    "found": true/false,
    "point": [x, y],
    "label": "Promotions",
    "thinking": "I can see the Promotions folder at..."
}

If Promotions is not visible, look for "Social" folder instead.
"""

FIND_EMAIL_PROMPT = """
You are analyzing Gmail's inbox/Promotions folder (720x1600 pixels).

TASK: Find a promotional email to click on.

Look for:
- Email rows with sender name, subject line, preview text
- Each email row spans most of the screen width
- The CLICKABLE area is the email subject/sender text (LEFT side)
- AVOID: Reply icons, star icons, checkboxes on the right side

Return JSON:
{
    "found": true/false,
    "point": [x, y],
    "email_subject": "brief subject text you see",
    "thinking": "I see an email from [sender] about [topic], clicking on subject area..."
}

IMPORTANT: Return coordinates for the EMAIL SUBJECT TEXT, not icons!
The subject text is usually x < 500 (left-center of screen).
"""

FIND_UNSUBSCRIBE_PROMPT = """
You are analyzing an open marketing email (720x1600 pixels).

TASK: Find ANY clickable "Unsubscribe" or "opt-out" link in the email.

Unsubscribe links appear as:
- Text: "Unsubscribe", "Opt out", "Opt-out", "Manage preferences", "Stop emails", "Email preferences", "Unsubscribe from this list", "Click here to unsubscribe"
- Usually small gray or blue text
- Often at the very BOTTOM of email content
- Sometimes in tiny footer text near "Privacy Policy"
- Can be underlined or hyperlinked text

ALSO LOOK FOR:
- "Manage your subscription"
- "Update email preferences" 
- "Remove from mailing list"
- Links with "unsub" in visible text

DO NOT CONFUSE WITH:
- Reply/Forward buttons (these are icons, not text links)
- Large colorful CTA buttons (Shop Now, Learn More, etc.)
- Floating compose button (FAB in corner)

Return JSON:
{
    "found": true/false,
    "point": [x, y],
    "link_text": "exact text you see",
    "thinking": "I found unsubscribe text at..."
}

If the unsubscribe link IS visible, return found:true with coordinates.
If truly NOT visible after careful search, return found:false.
"""

BROWSER_CONFIRM_PROMPT = """
You are analyzing a browser page (720x1600 pixels) - likely an unsubscribe confirmation page.

TASK: Find the confirmation button to complete unsubscribe.

Look for buttons/links with text like:
- "Unsubscribe"
- "Confirm"
- "Yes, unsubscribe"
- "Remove me"
- "Update preferences"
- Any button that confirms the action

Return JSON:
{
    "found": true/false,
    "point": [x, y],
    "button_text": "the button text",
    "thinking": "I see a confirm button saying..."
}
"""

# ============================================
# SCREENSHOT UTILITY
# ============================================
def get_screenshot():
    """Capture screenshot from device."""
    try:
        result = subprocess.run(
            ["adb", "exec-out", "screencap", "-p"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=10
        )
        if result.returncode != 0:
            return None
        image_data = io.BytesIO(result.stdout)
        img = Image.open(image_data)
        
        # Save debug copy
        ts = datetime.datetime.now().strftime("%H-%M-%S")
        img.save(os.path.join(OUTPUT_FOLDER, f"screen_{ts}.png"))
        return img
    except Exception as e:
        logger.error(f"Screenshot error: {e}")
        return None

def image_to_base64(pil_image):
    """Convert PIL image to base64."""
    buffered = io.BytesIO()
    # Resize for faster processing (max 1024 width)
    if pil_image.width > 1024:
        ratio = 1024 / pil_image.width
        new_size = (1024, int(pil_image.height * ratio))
        pil_image = pil_image.resize(new_size, Image.LANCZOS)
    pil_image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")

# ============================================
# GROQ VISION API - LLAMA 4 SCOUT
# ============================================
def ask_groq_vision(pil_image, prompt, model=None):
    """
    Call Groq's Llama 4 Scout Vision model.
    This is the primary AI for screen analysis.
    """
    if not groq_client or not pil_image:
        return None
    
    if model is None:
        model = GROQ_VISION_MODEL
    
    base64_img = image_to_base64(pil_image)
    
    try:
        response = groq_client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{base64_img}"
                            }
                        }
                    ]
                }
            ],
            response_format={"type": "json_object"},
            temperature=0.1,
            max_tokens=500
        )
        
        text = response.choices[0].message.content.strip()
        data = json.loads(text)
        
        # Log AI thinking
        if "thinking" in data:
            logger.info(f"🧠 AI: {data['thinking']}")
        
        return data
        
    except json.JSONDecodeError as e:
        logger.warning(f"⚠️ JSON parse error: {e}")
        return None
    except Exception as e:
        error_str = str(e)
        if "429" in error_str or "rate" in error_str.lower():
            logger.warning("⏳ Groq rate limited, waiting...")
            time.sleep(5)
            return None
        logger.warning(f"⚠️ Groq error: {e}")
        # Try backup model
        if model == GROQ_VISION_MODEL:
            logger.info("🔄 Trying backup model...")
            return ask_groq_vision(pil_image, prompt, GROQ_VISION_BACKUP)
        return None

# ============================================
# GEMINI VISION API
# ============================================
def ask_gemini_vision(pil_image, prompt):
    """Call Gemini for vision analysis."""
    if not pil_image or not GEMINI_API_KEY:
        return None
    
    try:
        model = genai.GenerativeModel(GEMINI_MODEL)
        response = model.generate_content(
            [prompt, pil_image],
            generation_config={"response_mime_type": "application/json"}
        )
        data = json.loads(response.text)
        
        if "thinking" in data:
            logger.info(f"🤖 Gemini: {data['thinking']}")
        
        return data
    except Exception as e:
        error_str = str(e)
        if "429" in error_str or "ResourceExhausted" in error_str:
            logger.warning("⏳ Gemini rate limited")
            return None
        logger.warning(f"⚠️ Gemini error: {e}")
        return None

# ============================================
# SMART AI ROUTER
# ============================================
def analyze_screen(pil_image, prompt):
    """
    Smart AI routing: Try Groq first (Llama 4 Scout), then Gemini.
    Returns analysis result or None.
    """
    # Try Groq Llama 4 Scout (best for vision)
    if groq_client:
        result = ask_groq_vision(pil_image, prompt)
        if result:
            return result
    
    # Fallback to Gemini
    if GEMINI_API_KEY:
        logger.info("🔄 Switching to Gemini...")
        result = ask_gemini_vision(pil_image, prompt)
        if result:
            return result
    
    return None

# ============================================
# NAVIGATION ACTIONS
# ============================================
def open_hamburger_menu(device):
    """Find and tap hamburger menu using AI."""
    logger.info("📂 Finding hamburger menu...")
    
    for attempt in range(3):
        img = get_screenshot()
        if not img:
            time.sleep(1)
            continue
            
        result = analyze_screen(img, FIND_MENU_PROMPT)
        
        if result and result.get("found") and result.get("point"):
            pt = result["point"]
            confidence = result.get("confidence", "medium")
            logger.info(f"✅ Found menu at {pt} (confidence: {confidence})")
            utils.input_tap(device, pt[0], pt[1])
            time.sleep(1.5)
            return True
        
        logger.info(f"🔄 Attempt {attempt+1}: Menu not found, retrying...")
        time.sleep(1)
    
    logger.error("❌ Could not find hamburger menu")
    return False

def navigate_to_promotions(device):
    """Navigate to Promotions folder using AI."""
    logger.info("📂 Navigating to Promotions...")
    
    # First open the menu
    if not open_hamburger_menu(device):
        return False
    
    time.sleep(1)
    
    # Find Promotions folder
    for attempt in range(3):
        img = get_screenshot()
        if not img:
            time.sleep(1)
            continue
            
        result = analyze_screen(img, FIND_FOLDER_PROMPT)
        
        if result and result.get("found") and result.get("point"):
            pt = result["point"]
            label = result.get("label", "Promotions")
            logger.info(f"✅ Found {label} at {pt}")
            utils.input_tap(device, pt[0], pt[1])
            time.sleep(2)
            return True
        
        # Maybe need to scroll the menu
        logger.info("🔄 Scrolling menu to find Promotions...")
        utils.input_swipe(device, 360, 800, 360, 400, 300)
        time.sleep(1)
    
    logger.error("❌ Could not find Promotions folder")
    return False

def scroll_to_footer(device):
    """Scroll down to reach email footer where unsubscribe lives."""
    logger.info("📉 Scrolling to email footer...")
    
    # Marketing emails are long - scroll multiple times
    for i in range(10):  # More scrolls to reach bottom
        utils.input_swipe(device, 360, 1300, 360, 400, 100)
        time.sleep(0.15)
    
    time.sleep(0.5)
    logger.info("✅ Reached footer area")

def return_to_inbox(device):
    """Return to inbox by pressing back."""
    logger.info("🔙 Returning to inbox...")
    for _ in range(4):
        utils.press_back(device)
        time.sleep(0.6)
    time.sleep(1)

# ============================================
# EMAIL PROCESSING WITH AI
# ============================================
def find_and_open_email(device):
    """Use AI to find and open a promotional email."""
    logger.info("👀 Looking for email to open...")
    
    for attempt in range(3):
        img = get_screenshot()
        if not img:
            time.sleep(1)
            continue
            
        result = analyze_screen(img, FIND_EMAIL_PROMPT)
        
        if result and result.get("found") and result.get("point"):
            pt = result["point"]
            subject = result.get("email_subject", "email")
            logger.info(f"✅ Found email: '{subject}' at {pt}")
            
            # Validate point is in safe zone (not on icons)
            if pt[0] > 600:
                logger.warning("⚠️ Point too far right (icon zone), adjusting...")
                pt[0] = 300  # Move to center-left
            
            utils.input_tap(device, pt[0], pt[1])
            time.sleep(2.5)
            return True
        
        # Scroll inbox to find more emails
        logger.info("🔄 Scrolling inbox to find emails...")
        utils.input_swipe(device, 360, 800, 360, 500, 300)
        time.sleep(1)
    
    logger.error("❌ Could not find email to open")
    return False

def find_unsubscribe(device):
    """Use AI to find and click unsubscribe link."""
    logger.info("🔗 Looking for Unsubscribe link...")
    
    # First scroll to footer
    scroll_to_footer(device)
    
    for attempt in range(3):
        img = get_screenshot()
        if not img:
            time.sleep(1)
            continue
            
        result = analyze_screen(img, FIND_UNSUBSCRIBE_PROMPT)
        
        if result and result.get("found") and result.get("point"):
            pt = result["point"]
            link_text = result.get("link_text", "Unsubscribe")
            logger.info(f"✅ Found '{link_text}' at {pt}")
            utils.input_tap(device, pt[0], pt[1])
            time.sleep(3)
            return True
        
        # Scroll a bit more
        logger.info("🔄 Scrolling more to find unsubscribe...")
        utils.input_swipe(device, 360, 1200, 360, 600, 200)
        time.sleep(1)
    
    logger.warning("⚠️ Unsubscribe link not found")
    return False

def handle_browser_confirm(device):
    """Handle browser confirmation page using AI."""
    logger.info("🌐 Checking for browser confirmation...")
    time.sleep(2)  # Wait for page load
    
    img = get_screenshot()
    if not img:
        return False
        
    result = analyze_screen(img, BROWSER_CONFIRM_PROMPT)
    
    if result and result.get("found") and result.get("point"):
        pt = result["point"]
        btn_text = result.get("button_text", "Confirm")
        logger.info(f"✅ Found confirm button '{btn_text}' at {pt}")
        utils.input_tap(device, pt[0], pt[1])
        time.sleep(2)
        return True
    
    logger.info("ℹ️ No confirmation button found (may be auto-confirmed)")
    return True

# ============================================
# SINGLE EMAIL PROCESSING PIPELINE
# ============================================
def process_email(device, email_num):
    """Process one email: open → scroll → unsubscribe → confirm → return."""
    logger.info("")
    logger.info("=" * 50)
    logger.info(f"📧 PROCESSING EMAIL #{email_num}")
    logger.info("=" * 50)
    
    # Step 1: Find and open email
    if not find_and_open_email(device):
        logger.warning(f"⚠️ Could not open email #{email_num}, skipping...")
        return False
    
    # Step 2: Find and click unsubscribe
    if not find_unsubscribe(device):
        logger.warning(f"⚠️ No unsubscribe found in email #{email_num}")
        return_to_inbox(device)
        return False
    
    # Step 3: Handle browser confirmation
    handle_browser_confirm(device)
    
    # Step 4: Return to inbox
    return_to_inbox(device)
    
    logger.info(f"✅ Email #{email_num} processed!")
    return True

# ============================================
# FOLDER CLEANING
# ============================================
def clean_promotions(device, num_emails=4):
    """Clean promotional emails using AI vision."""
    logger.info("")
    logger.info("=" * 60)
    logger.info(f"🧹 CLEANING PROMOTIONS ({num_emails} emails)")
    logger.info("=" * 60)
    
    # Navigate to Promotions
    if not navigate_to_promotions(device):
        logger.error("❌ Failed to navigate to Promotions")
        return 0
    
    # Process emails
    success_count = 0
    for i in range(num_emails):
        if process_email(device, i + 1):
            success_count += 1
        time.sleep(1)
    
    logger.info(f"✅ Cleaned {success_count}/{num_emails} emails")
    return success_count

# ============================================
# MAIN MODES
# ============================================
def run_demo(device, num_emails=3):
    """Run demo mode."""
    logger.info("")
    logger.info("🎬" + "=" * 58)
    logger.info("🧹 DECLUTTER DROID - AI VISION MODE")
    logger.info("   Powered by Llama 4 Scout + Gemini")
    logger.info("🎬" + "=" * 58)
    
    # Launch Gmail
    logger.info("🚀 Launching Gmail...")
    utils.launch_app(device, "com.google.android.gm")
    time.sleep(4)
    
    # Clean Promotions
    cleaned = clean_promotions(device, num_emails)
    
    logger.info("")
    logger.info("🎬" + "=" * 58)
    logger.info(f"🏁 DEMO COMPLETE! Processed {cleaned} emails")
    logger.info("🎬" + "=" * 58)

def run_full_clean(device):
    """Run full cleaning mode."""
    logger.info("")
    logger.info("🎬" + "=" * 58)
    logger.info("🧹 DECLUTTER DROID - FULL CLEAN")
    logger.info("🎬" + "=" * 58)
    
    logger.info("🚀 Launching Gmail...")
    utils.launch_app(device, "com.google.android.gm")
    time.sleep(4)
    
    # Clean multiple folders
    total = 0
    total += clean_promotions(device, num_emails=5)
    
    logger.info("")
    logger.info("🎬" + "=" * 58)
    logger.info(f"🏁 FULL CLEAN COMPLETE! Total: {total} emails")
    logger.info("🎬" + "=" * 58)

# ============================================
# MAIN ENTRY POINT
# ============================================
if __name__ == "__main__":
    import sys
    
    # Check APIs
    if not GEMINI_API_KEY and not groq_client:
        logger.error("❌ No AI API configured!")
        logger.info("💡 Add GEMINI_API_KEY or GROQ_API_KEY to .env file")
        exit(1)
    
    # Connect to device
    device = utils.get_device()
    if not device:
        logger.error("❌ No device connected!")
        logger.info("💡 Run: adb devices")
        exit(1)
    
    logger.info(f"📱 Connected: {device.serial}")
    
    # Parse arguments
    if len(sys.argv) > 1:
        mode = sys.argv[1].lower()
        if mode == "demo" or mode == "quick":
            run_demo(device, 3)
        elif mode == "full":
            run_full_clean(device)
        else:
            run_demo(device, 3)
    else:
        print("\n🧹 DECLUTTER DROID - AI VISION")
        print("=" * 40)
        print("Usage: python main.py [mode]")
        print("")
        print("Modes:")
        print("  demo  - Process 3 emails")
        print("  full  - Full clean (5 emails)")
        print("=" * 40)
        print("\nRunning demo...\n")
        run_demo(device, 3)
