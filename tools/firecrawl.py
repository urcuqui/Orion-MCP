import logging
import os
from typing import Any, Dict, List, Optional

import httpx
from fastmcp import FastMCP

from .utils import require_env

logger = logging.getLogger(__name__)


class FirecrawlWebScrapeTool:
    def __init__(self, mcp: FastMCP) -> None:
        self._mcp = mcp
        self._api_url = os.getenv(
            "FIRECRAWL_API_URL",
            "https://api.firecrawl.dev/v1/scrape",
        )

    def register(self) -> None:
        @self._mcp.tool(description="Web scraping tool")
        async def web_scrape(
            url: str,
            formats: Optional[List[str]] = None,
            only_main_content: bool = True,
        ) -> Dict[str, Any]:
            """Scrape a web page with Firecrawl and return formatted content.

            Use this tool to fetch and parse a single URL into structured outputs
            such as markdown, HTML, or plain text. You can request multiple output
            formats and optionally limit the response to the main content (e.g.,
            exclude navigation, ads, or boilerplate).
            """
            api_key = require_env("FIRECRAWL_API_KEY")

            logger.info("Executing Firecrawl scrape for URL: %s", url)
            payload = {
                "url": url,
                "formats": formats or ["markdown"],
                "onlyMainContent": only_main_content,
            }

            headers = {"Authorization": f"Bearer {api_key}"}

            async with httpx.AsyncClient(timeout=60) as client:
                try:
                    response = await client.post(
                        self._api_url,
                        json=payload,
                        headers=headers,
                    )
                    response.raise_for_status()
                    logger.info("Firecrawl scrape succeeded for URL: %s", url)
                    return response.json()
                except httpx.HTTPError as exc:
                    logger.error("Firecrawl request failed: %s", exc)
                    raise
