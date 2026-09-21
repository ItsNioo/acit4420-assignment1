"""
Wraps the instructor-supplied data_generator.py with one fixed seed per
scenario, so main.py and tests.py always see the same reproducible data
for the five required cases. This file does not implement any of the
data itself, it only chooses which generator scenario and seed to use.

Each function returns (profile, observations) exactly as
generate_fitness_data() does.
"""

from data_generator import generate_fitness_data

WINDOWS_PER_SESSION = 8


def resting_session_data():
    return generate_fitness_data(
        participant_id="P001", scenario="resting", seed=1,
        number_of_windows=WINDOWS_PER_SESSION,
    )


def moderate_activity_data():
    return generate_fitness_data(
        participant_id="P002", scenario="moderate_activity", seed=2,
        number_of_windows=WINDOWS_PER_SESSION,
    )


def high_activity_data():
    return generate_fitness_data(
        participant_id="P003", scenario="high_activity", seed=3,
        number_of_windows=WINDOWS_PER_SESSION,
    )


def activity_then_recovery_data():
    return generate_fitness_data(
        participant_id="P004", scenario="recovery", seed=4,
        number_of_windows=WINDOWS_PER_SESSION,
    )


def poor_quality_data():
    return generate_fitness_data(
        participant_id="P005", scenario="poor_quality", seed=5,
        number_of_windows=WINDOWS_PER_SESSION,
    )
