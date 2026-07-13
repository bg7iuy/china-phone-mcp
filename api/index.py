"""China Phone MCP Server — pure stdlib, zero dependencies."""
import json, os, uuid, urllib.request
from http.server import BaseHTTPRequestHandler

KEY = os.environ.get("RAPIDAPI_KEY", "")
HOST = "china-phone-number-api2.p.rapidapi.com"
BASE = f"https://{HOST}"
SESSIONS = {}

TOOLS = [
    {"name":"lookup_china_phone","description":"Look up a Chinese mobile phone prefix attribution. Returns carrier, province, city, area code, postal code, region code, number type from MIIT data.","inputSchema":{"type":"object","properties":{"phone":{"type":"string","description":"11-digit Chinese phone number"}},"required":["phone"]}},
    {"name":"get_china_phone_info","description":"Get detailed carrier and geographic attribution for a Chinese phone number.","inputSchema":{"type":"object","properties":{"phone":{"type":"string","description":"11-digit Chinese phone number"}},"required":["phone"]}},
]

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(length))
        method = body.get("method", "")
        rid = body.get("id", 0)

        if method == "initialize":
            sid = uuid.uuid4().hex
            SESSIONS[sid] = True
            self._sse({"jsonrpc":"2.0","id":rid,"result":{"protocolVersion":"2025-11-25","capabilities":{"tools":{}},"serverInfo":{"name":"china-phone","version":"1.0"}}}, new_sid=sid)
            return

        sid = self.headers.get("Mcp-Session-Id", "")
        if method == "tools/list":
            self._sse({"jsonrpc":"2.0","id":rid,"result":{"tools":TOOLS}}, sid=sid)
            return

        if method == "tools/call":
            name = body["params"]["name"]
            phone = body["params"]["arguments"]["phone"]
            ep = "/api/info" if name == "get_china_phone_info" else "/api/validate"
            req = urllib.request.Request(f"{BASE}{ep}?phone={phone}", headers={
                "X-RapidAPI-Key": KEY, "X-RapidAPI-Host": HOST
            })
            with urllib.request.urlopen(req, timeout=10) as r:
                result = json.loads(r.read())
            self._sse({"jsonrpc":"2.0","id":rid,"result":{"content":[{"type":"text","text":json.dumps(result,ensure_ascii=False)}],"isError":False}}, sid=sid)
            return

        self._sse({"jsonrpc":"2.0","id":rid,"error":{"code":-32601,"message":"Method not found"}}, sid=sid)

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({"status":"ok","name":"china-phone-mcp","endpoint":"/mcp"}).encode())

    def _sse(self, data, new_sid=None, sid=None):
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream")
        self.send_header("Cache-Control", "no-cache")
        if new_sid:
            self.send_header("Mcp-Session-Id", new_sid)
        elif sid:
            self.send_header("Mcp-Session-Id", sid)
        self.end_headers()
        body = f"event: message\ndata: {json.dumps(data)}\n\n"
        self.wfile.write(body.encode())
        self.wfile.flush()
