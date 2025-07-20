from utils.shopify_client import make_shopify_request
from utils.logger import logger

async def discount_codes_list(first: int = 10, after: str = None, query: str = None) -> dict:
    """
    Retrieve a list of discount codes from the Shopify store.
    """
    query_str = """
    query DiscountCodesList($first: Int, $after: String, $query: String) {
      discountCodes(first: $first, after: $after, query: $query) {
        edges {
          cursor
          node {
            id
            code
            usageCount
            startsAt
            endsAt
            status
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
        return res["data"]["discountCodes"]
    except Exception as e:
        logger.error(f"discount_codes_list failed: {e}")
        return {"error": str(e)}

async def discount_code_get(discount_code_id: str) -> dict:
    """
    Retrieve a discount code by ID.
    """
    query_str = """
    query DiscountCodeGet($id: ID!) {
      discountCode(id: $id) {
        id
        code
        usageCount
        startsAt
        endsAt
        status
      }
    }
    """
    try:
        res = await make_shopify_request(query_str, variables={"id": discount_code_id})
        return res["data"]["discountCode"]
    except Exception as e:
        logger.error(f"discount_code_get failed: {e}")
        return {"error": str(e)}

async def discount_code_create(code: str, starts_at: str, ends_at: str = None) -> dict:
    """
    Create a new discount code.
    """
    mutation = """
    mutation DiscountCodeCreate($code: String!, $startsAt: DateTime!, $endsAt: DateTime) {
      discountCodeCreate(input: {
        code: $code,
        startsAt: $startsAt,
        endsAt: $endsAt
      }) {
        discountCode {
          id
          code
          startsAt
          endsAt
          status
        }
        userErrors {
          field
          message
        }
      }
    }
    """
    variables = {"code": code, "startsAt": starts_at, "endsAt": ends_at}
    variables = {k: v for k, v in variables.items() if v is not None}
    try:
        res = await make_shopify_request(mutation, variables=variables)
        return res["data"]["discountCodeCreate"]
    except Exception as e:
        logger.error(f"discount_code_create failed: {e}")
        return {"error": str(e)}

async def discount_code_update(discount_code_id: str, code: str = None, ends_at: str = None) -> dict:
    """
    Update an existing discount code.
    """
    mutation = """
    mutation DiscountCodeUpdate($id: ID!, $code: String, $endsAt: DateTime) {
      discountCodeUpdate(id: $id, input: {
        code: $code,
        endsAt: $endsAt
      }) {
        discountCode {
          id
          code
          startsAt
          endsAt
          status
        }
        userErrors {
          field
          message
        }
      }
    }
    """
    variables = {"id": discount_code_id, "code": code, "endsAt": ends_at}
    variables = {k: v for k, v in variables.items() if v is not None}
    try:
        res = await make_shopify_request(mutation, variables=variables)
        return res["data"]["discountCodeUpdate"]
    except Exception as e:
        logger.error(f"discount_code_update failed: {e}")
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