"""
Data classes for the fitness session analyzer.

Person and Participant model who is training. Observation is a single
reading from a wearable device during a session. Session ties a
participant to all the readings collected while they were training.
"""

# Roughly what's physiologically possible for these sensors. Values
# outside these ranges get flagged as bad readings.
MIN_HEART_RATE = 30
MAX_HEART_RATE = 220
MIN_TEMPERATURE = 25.0
MAX_TEMPERATURE = 42.0
MIN_SKIN_RESPONSE = 0.0
MAX_SKIN_RESPONSE = 60.0
MIN_SIGNAL_QUALITY_FOR_USE = 0.5  # below this, a reading is "poor quality"


class Person:
    """Minimal shared identity for anyone tracked by the system."""

    def __init__(self, name: str, person_id: str):
        self.name = name
        self.person_id = person_id

    def __str__(self) -> str:
        return f"{self.name} (ID: {self.person_id})"


class Participant(Person):
    """
    A person who trains, with the personal baseline values their
    sessions get compared against.
    """

    def __init__(
        self,
        name: str,
        person_id: str,
        resting_heart_rate: float,
        max_heart_rate: float,
        typical_activity_level: float,
    ):
        super().__init__(name, person_id)
        self.resting_heart_rate = resting_heart_rate
        self.max_heart_rate = max_heart_rate
        self.typical_activity_level = typical_activity_level

    def __str__(self) -> str:
        return (
            f"{self.name} (ID: {self.person_id}) | "
            f"resting HR: {self.resting_heart_rate} bpm, "
            f"max HR: {self.max_heart_rate} bpm, "
            f"typical activity: {self.typical_activity_level:.2f}"
        )

    def reference_summary(self) -> dict:
        """Return the participant's reference values as a plain dict."""
        return {
            "resting_heart_rate": self.resting_heart_rate,
            "max_heart_rate": self.max_heart_rate,
            "typical_activity_level": self.typical_activity_level,
        }


class Observation:
    """
    One measurement window from the wearable device. Validity is checked
    once when the object is created and cached in _is_valid, which is
    only meant to be read through the is_valid property below, not
    touched directly.
    """

    def __init__(
        self,
        timestamp,
        heart_rate,
        skin_response,
        temperature,
        activity_level,
        signal_quality,
    ):
        self.timestamp = timestamp
        self.heart_rate = heart_rate
        self.skin_response = skin_response
        self.temperature = temperature
        self.activity_level = activity_level
        self.signal_quality = signal_quality

        self.__is_valid = None
        self.__issues = []
        self.validate()

    @classmethod
    def from_dict(cls, data: dict) -> "Observation":
        """
        Build an Observation straight from a raw dict, e.g. from the
        data generator. Missing keys just come through as None instead
        of raising a KeyError, since a missing value is something
        validate() should catch and report, not something that should
        crash the program.
        """
        return cls(
            timestamp=data.get("timestamp"),
            heart_rate=data.get("heart_rate"),
            skin_response=data.get("skin_response"),
            temperature=data.get("temperature"),
            activity_level=data.get("activity_level"),
            signal_quality=data.get("signal_quality"),
        )

    @property
    def is_valid(self) -> bool:
        """Whether this reading passed validation."""
        if self.__is_valid is None:
            self.validate()
        return bool(self.__is_valid)

    @property
    def issues(self) -> list[str]:
        """Human-readable reasons this observation was flagged, if any."""
        return list(self.__issues)

    def validate(self) -> bool:
        """
        Check for missing, impossible or poor-quality values.
        Sets and returns self._is_valid.
        """
        issues: list[str] = []

        required = {
            "timestamp": self.timestamp,
            "heart_rate": self.heart_rate,
            "skin_response": self.skin_response,
            "temperature": self.temperature,
            "activity_level": self.activity_level,
            "signal_quality": self.signal_quality,
        }
        for field_name, value in required.items():
            if value is None:
                issues.append(f"missing {field_name}")

        # Only range-check fields that are actually present.
        if self.heart_rate is not None and not (
            MIN_HEART_RATE <= self.heart_rate <= MAX_HEART_RATE
        ):
            issues.append("heart_rate out of plausible range")

        if self.temperature is not None and not (
            MIN_TEMPERATURE <= self.temperature <= MAX_TEMPERATURE
        ):
            issues.append("temperature out of plausible range")

        if self.skin_response is not None and not (
            MIN_SKIN_RESPONSE <= self.skin_response <= MAX_SKIN_RESPONSE
        ):
            issues.append("skin_response out of plausible range")

        if self.activity_level is not None and not (0.0 <= self.activity_level <= 1.0):
            issues.append("activity_level outside 0-1")

        if self.signal_quality is not None and not (0.0 <= self.signal_quality <= 1.0):
            issues.append("signal_quality outside 0-1")
        elif (
            self.signal_quality is not None
            and self.signal_quality < MIN_SIGNAL_QUALITY_FOR_USE
        ):
            issues.append("signal_quality below usable threshold")

        self.__issues = issues
        self.__is_valid = len(issues) == 0
        return self.__is_valid


class Session:
    """A training session: one participant plus all readings taken during it."""

    def __init__(self, participant: Participant, label: str = ""):
        self.participant = participant
        self.label = label
        self.observations: list[Observation] = []

    def add_observation(self, observation: Observation) -> None:
        self.observations.append(observation)

    def add_observations_from_dicts(self, raw_observations: list[dict]) -> None:
        for raw in raw_observations:
            self.add_observation(Observation.from_dict(raw))

    @property
    def valid_observations(self) -> list[Observation]:
        return [obs for obs in self.observations if obs.is_valid]

    @property
    def total_count(self) -> int:
        return len(self.observations)

    @property
    def valid_count(self) -> int:
        return len(self.valid_observations)
