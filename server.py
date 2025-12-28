import logging

from fastmcp import FastMCP

from tools import FirecrawlWebScrapeTool, TavilySearchTool

mcp = FastMCP("orion-mcp",streamable_http_path="/",port=8000)

logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(name)s:%(message)s")
logger = logging.getLogger("orion-mcp")


def _init_tools() -> None:
    tools = [
        TavilySearchTool(mcp),
        FirecrawlWebScrapeTool(mcp),
    ]
    for tool in tools:
        logger.info("Registering tool: %s", tool.__class__.__name__)
        tool.register()


if __name__ == "__main__":
    logger.info("Starting MCP server.")
    _init_tools()
    mcp.run()
