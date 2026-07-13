"""
China Phone MCP Server
A Model Context Protocol server for Chinese phone number lookup.
Uses official MIIT allocation data via RapidAPI.
"""
import os
import httpx
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("china-phone")

RAPIDAPI_KEY = os.environ.get("RAPIDAPI_KEY", "")
RAPIDAPI_HOST = "china-phone-number-api2.p.rapidapi.com"
BASE_URL = f"https://{RAPIDAPI_HOST}"


@mcp.tool()
async def lookup_china_phone(phone: str) -> dict:
    """Look up a Chinese mobile phone number's prefix attribution.

    Returns carrier name, province, city, area code, postal code,
    region code, and number type (mobile/landline) based on official
    MIIT (Ministry of Industry and Information Technology) allocation tables.

    This is a prefix-level lookup only. It does NOT verify whether a
    specific subscriber is active or real, does NOT access carrier
    networks, and does NOT return personal information.

    Data source: MIIT official public number allocation tables, updated monthly.

    Args:
        phone: An 11-digit Chinese mobile phone number, e.g. 13800138000
    """
    if not RAPIDAPI_KEY:
        return {"error": "Server not configured with RapidAPI key"}

    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(
            f"{BASE_URL}/api/validate",
            params={"phone": phone},
            headers={
                "X-RapidAPI-Key": RAPIDAPI_KEY,
                "X-RapidAPI-Host": RAPIDAPI_HOST,
            },
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def get_china_phone_info(phone: str) -> dict:
    """Get detailed carrier and geographic attribution for a Chinese phone number.

    Returns the same fields as lookup_china_phone: carrier, province,
    city, area code, postal code, region code, number type, and prefix
    validity status from MIIT official allocation data.

    Use this when you need the full attribution details including
    region_code and prefix-level validation.

    Args:
        phone: An 11-digit Chinese mobile phone number, e.g. 19231327286
    """
    if not RAPIDAPI_KEY:
        return {"error": "Server not configured with RapidAPI key"}

    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(
            f"{BASE_URL}/api/info",
            params={"phone": phone},
            headers={
                "X-RapidAPI-Key": RAPIDAPI_KEY,
                "X-RapidAPI-Host": RAPIDAPI_HOST,
            },
        )
        response.raise_for_status()
        return response.json()


if __name__ == "__main__":
    import uvicorn
    app = mcp.streamable_http_app()
    uvicorn.run(app, host="0.0.0.0", port=8000)
