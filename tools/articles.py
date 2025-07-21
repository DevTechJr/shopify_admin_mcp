from utils.shopify_client import make_shopify_request
from utils.logger import logger

async def article_create(blog_id: str, title: str, body: str, author_name: str) -> str:
    """Create a new article within a blog.

    Args:
        blog_id: The ID of the blog to post in.
        title: Title of the article.
        body: HTML content.
        author_name: Name of the article author.
    """
    query = """
    mutation ArticleCreate($article: ArticleCreateInput!) {
      articleCreate(article: $article) {
        article {
          id
          title
          body
        }
        userErrors {
          field
          message
        }
      }
    }
    """
    article_input = {
        "blogId": blog_id,
        "title": title,
        "body": body,
        "author": {"name": author_name},  # ✅ fix: must be an object
        "isPublished": True               # ✅ optional, but good to set
    }

    try:
        res = await make_shopify_request(query, variables={"article": article_input})

        # ✅ Log top-level errors if present
        if "errors" in res:
            logger.error(f"Top-level Shopify errors: {res['errors']}")
            return f"GraphQL error: {res['errors'][0]['message']}"

        data = res.get("data", {}).get("articleCreate", {})
        if not data:
            return f"❌ Unexpected response: {res}"

        if data.get("userErrors"):
            errors = "\n".join(f"- {e['message']} (field: {e.get('field')})" for e in data["userErrors"])
            return f"❌ Failed to create article:\n{errors}"

        article = data.get("article")
        if not article:
            return "❌ Article creation failed: No article returned."

        return f"📝 Created article '{article['title']}' (ID: {article['id']})"

    except Exception as e:
        logger.error(f"article_create failed: {e}")
        return f"❌ Exception: {e}"


async def article_update(article_id: str, title: str, body: str) -> str:
    """Update an existing article.

    Args:
        article_id: The ID of the article to update.
        title: New title.
        body: New HTML content.
    """
    query = """
    mutation ArticleUpdate($id: ID!, $article: ArticleInput!) {
      articleUpdate(id: $id, article: $article) {
        article { id title body }
        userErrors { message }
      }
    }
    """
    try:
        res = await make_shopify_request(query, variables={"id": article_id, "article": {"title": title, "body": body}})
        a = res["data"]["articleUpdate"]["article"]
        return f"✏️ Updated article '{a['title']}' (ID: {a['id']})"
    except Exception as e:
        logger.error(f"article_update failed: {e}")
        return f"Error: {e}"


async def article_delete(article_id: str) -> str:
    """Delete an article.

    Args:
        article_id: The ID of the article to delete.
    """
    query = """
    mutation ArticleDelete($id: ID!) {
      articleDelete(id: $id) {
        deletedArticleId
        userErrors { message }
      }
    }
    """
    try:
        res = await make_shopify_request(query, variables={"id": article_id})
        deleted_id = res["data"]["articleDelete"]["deletedArticleId"]
        return f"🗑️ Deleted article (ID: {deleted_id})"
    except Exception as e:
        logger.error(f"article_delete failed: {e}")
        return f"Error: {e}"


async def get_articles_for_blog(blog_id: str, first_n: int = 5) -> str:
    """Retrieve articles from a specific blog.

    Args:
        blog_id: The ID of the blog.
        first_n: Number of articles to retrieve (default: 5)
    """
    query = """
    query GetArticles($id: ID!, $first: Int!) {
      blog(id: $id) {
        articles(first: $first) {
          nodes {
            id
            title
            body
          }
        }
      }
    }
    """
    try:
        res = await make_shopify_request(query, variables={"id": blog_id, "first": first_n})
        articles = res["data"]["blog"]["articles"]["nodes"]
        if not articles:
            return "No articles found in this blog."
        return "\n".join(f"{a['title']} (ID: {a['id']})" for a in articles)
    except Exception as e:
        logger.error(f"get_articles_for_blog failed: {e}")
        return f"Error: {e}"


async def get_article(article_id: str) -> str:
    """Get a single article by ID.

    Args:
        article_id: The ID of the article.
    """
    query = """
    query GetArticle($id: ID!) {
      article(id: $id) {
        id
        title
        body
        authorV2 { name }
        blog { id title }
      }
    }
    """
    try:
        res = await make_shopify_request(query, variables={"id": article_id})
        a = res["data"]["article"]
        return (
            f"📄 Article: {a['title']} (ID: {a['id']})\n"
            f"Author: {a['authorV2']['name']}\n"
            f"Blog: {a['blog']['title']}\n"
            f"Content Preview: {a['body'][:100]}..."
        )
    except Exception as e:
        logger.error(f"get_article failed: {e}")
        return f"Error: {e}"
