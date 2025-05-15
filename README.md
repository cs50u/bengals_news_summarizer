# 🐅 Bengals News Summarizer

_Automated, LLM-powered curation and summarization of Cincinnati Bengals news._

![Bengals Logo](https://cdn.vox-cdn.com/community_logos/48495/cincyjungle_fave.png)

---

## Overview

**Bengals News Summarizer** is a Python-based tool for automatically collecting, summarizing, and curating the latest Cincinnati Bengals news from [Cincy Jungle](https://www.cincyjungle.com) and other sources. It uses large language models (LLMs) running locally via [Ollama](https://ollama.com/) to generate concise, readable digests in the style of ProFootballTalk’s Mike Florio—complete with wit, critical insight, and fan perspective.

The project is designed for **repeatable, robust, and customizable** content creation, suitable for newsletter authors, podcasters, or passionate fans.

---

## Features

- **Automated RSS fetching** from Cincy Jungle (and easily extensible for more sources)
- **HTML-to-text cleaning** for clean, model-friendly input
- **Local LLM summarization** (supports [Llama 3/4, Mistral, DeepSeek R1, etc.] via Ollama)
- **Style-tuned prompts** for Florio-like voice and critical Bengals coverage
- **Performance metrics:** Article-by-article timing, CPU, and GPU usage for benchmarking different models
- **Bulletproof error handling:** Skips blank/garbled summaries, flags failures in output
- **Markdown digest output:** Time-stamped and archived for each run, plus always-updated `latest` version
- **Extensible:** Easily add more sources or adjust prompts/models

---

## Example Output

🐅 Bengals News Digest – Florio Style (Ollama Edition)
The good, bad, and ugly from the Bengals’ official 2025 schedule
The Bengals' 2025 schedule is out, and it's a mixed bag. On the plus side, they open at Cleveland and host Jacksonville; on the minus, it's another year of primetime disrespect and a brutal three-week gauntlet in November.

...

yaml
Copy
Edit

---

## Installation & Setup

### 1. **Clone the Repo**

```bash
git clone https://github.com/cs50u/bengals_news_summarizer.git
cd bengals_news_summarizer
2. Set Up Your Python Environment
bash
Copy
Edit
python -m venv .venv
.venv\Scripts\activate   # Windows
# or
source .venv/bin/activate   # macOS/Linux
pip install -r requirements.txt
3. Install and Set Up Ollama
Download and install Ollama (Windows/Mac/Linux)

Pull your desired model (e.g., llama4:scout)

bash
Copy
Edit
ollama pull llama4:scout
4. Run the Script
bash
Copy
Edit
python cincy_jungle.py
Output is saved to digests/ as a time-stamped Markdown digest.

Usage
Change the model: Edit MODEL_NAME in the script (e.g., "llama4:scout", "llama3", "deepseek-r1:32b")

Adjust number of articles: Change the entries[:5] slice.

Add more sources: Add new RSS URLs and parsing logic as needed.

Testing
Unit and integration tests are provided using pytest:

bash
Copy
Edit
pytest
Requirements
Python 3.8+

Ollama (for running local LLMs)

feedparser

psutil

pynvml

beautifulsoup4

(Optional for testing): pytest

Credits
Cincy Jungle – News source

Ollama – Local LLM serving

Meta – Llama 3/4

Mistral AI

DeepSeek AI

BeautifulSoup

License
MIT License

Who Dey!

yaml
Copy
Edit

---

**This is 100% copy-paste safe** for your `README.md` in GitHub.  
Let me know if you want an even simpler version or a different project name
