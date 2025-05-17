# 🐅 Bengals Daily Digest Generator

A Python-powered tool that automatically scrapes Cincinnati Bengals news from trusted sources, filters out unrelated NFL content, 
and uses a local Ollama LLM (e.g., LLaMA 4) to summarize each article into a fan-friendly daily digest.

---

## 📌 Features

- ✅ Pulls articles from multiple Bengals-related RSS feeds (Yahoo, USA Today, ESPN, Bengals.com, etc.)
- ✅ Filters only Bengals-relevant stories, even from general NFL feeds like ESPN
- ✅ Summarizes articles using your local Ollama installation (e.g., `llama4`, `mistral`, etc.)
- ✅ Outputs a clean Markdown digest with headlines, links, and summaries
- ✅ Tracks CPU and GPU usage per article during summarization
- ✅ Saves both date-stamped and “latest” versions of the digest to disk

---

## 🚀 How It Works

1. **Feeds**: The script parses a list of trusted RSS feeds for Bengals content.
2. **Filtering**: It applies keyword filtering and team exclusion to discard unrelated NFL stories (e.g., Jets or Cowboys).
3. **Summarizing**: Each article is summarized locally using an Ollama-compatible model like LLaMA 4, with a prompt tuned for Bengals fans.
4. **Markdown Output**: A formatted digest is generated in Markdown and saved to the `digests/` folder.

---

## 📂 Output

Your digest is saved to:

```
digests/
├── bengals_digest_llama4_latest.md
└── bengals_digest_llama4_YYYY-MM-DD.md
```

Each digest contains:

- ✅ Headline as a clickable link
- ✅ Short summary in PFT style (punchy, factual, no fluff)
- ✅ Timestamped performance metrics per article

---

## 🧠 Prompt Style

The summarization uses a carefully crafted prompt:

> “You are a Bengals beat writer crafting a short summary for a daily fan newsletter… written in the voice and tone of Mike Florio from ProFootballTalk: punchy, direct, occasionally snarky, but always fact-based…”

This ensures your summaries are **informative, no-nonsense, and tailored to Bengals fans**.

---

## 🧰 Requirements

- **Python 3.8+**
- **Local LLM via [Ollama](https://ollama.com/)** (e.g., `llama4`, `deepseek`, or `mistral`)
- Python packages:
- `feedparser`
- `beautifulsoup4`
- `psutil`
- `nvidia-ml-py3`

You can install the dependencies with:

```bash
pip install feedparser beautifulsoup4 psutil nvidia-ml-py3
```

---

## ⚙️ Configuration

### 🖥️ Model & Path

Edit these variables at the top of the script to match your system:

```python
OLLAMA_PATH = r"C:\Users\yourname\AppData\Local\Programs\Ollama\ollama.exe"
MODEL_NAME = "llama4:latest"
```

### 📰 RSS Feeds

You can add or remove feeds from the `BENGALS_FEEDS` list. ESPN and other general feeds are filtered to include only Bengals content.

---

## 🔍 Filtering Logic

To avoid irrelevant stories:

- Keeps only stories containing:
    - “bengals”, “cincinnati bengals”
    - Names like “joe burrow”, “ja'marr chase”, etc.
- Excludes stories that **only** mention other NFL teams, like:
    - `chiefs`, `eagles`, `jets`, etc. (full list of 31 non-Bengals teams)

---

## 📊 Performance Metrics

After summarization, the script prints and logs:

- CPU % before and after
- GPU % (if NVIDIA)
- Time per article
- Total processing time
- Output summary issues (timeouts, blank results, etc.)

---

## 🏁 Example Usage

Just run the script:

```bash
python bengals_digest.py
```

Then open the latest digest:

```bash
digests/bengals_digest_llama4_latest.md
```

---

## 🙋‍♂️ Author

This project was built as a way to **automate and summarize Bengals news** for podcast preparation, fan engagement, and personal use—without reading through 100 articles a day.
