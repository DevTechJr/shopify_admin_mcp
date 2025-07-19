import requests

def query_shopify_inventory_items(store_url, access_token, first_n=2):
    url = f"https://{store_url}/admin/api/2025-07/graphql.json"
    headers = {
        "Content-Type": "application/json",
        "X-Shopify-Access-Token": access_token
    }
    query = f"""
    query inventoryItems {{
        inventoryItems(first: {first_n}) {{
            edges {{
                node {{
                    id
                    tracked
                    sku
                }}
            }}
        }}
    }}
    """
    payload = {"query": query}
    
    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Query failed with status {response.status_code}: {response.text}")


try:
    result = query_shopify_inventory_items(store, token)
    print(result)
except Exception as e:
    print(e)
