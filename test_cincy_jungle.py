import pytest
from cincy_jungle import get_article_text, summarize_with_ollama
import feedparser
from bs4 import BeautifulSoup

# Example test article entry (mocked)
class MockEntry:
    def __init__(self, title, html, summary=None):
        self.title = title
        self.content = [{"value": html}]
        self.summary = summary if summary else "No summary available"

def test_get_article_text_html_stripping():
    html = "<p>This is <b>bold</b> and <a href='http://test.com'>link</a>.</p>"
    entry = MockEntry("Test", html)
    result = get_article_text(entry)
    assert "This is bold and link" in result.replace(" .", ".")

def test_get_article_text_prefers_content_over_summary():
    entry = MockEntry("Test", "<p>Content wins</p>", summary="Summary loses")
    result = get_article_text(entry)
    assert "Content wins" in result and "Summary loses" not in result

def test_get_article_text_handles_missing_content():
    # Entry with only summary, no content
    class NoContentEntry:
        summary = "Just a summary here"
    entry = NoContentEntry()
    result = get_article_text(entry)
    assert result == "Just a summary here"

def test_strip_jeta_artifact():
    # Simulate model returning 'jeta'
    summary = "Good stuff jeta Bad stuffjeta"
    clean = summary.replace("jeta", "")
    assert "jeta" not in clean

def test_blank_summary_handling():
    # Simulate a blank summary
    summary = ""
    processed = "[Summary missing or blank]" if not summary else summary
    assert processed == "[Summary missing or blank]"

def test_rss_feed_has_entries():
    feed = feedparser.parse("https://www.cincyjungle.com/rss/current")
    assert hasattr(feed, "entries")
    assert len(feed.entries) > 0

@pytest.mark.skip(reason="Requires Ollama to be running with a model loaded")
def test_summarize_with_ollama_runs():
    # Run only if you want to test model inference (slow!)
    text = "The Bengals are opening the 2025 season with a divisional game against the Browns."
    summary, *_ = summarize_with_ollama(text)
    assert isinstance(summary, str)
    assert len(summary) > 0
    # Optionally check for blank/placeholder
    assert "[Summary" not in summary

# Advanced: parametrize input edge cases, HTML quirks, etc.
@pytest.mark.parametrize("html", [
    "<p>Normal text.</p>",
    "<p>&amp;#39;Quote&amp;#39; and &lt;html&gt; entities</p>",
    "<p>Emoji 😃 and non-ASCII</p>",
])
def test_get_article_text_handles_various_html(html):
    entry = MockEntry("Test", html)
    result = get_article_text(entry)
    assert isinstance(result, str)
    assert len(result) > 0

