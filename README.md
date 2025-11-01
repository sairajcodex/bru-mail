# 📧 Email Agent - AI-Powered Email Management

An intelligent email management agent that processes your inbox using **Ollama (local LLM)**. The agent categorizes emails, extracts unsubscribe links, generates AI summaries, and provides an interactive web dashboard with chat functionality.

## ✨ Features

- ✅ **IMAP Email Fetching** - Connect to any IMAP email server (Gmail, Outlook, etc.)
- ✅ **Unsubscribe Link Extraction** - Automatically finds unsubscribe links using regex
- ✅ **Smart Categorization** - Hybrid approach: rules-based first, LLM fallback for out-of-vocabulary
- ✅ **Email Summarization** - AI-powered summaries using Ollama
- ✅ **Web Dashboard** - Beautiful HTML interface with statistics, summaries, and filters
- ✅ **AI Chat Assistant** - Interactive chat powered by Ollama to ask questions about your emails
- ✅ **Multiple Report Formats** - JSON, CSV, or TXT reports
- ✅ **100% Free & Local** - Uses Ollama for completely free, local AI processing

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- IMAP access to your email account
- Ollama installed and running

### Step 1: Install Ollama

1. **Download and Install Ollama:**
   - Visit: https://ollama.ai
   - Download for your OS (Windows/Mac/Linux)
   - Install and run Ollama (usually auto-starts)

2. **Download a Model:**
   ```bash
   ollama pull llama3.2
   ```
   This downloads ~2GB. Alternative models:
   - `ollama pull mistral` (smaller, faster)
   - `ollama pull qwen2.5` (good alternative)

3. **Verify Installation:**
   ```bash
   ollama list
   ```
   Should show your downloaded model.

### Step 2: Clone and Install Project

```bash
# Clone repository
git clone <your-repo-url>
cd lama

# Install Python dependencies
pip install -r requirements.txt
```

### Step 3: Configure Email Access

1. **Copy environment template:**
   ```bash
   cp .env.example .env
   ```

2. **Edit `.env` file with your credentials:**
   ```env
   # Email Configuration
   EMAIL_USERNAME=your_email@gmail.com
   EMAIL_PASSWORD=your_app_password
   
   # LLM Provider - Use Ollama
   LLM_PROVIDER=ollama
   OLLAMA_MODEL=llama3.2
   ```

3. **For Gmail Users - Create App Password:**
   - Go to: https://myaccount.google.com/security
   - Enable **2-Step Verification** (if not already)
   - Go to: https://myaccount.google.com/apppasswords
   - Select "Mail" and your device
   - Generate and copy the 16-character password
   - Use this password in `.env` (NOT your regular Gmail password!)

### Step 4: Run the Project

#### Generate Email Reports

Process your emails and generate reports:

```bash
python main.py
```

This will:
1. Connect to your email server via IMAP
2. Fetch recent emails (default: last 50)
3. Extract unsubscribe links
4. Categorize emails (Work, Promotions, Social, News, Other)
5. Generate AI summaries using Ollama
6. Create a JSON report in `reports/` directory

#### View Web Dashboard

Launch the interactive web dashboard:

```bash
python web_dashboard.py
```

Then open your browser to: **http://localhost:5000**

**Dashboard Features:**
- 📊 Statistics overview (total emails, categories, unsubscribe links)
- 📈 Category breakdown with visual charts
- 📬 All emails with AI-generated summaries
- 🔗 Complete list of unsubscribe links
- 💬 **AI Chat Assistant** - Ask questions about your emails
- 🔍 Filter emails by category (Work, Promotions, Social, etc.)

#### Using the AI Chat

1. **Open the chat:**
   - Click the chat button (💬) in the bottom-right corner of the dashboard

2. **Ask questions:**
   - "How many emails did I receive?"
   - "What are my email categories?"
   - "Explain my email statistics"
   - "Which emails have unsubscribe links?"
   - "Summarize my email patterns"

3. **The chat uses Ollama** to provide intelligent responses about your email data.

## 📖 Detailed Usage

### Processing Emails

```bash
python main.py
```

**What happens:**
- Fetches your most recent emails
- Each email is categorized (rules first, then Ollama if needed)
- AI summaries are generated for all emails
- Unsubscribe links are extracted
- A report is saved to `reports/email_report_YYYYMMDD_HHMMSS.json`

**View the report:**
- Open the JSON file in `reports/` folder
- Or use the web dashboard to view it visually

### Viewing Dashboard

```bash
python web_dashboard.py
```

The dashboard:
- Automatically loads the **latest** report
- Shows all statistics and email data
- Provides interactive filtering
- Includes AI chat for questions

**To see new data:**
1. Run `python main.py` to generate a new report
2. Refresh the browser - dashboard loads the latest report automatically

### Chat Assistant Features

The AI chat assistant can:
- Answer questions about your email statistics
- Explain category breakdowns
- Help understand email patterns
- Provide insights about your inbox

All processing happens **locally** using Ollama - your data stays private!

## 📄 License

MIT License - Feel free to use and modify!


