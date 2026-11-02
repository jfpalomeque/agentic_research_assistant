"""Offline tests for OpenAlex citation export."""

import contextlib
import io
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

import openalex_citations as exporter


def work(number):
    return {"id": f"https://openalex.org/W{number}", "title": "Crops & 14C",
            "type": "article", "publication_year": 2022,
            "authorships": [{"author": {"display_name": "Jane Doe"}}]}


class ExportTests(unittest.TestCase):
    def test_bibtex_escapes_and_preserves_titles(self):
        text = exporter.bibtex(work(1))
        self.assertIn(r"title = {{Crops \& 14C}}", text)
        self.assertIn("author = {{Jane Doe}}", text)

    def run_export(self, payloads, key=None):
        folder = tempfile.TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        root = Path(folder.name)
        workdir = root / "raw"
        workdir.mkdir()
        output = root / "result.bib"
        argv = ["openalex_citations.py", "10.1000/test", "--workdir", str(workdir), "--output", str(output)]
        environment = {"OPENALEX_API_KEY": key} if key else {}
        with patch.dict(os.environ, environment, clear=True), patch.object(sys, "argv", argv), \
             patch.object(exporter, "request_json", side_effect=payloads), contextlib.redirect_stdout(io.StringIO()):
            status = exporter.main()
        return status, output, json.loads((workdir / "manifest.json").read_text())

    def test_complete_export(self):
        seed = {"id": "https://openalex.org/W1", "title": "Seed"}
        status, output, manifest = self.run_export([seed, {"meta": {"count": 1}, "results": [work(2)]}])
        self.assertEqual(status, 0)
        self.assertTrue(manifest["complete"])
        self.assertIn("@article{W2,", output.read_text())

    def test_count_mismatch_reports_incomplete(self):
        seed = {"id": "https://openalex.org/W1"}
        status, output, manifest = self.run_export([seed, {"meta": {"count": 2}, "results": [work(2)]}])
        self.assertEqual(status, 1)
        self.assertTrue(output.exists())
        self.assertFalse(manifest["complete"])

    def test_large_result_requires_key(self):
        seed = {"id": "https://openalex.org/W1"}
        status, output, manifest = self.run_export([seed, {"meta": {"count": 10001}, "results": [work(2)]}])
        self.assertEqual(status, 1)
        self.assertFalse(output.exists())
        self.assertIn("OPENALEX_API_KEY", manifest["error"])


if __name__ == "__main__":
    unittest.main()
