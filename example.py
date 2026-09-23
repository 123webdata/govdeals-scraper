"""Run the 123webdata/govdeals-scraper Actor on one category URL."""

import argparse
import json
import os

ACTOR_ID = "123webdata/govdeals-scraper"
DEFAULT_CATEGORY_URL = "https://prod-seo.govdeals.com/automobiles-cars"


def run_example(client, category_url):
    run = client.actor(ACTOR_ID).call(run_input={
        "categoryUrls": [category_url],
        "maxResultsPerScrape": 10,
        "usePagination": False,
        "scrapeProductDetails": False,
    })
    if run is None or run.status != "SUCCEEDED":
        raise RuntimeError(f"Actor run ended with status {getattr(run, 'status', 'UNKNOWN')}")
    return client.dataset(run.default_dataset_id).list_items(limit=5).items


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("category_url", nargs="?", default=DEFAULT_CATEGORY_URL)
    args = parser.parse_args()
    token = os.environ.get("APIFY_TOKEN")
    if not token:
        raise SystemExit("Set APIFY_TOKEN before running this example.")
    from apify_client import ApifyClient

    print(json.dumps(run_example(ApifyClient(token=token), args.category_url), indent=2))


if __name__ == "__main__":
    main()
