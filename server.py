from mcp.server.fastmcp import FastMCP
import random
from ddgs import DDGS
import glob, os

mcp = FastMCP("playscape", log_level="WARNING")

@mcp.tool()
def get_my_style(n: int = 30) -> str:
    """Random samples of how I text."""
    lines = open("my_style.txt").read().splitlines()
    return "\n".join(random.sample(lines, min(n, len(lines))))

@mcp.tool()
def get_tiktok_data(n: int = 20) -> str:
    """Random samples of my TikTok engagement data (topics/taste)."""
    lines = [l for l in open("tiktok_data.txt").read().splitlines() if l.strip()]
    return "\n".join(random.sample(lines, min(n, len(lines))))

@mcp.tool()
def search_web(query: str) -> str:
    """Search the web for real-world info."""
    try:
        results = DDGS().text(query, max_results=3)
    except Exception:
        return ""
    return "\n".join(f"{r['title']}: {r['body']}" for r in results)

@mcp.tool()
def get_book_passages(n: int = 3) -> str:
    """Random passages from books I love."""
    paras = [p.strip() for p in open("Maurice.txt").read().split("\n\n") if len(p.strip()) > 100]
    return "\n\n".join(random.sample(paras, min(n, len(paras))))


@mcp.tool()
def get_transcripts() -> str:
    folder = os.path.join(os.path.dirname(__file__), "Amar_22")
    text = ""
    for f in sorted(glob.glob(os.path.join(folder, "*.txt"))):
        text += open(f).read()[:1500] + "\n---\n"
    return text

if __name__ == "__main__":
    mcp.run()