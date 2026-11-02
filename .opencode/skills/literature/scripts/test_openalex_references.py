"""Offline tests for backward citation export."""

import contextlib
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

import openalex_references as exporter


class ReferenceTests(unittest.TestCase):
    def run_export(self, seed, batches, crossref=None):
        folder = tempfile.TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        root = Path(folder.name)
        raw = root / "raw"
        raw.mkdir()
        output = root / "references.bib"
        argv = ["openalex_references.py", "W1", "--workdir", str(raw), "--output", str(output)]
        with patch.object(sys, "argv", argv), patch.object(exporter, "request_json", side_effect=[seed] + batches), \
             patch.object(exporter, "crossref_record", return_value=crossref), contextlib.redirect_stdout(io.StringIO()):
            code = exporter.main()
        return code, output, json.loads((raw / "manifest.json").read_text())

    def test_export_and_doi_comparison(self):
        seed = {"id": "https://openalex.org/W1", "doi": "https://doi.org/10.1000/seed", "referenced_works_count": 2,
                "referenced_works": ["https://openalex.org/W2", "https://openalex.org/W3"]}
        works = [{"id": "https://openalex.org/W2", "doi": "https://doi.org/10.1000/ABC", "title": "One"},
                 {"id": "https://openalex.org/W3", "title": "Two"}]
        crossref = ("url", {"message": {"reference-count": 2, "reference": [{"DOI": "10.1000/abc"}, {"year": "2000"}]}})
        status, output, result = self.run_export(seed, [{"results": works}], crossref)
        self.assertEqual(status, 0)
        self.assertEqual(output.read_text().count("@misc{"), 2)
        self.assertEqual(result["crossref_comparison"]["unique_dois_matching_openalex"], 1)
        self.assertEqual(result["missing_doi"], 1)

    def test_missing_linked_work_is_incomplete(self):
        seed = {"id": "https://openalex.org/W1", "referenced_works": ["https://openalex.org/W2"]}
        status, output, result = self.run_export(seed, [{"results": []}])
        self.assertEqual(status, 1)
        self.assertEqual(result["unresolved_ids"], ["https://openalex.org/W2"])
        self.assertTrue(output.exists())

    def test_missing_reference_field_is_not_empty_success(self):
        status, output, result = self.run_export({"id": "https://openalex.org/W1"}, [])
        self.assertEqual(status, 1)
        self.assertFalse(output.exists())
        self.assertIn("error", result)

    def test_reference_ids_are_batched(self):
        works = [{"id": f"https://openalex.org/W{i}", "title": str(i)} for i in range(2, 103)]
        seed = {"id": "https://openalex.org/W1", "referenced_works": [w["id"] for w in works],
                "referenced_works_count": 101}
        status, output, result = self.run_export(seed, [{"results": works[:100]}, {"results": works[100:]}])
        self.assertEqual(status, 0)
        self.assertEqual([b["requested"] for b in result["batches"]], [100, 1])
        self.assertEqual(output.read_text().count("@misc{"), 101)


if __name__ == "__main__":
    unittest.main()
