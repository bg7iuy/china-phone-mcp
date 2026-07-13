# China Phone MCP Server

[![MCP](https://img.shields.io/badge/MCP-Server-blue)](https://modelcontextprotocol.io)
[![RapidAPI](https://img.shields.io/badge/RapidAPI-China%20Phone%20Number%20API-green)](https://rapidapi.com/liluismx/api/china-phone-number-api2)

A Model Context Protocol (MCP) server that enables AI agents (Claude Code, Cursor, Windsurf) to look up Chinese phone number carrier and location information.

## What it does

Given an 11-digit Chinese mobile number, returns:
- **Carrier**: China Mobile / China Unicom / China Telecom / China Broadnet
- **Location**: Province, city, area code, postal code, region code
- **Number type**: Mobile or landline
- **Prefix validity**: Based on MIIT official allocation tables

## Tools

| Tool | Description |
|------|-------------|
| `lookup_china_phone` | Full attribution lookup with all fields |
| `get_china_phone_info` | Detailed carrier + geographic info |

## Data Source

Official MIIT (Ministry of Industry and Information Technology) public number allocation tables, updated monthly. No carrier networks accessed. No personal data collected.

## Quick Start

### Install in Claude Code

```bash
claude mcp add china-phone https://china-phone-mcp.vercel.app/api/index
```

### Use with Cursor

Add to your Cursor MCP config:

```json
{
  "mcpServers": {
    "china-phone": {
      "url": "https://china-phone-mcp.vercel.app/api/index"
    }
  }
}
```

### Run locally

```bash
pip install -r requirements.txt
export RAPIDAPI_KEY=your_key_here
python server.py
```

## Deployment

Deploy to Vercel with one click, or run on any Python host.

Set the environment variable `RAPIDAPI_KEY` in your deployment.

## Pricing

The underlying API has a free tier (1,000 requests/day). Paid plans start at $14.99/month for 100,000 requests/month.

[Get your RapidAPI key →](https://rapidapi.com/liluismx/api/china-phone-number-api2/pricing)

## License

MIT
