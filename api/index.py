#!/usr/bin/env python3
"""Vercel serverless entrypoint — China Phone MCP Server."""
import os, httpx
from mcp.server.fastmcp import FastMCP
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Mount, Route

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

async def debug(request):
    return JSONResponse({
        "path": request.url.path,
        "headers": dict(request.headers),
        "scope_path": request.scope.get("path", ""),
        "root_path": request.scope.get("root_path", ""),
    })

app = Starlette(routes=[
    Route("/", debug),
    Mount("/api/index", app=mcp.streamable_http_app()),
])
