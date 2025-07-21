from utils.shopify_client import make_shopify_request
from utils.logger import logger

async def get_blogs(first_n: int = 5) -> str:
    """Get blogs from the Shopify store, including their full GIDs.

    Args:
        first_n: Number of blogs to retrieve (default: 5)
    """
    query = """
    query GetBlogs($first: Int!) {
      blogs(first: $first) {
        nodes {
          id
          title
          handle
          updatedAt
          commentPolicy
          createdAt
          templateSuffix
          tags
        }
      }
    }
    """
    try:
        res = await make_shopify_request(query, variables={"first": first_n})
        blogs = res["data"]["blogs"]["nodes"]
        if not blogs:
            return "No blogs found."
        return "\n".join(
            f"{b['title']} (/{b['handle']}) - ID: {b['id']}" for b in blogs
        )
    except Exception as e:
        logger.error(f"get_blogs failed: {e}")
        return f"Error: {e}"

async def get_blog_by_id(blog_id: str) -> str:
    """Retrieve a single blog by its Shopify GID.

    Args:
        blog_id: The full Shopify GID (e.g., gid://shopify/Blog/123456789)
    """
    query = """
    query BlogByID($id: ID!) {
      blog(id: $id) {
        id
        title
        handle
        commentPolicy
        createdAt
        updatedAt
        templateSuffix
        tags
      }
    }
    """
    try:
        res = await make_shopify_request(query, variables={"id": blog_id})
        blog = res["data"]["blog"]
        if not blog:
            return f"Blog not found for ID: {blog_id}"
        return (
            f"📝 Blog: {blog['title']}\n"
            f"- Handle: /{blog['handle']}\n"
            f"- ID: {blog['id']}\n"
            f"- Comment Policy: {blog['commentPolicy']}\n"
            f"- Created: {blog['createdAt']}\n"
            f"- Updated: {blog['updatedAt']}\n"
            f"- Template: {blog.get('templateSuffix') or 'None'}\n"
            f"- Tags: {', '.join(blog['tags']) if blog['tags'] else 'None'}"
        )
    except Exception as e:
        logger.error(f"get_blog_by_id failed: {e}")
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

async def blog_update(blog_id: str, title: str) -> str:
    """Update the title of an existing blog.

    Args:
        blog_id: The ID of the blog to update.
        title: The new title for the blog.
    """
    query = """
    mutation BlogUpdate($id: ID!, $blog: BlogInput!) {
      blogUpdate(id: $id, blog: $blog) {
        blog { id title }
        userErrors { message }
      }
    }
    """
    try:
        res = await make_shopify_request(query, variables={"id": blog_id, "blog": {"title": title}})
        b = res["data"]["blogUpdate"]["blog"]
        return f"✅ Blog updated: '{b['title']}' (ID: {b['id']})"
    except Exception as e:
        logger.error(f"blog_update failed: {e}")
        return f"Error: {e}"


async def blog_delete(blog_id: str) -> str:
    """Delete a blog from the Shopify store.

    Args:
        blog_id: The ID of the blog to delete.
    """
    query = """
    mutation BlogDelete($id: ID!) {
      blogDelete(id: $id) {
        deletedBlogId
        userErrors { message }
      }
    }
    """
    try:
        res = await make_shopify_request(query, variables={"id": blog_id})
        deleted_id = res["data"]["blogDelete"]["deletedBlogId"]
        return f"🗑️ Blog deleted: ID {deleted_id}"
    except Exception as e:
        logger.error(f"blog_delete failed: {e}")
        return f"Error: {e}"


