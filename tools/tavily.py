import logging
from typing import Any, Dict

import httpx
from fastmcp import FastMCP

from .utils import require_env

logger = logging.getLogger(__name__)


class TavilySearchTool:
    def __init__(self, mcp: FastMCP) -> None:
        self._mcp = mcp

    def register(self) -> None:
        @self._mcp.tool()
        async def search_internet(
            query: str,
            max_results: int = 5,
            search_depth: str = "basic",
            include_answer: bool = False,
            include_raw_content: bool = False,
        ) -> Dict[str, Any]:
            """Search the internet using Tavily and return structured results."""
            api_key = require_env("TAVILY_API_KEY")

            logger.info("Executing Tavily search for query: %s", query)
            payload = {
                "api_key": api_key,
                "query": query,
                "max_results": max_results,
                "search_depth": search_depth,
                "include_answer": include_answer,
                "include_raw_content": include_raw_content,
            }

            async with httpx.AsyncClient(timeout=30) as client:
                try:
                    response = await client.post(
                        "https://api.tavily.com/search",
                        json=payload,
                    )
                    response.raise_for_status()
                    return response.json()
                except httpx.HTTPError as exc:
                    logger.error("Tavily request failed: %s", exc)
                    raise
