from utils.shopify_client import make_shopify_request
from utils.logger import logger

async def customer_send_account_invite_email(customer_id: str) -> str:
    """
    Send an account invite email to a Shopify customer.

    Args:
        customer_id: The ID of the customer to invite (e.g., 'gid://shopify/Customer/105906728')
    """
    mutation = """
    mutation CustomerSendAccountInviteEmail($customerId: ID!) {
      customerSendAccountInviteEmail(customerId: $customerId) {
        customer {
          id
        }
        userErrors {
          field
          message
        }
      }
    }
    """
    try:
        res = await make_shopify_request(mutation, variables={"customerId": customer_id})
        result = res["data"]["customerSendAccountInviteEmail"]
        customer = result.get("customer")
        errors = result.get("userErrors", [])
        if errors:
            err_msgs = "; ".join(e["message"] for e in errors)
            return f"Account invite failed: {err_msgs}"
        return f"Successfully sent account invite to customer ID: {customer['id'] if customer else customer_id}"
    except Exception as e:
        logger.error(f"customer_send_account_invite_email failed: {e}")
        return f"Error: {e}"
    
async def customers_list(
    first: int = 10,
    after: str = None,
    query: str = None,
    sort_key: str = None
) -> dict:
    """
    Retrieve a list of customers from the Shopify store.

    Args:
        first: The number of customers to retrieve.
        after: The cursor for pagination.
        query: A filter string using Shopify's search syntax.
        sort_key: The field to sort by.
    """
    query_str = """
    query CustomersList($first: Int, $after: String, $query: String, $sortKey: CustomerSortKeys) {
      customers(first: $first, after: $after, query: $query, sortKey: $sortKey) {
        edges {
          cursor
          node {
            id
            firstName
            lastName
            email
            createdAt
            updatedAt
            numberOfOrders
            amountSpent {
              amount
              currencyCode
            }
            tags
            defaultAddress {
              address1
              city
              province
              country
              zip
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
    # Remove None values for cleaner requests
    variables = {k: v for k, v in variables.items() if v is not None}
    try:
        res = await make_shopify_request(query_str, variables=variables)
        return res["data"]["customers"]
    except Exception as e:
        logger.error(f"customers_list failed: {e}")
        return {"error": str(e)}
    
async def customers_count(query: str = None, limit: int = 10000) -> int:
    """
    Retrieve the count of customers in the Shopify store.

    Args:
        query: A filter string using Shopify's search syntax.
        limit: The upper bound on the count value before returning a result.
    """
    query_str = """
    query CustomersCount($query: String, $limit: Int) {
      customersCount(query: $query, limit: $limit) {
        count
      }
    }
    """
    variables = {
        "query": query,
        "limit": limit
    }
    # Remove None values for cleaner requests
    variables = {k: v for k, v in variables.items() if v is not None}
    try:
        res = await make_shopify_request(query_str, variables=variables)
        return res["data"]["customersCount"]["count"]
    except Exception as e:
        logger.error(f"customers_count failed: {e}")
        return -1
    
async def customer_get(customer_id: str) -> dict:
    """
    Retrieve a customer by ID from the Shopify store.

    Args:
        customer_id: The ID of the customer to retrieve.
    """
    query_str = """
    query CustomerGet($id: ID!) {
      customer(id: $id) {
        id
        firstName
        lastName
        email
        phone
        numberOfOrders
        amountSpent {
          amount
          currencyCode
        }
        createdAt
        updatedAt
        tags
        defaultAddress {
          address1
          city
          province
          zip
          country
        }
      }
    }
    """
    variables = {"id": customer_id}
    try:
        res = await make_shopify_request(query_str, variables=variables)
        return res["data"]["customer"]
    except Exception as e:
        logger.error(f"customer_get failed: {e}")
        return {"error": str(e)}