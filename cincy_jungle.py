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
MODEL_NAME = "llama4:latest"  # Change to "deepseek-r1:32b", "mistral", etc.

def get_cpu_usage():
    return psutil.cpu_percent(interval=0.1)

def get_gpu_usage():
    try:
        nvmlInit()
        handle = nvmlDeviceGetHandleByIndex(0)
        info = nvmlDeviceGetMemoryInfo(handle)
        used_gb = info.used / (1024 ** 3)
        total_gb = info.total / (1024 ** 3)
        percent = used_gb / total_gb * 100
        nvmlShutdown()
        return used_gb, total_gb, percent
    except Exception as e:
        return None, None, None

def get_article_text(entry):
    # Prefer full HTML content if present, else fallback to summary
    if hasattr(entry, "content") and len(entry.content) > 0:
        # Handle both dict (real) and possible .value (legacy) cases
        html_container = entry.content[0]
        html = html_container['value'] if isinstance(html_container, dict) and 'value' in html_container else getattr(html_container, 'value', "")
    else:
        html = entry.summary if hasattr(entry, "summary") else ""
    # Strip HTML tags for cleaner LLM prompt
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text(separator=" ", strip=True)
    return text


def summarize_with_ollama(text, model=MODEL_NAME):
    prompt = (
        "You are a sharp, no-nonsense Bengals news analyst in the style of ProFootballTalk's Mike Florio. "
        "Summarize the following article in exactly 2 sentences, highlighting the key details, contract drama, injuries, rumors, and controversial angles. "
        "Inject a touch of dry wit. Do not include your thought process or reasoning—write only the summary. Do not invent facts. Article:\n\n"
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
            timeout=180
        )
        elapsed = time.perf_counter() - start
        cpu_after = get_cpu_usage()
        gpu_used_after, _, gpu_percent_after = get_gpu_usage()
        summary = result.stdout.decode("utf-8").strip()
        # Clean up model output
        if not summary:
            summary = "[Summary missing or blank]"
        if "jeta" in summary:
            summary = summary.replace("jeta", "")
        if summary.isspace() or len(summary) < 10:
            summary = "[Summary missing or blank]"
        return (
            summary,
            elapsed,
            cpu_before,
            cpu_after,
            gpu_percent_before,
            gpu_percent_after
        )
    except subprocess.TimeoutExpired:
        return "[Summary failed: timeout]", 180, None, None, None, None

def main():
    feed = feedparser.parse("https://www.cincyjungle.com/rss/current")
    entries = feed.entries[:5]
    digest = ["# 🐅 Bengals News Digest – Florio Style (Ollama Edition)\n"]

    # For performance tracking
    article_times = []
    overall_start = time.perf_counter()

    for idx, entry in enumerate(entries, 1):
        title = entry.title
        link = entry.link
        article_text = get_article_text(entry)
        # Truncate input text to 1,500 characters (usually plenty for news)
        truncated_text = article_text[:1500]
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

    # Ensure the digests folder exists
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

    # Print performance metrics
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
