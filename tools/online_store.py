from utils.shopify_client import make_shopify_request
from utils.logger import logger

async def get_pages(first_n: int = 5) -> str:
    """Get online store pages from the Shopify store.

    Args:
        first_n: Number of pages to retrieve (default: 5)
    """
    query = """
    query GetPages($first: Int!) {
      pages(first: $first) {
        edges {
          node {
            id
            title
            handle
            publishedAt
          }
        }
      }
    }
    """
    try:
        res = await make_shopify_request(query, variables={"first": first_n})
        edges = res["data"]["pages"]["edges"]
        if not edges:
            return "No pages found."

        return "\n".join(
            f"{e['node']['title']} (/{e['node']['handle']}) – ID: {e['node']['id']}"
            for e in edges
        )
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
    """Create a new store page. If you execute this function, make sure to query the menu endpoint to find the menu and also update the menu (nav bar) to include the new page, based on its id.

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


async def get_page_html(page_id: str) -> str:
    """Fetch the HTML content of a Shopify page.

    Args:
        page_id: The ID of the page to fetch (format: gid://shopify/Page/<id>)
    """
    query = """
    query GetPageHtml($id: ID!) {
      page(id: $id) {
        id
        title
        body
        handle
      }
    }
    """
    try:
        variables = {"id": page_id}
        result = await make_shopify_request(query, variables)
        page = result.get("data", {}).get("page")

        if not page:
            return f"No page found with ID {page_id}."

        return (
            f"Page: {page['title']}\n"
            f"Handle: {page['handle']}\n"
            f"ID: {page['id']}\n"
            f"\nHTML Content:\n{page['body']}"
        )
    except Exception as e:
        logger.error(f"get_page_html failed: {e}")
        return f"Error: {e}"


async def update_page_html(page_id: str, new_html: str) -> str:
    """Update the HTML content of a Shopify page.

    Args:
        page_id: The ID of the page to update (format: gid://shopify/Page/<id>)
        new_html: The new HTML content to replace the existing body
    """
    mutation = """
    mutation UpdatePageHtml($id: ID!, $page: PageUpdateInput!) {
      pageUpdate(id: $id, page: $page) {
        page {
          id
          title
          body
        }
        userErrors {
          field
          message
        }
      }
    }
    """
    try:
        variables = {
            "id": page_id,
            "page": {
                "body": new_html
            }
        }
        result = await make_shopify_request(mutation, variables)
        data = result.get("data", {}).get("pageUpdate", {})

        if data.get("userErrors"):
            errors = "\n".join([f"- {e['message']} (field: {e.get('field')})" for e in data["userErrors"]])
            return f"Page update failed with errors:\n{errors}"

        page = data.get("page")
        if not page:
            return f"Page update failed: No page object returned. Raw response: {result}"

        return f"✅ Updated page '{page['title']}' (ID: {page['id']})"
    except Exception as e:
        logger.error(f"update_page_html failed: {e}")
        return f"Error: {e}"



async def page_delete(page_id: str) -> str:
    """Delete an online store page from the Shopify store.

    Args:
        page_id: The ID of the page to delete (e.g., 'gid://shopify/Page/123456789')
    """
    mutation = """
    mutation DeletePage($id: ID!) {
      pageDelete(id: $id) {
        deletedPageId
        userErrors {
          code
          field
          message
        }
      }
    }
    """
    try:
        res = await make_shopify_request(mutation, variables={"id": page_id})
        result = res["data"]["pageDelete"]
        deleted_id = result.get("deletedPageId")
        errors = result.get("userErrors", [])
        if errors:
            err_msgs = "; ".join(e["message"] for e in errors)
            return f"Page deletion failed: {err_msgs}"
        return f"Successfully deleted page with ID: {deleted_id}"
    except Exception as e:
        logger.error(f"page_delete failed: {e}")
        return f"Error: {e}"