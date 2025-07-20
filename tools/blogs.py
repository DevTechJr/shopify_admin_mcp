from utils.shopify_client import make_shopify_request
from utils.logger import logger

async def get_blogs(first_n: int = 5) -> str:
    """Get blogs from the Shopify store.

    Args:
        first_n: Number of blogs to retrieve (default: 5)
    """
    query = """
    query blogs($first: Int!) {
      blogs(first: $first) {
        nodes { id title handle updatedAt }
      }
    }
    """
    try:
        res = await make_shopify_request(query, variables={"first": first_n})
        blogs = res["data"]["blogs"]["nodes"]
        if not blogs:
            return "No blogs found."
        return "\n".join(f"{b['title']} (/{b['handle']})" for b in blogs)
    except Exception as e:
        logger.error(f"get_blogs failed: {e}")
        return f"Error: {e}"

async def blog_create(title: str, handle: str, comment_policy: str = "MODERATED") -> str:
    """Create a new blog.

    Args:
        title: Title of the blog.
        handle: URL handle.
        comment_policy: Comment policy.
    """
    query = """
    mutation BlogCreate($blog: BlogCreateInput!) {
      blogCreate(blog: $blog) {
        blog { id title handle }
        userErrors { message }
      }
    }
    """
    try:
        res = await make_shopify_request(query, variables={"blog": {"title": title, "handle": handle, "commentPolicy": comment_policy}})
        b = res["data"]["blogCreate"]["blog"]
        return f"Created blog '{b['title']}' (ID: {b['id']})"
    except Exception as e:
        logger.error(f"blog_create failed: {e}")
        return f"Error: {e}"
