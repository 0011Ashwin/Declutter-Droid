<div align="center">

🤖 Declutter Droid

The Autonomous Digital Janitor for Android

<img src="Declutter-droid.png" alt="Droid AI Janitor" width="600"/>

Declutter Droid is an intelligent AI agent that achieves Inbox Zero by physically unsubscribing you from spam. Unlike standard filters that just label emails, this agent visually navigates your Android phone, finds hidden "Unsubscribe" links, and manages browser confirmations just like a human would.

Features •
Demo •
How It Works •
Installation •
Usage •
Tech Stack

</div>

🌟 Features

Feature

Description

🧹 Digital Janitor

actively removes spam by clicking "Unsubscribe" links, not just hiding them.

🧠 Hybrid Vision Intelligence

Uses Gemini 2.0 Flash for reasoning and Groq Llama 4 Scout for high-speed UI element detection.

📱 True Agentic Workflow

Navigates across apps (Gmail → Chrome → System UI) maintaining context throughout the task.

📉 Smart API Usage

Implements "Blind Scrolling" algorithms to navigate long emails without burning API credits.

🎯 Multi-Brand Support

Trained to detect marketing patterns from Zomato, Swiggy, Flipkart, Coursera, LinkedIn, and more.

🛡️ Privacy First

Runs locally on your device via ADB; no personal data is stored on external servers.

🎬 Demo

<div align="center">
<img src="demon_of_terminal.png" alt="Terminal Output Demo" width="700"/>
</div>

🎥 Watch the Full Demo Video on YouTube

⚙️ How It Works

The agent follows a human-like cognitive workflow to clean the inbox:

graph TD
  A[📸 Capture Screen] --> B[🧠 AI Vision Analysis]
  B --> C{Is it Spam?}
  
  C -->|No| D[⬇️ Ignore / Scroll]
  D --> A
  
  C -->|Yes| E[👆 Action: Tap & Open Email]
  E --> F[📉 Blind Scroll to Footer x4]
  
  F --> G[🔍 Vision Search: Find Unsubscribe Link]
  G --> H[🔗 Action: Click Link]
  
  H --> I[🌐 Opens Chrome Browser]
  I --> J[🧠 Vision Search: Find Confirm Button]
  J --> K[✅ Action: Click Confirm & Unsubscribe]


🏗️ Architecture

Component

Technology

Purpose

The Brain

Google Gemini 2.0 Flash

Decides what is on the screen and where to click.

The Eyes

Groq Llama 4 Scout

Rapid UI object detection (buttons, menus, links).

The Hands

ADB (Android Debug Bridge)

Executes physical taps, swipes, and text input.

The Logic

Python 3.11

Orchestrates the agent loop and error handling.

🚀 Installation

1️⃣ Clone the Repository

git clone [https://github.com/0011Ashwin/Declutter-Droid.git](https://github.com/0011Ashwin/Declutter-Droid.git)
cd Declutter-Droid


2️⃣ Install Dependencies

pip install -r requirements.txt


3️⃣ Configure API Keys

Create a .env file in the project root:

GEMINI_API_KEY=your_gemini_api_key_here
GROQ_API_KEY=your_groq_api_key_here


4️⃣ Connect Your Android Device

Enable USB Debugging on your phone and connect via USB.

adb devices
# Output should show: List of devices attached -> XXXXX device


💡 Usage

Run the agent in one of two modes:

Quick Demo Mode (Processes 3 emails)

python main.py demo


Full Clean Mode (Deep cleaning of Promotions folder)

python main.py full


📁 Project Structure

Declutter-Droid/
├── main.py           # 🧠 Core Agent Logic & Router
├── prompts.py        # 🗣️ AI System Instructions
├── utils.py          # 🛠️ ADB Helper Functions
├── requirements.txt  # 📦 Dependencies
├── .env              # 🔑 API Credentials
└── Agent-output/     # 📸 Debug Screenshots


🔧 Troubleshooting

Issue

Solution

GEMINI_API_KEY missing!

Ensure your .env file is created and saved correctly.

No devices found

Reconnect USB cable and verify USB Debugging is ON.

Rate limit (429)

The agent has built-in retry logic. Wait 30s and it will resume.

Unsubscribe not found

Some emails use images instead of text links. The agent will skip these safely.

📜 License

This project is licensed under the MIT License — see the LICENSE file for details.

<div align="center">

Built by Ashwin

🚀 Droidrun DevSprint 2026 • Track: B2C Productivity

</div>