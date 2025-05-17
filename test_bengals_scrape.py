import pytest
from types import SimpleNamespace

import bengals_scrape

def make_entry(title, summary=None, content_html=None):
    entry = SimpleNamespace(title=title)
    if summary is not None:
        entry.summary = summary
    if content_html is not None:
        entry.content = [{'value': content_html}]
    else:
        entry.content = []
    return entry

def test_get_article_text_prefers_content_over_summary():
    entry = make_entry("Test Article", summary="This is the summary.", content_html="<p>This is <b>content</b>.</p>")
    text = bengals_scrape.get_article_text(entry)
    assert "This is content." in text

def test_get_article_text_falls_back_to_summary():
    entry = make_entry("Test Article", summary="This is the summary.", content_html=None)
    text = bengals_scrape.get_article_text(entry)
    assert "This is the summary." in text

@pytest.mark.parametrize("html,expected", [
    ("<p>This is <b>bold</b> and <a href='#'>link</a>.</p>", "This is bold and link."),
    ("Normal text.", "Normal text."),
    ("<p>&amp;#39;Quote&amp;#39; and &lt;html&gt; entities</p>", "'Quote' and <html> entities"),
    ("<p>Emoji 😃 and non-ASCII</p>", "Emoji 😃 and non-ASCII"),
])
def test_get_article_text_strips_html_and_entities(html, expected):
    entry = make_entry("Test Article", content_html=html)
    text = bengals_scrape.get_article_text(entry)
    # Sometimes spacing/quotes can differ slightly
    assert expected.replace("'", "") in text.replace("'", "")

def test_fetch_bengals_articles_deduplicates(monkeypatch):
    # Two feeds, some duplicate titles
    feeds = ["feed1", "feed2"]

    def fake_parse(url):
        # Return different entries for each feed, with some overlap
        if url == "feed1":
            return SimpleNamespace(entries=[
                make_entry("Title A"),
                make_entry("Title B"),
                make_entry("Title C"),
            ])
        else:
            return SimpleNamespace(entries=[
                make_entry("Title B"),
                make_entry("Title D"),
            ])
    monkeypatch.setattr(bengals_scrape.feedparser, "parse", fake_parse)
    results = bengals_scrape.fetch_bengals_articles(feeds, limit_per_feed=3, max_total=10)
    titles = [e.title for e in results]
    assert sorted(titles) == sorted(["Title A", "Title B", "Title C", "Title D"])
    assert len(titles) == 4

def test_summarize_with_ollama_timeout(monkeypatch):
    # Simulate a timeout
    def fake_run(*args, **kwargs):
        raise bengals_scrape.subprocess.TimeoutExpired(cmd="ollama", timeout=1)
    monkeypatch.setattr(bengals_scrape.subprocess, "run", fake_run)
    summary, elapsed, *_ = bengals_scrape.summarize_with_ollama("Test")
    assert "[Summary failed: timeout]" in summary

def test_summarize_with_ollama_blanks(monkeypatch):
    # Simulate model returning blank/short/garbled output
    class FakeResult:
        def __init__(self, output):
            self.stdout = output.encode("utf-8")
    monkeypatch.setattr(bengals_scrape.subprocess, "run", lambda *a, **k: FakeResult(""))
    summary, *_ = bengals_scrape.summarize_with_ollama("Test")
    assert "[Summary missing or blank]" in summary

    monkeypatch.setattr(bengals_scrape.subprocess, "run", lambda *a, **k: FakeResult("   "))
    summary, *_ = bengals_scrape.summarize_with_ollama("Test")
    assert "[Summary missing or blank]" in summary

    monkeypatch.setattr(bengals_scrape.subprocess, "run", lambda *a, **k: FakeResult("jeta not enough"))
    summary, *_ = bengals_scrape.summarize_with_ollama("Test")
    assert "not enough" in summary

def test_integration_fake(monkeypatch):
    # End-to-end smoke test with all logic mocked
    fake_entries = [make_entry(f"Title {i}", summary=f"Summary {i}") for i in range(3)]

    monkeypatch.setattr(bengals_scrape, "fetch_bengals_articles", lambda feeds, limit_per_feed=5, max_total=12: fake_entries)
    monkeypatch.setattr(bengals_scrape, "summarize_with_ollama", lambda text, model=None: (f"Summary for: {text[:12]}", 1, 0, 0, 0, 0))
    monkeypatch.setattr(bengals_scrape, "get_article_text", lambda entry: entry.summary)

    # Patch out file writing (no actual I/O)
    monkeypatch.setattr(bengals_scrape.os, "makedirs", lambda *a, **k: None)
    monkeypatch.setattr(bengals_scrape, "open", lambda *a, **k: SimpleNamespace(write=lambda x: None).__enter__())

    # Should not raise
    bengals_scrape.main()
