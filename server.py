from mcp.server.fastmcp import FastMCP
from tools.inventory import get_inventory_items
from tools.products import get_products, get_product, create_product, update_product, delete_product
from tools.blogs import get_blogs, blog_create
from tools.online_store import get_pages, page_create, get_page_html, update_page_html, page_delete
from utils.shopify_client import SHOPIFY_STORE, SHOPIFY_TOKEN, API_VERSION
from utils.logger import logger
from tools.menus import get_menus, update_menu
from tools.articles import (
    article_create,
    article_update,
    article_delete,
    get_articles_for_blog,
    get_article
)
from tools.blogs import blog_update, blog_delete, blog_create, get_blogs, blog_update, blog_delete, get_blog_by_id
from tools.customers import customer_send_account_invite_email, customers_list, customers_count, customer_get
from tools.orders import orders_list, orders_count
from tools.discount_codes import (
    discount_codes_list, discount_code_create, discount_code_get, discount_code_update, discount_code_delete)

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


@mcp.tool()
async def get_page_html_impl(page_id: str) -> str:
    """Get the HTML content of a page by its ID.
    
    Args:
        page_id: The ID of the page (Shopify global ID format).
    """
    return await get_page_html(page_id)

@mcp.tool()
async def update_page_html_impl(page_id: str, new_html: str) -> str:
    """Update the HTML content of an existing page.
    
    Args:
        page_id: The ID of the page to update.
        new_html: The new HTML content to replace the existing one.
    """
    return await update_page_html(page_id, new_html)

@mcp.tool()
async def page_delete_impl(page_id: str) -> str:
    """Delete an online store page from the Shopify store.

    Args:
        page_id: The ID of the page to delete (e.g., 'gid://shopify/Page/123456789')

    Example:

        {
  "id": "gid://shopify/Page/105984196719",
  "page": {
    "body": "<h1>Updated Page Content</h1>"
  }
}
    """
    return await page_delete(page_id)

@mcp.tool()
async def get_blogs_impl(first_n: int = 5) -> str:
    """Get blogs from the Shopify store.

    Args:
        first_n: Number of blogs to retrieve (default: 5)
    """
    return await get_blogs(first_n)

@mcp.tool()
async def get_blog_by_id_impl(blog_id: str) -> str:
    """Retrieve a single blog by its Shopify ID.
    
    Args:
        blog_id: Shopify GID of the blog to retrieve.
    """
    return await get_blog_by_id(blog_id)


@mcp.tool()
async def blog_create_impl(title: str, handle: str, comment_policy: str = "MODERATED") -> str:
    """Create a new blog.

    Args:
        title: Title of the blog.
        handle: URL handle.
        comment_policy: Comment policy (e.g., MODERATED).
    """
    return await blog_create(title, handle, comment_policy)


@mcp.tool()
async def blog_update_impl(blog_id: str, title: str) -> str:
    """Update the title of an existing blog.

    Args:
        blog_id: The ID of the blog to update.
        title: The new title for the blog.
    """
    return await blog_update(blog_id, title)


@mcp.tool()
async def blog_delete_impl(blog_id: str) -> str:
    """Delete a blog from the Shopify store.

    Args:
        blog_id: The ID of the blog to delete.
    """
    return await blog_delete(blog_id)


@mcp.tool()
async def article_create_impl(blog_id: str, title: str, body: str, author_name: str) -> str:
    """Create a new article within a blog.

    Args:
        blog_id: The ID of the blog to post in.
        title: Title of the article.
        body: HTML content.
        author_name: Name of the article author.
    """
    return await article_create(blog_id, title, body, author_name)


@mcp.tool()
async def article_update_impl(article_id: str, title: str, body: str) -> str:
    """Update an existing article.

    Args:
        article_id: The ID of the article to update.
        title: New title.
        body: New HTML content.
    """
    return await article_update(article_id, title, body)


@mcp.tool()
async def article_delete_impl(article_id: str) -> str:
    """Delete an article.

    Args:
        article_id: The ID of the article to delete.
    """
    return await article_delete(article_id)


@mcp.tool()
async def get_articles_for_blog_impl(blog_id: str, first_n: int = 5) -> str:
    """Retrieve articles from a specific blog.

    Args:
        blog_id: The ID of the blog.
        first_n: Number of articles to retrieve (default: 5)
    """
    return await get_articles_for_blog(blog_id, first_n)


@mcp.tool()
async def get_article_impl(article_id: str) -> str:
    """Get a single article by ID.

    Args:
        article_id: The ID of the article.
    """
    return await get_article(article_id)

