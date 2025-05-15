import subprocess
import feedparser
from datetime import datetime
import os
import time

# Path to your local Ollama executable
OLLAMA_PATH = r"C:\Users\ddavi\AppData\Local\Programs\Ollama\ollama.exe"
MODEL_NAME = "llama4:scout"  # Change to "deepseek-r1:32b", "mistral", etc. to compare

def summarize_with_ollama(text, model=MODEL_NAME):
    prompt = (
        "You are a sharp, no-nonsense Bengals news analyst in the style of ProFootballTalk's Mike Florio. "
        "Summarize the following article in exactly 2 sentences, highlighting the key details, contract drama, injuries, rumors, and controversial angles. "
        "Inject a touch of dry wit. Do not include your thought process or reasoning—write only the summary. Do not invent facts. Article:\n\n"
        f"{text.strip()}"
    )
    try:
        start = time.perf_counter()
        result = subprocess.run(
            [OLLAMA_PATH, "run", model],
            input=prompt.encode("utf-8"),
            capture_output=True,
            timeout=180
        )
        elapsed = time.perf_counter() - start
        return result.stdout.decode("utf-8").strip(), elapsed
    except subprocess.TimeoutExpired:
        return "[Summary failed: timeout]", 180

def main():
    # Parse the RSS feed for Bengals news articles
    feed = feedparser.parse("https://www.cincyjungle.com/rss/current")
    entries = feed.entries[:5]  # Only process the first 5 articles

    # Start building the Markdown digest
    digest = ["# 🐅 Bengals News Digest – Florio Style (Ollama Edition)\n"]

    # For performance tracking
    article_times = []
    overall_start = time.perf_counter()

    # Process each entry/article
    for idx, entry in enumerate(entries, 1):
        title = entry.title
        link = entry.link
        summary_input = f"{title}\n\n{entry.summary}"

        print(f"Summarizing article {idx}/{len(entries)}: {title}")

        summary, elapsed = summarize_with_ollama(summary_input, model=MODEL_NAME)

        print(f"Done summarizing article {idx}. Time: {elapsed:.2f} seconds.\n")

        digest.append(f"### [{title}]({link})\n")
        digest.append(f"> {summary}\n")
        article_times.append((title, elapsed))

    total_time = time.perf_counter() - overall_start

    # Ensure the digests folder exists
    os.makedirs("digests", exist_ok=True)
    now = datetime.now().strftime("%Y-%m-%d")
    safe_model_name = MODEL_NAME.replace(":", "_").replace("-", "_")
    filename = os.path.join("digests", f"bengals_digest_{safe_model_name}_{now}.md")
    latest_filename = os.path.join("digests", f"bengals_digest_{safe_model_name}_latest.md")

    # Save the final digest to a timestamped and latest Markdown file
    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(digest))

    with open(latest_filename, "w", encoding="utf-8") as f:
        f.write("\n".join(digest))

    print(f"\n✅ Digest saved to {filename}")
    print(f"✅ Latest digest also saved to {latest_filename}")

    # Print performance metrics
    print("\n--- Performance Metrics ---")
    for idx, (title, elapsed) in enumerate(article_times, 1):
        print(f"{idx}. {title[:50]}...  {elapsed:.2f} sec")
    print(f"\nTotal time for digest: {total_time:.2f} seconds")

if __name__ == "__main__":
    main()
