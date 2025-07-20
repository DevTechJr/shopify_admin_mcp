# utils/logger.py

import logging
import sys

# Create logger
logger = logging.getLogger("shopify-admin-mcp-logger")
logger.setLevel(logging.DEBUG)  # Set to INFO or WARNING in prod

# Avoid adding handlers multiple times (useful in notebooks, reloads)
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        fmt="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

