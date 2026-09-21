"""
Tests for the main session scenarios: resting, moderate, high,
recovery, and poor-quality data, all sourced from the instructor's
data_generator.py through sample_data.py.

Run with: python3 -m unittest tests.py -v
"""

import unittest

from models import Participant, Session
from analyzer import SessionAnalyzer
import sample_data


class TestSessionAnalyzer(unittest.TestCase):
    def _run(self, label, profile, raw_observations):
        participant = Participant.from_profile(profile)
        session = Session(participant=participant, label=label)
        session.add_observations_from_dicts(raw_observations)
        return SessionAnalyzer.analyze(session)

    def test_resting_session(self):
        profile, raw_observations = sample_data.resting_session_data()
        result = self._run("resting", profile, raw_observations)
        self.assertEqual(result["classification"], "resting")
        self.assertEqual(result["usable_observations"], result["total_observations"])
        self.assertFalse(result["recovery_detected"])

    def test_moderate_activity_session(self):
        profile, raw_observations = sample_data.moderate_activity_data()
        result = self._run("moderate", profile, raw_observations)
        self.assertEqual(result["classification"], "moderate activity")

    def test_high_activity_session(self):
        profile, raw_observations = sample_data.high_activity_data()
        result = self._run("high", profile, raw_observations)
        self.assertEqual(result["classification"], "high activity")

    def test_activity_then_recovery(self):
        profile, raw_observations = sample_data.activity_then_recovery_data()
        result = self._run("recovery", profile, raw_observations)
        self.assertTrue(result["recovery_detected"])
        self.assertEqual(result["classification"], "recovering")

    def test_poor_quality_data(self):
        profile, raw_observations = sample_data.poor_quality_data()
        result = self._run("poor quality", profile, raw_observations)
        # The generator corrupts every window in this scenario, so
        # every observation should end up flagged.
        self.assertEqual(result["usable_observations"], 0)
        self.assertEqual(result["classification"], "insufficient data")
        self.assertEqual(len(result["flagged_issues"]), result["total_observations"])


if __name__ == "__main__":
    unittest.main()
