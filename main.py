"""
Builds a test participant, runs each sample session through the
analyzer, and prints a report for each one.
"""

from models import Participant, Session
from analyzer import SessionAnalyzer, format_console_report
import sample_data


def build_participant() -> Participant:
    return Participant(
        name="Test Participant",
        person_id="P-001",
        resting_heart_rate=65,
        max_heart_rate=190,
        typical_activity_level=0.30,
    )


def run_scenario(participant: Participant, label: str, raw_observations: list[dict]) -> None:
    session = Session(participant=participant, label=label)
    session.add_observations_from_dicts(raw_observations)

    result = SessionAnalyzer.analyze(session)
    print(format_console_report(result))
    print()


def main() -> None:
    participant = build_participant()

    scenarios = [
        ("Resting session", sample_data.resting_session_data()),
        ("Moderate activity session", sample_data.moderate_activity_data()),
        ("High activity session", sample_data.high_activity_data()),
        ("Activity followed by recovery", sample_data.activity_then_recovery_data()),
        ("Poor-quality / invalid data", sample_data.poor_quality_data()),
    ]

    for label, raw_observations in scenarios:
        run_scenario(participant, label, raw_observations)


if __name__ == "__main__":
    main()
