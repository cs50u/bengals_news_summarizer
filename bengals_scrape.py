import feedparser
import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variable from .env
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Initialize the OpenAI client
client = OpenAI(api_key=api_key)

def summarize_article(title, rss_summary):
    prompt = f"Summarize this Bengals article in one short sentence:\n\nTitle: {title}\n\nSummary: {rss_summary}"
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
            max_tokens=50
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"[Summary failed: {e}]"

def main():
    feed = feedparser.parse("https://www.cincyjungle.com/rss/current")
    entries = feed.entries[:8]  # Limit to top 8 for cost control

    digest_lines = ["# 🐅 Bengals News Digest – Summarized\n"]

    for entry in entries:
        title = entry.title
        link = entry.link
        summary = summarize_article(title, entry.summary)

        digest_lines.append(f"### [{title}]({link})\n")
        digest_lines.append(f"> {summary}\n")

    # Save to Markdown
    with open("bengals_digest.md", "w", encoding="utf-8") as f:
        f.write("\n".join(digest_lines))

    print("✅ Digest saved to bengals_digest.md")

if __name__ == "__main__":
    main()
