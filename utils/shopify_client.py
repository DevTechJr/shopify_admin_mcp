# utils/shopify.py

from typing import Optional
import httpx

SHOPIFY_STORE = "your-store-id.myshopify.com"
SHOPIFY_TOKEN = "admin access token"
API_VERSION = "2025-07"

async def make_shopify_request(query: str, variables: Optional[dict] = None):
    url = f"https://{SHOPIFY_STORE}/admin/api/{API_VERSION}/graphql.json"
    headers = {
        "Content-Type": "application/json",
        "X-Shopify-Access-Token": SHOPIFY_TOKEN
    }
    payload = {"query": query}
    if variables:
        payload["variables"] = variables

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, headers=headers, timeout=30.0)
        response.raise_for_status()
        return response.json()
