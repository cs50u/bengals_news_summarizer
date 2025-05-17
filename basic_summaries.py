import subprocess
import feedparser

# Path to your local Ollama executable
OLLAMA_PATH = r"C:\Users\ddavi\AppData\Local\Programs\Ollama\ollama.exe"

def summarize_with_ollama(text):
    """
    Use Ollama to generate a summary of the provided text.
    Calls the deepseek-r1:32b model and limits summary to 2-3 sentences.
    Includes a timeout to prevent the script from hanging on slow/failed runs.
    """
    prompt = f"Summarize this Bengals article in 2-3 sentences:\n\n{text.strip()}"
    try:
        # Run the Ollama CLI command with the prompt as input
        result = subprocess.run(
            [OLLAMA_PATH, "run", "deepseek-r1:32b"],
            input=prompt.encode("utf-8"),
            capture_output=True,
            timeout=180  # Timeout in seconds (adjust as needed)
        )
        return result.stdout.decode("utf-8").strip()
    except subprocess.TimeoutExpired:
        return "[Summary failed: timeout]"

def main():
    # Parse the RSS feed for Bengals news articles
    feed = feedparser.parse("https://www.cincyjungle.com/rss/current")
    entries = feed.entries[:5]  # Only process the first 5 articles

    # Start building the Markdown digest
    digest = ["# 🐅 Bengals News Digest – Ollama Edition\n"]

    # Process each entry/article
    for idx, entry in enumerate(entries, 1):
        title = entry.title
        link = entry.link
        summary_input = f"{title}\n\n{entry.summary}"

        # Progress print before summarizing
        print(f"Summarizing article {idx}/{len(entries)}: {title}")

        # Generate the summary with Ollama
        summary = summarize_with_ollama(summary_input)

        # Progress print after summarizing
        print(f"Done summarizing article {idx}.\n")

        # Append the formatted summary to the digest
        digest.append(f"### [{title}]({link})\n")
        digest.append(f"> {summary}\n")

    # Save the final digest to a Markdown file
    with open("bengals_digest_v2.md", "w", encoding="utf-8") as f:
        f.write("\n".join(digest))

    print("✅ Digest saved to bengals_digest_v2.md")

if __name__ == "__main__":
    main()
