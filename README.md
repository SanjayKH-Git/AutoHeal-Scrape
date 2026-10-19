# AutoHeal Scraper 🤖

An intelligent web scraper that **automatically repairs broken CSS selectors** when websites change their HTML structure. Uses AI (Google Gemini) to intelligently detect and fix selector failures without manual intervention.

> ⚠️ **Demo Project** — This is a proof-of-concept demonstrating an innovative approach to solving the web scraping problem. The strategy shown here can be applied to adapt dynamically to websites that change their HTML structure and ambiguous selectors over time.

## 🎯 Overview

When websites frequently update their HTML structure, CSS selectors break and manual maintenance becomes a burden. **AutoHeal Scraper** solves this by:

1. **Detecting broken selectors** — When a CSS selector fails to match any elements
2. **Comparing old vs new HTML** — Using AI to understand what changed
3. **Generating new selectors** — Automatically finding the new CSS selector in the updated page
4. **Learning over time** — Caching successful selectors in SQLite for faster future extractions
5. **Self-healing** — No manual updates needed when websites change their structure
6. **Handling ambiguous websites** — Works with websites that frequently modify their HTML structure

## ✨ Key Features

- **AI-Powered Selector Repair** — Uses Google Generative AI (Gemini) to intelligently fix broken selectors
- **Automatic Fallback System** — Tries multiple known selectors before invoking AI healing
- **SQLite-Based Caching** — Stores working selectors and HTML snapshots for optimization
- **Validation Layer** — Verifies AI-suggested selectors against actual page HTML before saving
- **Web Dashboard** — Flask app to view original and updated page HTML
- **Priority-Based Selector Queue** — Recently successful selectors are tried first


## 🔄 How It Works

### Normal Operation (Selector Works)
```
Fetch Page → Parse HTML → Try CSS Selectors → Match Found → Extract & Cache → Done
```

### Self-Healing Flow (Selector Broken)
```
Fetch Page → Parse HTML → Try CSS Selectors → All Failed 
  → Trigger AI Healing
    → Send Old HTML + New HTML to Gemini
    → Gemini analyzes structure changes
    → Generate new CSS selector
    → Validate selector against actual page
    → Store working selector in SQLite
  → Extract price with new selector
```

## 📋 Prerequisites

- **Python 3.8+**
- **Google Generative AI API Key** (free tier available at [ai.google.dev](https://ai.google.dev))
- **Internet connection** (for API calls)

## 🚀 Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd AutoHeal-Scrape
```

### 2. Create Virtual Environment
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```bash
cp example.env .env
```

Edit `.env` with your configuration:

```bash
# Google Generative AI API Key (required)
GOOGLE_API_KEY=your-google-api-key-here

# Optional API keys for future LLM provider support
OPENAI_API_KEY=
ANTHROPIC_API_KEY=

# LLM Provider
LLM_PROVIDER=gemini

# Target URLs
ORIGINAL_URL=http://127.0.0.1:5000
UPDATED_URL=http://127.0.0.1:5000/updated
```

**Get your free Google API key:** [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)

**Security:** Never commit `.env` to version control. Use `example.env` as a template for new developers.

## ⚙️ Configuration

### Environment Variables (.env)

All configuration is managed via environment variables loaded from `.env`:

| Variable | Default | Purpose |
|----------|---------|----------|
| `GOOGLE_API_KEY` | Required | API key for Google Generative AI |
| `OPENAI_API_KEY` | | Optional: For future OpenAI support |
| `ANTHROPIC_API_KEY` | | Optional: For future Anthropic support |
| `LLM_PROVIDER` | `gemini` | Current AI provider: `'gemini'` |
| `ORIGINAL_URL` | `http://127.0.0.1:5000` | Target website for scraping |
| `UPDATED_URL` | `http://127.0.0.1:5000/updated` | Alternative URL to test selector healing |

### Default CSS Selector

Edit the default selector in [utils.py](autoheal_scraper/utils.py):

```python
DEFAULT_SELECTOR = {"type": "css", "value": "div.price"}
```
## Usage
### Run the Flask Web Dashboard
```bash
python app.py
```

Visit `http://localhost:5000` to view:
- **`/`** — Original page HTML
- **`/updated`** — Updated page HTML (for debugging selector changes)
### Run the Scraper
```bash
python autoheal_scraper/main.py
```

This will:
1. Fetch the page from `ORIGINAL_URL`
2. Extract price using CSS selectors
3. Fetch the page from `UPDATED_URL`
4. Auto-heal if selectors are broken
5. Extract and print the result


## 🧠 The Self-Healing Algorithm

### 1. **Selector Discovery Phase**
- Load all known selectors from SQLite (prioritized by recency)
- Try each selector against the page HTML
- If any matches, extract the content and return

### 2. **Healing Phase** (when all selectors fail)
- Fetch the last known working HTML from SQLite
- Send to Gemini with context about what the selectors were looking for
- Gemini analyzes structural differences and suggests a new selector

### 3. **Validation Phase** (critical for reliability)
- Test the AI-suggested selector against the actual page
- Only save it if it successfully matches an element
- Never save unvalidated selectors

### 4. **Storage Phase**
- Add new selector to SQLite with highest priority
- Save current page HTML as reference for future comparisons
- Return the extracted content

## 📦 Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `Flask` | ≥3.1.0 | Web dashboard |
| `requests` | ≥2.31.0 | HTTP requests |
| `beautifulsoup4` | ≥4.13.0 | HTML parsing |
| `google-generativeai` | ≥0.8.6 | AI healing engine |
| `python-dotenv` | ≥1.0.0 | Environment variable management |

## Project Structure

```
autoheal_scraper/
├── __init__.py           # Package initialization
├── config.py             # Configuration constants
├── fetcher.py            # HTTP fetching 
├── parser.py             # Selector extraction 
├── healer.py             # AI healing engine 
├── llm_client.py         # Gemini API client 
└── utils.py              # SQLite storage layer 
```

## Key Concepts

### CSS Selectors Priority Queue
Successful selectors are stored in SQLite with insertion at position 0, so:
- Most recently working selectors are tried first
- Reduces API calls and improves performance
- Automatically learns from successful extractions

### HTML Snapshots
The system caches the last successful page HTML, enabling:
- AI to compare old vs new structure
- Understanding what changed between versions
- Better context for generating new selectors

### Validation Before Storage
Never blindly trusts AI suggestions:
- Validates selector against actual page HTML
- Only saves if element matches
- Falls back gracefully if validation fails

## 🤝 Contributing

This demo project demonstrates a novel strategy for handling websites with ambiguous or frequently-changing HTML structures. Feel free to extend it with:

**Core Enhancements:**
- Support for XPath selectors in addition to CSS
- Additional LLM providers (OpenAI, Claude, etc.)
- Multi-element extraction (tables, lists, nested data)
- Retry logic for transient failures
- Metrics & monitoring dashboard

**Strategy Applications:**
- Apply this self-healing approach to other dynamic data extraction tasks
- Extend to handle API endpoints that change their response structure
- Build adaptive data pipelines that learn from structural changes
- Use for maintaining scraping workflows across website redesigns


## 🔗 Resources

- [Google Generative AI Guide](https://ai.google.dev/docs)
- [BeautifulSoup Documentation](https://www.crummy.com/software/BeautifulSoup/)
- [CSS Selectors Reference](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Selectors)

---

**Made with ❤️ for intelligent, self-healing web scraping**

*This demo project showcases how AI can solve the web scraping maintenance problem by automatically adapting to website changes.*
