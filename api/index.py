#!/usr/bin/env python3
"""Minimal debug: verify Vercel loads the function."""
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route

async def debug(request):
    return JSONResponse({"ok": True, "path": request.url.path})

app = Starlette(routes=[Route("/{path:path}", debug)])
