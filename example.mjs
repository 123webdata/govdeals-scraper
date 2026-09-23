/** Run the 123webdata/govdeals-scraper Actor on one category URL. */
import { resolve } from 'node:path';
import { pathToFileURL } from 'node:url';

export const ACTOR_ID = '123webdata/govdeals-scraper';
export const DEFAULT_CATEGORY_URL = 'https://prod-seo.govdeals.com/automobiles-cars';

export async function runExample(client, categoryUrl) {
  const run = await client.actor(ACTOR_ID).call({
    categoryUrls: [categoryUrl],
    maxResultsPerScrape: 10,
    usePagination: false,
    scrapeProductDetails: false,
  });
  if (!run || run.status !== 'SUCCEEDED') {
    throw new Error(`Actor run ended with status ${run?.status ?? 'UNKNOWN'}`);
  }
  const { items } = await client.dataset(run.defaultDatasetId).listItems({ limit: 5 });
  return items;
}

if (process.argv[1] && import.meta.url === pathToFileURL(resolve(process.argv[1])).href) {
  if (!process.env.APIFY_TOKEN) {
    console.error('Set APIFY_TOKEN before running this example.');
    process.exitCode = 1;
  } else {
    const { ApifyClient } = await import('apify-client');
    const client = new ApifyClient({ token: process.env.APIFY_TOKEN });
    const categoryUrl = process.argv[2] || DEFAULT_CATEGORY_URL;
    console.log(JSON.stringify(await runExample(client, categoryUrl), null, 2));
  }
}
