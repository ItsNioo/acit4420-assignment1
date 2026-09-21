"""
Sample observation data covering the main cases: a resting session,
moderate activity, high activity, a session that ends in recovery, and
one full of bad/missing sensor readings.
"""


def resting_session_data() -> list[dict]:
    return [
        {"timestamp": t, "heart_rate": hr, "skin_response": 1.1, "temperature": 33.0,
         "activity_level": act, "signal_quality": 0.95}
        for t, hr, act in [
            (1, 62, 0.05), (2, 64, 0.06), (3, 63, 0.05),
            (4, 65, 0.07), (5, 63, 0.06), (6, 64, 0.05),
        ]
    ]


def moderate_activity_data() -> list[dict]:
    return [
        {"timestamp": t, "heart_rate": hr, "skin_response": 2.0, "temperature": 33.8,
         "activity_level": act, "signal_quality": 0.92}
        for t, hr, act in [
            (1, 112, 0.42), (2, 118, 0.45), (3, 115, 0.44),
            (4, 120, 0.48), (5, 117, 0.46), (6, 119, 0.47),
        ]
    ]


def high_activity_data() -> list[dict]:
    return [
        {"timestamp": t, "heart_rate": hr, "skin_response": 3.4, "temperature": 34.5,
         "activity_level": act, "signal_quality": 0.9}
        for t, hr, act in [
            (1, 150, 0.75), (2, 158, 0.80), (3, 162, 0.83),
            (4, 170, 0.88), (5, 168, 0.86), (6, 172, 0.89),
        ]
    ]


def activity_then_recovery_data() -> list[dict]:
    # First half: high intensity. Second half: heart rate and activity
    # both decline noticeably -> should trigger detect_recovery().
    high_part = [
        {"timestamp": t, "heart_rate": hr, "skin_response": 3.0, "temperature": 34.2,
         "activity_level": act, "signal_quality": 0.91}
        for t, hr, act in [
            (1, 160, 0.80), (2, 165, 0.84), (3, 168, 0.85), (4, 170, 0.87),
        ]
    ]
    recovering_part = [
        {"timestamp": t, "heart_rate": hr, "skin_response": 1.8, "temperature": 33.6,
         "activity_level": act, "signal_quality": 0.93}
        for t, hr, act in [
            (5, 140, 0.55), (6, 120, 0.35), (7, 100, 0.20), (8, 85, 0.12),
        ]
    ]
    return high_part + recovering_part


def poor_quality_data() -> list[dict]:
    return [
        # Missing a required field.
        {"timestamp": 1, "heart_rate": 118, "skin_response": 2.1,
         "temperature": 33.9, "activity_level": 0.5},
        # Impossible heart rate value.
        {"timestamp": 2, "heart_rate": 320, "skin_response": 2.0,
         "temperature": 33.9, "activity_level": 0.48, "signal_quality": 0.9},
        # Signal quality far too low to trust.
        {"timestamp": 3, "heart_rate": 115, "skin_response": 2.2,
         "temperature": 34.0, "activity_level": 0.46, "signal_quality": 0.1},
        # activity_level outside the valid 0-1 range.
        {"timestamp": 4, "heart_rate": 116, "skin_response": 2.1,
         "temperature": 34.0, "activity_level": 1.4, "signal_quality": 0.9},
        # One genuinely valid reading, so the session isn't 100% empty.
        {"timestamp": 5, "heart_rate": 117, "skin_response": 2.2,
         "temperature": 34.0, "activity_level": 0.47, "signal_quality": 0.92},
    ]
