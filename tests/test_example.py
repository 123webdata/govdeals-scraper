import unittest
from types import SimpleNamespace
from example import run_example


class ExampleTests(unittest.TestCase):
    def test_runs_the_published_actor_and_reads_a_bounded_dataset_page(self):
        calls = []

        class Actor:
            def call(self, *, run_input):
                calls.append(("call", run_input))
                return SimpleNamespace(status="SUCCEEDED", default_dataset_id="dataset-1")

        class Dataset:
            def list_items(self, *, limit):
                calls.append(("list_items", limit))
                return SimpleNamespace(items=[{"url": "https://example.com/item"}])

        class Client:
            def actor(self, actor_id):
                calls.append(("actor", actor_id))
                return Actor()

            def dataset(self, dataset_id):
                calls.append(("dataset", dataset_id))
                return Dataset()

        items = run_example(Client(), "https://prod-seo.govdeals.com/automobiles-cars")
        self.assertEqual(items, [{"url": "https://example.com/item"}])
        self.assertEqual(calls, [
            ("actor", "123webdata/govdeals-scraper"),
            ("call", {"categoryUrls": ["https://prod-seo.govdeals.com/automobiles-cars"], "maxResultsPerScrape": 10, "usePagination": False, "scrapeProductDetails": False}),
            ("dataset", "dataset-1"),
            ("list_items", 5),
        ])

    def test_refuses_to_read_results_from_a_failed_run(self):
        class Client:
            def actor(self, actor_id):
                return SimpleNamespace(call=lambda **kwargs: SimpleNamespace(status="FAILED", default_dataset_id="dataset-1"))

            def dataset(self, dataset_id):
                raise AssertionError("dataset must not be read after failure")

        with self.assertRaisesRegex(RuntimeError, "FAILED"):
            run_example(Client(), "https://prod-seo.govdeals.com/automobiles-cars")


if __name__ == "__main__":
    unittest.main()
