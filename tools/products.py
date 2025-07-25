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
                    id
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
                f"  - {v['node']['title']} (${v['node']['price']}) [SKU: {v['node']['sku'] or 'N/A'}]" 
                for v in node['variants']['edges']
            )
            formatted.append(
                f"🛍️ Product: {node['title']}\n"
                f"🆔 ID: {node['id']}\n"
                f"🔗 Handle: {node['handle']}\n"
                f"📦 Status: {node['status']} | Inventory: {node['totalInventory']}\n"
                f"🧵 Variants:\n{variants}\n"
                f"🌐 URL: https://{node['handle']}\n"
            )
        return "\n\n".join(formatted)
    except Exception as e:
        logger.error(f"get_products failed: {str(e)}")
        return f"Error: {str(e)}"


async def get_product(product_id: str) -> str:
    query = """
    query GetProduct($id: ID!) {
      product(id: $id) {
        id
        title
        descriptionHtml
        handle
        metafields(first: 5) {
          edges {
            node {
              namespace
              key
              value
            }
          }
        }
      }
    }
    """
    try:
        res = await make_shopify_request(query, variables={"id": product_id})
        p = res["data"]["product"]
        metafields = p.get("metafields", {}).get("edges", [])
        meta_str = "\n".join(f"- {m['node']['namespace']}:{m['node']['key']} = {m['node']['value']}" for m in metafields)
        return f"{p['title']}\nID: {p['id']}\nHandle: {p['handle']}\nDescription: {p['descriptionHtml']}\nMetafields:\n{meta_str or 'None'}"
    except Exception as e:
        logger.error(f"get_product failed: {e}")
        return f"Error: {e}"

async def create_product(product: dict, media: list = None) -> str:
    mutation = """
    mutation ProductCreate($input: ProductInput!, $media: [CreateMediaInput!]) {
      productCreate(input: $input, media: $media) {
        product {
          id
          title
        }
        userErrors {
          field
          message
        }
      }
    }
    """

    # Clean up productOptions if provided
    if "productOptions" in product:
        for option in product["productOptions"]:
            if "values" in option:
                option["values"] = [{"name": v} for v in option["values"]]

    try:
        variables = {
            "input": product,
            "media": media or []
        }
        res = await make_shopify_request(mutation, variables=variables)
        if "errors" in res:
            return f"GraphQL error: {res['errors']}"
        if "data" not in res or "productCreate" not in res["data"]:
            return f"Malformed response: {res}"
        data = res["data"]["productCreate"]
        if data["userErrors"]:
            return "\n".join([f"- {e['field']}: {e['message']}" for e in data["userErrors"]])
        return f"✅ Created product '{data['product']['title']}' (ID: {data['product']['id']})"
    except Exception as e:
        logger.error(f"create_product failed: {e}")
        return f"Error: {e}"




async def update_product(product: dict, media: list = None) -> str:
    """
    Core logic for updating a Shopify product via the Admin GraphQL API.

    Args:
        product (dict): Product update fields (must include 'id').
        media (list, optional): List of CreateMediaInput dicts.

    Returns:
        str: Success or error message.
    """
    mutation = """
    mutation UpdateProductWithNewMedia($product: ProductUpdateInput!, $media: [CreateMediaInput!]) {
      productUpdate(product: $product, media: $media) {
        product {
          id
          title
          media(first: 10) {
            nodes {
              alt
              mediaContentType
              preview {
                status
              }
            }
          }
        }
        userErrors {
          field
          message
        }
      }
    }
    """
    try:
        variables = {"product": product, "media": media or []}
        res = await make_shopify_request(mutation, variables=variables)
        if "errors" in res:
            return f"GraphQL error: {res['errors']}"
        if "data" not in res or "productUpdate" not in res["data"]:
            return f"Malformed response: {res}"
        data = res["data"]["productUpdate"]
        if data["userErrors"]:
            return "\n".join([f"- {e['field']}: {e['message']}" for e in data["userErrors"]])
        product_info = data["product"]
        return f"✅ Updated product '{product_info['title']}' (ID: {product_info['id']})"
    except Exception as e:
        logger.error(f"update_product failed: {e}")
        return f"Error: {e}"
    
    
async def delete_product(product_id: str, synchronous: bool = True) -> str:
    mutation = """
    mutation DeleteProduct($input: ProductDeleteInput!, $sync: Boolean) {
      productDelete(input: $input, synchronous: $sync) {
        deletedProductId
        userErrors { field message }
      }
    }
    """
    try:
        variables = {"input": {"id": product_id}, "sync": synchronous}
        res = await make_shopify_request(mutation, variables=variables)
        data = res["data"]["productDelete"]
        if data["userErrors"]:
            return "\n".join([f"- {e['field']}: {e['message']}" for e in data["userErrors"]])
        return f"🗑️ Deleted product ID: {data['deletedProductId']}"
    except Exception as e:
        logger.error(f"delete_product failed: {e}")
        return f"Error: {e}"
    
async def create_product_variants(
    product_id: str,
    variants: list,
    media: list = None,
    strategy: str = "DEFAULT"
) -> str:
    """
    Create one or more product variants for an existing Shopify product, setting price and inventory.

    Args:
        product_id (str): The Shopify GID of the product to add variants to (e.g., "gid://shopify/Product/123456789").
        variants (list): List of variant dicts. Each variant can include:
            - price (float or str): The price for the variant.
            - compareAtPrice (float or str, optional): The compare-at price.
            - optionValues (list[dict], optional): List of option values, e.g.:
                [{ "name": "Color", "optionId": "gid://shopify/ProductOption/123" }]
            - inventoryQuantities (list[dict], optional): List of inventory quantities per location:
                [{ "availableQuantity": 10, "locationId": "gid://shopify/Location/123" }]
            - sku (str, optional): SKU for the variant.
            - barcode (str, optional): Barcode for the variant.
            - taxable (bool, optional): Whether the variant is taxable.
            - inventoryPolicy (str, optional): Inventory policy ("DENY" or "CONTINUE").
            - metafields (list[dict], optional): Metafields for the variant.
        media (list, optional): List of CreateMediaInput objects to associate with the product or variants.
        strategy (str, optional): Bulk create strategy. Default is "DEFAULT".

    Returns:
        str: Success message with variant IDs or error message(s).
    """
 
    mutation = """
mutation ProductVariantsBulkCreate(
  $productId: ID!,
  $variants: [ProductVariantsBulkInput!]!,
  $media: [CreateMediaInput!],
  $strategy: ProductVariantsBulkCreateStrategy
) {
  productVariantsBulkCreate(
    productId: $productId,
    variants: $variants,
    media: $media,
    strategy: $strategy
  ) {
    productVariants {
      id
      title
      price
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
            "productId": product_id,
            "variants": variants,
            "media": media or [],
            "strategy": strategy
        }
        res = await make_shopify_request(mutation, variables=variables)
        if "errors" in res:
            return f"GraphQL error: {res['errors']}"
        if "data" not in res or "productVariantsBulkCreate" not in res["data"]:
            return f"Malformed response: {res}"
        data = res["data"]["productVariantsBulkCreate"]
        if data["userErrors"]:
            return "\n".join([f"- {e['field']}: {e['message']}" for e in data["userErrors"]])
        variants_info = data["productVariants"]
        variant_ids = [v["id"] for v in variants_info]
        return f"✅ Created variants: {variant_ids}"
    except Exception as e:
        logger.error(f"create_product_variants failed: {e}")
        return f"Error: {e}"