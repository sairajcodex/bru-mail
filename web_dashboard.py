"""
Web Dashboard Server for Email Agent Reports
Automatically loads the latest JSON report and displays all sections
Includes LLM chat functionality
"""
import os
import json
from pathlib import Path
from flask import Flask, render_template, jsonify, request
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__, template_folder='templates', static_folder='static')

# Initialize LLM client for chat
llm_client = None
try:
    from config import (
        LLM_PROVIDER, OLLAMA_BASE_URL, OLLAMA_MODEL,
        GEMINI_API_KEY, GEMINI_MODEL
    )
    from llm_client import LLMClientFactory
    
    if LLM_PROVIDER != "none":
        llm_kwargs = {}
        if LLM_PROVIDER == "ollama":
            llm_kwargs = {
                "base_url": OLLAMA_BASE_URL,
                "model": OLLAMA_MODEL
            }
        elif LLM_PROVIDER == "gemini":
            if GEMINI_API_KEY:
                llm_kwargs = {
                    "api_key": GEMINI_API_KEY,
                    "model": GEMINI_MODEL
                }
        
        if llm_kwargs:
            try:
                llm_client = LLMClientFactory.create_client(LLM_PROVIDER, **llm_kwargs)
                logger.info(f"Chat LLM initialized: {LLM_PROVIDER}")
            except Exception as e:
                logger.warning(f"Failed to initialize LLM for chat: {e}")
except Exception as e:
    logger.warning(f"Could not initialize LLM client: {e}")

# Get reports directory from config
try:
    from config import REPORT_OUTPUT_DIR
    REPORTS_DIR = Path(REPORT_OUTPUT_DIR)
except:
    REPORTS_DIR = Path("reports")

REPORTS_DIR.mkdir(exist_ok=True)


def get_latest_report():
    """Get the most recent report file"""
    reports = sorted(REPORTS_DIR.glob("email_report_*.json"), reverse=True)
    if reports:
        return reports[0]
    return None


def load_report_data(file_path):
    """Load and parse report data"""
    if not file_path or not file_path.exists():
        return None
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except Exception as e:
        logger.error(f"Error loading report {file_path}: {e}")
        return None


@app.route('/')
def index():
    """Main dashboard - loads latest report automatically"""
    latest_report_file = get_latest_report()
    report_data = load_report_data(latest_report_file)
    
    if not report_data:
        # Return empty state
        return render_template('dashboard.html', 
                             report=None, 
                             filename=None,
                             has_data=False)
    
    # Get all reports for the sidebar
    all_reports = []
    for file in sorted(REPORTS_DIR.glob("email_report_*.json"), reverse=True):
        try:
            with open(file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                stats = data.get('statistics', {})
                all_reports.append({
                    'filename': file.name,
                    'timestamp': stats.get('timestamp', ''),
                    'total_emails': stats.get('total_emails', 0)
                })
        except:
            pass
    
    return render_template('dashboard.html', 
                         report=report_data,
                         filename=latest_report_file.name if latest_report_file else None,
                         all_reports=all_reports,
                         has_data=True)


@app.route('/api/latest')
def api_latest():
    """API endpoint to get latest report"""
    latest_report_file = get_latest_report()
    report_data = load_report_data(latest_report_file)
    
    if not report_data:
        return jsonify({'error': 'No reports found'}), 404
    
    return jsonify({
        'filename': latest_report_file.name,
        'data': report_data
    })


@app.route('/api/report/<filename>')
def api_report(filename):
    """API endpoint to get specific report"""
    file_path = REPORTS_DIR / filename
    if not file_path.exists() or not filename.endswith('.json'):
        return jsonify({'error': 'Report not found'}), 404
    
    report_data = load_report_data(file_path)
    if not report_data:
        return jsonify({'error': 'Error loading report'}), 500
    
    return jsonify({
        'filename': filename,
        'data': report_data
    })


@app.route('/refresh')
def refresh():
    """Refresh to get latest report"""
    return jsonify({'redirect': '/'})


@app.route('/api/chat', methods=['POST'])
def chat():
    """API endpoint for LLM chat"""
    try:
        data = request.json
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({'error': 'Message is required'}), 400
        
        if not llm_client:
            return jsonify({
                'error': 'LLM not available',
                'message': 'LLM provider is not configured or not available. Please check your .env configuration.'
            }), 503
        
        # Create a contextual prompt that includes email report info
        latest_report_file = get_latest_report()
        report_data = load_report_data(latest_report_file)
        
        context = ""
        if report_data:
            stats = report_data.get('statistics', {})
            context = f"\n\nCurrent Email Report Context:\n- Total emails processed: {stats.get('total_emails', 0)}\n- Categories: {', '.join(stats.get('category_counts', {}).keys())}\n- Unsubscribe links found: {stats.get('unique_unsubscribe_links', 0)}"
        
        # Create prompt
        prompt = f"""You are an AI assistant helping users with their email management dashboard. 
You can help users understand their email reports, categories, statistics, and answer questions about their emails.

User question: {user_message}{context}

Please provide a helpful, concise response."""
        
        # Generate response
        response = llm_client.generate(prompt, max_tokens=800)
        
        if not response:
            return jsonify({
                'error': 'No response from LLM',
                'message': 'The LLM did not generate a response. Please try again.'
            }), 500
        
        return jsonify({
            'success': True,
            'response': response.strip(),
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Chat error: {e}")
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500


@app.route('/api/chat/status')
def chat_status():
    """Check if chat is available"""
    try:
        from config import LLM_PROVIDER
        provider = LLM_PROVIDER if llm_client else 'none'
    except:
        provider = 'none'
    
    return jsonify({
        'available': llm_client is not None,
        'provider': provider
    })


if __name__ == '__main__':
    print("=" * 60)
    print("Email Agent Web Dashboard")
    print("=" * 60)
    
    latest = get_latest_report()
    if latest:
        print(f"Latest report: {latest.name}")
    else:
        print("No reports found. Run main.py first to generate reports.")
    
    print(f"\nReports directory: {REPORTS_DIR.absolute()}")
    print("\nStarting web server...")
    print("Open your browser and go to: http://localhost:5000")
    print("\nPress Ctrl+C to stop the server")
    print("=" * 60 + "\n")
    
    app.run(debug=True, host='127.0.0.1', port=5000)
