# GovDeals scraper examples

Need a small GovDeals dataset for an auction watchlist? These examples run a category scrape and print five records so you can see the shape of the output before building a larger workflow.

The examples use [the GovDeals Actor](https://apify.com/123webdata/govdeals-scraper?fpr=9lmok3) published by 123webdata on Apify. That link includes an affiliate tracking code; the full URL is `https://apify.com/123webdata/govdeals-scraper?fpr=9lmok3`. Running the Actor may use paid Apify resources.

## Get set up

You need Python 3.11+ for the Python client or Node.js 20+ for the JavaScript example.

1. Create an [Apify account](https://console.apify.com/sign-up), then copy your token from **API & Integrations** in Apify Console. Keep the token out of Git.
2. Open a terminal in this repository and set `APIFY_TOKEN` for that session:

   ```bash
   export APIFY_TOKEN='paste-your-token-here'
   ```

3. Pick Python or JavaScript:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   python example.py
   ```

   ```bash
   npm install
   node example.mjs
   ```

The default is the automobiles category. Pass another GovDeals category URL after `example.py` or `example.mjs`. Both scripts request at most ten category records and print the first five JSON items. They stop if the Actor run fails.

## Use it from chat

`mcp.example.json` is a remote MCP config. In Cursor, save a copy as `.cursor/mcp.json` (merge its server entry if you already have that file), restart Cursor, and sign in to Apify when prompted. The config limits the tool list to this Actor and contains no token.

Try asking:

- “Run GovDeals Scraper on the automobiles category and show me five listings with their URLs and prices.”
- “Collect ten GovDeals listings from this category URL, then tell me which fields I could use for an auction watchlist.”

The MCP server can run the Actor and read its dataset. As with the scripts, an Actor run can incur charges. Review the Actor's input and pricing before scaling up.

## Check the examples

Run `python3 -m unittest discover -s tests -v` and `npm test`. The tests use fake Apify clients, so they do not start a paid scrape.
