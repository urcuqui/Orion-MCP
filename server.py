import logging

import uvicorn
from fastmcp import FastMCP
from mcp.server.sse import SseServerTransport
from starlette.applications import Starlette
from starlette.responses import Response
from starlette.routing import Mount, Route

from tools import FirecrawlWebScrapeTool, TavilySearchTool

mcp = FastMCP("orion-mcp", host="127.0.0.1", port=8000)

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
    # FastMCP's built-in SSE runner doesn't return a Response, which can
    # trigger "NoneType is not callable" on client disconnect in Starlette.
    sse = SseServerTransport("/messages")

    async def handle_sse(request):
        async with sse.connect_sse(
            request.scope, request.receive, request._send
        ) as streams:
            await mcp._mcp_server.run(
                streams[0],
                streams[1],
                mcp._mcp_server.create_initialization_options(),
            )
        return Response()

    starlette_app = Starlette(
        debug=mcp.settings.debug,
        routes=[
            Route("/sse", endpoint=handle_sse),
            Mount("/messages", app=sse.handle_post_message),
        ],
    )
    uvicorn.run(
        starlette_app,
        host=mcp.settings.host,
        port=mcp.settings.port,
        log_level=mcp.settings.log_level.lower(),
    )
