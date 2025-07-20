from mcp.server.fastmcp import FastMCP
from tools.inventory import get_inventory_items
from tools.products import get_products
from tools.blogs import get_blogs, blog_create
from tools.online_store import get_pages, page_create
from utils.shopify_client import SHOPIFY_STORE, SHOPIFY_TOKEN, API_VERSION
from utils.logger import logger
from tools.menus import get_menus
from tools.menus import update_menu

mcp = FastMCP("shopify_anidev")


@mcp.tool()
async def update_menu_impl(
    menu_id: str,
    title: str,
    handle: str,
    items: list
) -> str:

    """
Update an existing menu on the Shopify store.

Args:
    menu_id: The ID of the menu to update.
    title: New title for the menu.
    handle: New handle (slug) for the menu.
    items: A list of menu items in MenuItemUpdateInput format.

MenuItemUpdateInput format:
    Each item in the list should be a dictionary with the following fields:

    - id (str, optional): The ID of the existing menu item to update. Omit for new items.
    - title (str, required): The display text for the menu item.
    - type (str, required): The type of menu item. Must be one of:
        'ARTICLE', 'BLOG', 'CATALOG', 'COLLECTION', 'COLLECTIONS',
        'CUSTOMER_ACCOUNT_PAGE', 'FRONTPAGE', 'HTTP', 'METAOBJECT',
        'PAGE', 'PRODUCT', 'SEARCH', 'SHOP_POLICY'
    - url (str, optional): The URL for the menu item. Required for type 'HTTP', optional for others.
    - resourceId (str, optional): The ID of the Shopify resource (e.g., product, collection) this item links to.
    - tags (list of str, optional): Tags for the menu item.
    - items (list of MenuItemUpdateInput, optional): Nested menu items (for submenus).

Example:
    items = [
        {
            "title": "Home",
            "type": "FRONTPAGE",
            "url": "/"
        },
        {
            "title": "Catalog",
            "type": "CATALOG",
            "url": "/collections/all"
        },
        {
            "title": "About Us",
            "type": "PAGE",
            "url": "/pages/about-us"
        },
        {
            "title": "Contact",
            "type": "PAGE",
            "url": "/pages/contact"
        }
    ]
"""
    return await update_menu(menu_id, title, handle, items)

@mcp.tool()
async def get_menus_impl() -> str:
    """Get the store’s single menu and its details.

    This fetches the first available menu and returns its items and metadata.
    """
    return await get_menus()

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

@mcp.tool()
async def get_blogs_impl(first_n: int = 5) -> str:
    """Get blogs from the Shopify store.

    Args:
        first_n: Number of blogs to retrieve (default: 5)
    """
    return await get_blogs(first_n)

@mcp.tool()
async def blog_create_impl(title: str, handle: str, comment_policy: str = "MODERATED") -> str:
    """Create a new blog.

    Args:
        title: Title of the blog.
        handle: URL handle.
        comment_policy: Comment policy.
    """
    return await blog_create(title, handle, comment_policy)

@mcp.tool()
async def get_pages_impl(first_n: int = 5) -> str:
    """Get online store pages from the Shopify store.

    Args:
        first_n: Number of pages to retrieve (default: 5)
    """
    return await get_pages(first_n)

@mcp.tool()
async def page_create_impl(
    title: str,
    handle: str,
    body: str,
    is_published: bool = True,
    template_suffix: str = "custom"
) -> str:
    """Create a new store page.

    Args:
        title: Title of the page.
        handle: URL handle (slug).
        body: HTML content.
        is_published: Whether the page should be published immediately.
        template_suffix: Optional template suffix (default: "custom").
    """
    return await page_create(title, handle, body, is_published, template_suffix)


if __name__ == "__main__":
    logger.info("Starting Shopify MCP server...")
    mcp.run(transport='stdio')
