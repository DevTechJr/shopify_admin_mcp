from utils.shopify_client import make_shopify_request
from utils.logger import logger

async def get_inventory_items(first_n: int = 5) -> str:
    """Get inventory items from the Shopify store.

    Args:
        first_n: Number of items to retrieve (default: 5)
    """
    query = """
    query inventoryItems($first: Int!) {
        inventoryItems(first: $first) {
            edges {
                node {
                    id
                    tracked
                    sku
                    createdAt
                    updatedAt
                    inventoryLevels(first: 1) {
                        edges {
                            node {
                                available
                            }
                        }
                    }
                }
            }
        }
    }
    """
    try:
        result = await make_shopify_request(query, variables={"first": first_n})
        items = result.get('data', {}).get('inventoryItems', {}).get('edges', [])
        if not items:
            return "No inventory items found."
        formatted = []
        for item in items:
            node = item['node']
            stock = node.get('inventoryLevels', {}).get('edges', [{}])[0].get('node', {}).get('available', 'N/A')
            formatted.append(
                f"SKU: {node.get('sku', 'N/A')}\n"
                f"Tracked: {'Yes' if node['tracked'] else 'No'}\n"
                f"Stock: {stock}\n"
                f"Last Updated: {node['updatedAt']}\n"
                f"ID: {node['id'].split('/')[-1]}"
            )
        return "\n---\n".join(formatted)
    except Exception as e:
        logger.error(f"Inventory fetch failed: {str(e)}")
        return f"Error: {str(e)}"
