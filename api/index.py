"""China Phone MCP Server — Streamable HTTP, no fastmcp dependency."""
import json, os
import httpx
from starlette.applications import Starlette
from starlette.responses import Response, StreamingResponse
from starlette.routing import Route

KEY = os.environ.get("RAPIDAPI_KEY", "")
HOST = "china-phone-number-api2.p.rapidapi.com"
BASE = f"https://{HOST}"

TOOLS = [
    {"name":"lookup_china_phone","description":"Look up a Chinese mobile phone prefix attribution. Returns carrier, province, city, area code, postal code, region code, number type from MIIT data.","inputSchema":{"type":"object","properties":{"phone":{"type":"string","description":"11-digit Chinese phone number"}},"required":["phone"]}},
    {"name":"get_china_phone_info","description":"Get detailed carrier and geographic attribution for a Chinese phone number.","inputSchema":{"type":"object","properties":{"phone":{"type":"string","description":"11-digit Chinese phone number"}},"required":["phone"]}},
]

async def mcp_endpoint(request):
    body = await request.json()
    method = body.get("method","")
    rid = body.get("id",0)

    if method == "initialize":
        data = json.dumps({"jsonrpc":"2.0","id":rid,"result":{"protocolVersion":"2025-11-25","capabilities":{"tools":{}},"serverInfo":{"name":"china-phone","version":"1.0"}}})
        return _sse(data, new_session=True)

    sid = request.headers.get("Mcp-Session-Id","")
    if method == "tools/list":
        data = json.dumps({"jsonrpc":"2.0","id":rid,"result":{"tools":TOOLS}})
        return _sse(data, sid=sid)

    if method == "tools/call":
        name = body["params"]["name"]
        phone = body["params"]["arguments"]["phone"]
        ep = "/api/info" if name == "get_china_phone_info" else "/api/validate"
        async with httpx.AsyncClient(timeout=10) as c:
            r = await c.get(f"{BASE}{ep}", params={"phone":phone},
                headers={"X-RapidAPI-Key":KEY,"X-RapidAPI-Host":HOST})
            r.raise_for_status()
            result = r.json()
        data = json.dumps({"jsonrpc":"2.0","id":rid,"result":{"content":[{"type":"text","text":json.dumps(result,ensure_ascii=False)}],"isError":False}})
        return _sse(data, sid=sid)

    return _sse(json.dumps({"jsonrpc":"2.0","id":rid,"error":{"code":-32601,"message":"Method not found"}}), sid=sid)

def _sse(data, new_session=False, sid=None):
    headers = {"Content-Type":"text/event-stream","Cache-Control":"no-cache","Connection":"keep-alive"}
    if new_session:
        import uuid; headers["Mcp-Session-Id"] = uuid.uuid4().hex
    elif sid:
        headers["Mcp-Session-Id"] = sid
    body = f"event: message\ndata: {data}\n\n"
    return Response(body, headers=headers, media_type="text/event-stream")

async def health(request):
    return Response(json.dumps({"status":"ok","name":"china-phone-mcp"}), media_type="application/json")

app = Starlette(routes=[
    Route("/mcp", mcp_endpoint, methods=["POST"]),
    Route("/health", health),
])
