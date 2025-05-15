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

