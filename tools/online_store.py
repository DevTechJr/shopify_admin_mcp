from utils.shopify_client import make_shopify_request
from utils.logger import logger

async def get_pages(first_n: int = 5) -> str:
    """Get online store pages from the Shopify store.

    Args:
        first_n: Number of pages to retrieve (default: 5)
    """
    query = """
    query pages($first: Int!) {
      pages(first: $first) {
        edges { node { id title handle publishedAt } }
      }
    }
    """
    try:
        res = await make_shopify_request(query, variables={"first": first_n})
        nodes = res["data"]["pages"]["edges"]
        return "\n".join(f"{n['node']['title']} (/{n['node']['handle']})" for n in nodes)
    except Exception as e:
        logger.error(f"get_pages failed: {e}")
        return f"Error: {e}"
    

  
async def page_create(
    title: str,
    handle: str,
    body: str,
    is_published: bool = True,
    template_suffix: str = "custom"
) -> str:
    """Create a new store page. If you execute this function, make sure to query the menu endpoint to  find the menu and also update the menu (nav bar) to include the new page, based on its id.

    Args:
        title: Title of the page.
        handle: URL handle (slug).
        body: HTML content.
        isPublished: Whether the page should be published immediately (true).
        templateSuffix: Optional template suffix (default: "custom").
    """
    query = """
    mutation CreatePage($page: PageCreateInput!) {
      pageCreate(page: $page) {
        page {
          id
          title
          handle
        }
        userErrors {
          code
          field
          message
        }
      }
    }
    """
    variables = {
        "page": {
            "title": title,
            "handle": handle,
            "body": body,
            "isPublished": is_published,
            "templateSuffix": template_suffix
        }
    }

    try:
        res = await make_shopify_request(query, variables=variables)
        page_data = res["data"]["pageCreate"]["page"]
        errors = res["data"]["pageCreate"]["userErrors"]

        if errors:
            formatted_errors = "\n".join(
                f"- {e['message']} (field: {e.get('field', 'N/A')})"
                for e in errors
            )
            return f"Page creation failed with errors:\n{formatted_errors}"

        return f"Created page '{page_data['title']}' (ID: {page_data['id']})"

    except Exception as e:
        logger.error(f"page_create failed: {e}")
        return f"Error: {e}"
