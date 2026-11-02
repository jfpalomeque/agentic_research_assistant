"""Offline tests for the literature skill's Crossref helper."""

import contextlib
import io
import json
import unittest
from unittest.mock import patch
from urllib.error import HTTPError

import crossref


class CrossrefTests(unittest.TestCase):
    def test_doi_normalization(self):
        self.assertEqual(crossref.normalize_doi("https://doi.org/10.1007%2Fs10816-022-09559-5"),
                         "10.1007/s10816-022-09559-5")
        with self.assertRaises(ValueError):
            crossref.normalize_doi("https://example.org/10.1000/test")

    def test_markup_preserves_inline_text(self):
        self.assertEqual(crossref.plain_text("<jats:p><jats:sup>14</jats:sup>C &amp; rice</jats:p><jats:p>Next.</jats:p>"),
                         "14C & rice Next.")

    @patch("crossref.fetch")
    def test_search_and_get(self, fetch):
        item = {"DOI": "10.1000/test", "title": ["Example"], "author": [{"family": "Crema"}],
                "abstract": "<jats:p>Example abstract.</jats:p>"}
        fetch.return_value = {"message": {"total-results": 2, "items": [item]}}
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self.assertEqual(crossref.main(["search", "--author", "Crema", "--year", "2022"]), 0)
        result = json.loads(output.getvalue())
        self.assertEqual(result["total_results"], 2)
        self.assertNotIn("abstract", result["candidates"][0])
        self.assertIn("from-pub-date", result["source"]["request_url"])
        fetch.return_value = {"message": item}
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self.assertEqual(crossref.main(["get", "10.1000/test"]), 0)
        self.assertEqual(json.loads(output.getvalue())["record"]["abstract"], "Example abstract.")

    @patch("crossref.fetch", side_effect=HTTPError("url", 404, "Not Found", {}, None))
    def test_missing_doi_reports_error(self, _fetch):
        with contextlib.redirect_stderr(io.StringIO()) as errors:
            self.assertEqual(crossref.main(["get", "10.1000/missing"]), 1)
        self.assertIn("404", errors.getvalue())


if __name__ == "__main__":
    unittest.main()
