from utils.shopify_client import make_shopify_request
from utils.logger import logger


async def update_menu(menu_id: str, title: str, handle: str, items: list) -> str:
    """Update an existing menu on the Shopify store.

    Args:
        menu_id: The ID of the menu to update.
        title: New title for the menu.
        handle: New handle (slug) for the menu.
        items: A list of menu items in MenuItemUpdateInput format.
    """
    mutation = """
    mutation UpdateMenu($id: ID!, $title: String!, $handle: String!, $items: [MenuItemUpdateInput!]!) {
      menuUpdate(id: $id, title: $title, handle: $handle, items: $items) {
        menu {
          id
          handle
          items {
            id
            title
            items {
              id
              title
            }
          }
        }
        userErrors {
          message
          field
        }
      }
    }
    """

    try:
        variables = {
            "id": menu_id,
            "title": title,
            "handle": handle,
            "items": items
        }

        result = await make_shopify_request(mutation, variables=variables)
        data = result.get("data", {}).get("menuUpdate", {})

        if data.get("userErrors"):
            error_messages = "\n".join([
                f"- Field: {e.get('field', 'unknown')}, Message: {e['message']}"
                for e in data["userErrors"]
            ])
            return f"Menu update failed with errors:\n{error_messages}"

        menu = data.get("menu")
        if not menu:
            return "Menu update returned no menu object."

        return f"✅ Updated menu '{menu['handle']}' (ID: {menu['id']}) with {len(menu['items'])} top-level items."

    except Exception as e:
        logger.error(f"update_menu failed: {e}")
        return f"Error: {e}"


async def get_menus() -> str:
    """Get the store’s single menu and its details.

    This fetches the first available menu and returns its items and metadata.
    """
    get_id_query = """
    query {
      menus(first: 1) {
        edges {
          node {
            id
          }
        }
      }
    }
    """

    get_menu_by_id_query = """
    query GetMenu($id: ID!) {
      menu(id: $id) {
        id
        title
        handle
        items {
          id
          title
          type
          url
          items {
            id
            title
            type
            url
          }
        }
      }
    }
    """

    try:
        # Step 1: Get the first menu ID
        id_result = await make_shopify_request(get_id_query)
        edges = id_result.get("data", {}).get("menus", {}).get("edges", [])
        if not edges:
            return "No menus found in the store."

        menu_id = edges[0]["node"]["id"]

        # Step 2: Fetch full menu by ID
        menu_result = await make_shopify_request(get_menu_by_id_query, variables={"id": menu_id})
        menu = menu_result.get("data", {}).get("menu", None)
        if not menu:
            return "Menu not found or could not be fetched."

        def render_items(items, indent=2):
            lines = []
            for item in items:
                prefix = " " * indent + f"- {item['title']} ({item['type']}): {item.get('url', 'N/A')}"
                lines.append(prefix)
                if item.get("items"):
                    lines.extend(render_items(item["items"], indent + 2))
            return lines

        items_str = "\n".join(render_items(menu.get("items", []))) or "  - No items"

        return (
            f"Menu: {menu['title']}\n"
            f"Handle: {menu['handle']}\n"
            f"ID: {menu['id']}\n"
            f"Items:\n{items_str}"
        )

    except Exception as e:
        logger.error(f"get_menus failed: {e}")
        return f"Error: {e}"