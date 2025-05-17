import subprocess
import feedparser
from datetime import datetime
import os
import time
import psutil
from pynvml import nvmlInit, nvmlDeviceGetHandleByIndex, nvmlDeviceGetMemoryInfo, nvmlShutdown
from bs4 import BeautifulSoup

# Path to your local Ollama executable
OLLAMA_PATH = r"C:\Users\ddavi\AppData\Local\Programs\Ollama\ollama.exe"
MODEL_NAME = "llama4:latest"  # Options: "llama4:latest", "deepseek-r1:32b", "mistral", etc.

# List of Bengals-specific RSS feeds (add more as needed)
BENGALS_FEEDS = [
    "https://www.cincyjungle.com/rss/current",              # SB Nation - Cincy Jungle
    "https://sports.yahoo.com/nfl/teams/cin/rss/",          # Yahoo! Sports Bengals
    "https://bengalswire.usatoday.com/feed/",               # USA Today Bengals Wire
    "https://www.espn.com/espn/rss/nfl/news",               # ESPN NFL News (will filter to Bengals stories)
    "https://www.bengals.com/news/rss",                     # Bengals official site news
]

def get_cpu_usage():
    """Return system-wide CPU usage as a percentage."""
    return psutil.cpu_percent(interval=0.1)

def get_gpu_usage():
    """Return NVIDIA GPU usage if available, otherwise (None, None, None)."""
    try:
        nvmlInit()
        handle = nvmlDeviceGetHandleByIndex(0)
        info = nvmlDeviceGetMemoryInfo(handle)
        used_gb = info.used / (1024 ** 3)
        total_gb = info.total / (1024 ** 3)
        percent = used_gb / total_gb * 100
        nvmlShutdown()
        return used_gb, total_gb, percent
    except Exception:
        return None, None, None

def get_article_text(entry):
    """
    Extract and clean article text from a feedparser entry.
    Prefer full HTML content if present, else fallback to summary.
    """
    if hasattr(entry, "content") and len(entry.content) > 0:
        html_container = entry.content[0]
        html = html_container['value'] if isinstance(html_container, dict) and 'value' in html_container else getattr(html_container, 'value', "")
    else:
        html = entry.summary if hasattr(entry, "summary") else ""
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text(separator=" ", strip=True)
    return text

def is_bengals_story(entry):
    """
    Heuristic filter for ESPN/NFL feeds: keep if 'bengals' appears in title/summary/content.
    """
    text = f"{getattr(entry, 'title', '')} {getattr(entry, 'summary', '')}".lower()
    return "bengals" in text

def summarize_with_ollama(text, model=MODEL_NAME):
    """
    Summarize an article using Ollama + Llama 4.
    Prompt is designed for trustworthy, newsletter-ready, fact-focused summaries.
    """
    prompt = (
        "You are a Bengals news editor for a daily newsletter. Summarize the article below in a way that's accurate, concise, and engaging for fans. "
        "Focus on the most relevant news, context, or developments—mention contract drama, injuries, or controversy ONLY if clearly present. "
        "Never invent facts or rumors. Do not explain your reasoning, just write the summary. Make it sound natural and conversational in Miex.\n\n"
        "Article:\n\n"
        f"{text.strip()}"
    )
    try:
        cpu_before = get_cpu_usage()
        gpu_used_before, gpu_total, gpu_percent_before = get_gpu_usage()
        start = time.perf_counter()
        result = subprocess.run(
            [OLLAMA_PATH, "run", model],
            input=prompt.encode("utf-8"),
            capture_output=True,
            timeout=200
        )
        elapsed = time.perf_counter() - start
        cpu_after = get_cpu_usage()
        gpu_used_after, _, gpu_percent_after = get_gpu_usage()
        summary = result.stdout.decode("utf-8").strip()
        # Clean up model output
        if not summary or summary.isspace() or len(summary) < 10:
            summary = "[Summary missing or blank]"
        if "jeta" in summary:
            summary = summary.replace("jeta", "")
        return (
            summary,
            elapsed,
            cpu_before,
            cpu_after,
            gpu_percent_before,
            gpu_percent_after
        )
    except subprocess.TimeoutExpired:
        return "[Summary failed: timeout]", 200, None, None, None, None

