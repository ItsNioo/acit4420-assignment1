"""
Calculation and reporting logic for a session: summarizing readings,
classifying intensity, checking for recovery, and formatting a report.
"""

from statistics import mean
from models import Session, Observation

# Thresholds for classification, expressed as how far average heart
# rate sits above the participant's own baseline (the generator only
# gives us a resting baseline, not a max heart rate, so classification
# is offset-based rather than a fraction of some maximum).
MIN_OBSERVATIONS_FOR_CLASSIFICATION = 3
RESTING_HR_OFFSET = 15          # resting if avg HR <= baseline + this many bpm
RESTING_ACTIVITY_CEILING = 0.30
MODERATE_HR_OFFSET = 45         # moderate if avg HR <= baseline + this many bpm
RECOVERY_WINDOW_FRACTION = 0.5      # compare first half vs second half
RECOVERY_HR_DROP_FRACTION = 0.10    # >=10% HR drop counts as recovering
RECOVERY_ACTIVITY_DROP_FRACTION = 0.20


def summarize_values(values: list[float]) -> dict:
    """Return average/minimum/maximum for a list of numeric values."""
    if not values:
        return {"average": None, "minimum": None, "maximum": None}
    return {
        "average": round(mean(values), 2),
        "minimum": round(min(values), 2),
        "maximum": round(max(values), 2),
    }


def detect_recovery(valid_observations: list[Observation]) -> bool:
    """
    Compare the first half of the session against the second half. If
    heart rate and activity level both dropped noticeably, treat that
    as the participant recovering by the end.
    """
    n = len(valid_observations)
    if n < 4:
        return False

    ordered = sorted(valid_observations, key=lambda o: o.timestamp)
    split = max(1, int(n * RECOVERY_WINDOW_FRACTION))
    first_half, second_half = ordered[:split], ordered[split:]
    if not first_half or not second_half:
        return False

    first_hr = mean(o.heart_rate for o in first_half)
    second_hr = mean(o.heart_rate for o in second_half)
    first_activity = mean(o.activity_level for o in first_half)
    second_activity = mean(o.activity_level for o in second_half)

    hr_drop = (first_hr - second_hr) / first_hr if first_hr else 0
    activity_drop = (
        (first_activity - second_activity) / first_activity if first_activity else 0
    )

    return hr_drop >= RECOVERY_HR_DROP_FRACTION and activity_drop >= RECOVERY_ACTIVITY_DROP_FRACTION


def classify_intensity(
    valid_observations: list[Observation],
    baseline_heart_rate: float,
) -> str:
    """
    Work out whether a session was resting, moderate, high intensity,
    recovering, or too short to say anything about, based on how far
    average heart rate sits above the participant's own baseline.
    """
    if len(valid_observations) < MIN_OBSERVATIONS_FOR_CLASSIFICATION:
        return "insufficient data"

    if detect_recovery(valid_observations):
        return "recovering"

    avg_hr = mean(o.heart_rate for o in valid_observations)
    avg_activity = mean(o.activity_level for o in valid_observations)

    if avg_hr <= baseline_heart_rate + RESTING_HR_OFFSET and avg_activity <= RESTING_ACTIVITY_CEILING:
        return "resting"
    if avg_hr <= baseline_heart_rate + MODERATE_HR_OFFSET:
        return "moderate activity"
    return "high activity"


def format_console_report(result: dict) -> str:
    """Turn the structured result dict into a readable console report."""
    lines = [
        "=" * 60,
        f"Session report: {result['participant_name']} - {result['session_label']}",
        "=" * 60,
        f"Observations used: {result['usable_observations']} / {result['total_observations']}",
        f"Classification:     {result['classification']}",
        f"Recovery detected:  {result['recovery_detected']}",
        "",
        "Heart rate (bpm):",
        f"  avg={result['heart_rate_summary']['average']}  "
        f"min={result['heart_rate_summary']['minimum']}  "
        f"max={result['heart_rate_summary']['maximum']}",
        "Activity level (0-1):",
        f"  avg={result['activity_summary']['average']}  "
        f"min={result['activity_summary']['minimum']}  "
        f"max={result['activity_summary']['maximum']}",
    ]
    if result["flagged_issues"]:
        lines.append("")
        lines.append(f"Flagged/invalid observations: {len(result['flagged_issues'])}")
        for i, issues in enumerate(result["flagged_issues"], start=1):
            lines.append(f"  #{i}: {', '.join(issues)}")
    lines.append("=" * 60)
    return "\n".join(lines)


class SessionAnalyzer:
    """Turns a Session into one structured result dict."""

    @staticmethod
    def analyze(session: Session) -> dict:
        """Build the summary/classification result for one session."""
        valid = session.valid_observations
        heart_rates = [o.heart_rate for o in valid]
        activity_levels = [o.activity_level for o in valid]

        classification = classify_intensity(
            valid,
            session.participant.baseline_heart_rate,
        )
        recovery = detect_recovery(valid)

        return {
            "participant_name": session.participant.name,
            "session_label": session.label,
            "total_observations": session.total_count,
            "usable_observations": session.valid_count,
            "heart_rate_summary": summarize_values(heart_rates),
            "activity_summary": summarize_values(activity_levels),
            "classification": classification,
            "recovery_detected": recovery,
            "flagged_issues": [
                obs.issues for obs in session.observations if not obs.is_valid
            ],
        }