@mcp.tool()
async def get_product_impl(product_id: str) -> str:
    """Retrieve product details by ID.

    Args:
        product_id: The Shopify GID of the product.
    """
    return await get_product(product_id)

@mcp.tool()
async def create_product_impl(product: dict, media: list = None) -> str:
    """Create a new product.

    Args:
        product: A dictionary of product fields (e.g., title, options).
        media: Optional list of media to add to the product.
    """
    return await create_product(product, media)

@mcp.tool()
async def update_product_impl(product: dict, media: list = None) -> str:
    """Update an existing product.

    Args:
        product: A dictionary of fields to update. Must include the product ID.
        media: Optional list of media to add.
    """
    return await update_product(product, media)

@mcp.tool()
async def delete_product_impl(product_id: str, synchronous: bool = True) -> str:
    """Delete a product.

    Args:
        product_id: Shopify GID of the product to delete.
        synchronous: Whether to delete synchronously (default True).
    """
    return await delete_product(product_id, synchronous)



@mcp.tool()
async def customer_send_account_invite_email_impl(customer_id: str) -> str:
    """
    Send an account invite email to a Shopify customer.

    Args:
        customer_id: The ID of the customer to invite (e.g., 'gid://shopify/Customer/105906728')

    Example:
        {
            "customerId": "gid://shopify/Customer/105906728"
        }
    """
    return await customer_send_account_invite_email(customer_id)

@mcp.tool()
async def customers_list_impl(
    first: int = 10,
    after: str = None,
    query: str = None,
    sort_key: str = None
) -> dict:
    """
    Retrieve a list of customers from the Shopify store.

    Args:
        first: The number of customers to retrieve (default: 10).
        after: The cursor for pagination (optional).
        query: A filter string using Shopify's search syntax (optional).
        sort_key: The field to sort by (optional, e.g., 'ID', 'LAST_NAME').

    Example:
        await customers_list_impl(first=5, query="country:canada")
    """
    return await customers_list(first=first, after=after, query=query, sort_key=sort_key)

@mcp.tool()
async def customers_count_impl(query: str = None, limit: int = 10000) -> int:
    """
    Retrieve the count of customers in the Shopify store.

    Args:
        query: A filter string using Shopify's search syntax (optional).
        limit: The upper bound on the count value before returning a result (default: 10000).

    Example:
        await customers_count_impl(query="country:canada")
    """
    return await customers_count(query=query, limit=limit)

@mcp.tool()
async def customer_get_impl(customer_id: str) -> dict:
    """
    Retrieve a customer by ID from the Shopify store.

    Args:
        customer_id: The ID of the customer to retrieve (e.g., 'gid://shopify/Customer/544365967')

    Example:
        await customer_get_impl("gid://shopify/Customer/544365967")
    """
    return await customer_get(customer_id)

@mcp.tool()
async def orders_list_impl(
    first: int = 10,
    after: str = None,
    query: str = None,
    sort_key: str = None
) -> dict:
    """
    Retrieve a list of orders from the Shopify store.

    Args:
        first: The number of orders to retrieve (default: 10).
        after: The cursor for pagination (optional).
        query: A filter string using Shopify's search syntax (optional).
        sort_key: The field to sort by (optional).

    Example:
        await orders_list_impl(first=5, query="created_at:>=2024-01-01")
    """
    return await orders_list(first=first, after=after, query=query, sort_key=sort_key)

@mcp.tool()
async def orders_count_impl(query: str = None, limit: int = 10000) -> int:
    """
    Retrieve the count of orders in the Shopify store.

    Args:
        query: A filter string using Shopify's search syntax (optional).
        limit: The upper bound on the count value before returning a result (default: 10000).

    Example:
        await orders_count_impl(query="created_at:>=2024-01-01")
    """
    return await orders_count(query=query, limit=limit)

@mcp.tool()
async def discount_codes_list_impl(first: int = 10, after: str = None, query: str = None) -> dict:
    """
    Retrieve a list of discount codes from the Shopify store.
    """
    return await discount_codes_list(first=first, after=after, query=query)

@mcp.tool()
async def discount_code_get_impl(discount_code_id: str) -> dict:
    """
    Retrieve a discount code by ID.
    """
    return await discount_code_get(discount_code_id)


@mcp.tool()
async def discount_code_delete_impl(discount_code_id: str) -> dict:
    """
    Delete a discount code by ID.
    """
    return await discount_code_delete(discount_code_id)

if __name__ == "__main__":
    logger.info("Starting Shopify MCP server...")
    mcp.run(transport='stdio')