def fetch_bengals_articles(feeds, limit_per_feed=6, max_total=15):
    """
    Fetches articles from multiple feeds and returns deduplicated, recent Bengals news entries.
    For generic NFL feeds, keeps only Bengals-relevant articles.
    """
    all_entries = []
    seen_titles = set()
    for url in feeds:
        feed = feedparser.parse(url)
        count = 0
        for entry in feed.entries:
            # Only keep Bengals stories from generic NFL sources (like ESPN)
            if "espn.com" in url or "nfl/news" in url:
                if not is_bengals_story(entry):
                    continue
            # Only keep Bengals stories from Bengals.com, but their RSS is usually clean
            if "bengals.com" in url:
                # Could filter further, but their feed is Bengals-only
                pass
            # Deduplicate by title (case insensitive)
            title_key = entry.title.strip().lower()
            if title_key not in seen_titles:
                all_entries.append(entry)
                seen_titles.add(title_key)
                count += 1
            if count >= limit_per_feed:
                break
    # Sort by published date if available (reverse = newest first)
    all_entries.sort(key=lambda e: getattr(e, "published", ""), reverse=True)
    return all_entries[:max_total]

def main():
    print("Fetching Bengals articles from all sources...")
    entries = fetch_bengals_articles(BENGALS_FEEDS, limit_per_feed=6, max_total=15)
    today_str = datetime.now().strftime("%B %d, %Y")
    digest = [f"# 🐅 Bengals Daily Digest — {today_str}\n"]
    digest.append("Curated Bengals headlines & summaries from trusted sources. [Click any headline for the full article.]\n")

    article_times = []
    overall_start = time.perf_counter()

    for idx, entry in enumerate(entries, 1):
        title = entry.title
        link = entry.link
        article_text = get_article_text(entry)
        # Llama 4 can handle long context, but we'll trim to ~2000 chars for best speed/quality
        truncated_text = article_text[:2000]
        summary_input = f"{title}\n\n{truncated_text}"

        print(f"Summarizing article {idx}/{len(entries)}: {title}")

        summary, elapsed, cpu_before, cpu_after, gpu_before, gpu_after = summarize_with_ollama(summary_input, model=MODEL_NAME)

        print(f"Done summarizing article {idx}. Time: {elapsed:.2f} seconds.")
        print(f"  CPU usage before/after: {cpu_before}% → {cpu_after}%")
        if gpu_before is not None and gpu_after is not None:
            print(f"  GPU usage before/after: {gpu_before:.1f}% → {gpu_after:.1f}%")
        else:
            print("  GPU usage: Not available (is your GPU NVIDIA and drivers up to date?)")
        if "[Summary" in summary:
            print(f"  ⚠️ WARNING: {summary}")
        print("")

        digest.append(f"### [{title}]({link})\n")
        digest.append(f"> {summary}\n")
        article_times.append((title, elapsed, cpu_before, cpu_after, gpu_before, gpu_after))

    total_time = time.perf_counter() - overall_start

    # Save output to digests/ folder, date- and model-stamped
    os.makedirs("digests", exist_ok=True)
    now = datetime.now().strftime("%Y-%m-%d")
    safe_model_name = MODEL_NAME.replace(":", "_").replace("-", "_")
    filename = os.path.join("digests", f"bengals_digest_{safe_model_name}_{now}.md")
    latest_filename = os.path.join("digests", f"bengals_digest_{safe_model_name}_latest.md")

    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(digest))
    with open(latest_filename, "w", encoding="utf-8") as f:
        f.write("\n".join(digest))

    print(f"\n✅ Digest saved to {filename}")
    print(f"✅ Latest digest also saved to {latest_filename}")

    # Performance reporting
    print("\n--- Performance Metrics ---")
    cpu_list, gpu_list, times = [], [], []
    for idx, (title, elapsed, cpu_b, cpu_a, gpu_b, gpu_a) in enumerate(article_times, 1):
        print(f"{idx}. {title[:50]}...  {elapsed:.2f} sec | CPU: {cpu_b}%→{cpu_a}% | GPU: {gpu_b}%→{gpu_a}%")
        if cpu_b is not None: cpu_list.append(cpu_b)
        if cpu_a is not None: cpu_list.append(cpu_a)
        if gpu_b is not None: gpu_list.append(gpu_b)
        if gpu_a is not None: gpu_list.append(gpu_a)
        times.append(elapsed)
    print(f"\nTotal time for digest: {total_time:.2f} seconds")
    if cpu_list: print(f"Average CPU: {sum(cpu_list)/len(cpu_list):.2f}%")
    if gpu_list: print(f"Average GPU: {sum(gpu_list)/len(gpu_list):.2f}%")
    if times: print(f"Average time per article: {sum(times)/len(times):.2f} sec")

if __name__ == "__main__":
    main()
