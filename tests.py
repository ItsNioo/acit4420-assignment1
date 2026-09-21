"""
Tests for the main session scenarios: resting, moderate, high,
recovery, and poor-quality data.

Run with: python3 -m unittest tests.py -v
"""

import unittest

from models import Participant, Session
from analyzer import SessionAnalyzer
import sample_data


class TestSessionAnalyzer(unittest.TestCase):
    def setUp(self):
        self.participant = Participant(
            name="Test Participant",
            person_id="P-001",
            resting_heart_rate=65,
            max_heart_rate=190,
            typical_activity_level=0.30,
        )

    def _run(self, label, raw_observations):
        session = Session(participant=self.participant, label=label)
        session.add_observations_from_dicts(raw_observations)
        return SessionAnalyzer.analyze(session)

    def test_resting_session(self):
        result = self._run("resting", sample_data.resting_session_data())
        self.assertEqual(result["classification"], "resting")
        self.assertEqual(result["usable_observations"], result["total_observations"])
        self.assertFalse(result["recovery_detected"])

    def test_moderate_activity_session(self):
        result = self._run("moderate", sample_data.moderate_activity_data())
        self.assertEqual(result["classification"], "moderate activity")

    def test_high_activity_session(self):
        result = self._run("high", sample_data.high_activity_data())
        self.assertEqual(result["classification"], "high activity")

    def test_activity_then_recovery(self):
        result = self._run("recovery", sample_data.activity_then_recovery_data())
        self.assertTrue(result["recovery_detected"])
        self.assertEqual(result["classification"], "recovering")

    def test_poor_quality_data(self):
        result = self._run("poor quality", sample_data.poor_quality_data())
        self.assertLess(result["usable_observations"], result["total_observations"])
        self.assertEqual(result["classification"], "insufficient data")
        self.assertEqual(len(result["flagged_issues"]), 4)


if __name__ == "__main__":
    unittest.main()
