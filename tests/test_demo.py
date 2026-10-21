# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Dr. Ravi Teja Thiriveedhi
"""Tests for demo/heartbeat_model.py (standard library unittest)."""
import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "demo"))
import heartbeat_model as hm  # noqa: E402


class Model(unittest.TestCase):
    def test_before_is_wakes_times_tokens(self):
        r = hm.model({"name": "a", "interval_min": 30, "tokens": 1000, "changed": 0.1})
        self.assertAlmostEqual(r.before, 48 * 1000)

    def test_methods_never_increase_tokens(self):
        for a in hm.EXAMPLE_FLEET:
            r = hm.model(a)
            self.assertLessEqual(r.after_interval, r.before)
            self.assertLessEqual(r.after_sentinel, r.after_interval)

    def test_sentinel_with_every_heartbeat_changing_saves_nothing(self):
        r = hm.model({"name": "busy", "interval_min": 30, "tokens": 1000, "changed": 1.0})
        self.assertAlmostEqual(r.after_sentinel, r.before)

    def test_own_fleet_file(self):
        fleet = [{"name": "x", "interval_min": 60, "tokens": 500, "changed": 0.5, "new_interval_min": 120}]
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as fh:
            json.dump(fleet, fh)
        with redirect_stdout(io.StringIO()) as out:
            self.assertEqual(hm.main(["x", "--fleet", fh.name]), 0)
        self.assertIn("fleet", out.getvalue())
        self.assertNotIn("invented", out.getvalue())

    def test_example_is_labelled_synthetic(self):
        with redirect_stdout(io.StringIO()) as out:
            hm.main(["x"])
        self.assertIn("synthetic, not real", out.getvalue())

    def test_what_if(self):
        with redirect_stdout(io.StringIO()):
            res = hm.what_if(60, 1000, 0.1, None)
        self.assertAlmostEqual(res["per_day"], 24 * 1000)
        self.assertAlmostEqual(res["gated"], 2400)


if __name__ == "__main__":
    unittest.main()
