from utils.shopify_client import make_shopify_request
from utils.logger import logger

async def discount_codes_list(first: int = 10, after: str = None, query: str = None) -> dict:
    """
    Retrieve a list of discount codes from the Shopify store.
    """
    query_str = """
    query DiscountCodesList($first: Int, $after: String, $query: String) {
      codeDiscountNodes(first: $first, after: $after, query: $query) {
        nodes {
          id
          codeDiscount {
            ... on DiscountCodeBasic {
              title
              summary
            }
            ... on DiscountCodeBxgy {
              title
              codesCount {
                count
              }
            }
          }
        }
        pageInfo {
          hasNextPage
          endCursor
        }
      }
    }
    """
    variables = {k: v for k, v in {"first": first, "after": after, "query": query}.items() if v is not None}
    try:
        res = await make_shopify_request(query_str, variables=variables)
        return res["data"]["codeDiscountNodes"]
    except Exception as e:
        logger.error(f"discount_codes_list failed: {e}")
        return {"error": str(e)}

async def discount_code_get(discount_node_id: str) -> dict:
    """
    Retrieve a discount code node by ID.
    """
    query_str = """
    query DiscountCodeGet($id: ID!) {
      codeDiscountNode(id: $id) {
        id
        codeDiscount {
          ... on DiscountCodeBasic {
            title
            summary
            codes(first: 1) {
              nodes {
                code
                id
              }
            }
          }
        }
      }
    }
    """
    try:
        res = await make_shopify_request(query_str, variables={"id": discount_node_id})
        return res["data"]["codeDiscountNode"]
    except Exception as e:
        logger.error(f"discount_code_get failed: {e}")
        return {"error": str(e)}

async def discount_code_delete(discount_code_id: str) -> dict:
    """
    Delete a discount code by ID.
    """
    mutation = """
    mutation DiscountCodeDelete($id: ID!) {
      discountCodeDelete(id: $id) {
        deletedDiscountCodeId
        userErrors {
          field
          message
        }
      }
    }
    """
    try:
        res = await make_shopify_request(mutation, variables={"id": discount_code_id})
        return res["data"]["discountCodeDelete"]
    except Exception as e:
        logger.error(f"discount_code_delete failed: {e}")
        return {"error": str(e)}