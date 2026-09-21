# Smart Fitness Session Analyzer (Option A)

Student name: Nihat Ali  
Student number: 2785  
Course: ACIT4420, Problem-Solving with Scripting

## Description

This project is a Python program for analyzing fitness sessions based on simulated wearable-device data.

The program stores participants and their sessions, checks whether measurements are valid, compares the measurements with the participant's normal values, and classifies the session based on activity level and heart rate. It also checks whether the participant appears to be recovering near the end of the session.

## Class design

The project is split into a few small modules. The classes are defined in `models.py`, the analysis functions and `SessionAnalyzer` are in `analyzer.py`, and `main.py` connects everything and runs the example sessions.

| Class | Purpose |
|---|---|
| `Person` | Base class containing the person's name and ID. |
| `Participant(Person)` | Inherits from `Person` and adds resting heart rate, maximum heart rate, and typical activity level. |
| `Observation` | Represents one set of measurements from a session. It checks whether the measurement contains valid values. |
| `Session` | Stores one participant together with the observations recorded during a training session. |
| `SessionAnalyzer` | Runs the different analysis functions and returns the results in a dictionary. |

## OOP concepts used

Composition is used in the `Session` class. A session contains a `Participant` and a list of `Observation` objects.

Encapsulation is used in the `Observation` class. The `__is_valid` attribute is private and is accessed through the `is_valid` property instead of directly.

Inheritance is used with `Person` and `Participant`. `Participant` inherits the basic name and ID attributes from `Person`.

Method overriding is also used in `Participant`, where `__str__` is changed to include the participant's reference values.

The `Observation.from_dict` method is a classmethod. It creates an `Observation` object from a dictionary and handles missing values.

The `SessionAnalyzer.analyze` method is a staticmethod because the analysis does not depend on stored instance data.

The project also uses standalone functions in `analyzer.py`, including:

- `summarize_values`
- `classify_intensity`
- `detect_recovery`
- `format_console_report`

## Validation and classification rules

The following ranges are used to decide whether measurements are valid:

- Heart rate: 30 to 220 bpm
- Temperature: 25 to 42 °C
- Skin response: 0 to 60
- Activity level: 0.0 to 1.0
- Signal quality: 0.0 to 1.0

Measurements with signal quality below 0.5 are ignored.

For session classification:

- Fewer than 3 valid observations gives `insufficient data`.
- A session is classified as `recovering` if heart rate drops by at least 10% and activity level drops by at least 20% when comparing the first and second half of the session.
- A session is classified as `resting` when the average heart rate is no more than 1.15 times the participant's resting heart rate and average activity is 0.30 or lower.
- A session is classified as `moderate activity` when the average heart rate is no more than 70% of the participant's maximum heart rate.
- Sessions above this level are classified as `high activity`.

These thresholds are simple values chosen for the assignment. They are not based on a real medical or wearable-device dataset.

## Installation and running

The project only uses the Python standard library, so no extra packages are required.

```bash
git clone https://github.com/USERNAME/REPOSITORY.git
cd REPOSITORY
python3 main.py
```

Tests are run with:

```bash
python3 -m unittest tests.py -v
```

## Example output

```text
============================================================
Session report: Test Participant - Resting session
============================================================
Observations used: 6 / 6
Classification:     resting
Recovery detected:  False

Heart rate (bpm):
  avg=63.5  min=62  max=65
Activity level (0-1):
  avg=0.06  min=0.05  max=0.07
============================================================

============================================================
Session report: Test Participant - Activity followed by recovery
============================================================
Observations used: 8 / 8
Classification:     recovering
Recovery detected:  True

Heart rate (bpm):
  avg=138.5  min=85  max=170
Activity level (0-1):
  avg=0.57  min=0.12  max=0.87
============================================================

============================================================
Session report: Test Participant - Poor-quality / invalid data
============================================================
Observations used: 1 / 5
Classification:     insufficient data
Recovery detected:  False

Heart rate (bpm):
  avg=117  min=117  max=117
Activity level (0-1):
  avg=0.47  min=0.47  max=0.47

Flagged/invalid observations: 4
  #1: missing signal_quality
  #2: heart_rate out of plausible range
  #3: signal_quality below usable threshold
  #4: activity_level outside 0-1
============================================================
```

Running `python3 main.py` shows all five test scenarios.

## Known limitations

- Recovery detection only compares averages from the first and second half of the session. It does not calculate a full trend over time.
- The classification thresholds are manually chosen and are not calibrated using real wearable-device data.
- The program is intended as a simple fitness-session analysis example rather than a medical analysis tool.
