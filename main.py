"""
Runs each sample session through the analyzer and prints a report for
each one. Each scenario has its own generated participant, since
generate_fitness_data() returns a fresh profile alongside its
observations.
"""

from models import Participant, Session
from analyzer import SessionAnalyzer, format_console_report
import sample_data


def run_scenario(label: str, profile: dict, raw_observations: list) -> None:
    participant = Participant.from_profile(profile)
    session = Session(participant=participant, label=label)
    session.add_observations_from_dicts(raw_observations)

    result = SessionAnalyzer.analyze(session)
    print(format_console_report(result))
    print()


def main() -> None:
    scenarios = [
        ("Resting session", sample_data.resting_session_data()),
        ("Moderate activity session", sample_data.moderate_activity_data()),
        ("High activity session", sample_data.high_activity_data()),
        ("Activity followed by recovery", sample_data.activity_then_recovery_data()),
        ("Poor-quality / invalid data", sample_data.poor_quality_data()),
    ]

    for label, (profile, raw_observations) in scenarios:
        run_scenario(label, profile, raw_observations)


if __name__ == "__main__":
    main()
