# Orion-MCP
Orion-MCP is a security-first MCP server for orchestrating AI agents, tools, and cyber intelligence using schema-aware execution, controlled workflows, and hardened access boundaries.

## MCP server
This repo includes a FastMCP server with two tools:
- `search_internet` (Tavily)
- `web_scrape` (Firecrawl)

### Requirements
- Python 3.10+
- `fastmcp`
- `httpx`

### Environment variables
- `TAVILY_API_KEY`
- `FIRECRAWL_API_KEY`
- Optional: `FIRECRAWL_API_URL` (defaults to `https://api.firecrawl.dev/v1/scrape`)

### Run
```bash
python server.py
```
