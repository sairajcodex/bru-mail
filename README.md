# 📧 Email Agent - AI-Powered Email Management

An intelligent email management agent that processes your inbox using **free/open-source LLM alternatives**. The agent categorizes emails, extracts unsubscribe links, generates AI summaries, and provides an interactive web dashboard with chat functionality.

## ✨ Features

- ✅ **IMAP Email Fetching** - Connect to any IMAP email server (Gmail, Outlook, etc.)
- ✅ **Unsubscribe Link Extraction** - Automatically finds unsubscribe links using regex
- ✅ **Smart Categorization** - Hybrid approach: rules-based first, LLM fallback for out-of-vocabulary
- ✅ **Email Summarization** - AI-powered summaries of important emails
- ✅ **Web Dashboard** - Beautiful HTML interface with statistics, summaries, and filters
- ✅ **AI Chat Assistant** - Interactive chat to ask questions about your emails
- ✅ **Multiple Report Formats** - JSON, CSV, or TXT reports
- ✅ **Free LLM Options** - Uses Ollama (local) or Gemini (free tier) instead of paid APIs

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- IMAP access to your email account
- For LLM features: Ollama (recommended) or Gemini API key

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd lama
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   # Copy the example file
   cp .env.example .env
   
   # Edit .env with your credentials (see Configuration section)
   ```

4. **Set up Ollama (if using for LLM)**
   - Download from https://ollama.ai
   - Install and run Ollama
   - Pull a model:
     ```bash
     ollama pull llama3.2
     ```

5. **For Gmail users - Create App Password**
   - Go to Google Account → Security
   - Enable 2-Step Verification (if not already)
   - Under "2-Step Verification" → "App passwords"
   - Generate password for "Mail"
   - Use this password in `.env`, **NOT** your regular Gmail password

### Configuration

Edit the `.env` file with your settings:

```env
# Email Configuration
EMAIL_USERNAME=your_email@gmail.com
EMAIL_PASSWORD=your_app_password  # Use App Password for Gmail!

# LLM Provider (ollama, gemini, or none)
LLM_PROVIDER=ollama

# If using Ollama
OLLAMA_MODEL=llama3.2

# If using Gemini (optional)
GEMINI_API_KEY=your_api_key_here
```

## 📖 Usage

### Generate Email Reports

Process your emails and generate reports:

```bash
python main.py
```

This will:
1. Connect to your email server
2. Fetch recent emails
3. Extract unsubscribe links
4. Categorize emails (Work, Promotions, Social, News, Other)
5. Generate AI summaries
6. Create a report in the `reports/` directory

### View Web Dashboard

Launch the interactive web dashboard:

```bash
python web_dashboard.py
```

Then open your browser to: **http://localhost:5000**

**Dashboard Features:**
- 📊 Statistics overview
- 📈 Category breakdown with visual charts
- 📬 All emails with AI summaries
- 🔗 Unsubscribe links section
- 💬 **AI Chat Assistant** - Ask questions about your emails
- 🔍 Filter emails by category

### Using the AI Chat

1. Click the chat button (💬) in the bottom-right corner
2. Ask questions like:
   - "How many emails did I receive?"
   - "What are my email categories?"
   - "Explain my email statistics"
   - "Which emails have unsubscribe links?"

## 🔧 LLM Provider Options

### 1. Ollama (Recommended - Completely Free)

**Pros:**
- ✅ 100% free, no API keys
- ✅ Runs locally (private)
- ✅ No usage limits
- ✅ Works offline

**Setup:**
```bash
# Install Ollama from https://ollama.ai
ollama pull llama3.2
# Set in .env: LLM_PROVIDER=ollama
```

### 2. Google Gemini API (Free Tier)

**Pros:**
- ✅ Cloud-based (no local installation)
- ✅ Generous free tier (60 requests/minute)
- ✅ Easy setup

**Setup:**
1. Get API key: https://aistudio.google.com/app/apikey
2. Set in `.env`: `LLM_PROVIDER=gemini` and `GEMINI_API_KEY=your_key`

### 3. No LLM (Rules Only)

Set `LLM_PROVIDER=none` in `.env` to use only rule-based categorization (no AI summaries or chat).

## 📁 Project Structure

```
email-agent/
├── main.py                 # Main email processing script
├── web_dashboard.py        # Web dashboard server with chat
├── config.py               # Configuration management
├── email_fetcher.py       # IMAP email fetching
├── unsubscribe_extractor.py # Regex-based link extraction
├── email_categorizer.py   # Hybrid categorization
├── email_summarizer.py    # LLM-based summarization
├── llm_client.py         # LLM client (Ollama/Gemini)
├── report_generator.py   # Report generation
├── templates/
│   └── dashboard.html    # Web dashboard UI
├── requirements.txt      # Python dependencies
├── .env.example         # Environment template
└── README.md            # This file
```

## 🔐 Security & Privacy

- ✅ **Never commit `.env` file** - It's in `.gitignore`
- ✅ **Use App Passwords** - Never use your regular email password
- ✅ **Local Processing** - Emails are processed on your machine
- ✅ **Ollama Privacy** - With Ollama, all LLM processing is local

## 🐛 Troubleshooting

### Ollama Connection Issues

```bash
# Test if Ollama is running
ollama list

# If not running, start Ollama manually or restart computer
# Check if model is downloaded
ollama pull llama3.2
```

### Gmail IMAP Connection Failed

- ✅ Make sure you're using **App Password**, not regular password
- ✅ Enable IMAP in Gmail: Settings → Forwarding and POP/IMAP → Enable IMAP
- ✅ Ensure 2-Step Verification is enabled

### Gemini API Errors

- Check API key is correct
- Verify rate limits (free tier: 60 requests/minute)
- Ensure `google-generativeai` is installed: `pip install google-generativeai`

### Flask/Web Dashboard Not Working

```bash
# Install Flask
pip install flask

# Check if port 5000 is available
# Or modify web_dashboard.py to use a different port
```

## 📝 Environment Variables Reference

| Variable | Description | Default |
|----------|-------------|---------|
| `EMAIL_USERNAME` | Your email address | Required |
| `EMAIL_PASSWORD` | Email app password | Required |
| `IMAP_SERVER` | IMAP server address | `imap.gmail.com` |
| `LLM_PROVIDER` | LLM provider: `ollama`, `gemini`, or `none` | `ollama` |
| `OLLAMA_MODEL` | Ollama model name | `llama3.2` |
| `GEMINI_API_KEY` | Gemini API key (if using Gemini) | Optional |
| `MAX_EMAILS_TO_PROCESS` | Max emails to process per run | `50` |
| `REPORT_FORMAT` | Report format: `json`, `csv`, or `txt` | `json` |

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

- Built with free/open-source LLM alternatives
- Uses Ollama for local AI processing
- Google Gemini for cloud-based AI (free tier)

---

**⚠️ Important:** Never commit your `.env` file to version control. Always use `.env.example` as a template.

For issues or questions, please open an issue on GitHub.

