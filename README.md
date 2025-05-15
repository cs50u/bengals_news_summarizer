# 🐅 Bengals News Summarizer

_Automated, LLM-powered curation and summarization of Cincinnati Bengals news._

![Bengals Logo](https://cdn.vox-cdn.com/community_logos/48495/cincyjungle_fave.png)

---

## Overview

**Bengals News Summarizer** is a Python-based tool for automatically collecting, summarizing, and curating the latest Cincinnati Bengals news from [Cincy Jungle](https://www.cincyjungle.com) and other sources. It uses large language models (LLMs) running locally via [Ollama](https://ollama.com/) to generate concise, readable digests that are insightful, concise, and occasionally witty—written for Bengals fans who want the real story.

The project is designed for **repeatable, robust, and customizable** content creation, suitable for newsletter authors, podcasters, or passionate fans.

---

## Features

- **Automated RSS fetching** from Cincy Jungle (easily extensible for more sources)
- **HTML-to-text cleaning** for clean, model-friendly input
- **Local LLM summarization** (supports Llama 3/4, Mistral, DeepSeek R1, etc. via Ollama)
- **Style-tuned prompts** for direct, critical, and occasionally witty Bengals coverage
- **Performance metrics:** Article-by-article timing, CPU, and GPU usage for benchmarking
- **Bulletproof error handling:** Skips blank/garbled summaries, flags failures in output
- **Markdown digest output:** Time-stamped and archived for each run, plus always-updated `latest` version
- **Extensible:** Easily add more sources or adjust prompts/models

---

## Example Output

    # 🐅 Bengals News Digest – LLM Edition

    ### [The good, bad, and ugly from the Bengals’ official 2025 schedule](...)
    > The Bengals' 2025 schedule is out, and it's a mixed bag. On the plus side, they open at Cleveland and host Jacksonville; on the minus, it's another year of primetime disrespect and a brutal three-week gauntlet in November.

    ...

---

## Installation & Setup

### 1. Clone the Repo

    git clone https://github.com/cs50u/bengals_news_summarizer.git
    cd bengals_news_summarizer

### 2. Set Up Your Python Environment

    python -m venv .venv
    .venv\Scripts\activate   # Windows
    # or
    source .venv/bin/activate   # macOS/Linux
    pip install -r requirements.txt

### 3. Install and Set Up Ollama

- [Download and install Ollama](https://ollama.com/download) (Windows/Mac/Linux)
- Pull your desired model (for example, llama4:scout):

        ollama pull llama4:scout

### 4. Run the Script

        python cincy_jungle.py

- Output is saved to `digests/` as a time-stamped Markdown digest.

---

## Usage

- **Change the model:** Edit `MODEL_NAME` in the script (e.g., `"llama4:scout"`, `"llama3"`, `"deepseek-r1:32b"`)
- **Adjust number of articles:** Change the `entries[:5]` slice in the script.
- **Add more sources:** Add new RSS URLs and parsing logic as needed.

---

## Testing

Unit and integration tests are provided using [pytest](https://docs.pytest.org/):

    pytest

---

## Requirements

- Python 3.8+
- [Ollama](https://ollama.com/) (for running local LLMs)
- [feedparser](https://pypi.org/project/feedparser/)
- [psutil](https://pypi.org/project/psutil/)
- [pynvml](https://pypi.org/project/pynvml/)
- [beautifulsoup4](https://pypi.org/project/beautifulsoup4/)
- (Optional for testing): [pytest](https://pypi.org/project/pytest/)

---

## Credits

- [Cincy Jungle](https://www.cincyjungle.com) – News source
- [Ollama](https://ollama.com) – Local LLM serving
- [Meta](https://ai.meta.com/llama/) – Llama 3/4
- [Mistral AI](https://mistral.ai/)
- [DeepSeek AI](https://deepseek.com/)
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)

---

## License

MIT License

---

_Who Dey!_
