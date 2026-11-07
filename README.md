# Agent Toolkit

## What it does
My skill checks a live demo against requirements I give it and reports what works, what doesn't, and what it couldn't verify, with evidence. It runs when I ask to check a demo and doesn't change anything. My MCP tool, `search_local_docs`, searches Markdown and text files in folders I choose and returns up to five matches with paths and excerpts.

## Why I made it
I kept having to point out things the AI hadn't fixed. In my [Crossyroad log](https://github.com/a-gupta123/crossyroad/blob/main/prompt_log.md), I wrote, “The chicken flips the wrong way when moving left and right.” I also kept asking it to check project documents, like “how many acceptance criteria from SPEC.md and README are still missing? name them” in my [Pizzeria log](https://github.com/a-gupta123/pizzeria/blob/main/prompt_log.md). I wanted to make both tasks easier.

## Setup
With Python and uv installed, clone this repo, open its folder, and run `uv sync`. The skill goes in `.cursor/skills/check-live-requirements/SKILL.md`. Create `search_roots.txt` beside `server.py` with one full folder path per line. In `~/.cursor/mcp.json`, add the server using `{"mcpServers":{"search-local-docs":{"command":"/YOUR/PROJECT/PATH/.venv/bin/python","args":["/YOUR/PROJECT/PATH/server.py"]}}}`. Replace `/YOUR/PROJECT/PATH` with your own repo path and keep any existing servers. Restart Cursor, ask it to use the tool, and expand the call to check the result.

## What I tested
I tested both in Cursor Agent with Grok 4.7. The search tool found a test phrase and requirements from Movie Recommender and Crossyroad. I checked the demos in fresh chats. The Crossyroad checker inferred facing from internal state, so I updated the skill to require clear screenshots and reran it.

## Sources and AI use
I used ChatGPT for ideas and Cursor Agent to build and test the toolkit. The setup follows the [MCP docs](https://modelcontextprotocol.io/), [Cursor skill docs](https://cursor.com/docs/skills), and [Cursor MCP guide](https://cursor.com/guides/coding-agent-mcp).
