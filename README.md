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

## 📁 Project Structure

```
email-agent/
├── main.py                 # Main email processing script
├── web_dashboard.py        # Web dashboard server with chat
├── config.py               # Configuration management
├── email_fetcher.py       # IMAP email fetching
├── unsubscribe_extractor.py # Regex-based link extraction
├── email_categorizer.py   # Hybrid categorization (rules + Ollama)
├── email_summarizer.py    # Ollama-based summarization
├── llm_client.py         # Ollama client
├── report_generator.py   # Report generation (JSON/CSV/TXT)
├── templates/
│   └── dashboard.html    # Web dashboard UI
├── requirements.txt      # Python dependencies
├── .env.example         # Environment template
└── README.md            # This file
```

## ⚙️ Configuration

### Environment Variables (`.env` file)

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `EMAIL_USERNAME` | Your email address | - | ✅ Yes |
| `EMAIL_PASSWORD` | Email app password | - | ✅ Yes |
| `IMAP_SERVER` | IMAP server address | `imap.gmail.com` | No |
| `IMAP_PORT` | IMAP port | `993` | No |
| `LLM_PROVIDER` | LLM provider | `ollama` | No |
| `OLLAMA_BASE_URL` | Ollama server URL | `http://localhost:11434` | No |
| `OLLAMA_MODEL` | Ollama model name | `llama3.2` | No |
| `MAX_EMAILS_TO_PROCESS` | Max emails per run | `50` | No |
| `SUMMARY_LIMIT` | Max chars for summarization | `1000` | No |
| `REPORT_FORMAT` | Report format | `json` | No |
| `REPORT_OUTPUT_DIR` | Reports folder | `reports` | No |

### Example `.env` Configuration

```env
# Email Configuration
EMAIL_USERNAME=your_email@gmail.com
EMAIL_PASSWORD=your_16_char_app_password

# Ollama Configuration
LLM_PROVIDER=ollama
OLLAMA_MODEL=llama3.2

# Processing Configuration
MAX_EMAILS_TO_PROCESS=50
REPORT_FORMAT=json
```

## 🔐 Security & Privacy

- ✅ **Never commit `.env` file** - It's in `.gitignore`
- ✅ **Use App Passwords** - Never use your regular email password
- ✅ **Local Processing** - Emails are processed on your machine
- ✅ **Ollama Privacy** - All LLM processing happens locally
- ✅ **No Data Leaves Your Machine** - Everything runs locally

## 🐛 Troubleshooting

### Ollama Not Working

**Issue:** "Cannot connect to Ollama"

**Solutions:**
```bash
# Check if Ollama is running
ollama list

# If not, start Ollama application manually
# Or restart your computer (Ollama auto-starts on boot)

# Check if model is downloaded
ollama pull llama3.2

# Test Ollama connection
curl http://localhost:11434/api/tags
```

### Gmail IMAP Connection Failed

**Issue:** "Failed to connect to IMAP server"

**Solutions:**
- ✅ Make sure you're using **App Password** (16 characters), not regular password
- ✅ Enable IMAP in Gmail: Settings → Forwarding and POP/IMAP → Enable IMAP
- ✅ Ensure 2-Step Verification is enabled
- ✅ Try generating a new App Password

### Flask/Dashboard Not Working

**Issue:** "ModuleNotFoundError: No module named 'flask'"

**Solution:**
```bash
pip install flask
```

**Issue:** "Port 5000 already in use"

**Solution:**
- Close other applications using port 5000
- Or modify `web_dashboard.py` line 239 to use different port:
  ```python
  app.run(debug=True, host='127.0.0.1', port=5001)
  ```

### Email Processing Errors

**Issue:** "No emails found"

**Solutions:**
- Check your email credentials in `.env`
- Verify IMAP is enabled for your email provider
- Check if your inbox has emails
- Try increasing `MAX_EMAILS_TO_PROCESS` in `.env`

## 📝 Common Questions

### How often should I run `main.py`?

Run it whenever you want to process new emails. Each run creates a new timestamped report, so old reports are preserved.

### Can I change the Ollama model?

Yes! Edit `.env`:
```env
OLLAMA_MODEL=mistral
```
Make sure you've downloaded the model first:
```bash
ollama pull mistral
```

### How do I process more emails?

Edit `.env`:
```env
MAX_EMAILS_TO_PROCESS=100
```

### Can I use this without Ollama?

Yes, but you'll lose AI features:
- Set `LLM_PROVIDER=none` in `.env`
- Rule-based categorization will still work
- No AI summaries or chat functionality

## 🤝 Contributing

Contributions welcome! Some ideas:
- Add more LLM providers (Hugging Face, LocalAI, etc.)
- Support for email filtering rules
- Auto-unsubscribe functionality
- Email archiving based on categories
- Enhanced dashboard features

## 📄 License

MIT License - Feel free to use and modify!

## 🙏 Acknowledgments

- Built with **Ollama** for free, local AI processing
- All processing happens on your machine - 100% private

---

**⚠️ Important:** Never commit your `.env` file to version control. Always use `.env.example` as a template.

**For issues or questions, please open an issue on GitHub.**
