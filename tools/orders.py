from utils.shopify_client import make_shopify_request
from utils.logger import logger

async def orders_list(
    first: int = 10,
    after: str = None,
    query: str = None,
    sort_key: str = None
) -> dict:
    """
    Retrieve a list of orders from the Shopify store.

    Args:
        first: The number of orders to retrieve.
        after: The cursor for pagination.
        query: A filter string using Shopify's search syntax.
        sort_key: The field to sort by.
    """
    query_str = """
    query OrdersList($first: Int, $after: String, $query: String, $sortKey: OrderSortKeys) {
      orders(first: $first, after: $after, query: $query, sortKey: $sortKey) {
        edges {
          cursor
          node {
            id
            name
            createdAt
            totalPriceSet {
              shopMoney {
                amount
                currencyCode
              }
            }
            customer {
              id
              firstName
              lastName
              email
            }
            lineItems(first: 10) {
              edges {
                node {
                  title
                  quantity
                  price
                }
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
    variables = {
        "first": first,
        "after": after,
        "query": query,
        "sortKey": sort_key
    }
    variables = {k: v for k, v in variables.items() if v is not None}
    try:
        res = await make_shopify_request(query_str, variables=variables)
        return res["data"]["orders"]
    except Exception as e:
        logger.error(f"orders_list failed: {e}")
        return {"error": str(e)}
    

async def orders_count(query: str = None, limit: int = 10000) -> int:
    """
    Retrieve the count of orders in the Shopify store.

    Args:
        query: A filter string using Shopify's search syntax.
        limit: The upper bound on the count value before returning a result.
    """
    query_str = """
    query OrdersCount($query: String, $limit: Int) {
      ordersCount(query: $query, limit: $limit) {
        count
      }
    }
    """
    variables = {
        "query": query,
        "limit": limit
    }
    variables = {k: v for k, v in variables.items() if v is not None}
    try:
        res = await make_shopify_request(query_str, variables=variables)
        return res["data"]["ordersCount"]["count"]
    except Exception as e:
        logger.error(f"orders_count failed: {e}")
        return -1
    
