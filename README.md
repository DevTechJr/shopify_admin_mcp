# Shopify Admin MCP Server (35 tools)

This project is a Claude-powered developer copilot tailored for Shopify merchants. It replicates and **extends** Shopify Sidekick with powerful multi-app integrations — Shopify Admin, Google Calendar, and Airtable — all wired through a Model Control Protocol (MCP) server.

<img width="1918" height="1078" alt="image" src="https://github.com/user-attachments/assets/0065aee5-9d44-4c69-a41f-a1e9cf48f673" />

> 🎥 **[Watch my demo video](https://youtu.be/QHsmf9cPQJc)** ← *(insert your demo link here)*

---

## 🛠️ Features

Claude understands your business context, talks to your tools, and helps you run your store with a mere prompt.

### 🔧 Supported Tools (35 Total)

Each tool is implemented on the Shopify MCP server and callable from Claude's agent. Here's a breakdown of the prominent ones:

#### Shopify Tools
##### Store Management:

- Store info and locations (2 tools)
- Navigation/menu management (2 tools)

##### Product & Inventory:

- Product CRUD operations (6 tools)
- Inventory management (2 tools)
- Product variant creation (1 tool)

##### Content Management:

- Blog management (5 tools)
- Article management (4 tools)
- Page management (4 tools)

##### Customer & Order Management:

- Customer operations (4 tools)
- Order management (2 tools)

##### Marketing:

- Discount code management (3 tools)
- Customer invitations (1 tool)

#### Calendar Tools (external mcp server)
- `getCalendars`
- `getEvents`
- `createEvent`

#### Airtable Tools (external mcp server)
- `syncInventoryToAirtable`
- `addRowToAirtable`
- `updateAirtableRow`
- `getAirtableInventoryTable`

#### Utility Tools (external mcp server)
- `generateChart`
- `generateCompetitorAnalysis`
- `generateProductIdeas`
- `suggestBundlesAndOffers`

---

## 🚀 Setup Guide

### 1. Clone the Repo

```bash
git clone [this repo url]
cd shopify_admin_mcp
```

### 2. Configure Your Shopify Admin

Open `utils/shopify_client.py` and set your credentials:

```python
SHOPIFY_STORE = "your-store-id.myshopify.com"
SHOPIFY_TOKEN = "your-admin-access-token"
API_VERSION = "2025-07"
```

### 3. Connect the Server to Claude Desktop

In your Claude Desktop `config.json`, add the following entry:

```json
"shopify_anidev": {
  "command": "uv",
  "args": [
    "--directory",
    "your-cloned-git-repo-path-in-files",
    "run",
    "server.py"
  ]
}
```

Make sure Claude Desktop has file access to this path.

### 4. Run the MCP Server

From the project root:

```bash
uv run server.py
```

Claude will now be able to call any of the above tools as an autonomous Shopify assistant.

---

## 🕹 Example Prompts to Try

- “Launch a new candle called Ocean Breeze. Draft product copy, research pricing, and visualize search trends.”
- “What’s running low in inventory? Sync it to my Airtable board.”
- “Create a launch event on my Google Calendar for this Friday.”
- “Add this new candle to the store's front page and blog.”
- “Suggest bundles or discounts for this product.”

---

## 📹 Video Demo

> 🕯️ *Watch the full walkthrough with examples of Claude launching a product, planning a campaign, syncing inventory, and managing content across platforms.*

👉 **[Click here to view the demo](https://youtu.be/QHsmf9cPQJc)**

---

## 📩 Questions or Feedback?

Feel free to open an issue or email [you@example.com]. Proudly built for the Shopify team with ❤️ by Anirudh.
