import test from 'node:test';
import assert from 'node:assert/strict';
import { runExample } from '../example.mjs';

test('runs the published Actor and reads only five results', async () => {
  const calls = [];
  const client = {
    actor(actorId) {
      calls.push(['actor', actorId]);
      return { async call(input) {
        calls.push(['call', input]);
        return { status: 'SUCCEEDED', defaultDatasetId: 'dataset-1' };
      } };
    },
    dataset(datasetId) {
      calls.push(['dataset', datasetId]);
      return { async listItems(options) {
        calls.push(['listItems', options]);
        return { items: [{ url: 'https://example.com/item' }] };
      } };
    },
  };
  const items = await runExample(client, 'https://prod-seo.govdeals.com/automobiles-cars');
  assert.deepEqual(items, [{ url: 'https://example.com/item' }]);
  assert.deepEqual(calls, [
    ['actor', '123webdata/govdeals-scraper'],
    ['call', { categoryUrls: ['https://prod-seo.govdeals.com/automobiles-cars'], maxResultsPerScrape: 10, usePagination: false, scrapeProductDetails: false }],
    ['dataset', 'dataset-1'],
    ['listItems', { limit: 5 }],
  ]);
});

test('does not read a failed run dataset', async () => {
  const client = {
    actor: () => ({ call: async () => ({ status: 'FAILED', defaultDatasetId: 'dataset-1' }) }),
    dataset: () => { throw new Error('dataset must not be read after failure'); },
  };
  await assert.rejects(runExample(client, 'https://prod-seo.govdeals.com/automobiles-cars'), /FAILED/);
});
