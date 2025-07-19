from typing import Any, Optional
from mcp.server.fastmcp import FastMCP
from tools.inventory import get_inventory_items, get_products
from utils.shopify_client import make_shopify_request, SHOPIFY_STORE, SHOPIFY_TOKEN, API_VERSION
from utils.logger import logger


# Initialize MCP server
mcp = FastMCP("shopify")


@mcp.tool()
async def get_inventory_items_impl(first_n: int = 5) -> str:
    """Get inventory items from the Shopify store.
    
    Args:
        first_n: Number of items to retrieve (default: 5)
    """
    return await get_inventory_items(first_n)

@mcp.tool()
async def get_products_impl(first_n: int = 3) -> str:
    """Get product listings from the Shopify store.
    
    Args:
        first_n: Number of products to retrieve (default: 3)
    """
    return await get_products(first_n)

if __name__ == "__main__":
    logger.info("Starting Shopify MCP server...")
    mcp.run(transport='stdio')

