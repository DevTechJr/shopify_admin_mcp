from mcp.server.fastmcp import FastMCP
from tools.inventory import get_inventory_items
from tools.products import get_products, get_product, create_product, update_product, delete_product, create_product_variants
from tools.online_store import get_pages, page_create, get_page_html, update_page_html, page_delete, get_shopify_store_info, get_shopify_locations
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
    discount_codes_list, discount_code_get, discount_code_delete)
import json

mcp = FastMCP("shopify_anidev")

@mcp.tool()
async def get_shopify_store_info_impl() -> str:
    """Get information about the Shopify store."""
    info = await get_shopify_store_info()
    return str(info)

import json

@mcp.tool()
async def get_shopify_locations_impl(first: int = 50) -> str:
    """
    Get a list of locations from the Shopify store.

    Args:
        first (int): The number of locations to fetch (default: 50, max: 250).

    Returns:
        str: JSON string of locations or error message.
    """
    locations = await get_shopify_locations(first)
    return json.dumps(locations, indent=2)

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
async def create_product_variants_impl(
    product_id: str,
    variants: list,
    media: list = None,
    strategy: str = "DEFAULT"
) -> str:
    """
    Create one or more product variants for an existing Shopify product, setting price and inventory.
    Make sure you have the product_id and location_id to set inventory quantities.

    Args:
        product_id (str): The Shopify GID of the product to add variants to.
        variants (list): List of variant dicts. Each variant can include:
            - price (float or str): The price for the variant.
            - compareAtPrice (float or str, optional): The compare-at price.
            - optionValues (list[dict]): Required if the product has any options (e.g. 'Title').
                Example:
                [
                    {
                        "name": "Title",
                        "value": "Small",
                        "optionId": "gid://shopify/ProductOption/123456789"
                    }
                ]
            - inventoryQuantities (list[dict], optional): List of inventory quantities per location:
                [{ "availableQuantity": 10, "locationId": "gid://shopify/Location/123" }]
            - sku (str, optional): SKU for the variant.
            - barcode (str, optional): Barcode for the variant.
            - taxable (bool, optional): Whether the variant is taxable.
            - inventoryPolicy (str, optional): Inventory policy ("DENY" or "CONTINUE").
            - metafields (list[dict], optional): Metafields for the variant.
        media (list, optional): List of CreateMediaInput objects to associate with the product or variants.
        strategy (str, optional): Bulk create strategy. Default is "DEFAULT".

        Example:
        variants = [
    {
        "price": 15.99,
        "compareAtPrice": 19.99,
        "optionValues": [
            {"name": "Golden", "optionId": "gid://shopify/ProductOption/328272167"}
        ],
        "inventoryQuantities": [
            {"availableQuantity": 10, "locationId": "gid://shopify/Location/123"}
        ]
    }
]

Example input mutation:

{
  "productId": "gid://shopify/Product/7837358293103",
  "variants": [
    {
      "price": 10,
      "optionValues": [
        {
          "name": "Default Title",
          "optionName": "Title"
        }
      ],
      "inventoryQuantities": [
        {
          "locationId": "gid://shopify/Location/73769451631",
          "availableQuantity": 20
        }
      ]
    }
  ]
}


    Returns:
        str: Success message with variant IDs or error message(s).
    """
    return await create_product_variants(product_id, variants, media, strategy)

@mcp.tool()
async def create_product_impl(product: dict, media: list = None) -> str:
    """
    Create a new Shopify product with optional media attachments.

    Args:
        product (dict): A dictionary containing product details. Must follow Shopify's ProductInput format.
            Required keys:
                - title (str): Name of the product.
            Optional keys:
                - descriptionHtml (str): HTML-formatted product description.
                - handle (str): Unique URL handle.
                - tags (list[str]): Product tags.
                - vendor (str): Product vendor name.
                - status (str): 'ACTIVE', 'DRAFT', or 'ARCHIVED'.
                - productOptions (list[dict]): List of option dictionaries:
                    Example: [{ "name": "Color", "values": ["Red", "Blue"] }]
        media (list, optional): List of CreateMediaInput objects.
            Example:
                [
                    {
                        "mediaContentType": "IMAGE",
                        "originalSource": "https://example.com/image.png",
                        "alt": "Product image"
                    }
                ]

    Returns:
        str: Success message with product ID or error message(s).
    """
    return await create_product(product, media)


@mcp.tool()
async def update_product_impl(product: dict, media: list = None) -> str:
    """
    Update an existing Shopify product with optional new media attachments.

    Args:
        product (dict): A dictionary of fields to update for the product. Must include:
            - id (str): The Shopify GID of the product to update (e.g., "gid://shopify/Product/123456789").
            Optional keys:
                - title (str): New product title.
                - descriptionHtml (str): HTML-formatted product description.
                - handle (str): Unique URL handle.
                - tags (list[str]): Product tags (overwrites all existing tags).
                - vendor (str): Product vendor name.
                - status (str): 'ACTIVE', 'DRAFT', or 'ARCHIVED'.
                - productType (str): The product type.
                - metafields (list[dict]): List of metafields to update.
                - seo (dict): SEO title and description.
                - templateSuffix (str): Theme template for the product.
                - productOptions (list[dict]): List of option dictionaries:
                    Example: [{ "name": "Color", "values": ["Red", "Blue"] }]
                - requiresSellingPlan (bool): Whether the product is subscription-only.
                - redirectNewHandle (bool): Whether to redirect the old handle to the new one.
        media (list, optional): List of CreateMediaInput objects to add to the product.
            Each item should be a dict with:
                - mediaContentType (str): e.g., "IMAGE", "EXTERNAL_VIDEO"
                - originalSource (str): URL of the media file
                - alt (str, optional): Alt text for the media

    Returns:
        str: Success message with product ID or error message(s).
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