import asyncio, sys, requests

MODEL = "llama3.1"
URL = "http://localhost:11434/api/chat"

def ask(messages):
    return requests.post(URL, json={"model": MODEL, "stream": False,
                                    "messages": messages}).json()["message"]

async def get(session, name, args=None):
    r = await session.call_tool(name, args or {})
    return "".join(c.text for c in r.content if hasattr(c, "text"))

async def main():
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client
    params = StdioServerParameters(command=sys.executable, args=["server.py"])
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            history = []
            while True:
                msg = input("You: ")
                if not msg.strip():
                    continue
                check = ask([{"role": "user", "content":
                    "Does this message ask about real-world news, media,  people, or recent "
                    "events? Answer only YES or NO.\n\nMessage: " + msg}])
                web = ""
                if "YES" in check["content"].upper():
                    last = [m["content"] for m in history if m["role"] == "user"][-1:]
                    web = await get(session, "search_web", {"query": " ".join(last + [msg])})

                style = await get(session, "get_my_style")
                taste = await get(session, "get_tiktok_data")
                books = await get(session, "get_book_passages")
                speech = await get(session, "get_transcripts")
                system = ("You are me. Below are my real thoughts from my video diaries. "
                          "Answer from what I actually believe, worry about, and want in them, "
                          "using specific details from my life, never generic answers. "
                          "Unless asked try not to mention specific people unprovoked.\n\n"
                          "MY REAL THOUGHTS (raw, first person):\n" + speech +
                          "\n\nMY TEXTS (style only):\n" + style +
                          "\n\nTOPICS I LIKE (taste only, don't copy wording):\n" + taste +
                          "\n\nBOOK PASSAGES I LOVE (taste only, don't quote or copy):\n" + books +
                          "\n\nFINAL RULE: reply in 1-3 short sentences, texting style, "
                          "matching my slang and punctuation. Never repeat or list the examples.")
                if web:
                    system += ("\n\nWEB RESULTS (real, current facts). Use these for any "
                               "facts, never make facts up, still text in my style:\n" + web)

                history.append({"role": "user", "content": msg})
                r = ask([{"role": "system", "content": system}] + history[-6:])
                history.append(r)
                print("Amar:", r["content"])

asyncio.run(main())

# to run use: .venv312/bin/python mcp_chat.py
