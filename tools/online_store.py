from utils.shopify_client import make_shopify_request
from utils.logger import logger


async def get_shopify_store_info() -> dict:
    """
    Retrieve comprehensive Shopify store information.

    Returns:
        dict: Store info including name, description, emails, domains, currency, timezone, owner, and more.
    """
    query = """
    query GetShopInfo {
      shop {
        id
        name
        description
        email
        contactEmail
        url
        features {
          storefront
        }
      }
    }
    """
    try:
        res = await make_shopify_request(query)
        # Log the full response for debugging
        logger.info(f"Shopify response: {res}")
        if "errors" in res:
            return {"error": res["errors"]}
        if "data" not in res or "shop" not in res["data"]:
            return {"error": "Malformed response", "response": res}
        return res["data"]["shop"]
    except Exception as e:
        logger.error(f"get_shopify_store_info failed: {e}")
        return {"error": str(e)}
    
async def get_shopify_locations(first: int = 50) -> dict:
    """
    Retrieve a list of locations from the Shopify store.

    Args:
        first (int): The number of locations to fetch (default: 50, max: 250).

    Returns:
        dict: Dictionary containing a list of locations with their id, name, address, and more.
    """
    query = """
    query GetLocations($first: Int!) {
      locations(first: $first) {
        nodes {
          id
          name
          address {
            address1
            address2
            city
            province
            country
            zip
          }

        }
      }
    }
    """
    try:
        variables = {"first": first}
        res = await make_shopify_request(query, variables=variables)
        if "errors" in res:
            return {"error": res["errors"]}
        if "data" not in res or "locations" not in res["data"]:
            return {"error": "Malformed response", "response": res}
        return res["data"]["locations"]["nodes"]
    except Exception as e:
        logger.error(f"get_shopify_locations failed: {e}")
        return {"error": str(e)}


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

    
async def get_publications() -> list:
    """
    Retrieves all sales channel publications (e.g., Online Store) from the Shopify store.

    Returns:
        list: A list of dictionaries with 'id', 'name', and 'channel.handle' for each publication.
    """
    query = """
    query {
      publications(first: 20) {
        nodes {
          id
          name
          channel {
            handle
          }
        }
      }
    }
    """
    try:
        res = await make_shopify_request(query)
        publications = res["data"]["publications"]["nodes"]
        return [
            {
                "id": pub["id"],
                "name": pub["name"],
                "handle": pub["channel"]["handle"]
            }
            for pub in publications
        ]
    except Exception as e:
        logger.error(f"get_publications failed: {e}")
        return [{"error": str(e)}]


async def publish_product_to_online_store(product_id: str, publication_id: str) -> str:
    """
    Publishes a product to the Online Store sales channel using publishablePublish.

    Args:
        product_id (str): The GID of the product (e.g., "gid://shopify/Product/1234567890").
        publication_id (str): The GID of the publication (typically for Online Store).

    Returns:
        str: Success message with product ID and title, or error message.
    """
    mutation = """
    mutation PublishProduct($id: ID!, $publicationIds: [ID!]!) {
      publishablePublish(id: $id, input: { publicationIds: $publicationIds }) {
        publishable {
          ... on Product {
            id
            title
            publishedOnCurrentPublication
          }
        }
        userErrors {
          field
          message
        }
      }
    }
    """
    variables = {
        "id": product_id,
        "publicationIds": [publication_id]
    }

    try:
        res = await make_shopify_request(mutation, variables=variables)
        if "errors" in res:
            return f"GraphQL error: {res['errors']}"

        data = res["data"]["publishablePublish"]
        if data["userErrors"]:
            return "\n".join([f"- {e['field']}: {e['message']}" for e in data["userErrors"]])

        publishable = data["publishable"]
        return f"✅ Published product '{publishable['title']}' (ID: {publishable['id']})"
    except Exception as e:
        logger.error(f"publish_product_to_online_store failed: {e}")
        return f"Error: {e}"

async def is_product_published_on_publication(product_id: str, publication_id: str) -> bool:
    """
    Check if a product is published on a specific sales channel/publication.

    Args:
        product_id (str): The Shopify GID of the product.
        publication_id (str): The Shopify GID of the publication (sales channel).

    Returns:
        bool: True if published on the specified publication, False otherwise.
    """
    query = """
    query ProductShow($id: ID!, $publicationId: ID!) {
      product(id: $id) {
        id
        title
        publishedOnPublication(publicationId: $publicationId)
      }
    }
    """
    variables = {"id": product_id, "publicationId": publication_id}
    res = await make_shopify_request(query, variables=variables)
    if "errors" in res:
        raise Exception(f"GraphQL error: {res['errors']}")
    if "data" not in res or "product" not in res["data"]:
        raise Exception(f"Malformed response: {res}")
    product = res["data"]["product"]
    return product["publishedOnPublication"]
  
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