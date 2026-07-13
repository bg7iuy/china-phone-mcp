#!/usr/bin/env python3
"""
Vercel serverless entrypoint — China Phone MCP Server.
Serves at /api/index/mcp (no rewrite, use the real Vercel path).
"""
import os, httpx
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("china-phone")
RAPIDAPI_KEY = os.environ.get("RAPIDAPI_KEY", "")
HOST = "china-phone-number-api2.p.rapidapi.com"
BASE = f"https://{HOST}"

@mcp.tool()
async def lookup_china_phone(phone: str) -> dict:
    """Look up a Chinese mobile phone number prefix attribution from MIIT data."""
    async with httpx.AsyncClient(timeout=10) as c:
        r = await c.get(f"{BASE}/api/validate", params={"phone": phone},
            headers={"X-RapidAPI-Key": RAPIDAPI_KEY, "X-RapidAPI-Host": HOST})
        r.raise_for_status(); return r.json()

@mcp.tool()
async def get_china_phone_info(phone: str) -> dict:
    """Get detailed carrier and geographic attribution for a Chinese phone number."""
    async with httpx.AsyncClient(timeout=10) as c:
        r = await c.get(f"{BASE}/api/info", params={"phone": phone},
            headers={"X-RapidAPI-Key": RAPIDAPI_KEY, "X-RapidAPI-Host": HOST})
        r.raise_for_status(); return r.json()

app = mcp.streamable_http_app()
