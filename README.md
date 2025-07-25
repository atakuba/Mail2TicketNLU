# Mail2TicketNLU
Automating ticketing processes at NLU helpdesk

# 📬 Mail2TicketNLU - Email to Ticket Automation System

Mail2TicketNLU is an intelligent automation system designed for National Louis University tech support staff to streamline the conversion of email requests into structured IT support tickets. With built-in summarization, categorization, and UI-based automation, it reduces manual effort and boosts service efficiency.

---

## 🚀 Features

- 📥 Parses and processes email exports from Outlook CSV format.
- 🧠 Uses AI (OpenAI) to:
  - Summarize problem statements
  - Generate concise short descriptions
  - Identify categories, business services, and user contact info
- 📁 Outputs a structured Excel file ready for ticket submission
- 🧑‍💻 UI built with **Streamlit** for easy file upload and tech-user selection
- 🤖 Selenium-based automation script fills ServiceNow ticket form field-by-field
- ✅ Handles Shadow DOM elements and manual login flows
- 🧪 Includes Behave BDD test structure for future automation scenarios

---

## 🛠️ Tech Stack

**Frontend / UI:**
- Streamlit (Python)

**Backend & Automation:**
- Python (pandas, openpyxl, re, dotenv, etc.)
- OpenAI API
- Selenium (ChromeDriver)
- Behave (BDD Testing Framework)

**Excel & File Handling:**
- `openpyxl`, `csv`, and native `pandas` I/O

---

## 📂 Folder Structure

```bash
Mail2TicketNLU/
├── automation/                 # Selenium automation logic
│   ├── steps/                 # Behave step definitions
│   └── utils/                 # Driver and utility setup
├── core/                      # Email summarizer and Excel processor
├── pages/                     # Locators and form fields
├── features/                  # .feature files for BDD
├── ui/                        # Streamlit frontend
├── tests/                     # Testing structure (if applicable)
└── main.py                    # Entry point for processing & automation
🖥️ How to Run Locally
✅ Prerequisites
Python 3.8+

Chrome browser

Git

Virtualenv (optional)

ChromeDriver (auto-downloaded by script)

📦 Installation
git clone https://github.com/atakuba/Mail2TicketNLU.git
cd Mail2TicketNLU
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
🔑 Environment Setup
Create a .env file at the root with the following:

OPENAI_API_KEY=your-openai-key
▶️ Start the UI
cd ui
streamlit run app.py
🧪 Run Automation
Once emails are processed and Excel is generated:

cd automation
behave features/
You will be prompted to log in manually once per session.

📹 Demo

Demo video coming soon!

Update the list in:

utils/tech_list.py
📧 Processed Fields in Output
subject, body, description, short_description

user_first_name, user_last_name, user_email

business_service, category

to, date, time

🧠 AI Prompt Behavior
The system intelligently detects school emails (@nl.edu, @my.nl.edu) and uses personal ones if needed. It ensures names, categories, and summaries are clearly generated even from raw messy email threads.

🤝 Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

📫 Contact
Created by Atabek Kubanychbek uulu
Email: atakubanychbek@gmail.com
LinkedIn: linkedin.com/in/atakuba

📄 License
MIT License

