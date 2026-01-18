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
A[Capture Screen] --> B[Gemini Vision Analysis]
B --> C{Is it Spam?}
C -->|No| D[Ignore / Scroll]
D --> A
C -->|Yes| E[Action: Tap & Open Email]
E --> F[Blind Scroll to Footer x4]
F --> G[Vision Search: Find Unsubscribe Link]
G --> H[Action: Click Link]
H --> I[Opens Chrome Browser]
I --> J[Vision Search: Find Confirm Button]
J --> K[Action: Click Confirm & Unsubscribe]
```
```


---
## 🏗️ Architecture Overview

| Component         | File         | Purpose                                         |
|-------------------|--------------|-------------------------------------------------|
| **Main Agent**    | `main.py`    | Core logic and workflow orchestration            |
| **AI Prompts**    | `prompts.py` | Structured prompts for Gemini/Groq vision        |
| **ADB Utilities** | `utils.py`   | Android device interaction helpers               |
| **Config**        | `.env`       | API keys and environment configuration           |

---
## 📁 Project Structure

| Path                | Description                       |
|---------------------|-----------------------------------|
| `main.py`           | Main agent script                 |
| `prompts.py`        | AI prompt configurations          |
| `utils.py`          | ADB utility functions             |
| `requirements.txt`  | Python dependencies               |
| `.env`              | Environment variables (create this)|
| `Agent-output/`     | Debug screenshots                 |
| `README.md`         | Project documentation             |

---
## 🎯 Targeted Email Sources

| Category                | Brands                        |
|-------------------------|-------------------------------|
| 🍕 **Food Delivery**    | Zomato, Swiggy                |
| 🛒 **E-Commerce**       | Flipkart                      |
| 📚 **Education**        | Coursera                      |
| 💼 **Social/Professional** | Facebook, LinkedIn         |

---
## 🛠️ Troubleshooting

| Issue                    | Solution                                         |
|--------------------------|--------------------------------------------------|
| `GEMINI_API_KEY missing!`| Ensure `.env` file exists with valid API key     |
| `No devices found`       | Enable USB Debugging and reconnect device        |
| `ADB Error`              | Restart ADB server: `adb kill-server && adb start-server` |
| `Rate limit (429)`       | Wait a few seconds; the agent auto-retries       |

---
## 🤝 Contributing

| Step | Action                                                      |
|------|-------------------------------------------------------------|
|  1   | 🍴 Fork the repository                                      |
|  2   | 🌿 Create a feature branch (`git checkout -b feature/amazing-feature`) |
|  3   | 💾 Commit changes (`git commit -m 'Add amazing feature'`)   |
|  4   | 📤 Push to branch (`git push origin feature/amazing-feature`)|
|  5   | 🔃 Open a Pull Request                                      |

---
## 📜 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---
## 👨‍💻 Author

<div align="center">

**Ashwin**

[![GitHub](https://img.shields.io/badge/GitHub-0011Ashwin-181717?style=for-the-badge&logo=github)](https://github.com/0011Ashwin)

</div>

---
<div align="center">

### ⭐ Star this repo if you found it helpful!

Made by Ashwin Mehta **Droidrun DevSprint 2026**

</div>

---

## 🚀 Installation

```bash
# Clone repository
git clone https://github.com/0011Ashwin/Declutter-Droid.git
cd Declutter-Droid

# Create virtual environment
python -m venv env
.\env\Scripts\activate  # Windows
source env/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt
```

---

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