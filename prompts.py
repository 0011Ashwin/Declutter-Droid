# prompts.py
# ============================================
# DECLUTTER DROID - ROBUST EDITION
# "Strong Core Logic" - Never gives up!
# ============================================

# 1. STATE CHECKER: Where are we?
CHECK_STATE_PROMPT = """
Analyze this screen. Look at the Top Header (Action Bar).
Question: What folder or view are we in?
Options: 'Primary', 'Promotions', 'Social', 'Updates', 'Spam', 'Menu_Open', 'Unknown'.
Context:
- If you see a side menu covering the left, return 'Menu_Open'.
- If the top text says "Search in emails" and below it says "Promotions", return 'Promotions'.
- If the top label says "Primary", return 'Primary'.
Format: JSON {"state": "Promotions"} or {"state": "Menu_Open"}
"""

# 2. MENU NAVIGATOR: Find folder OR scroll
FIND_FOLDER_PROMPT = """
Analyze this Navigation Menu.
Goal: Find the 'Promotions' folder label.
Action: 
- If found: Return coordinates to TAP it.
- If NOT found (but menu is open): Return action "scroll_menu".
Format: JSON {"found": true, "point": [x, y]} OR {"found": false, "action": "scroll_menu"}
"""

# 3. AGGRESSIVE HUNTER: Find ANY click target
INBOX_SCAN_PROMPT = """
We are in the PROMOTIONS folder. EVERY row here is spam.
Goal: Find the first clickable email row.
Ignore: 'Top Picks' headers or 'Google Ads' if possible, but prioritize clicking ANY email subject.
Action: Return center [x, y] of the first email subject text.
Format: JSON {"action": "tap", "point": [x, y]}
If screen is completely empty/white, return {"action": "scroll"}.
"""

# 4. FOOTER SNIPER (Unsubscribe)
FIND_UNSUBSCRIBE_PROMPT = """
Analyze email footer. Find 'Unsubscribe', 'Opt-out', or 'Manage Preferences'.
It is tiny text at the very bottom.
Format: JSON {"found": true, "point": [x, y]}
If not found, return {"found": false}.
"""

# 5. BROWSER CONFIRM
BROWSER_CONFIRM_PROMPT = """
Mobile Browser. Find 'Confirm', 'Yes', 'Update', 'Remove' button.
Format: JSON {"found": true, "point": [x, y]}
If not found, return {"found": false}.
"""

# ============================================
# LEGACY PROMPTS (For backward compatibility)
# ============================================
SYSTEM_INSTRUCTION = INBOX_SCAN_PROMPT
OPEN_MENU_PROMPT = """
Find the hamburger menu (3 horizontal lines) in top-left.
Format: JSON {"found": true, "point": [x, y]}
"""
