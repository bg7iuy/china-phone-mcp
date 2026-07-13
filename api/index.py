"""
Vercel serverless entrypoint for China Phone MCP Server.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from server import app

# Vercel Python runtime auto-detects 'app' as the ASGI handler
