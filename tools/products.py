from utils.shopify_client import make_shopify_request
from utils.logger import logger

async def get_products(first_n: int = 3) -> str:
    """Get product listings from the Shopify store.

    Args:
        first_n: Number of products to retrieve (default: 3)
    """
    query = """
    query products($first: Int!) {
        products(first: $first) {
            edges {
                node {
                    title
                    handle
                    status
                    totalInventory
                    variants(first: 3) {
                        edges {
                            node {
                                title
                                price
                                sku
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
        products = result.get('data', {}).get('products', {}).get('edges', [])
        if not products:
            return "No products found."
        formatted = []
        for product in products:
            node = product['node']
            variants = "\n".join(
                f" - {v['node']['title']} (${v['node']['price']})" 
                for v in node['variants']['edges']
            )
            formatted.append(
                f"Product: {node['title']}\n"
                f"Status: {node['status']}\n"
                f"Total Inventory: {node['totalInventory']}\n"
                f"Variants:\n{variants}\n"
                f"URL: https://{node['handle']}"
            )
        return "\n\n".join(formatted)
    except Exception as e:
        logger.error(f"Products fetch failed: {str(e)}")
        return f"Error: {str(e)}"

