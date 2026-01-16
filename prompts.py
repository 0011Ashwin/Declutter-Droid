# prompts.py

# 1. FINDING THE EMAIL (Standard)
SYSTEM_INSTRUCTION = """
Analyze this Gmail Inbox.
Goal: Find a marketing/spam email row to SELECT.
Priority: 'Coursera', 'Zomato', 'Swiggy', 'Flipkart', 'Facebook', 'LinkedIn'.
If none, pick the FIRST email row.

CRITICAL:
- To select, LONG PRESS the email text center.
- IGNORE the left sidebar menu icon (3 lines).
- IGNORE the search bar.

Output JSON: {"action": "long_press", "location": [x, y]}
"""

# 2. FINDING THE MENU (After Selection)
CLEANUP_STEP_1 = """
The user has selected an email. Look at the TOP RIGHT corner.
Find the 'Three Dots' menu button (Vertical Ellipsis).
Return JSON: {"point": [x, y]}
"""

# 3. FINDING 'LABEL AS' (Inside the Menu)
CLEANUP_STEP_2 = """
We are in a popup menu.
Find the text 'Label as'.
Return JSON: {"point": [x, y]}
"""

# 4. SELECTING LABEL & CONFIRMING (The Checkbox Flow)
CLEANUP_STEP_3 = """
We are in the 'Label as' dialog.
Task 1: Find the text 'Marketing' and tap its CHECKBOX.
Task 2: If 'Marketing' is already checked, find 'OK'.
Output JSON: {"point": [x, y], "action": "tap_marketing_or_ok"}
"""

# 5. FINAL CONFIRMATION
CLEANUP_STEP_4 = """
Find the text 'OK' or 'Done' button to close the dialog.
Output JSON: {"point": [x, y]}
"""