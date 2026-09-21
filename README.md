# Smart Fitness Session Analyzer (Option A)

Student name: Nihat Ali
Student number: 2785
Course: ACIT4420, Problem-Solving with Scripting

## Description

This project is a Python program for analyzing fitness sessions based on simulated wearable-device data produced by the instructor-supplied `data_generator.py`.

The program builds a participant from the generator's profile data, checks whether each observation's measurements are valid, compares the session's measurements with the participant's baseline values, and classifies the session based on heart rate and activity level. It also checks whether the participant appears to be recovering near the end of the session.

## Class design

The project is split into a few small modules. The classes are defined in `models.py`, the analysis functions and `SessionAnalyzer` are in `analyzer.py`, `sample_data.py` wraps the instructor's generator with fixed seeds for reproducible scenarios, and `main.py` connects everything and runs the example sessions. `data_generator.py` is the instructor-supplied file and is not modified.

| Class | Purpose |
|---|---|
| `Person` | Base class containing the person's name and ID. |
| `Participant(Person)` | Inherits from `Person` and adds the participant's baseline heart rate, baseline skin response, and baseline temperature, built directly from the generator's profile dict. |
| `Observation` | Represents one set of measurements from a session. It checks whether the measurement contains valid values. |
| `Session` | Stores one participant together with the observations recorded during a training session. |
| `SessionAnalyzer` | Runs the different analysis functions and returns the results in a dictionary. |

## OOP concepts used

Composition is used in the `Session` class. A session contains a `Participant` and a list of `Observation` objects.

Encapsulation is used in the `Observation` class. The `__is_valid` attribute is private and is accessed through the `is_valid` property instead of directly.

Inheritance is used with `Person` and `Participant`. `Participant` inherits the basic name and ID attributes from `Person`.

Method overriding is also used in `Participant`, where `__str__` is changed to include the participant's baseline values.

Two classmethods build objects from raw generator output: `Observation.from_dict` creates an `Observation` from an observation dict and handles missing values, and `Participant.from_profile` creates a `Participant` from the generator's profile dict.

The `SessionAnalyzer.analyze` method is a staticmethod because the analysis does not depend on stored instance data.

The project also uses standalone functions in `analyzer.py`, including:

- `summarize_values`
- `classify_intensity`
- `detect_recovery`
- `format_console_report`

## Data source

All session data comes from `generate_fitness_data()` in the supplied `data_generator.py`. `sample_data.py` calls it once per scenario with a fixed seed, so the same five scenarios reproduce identically every run:

```python
from data_generator import generate_fitness_data

profile, observations = generate_fitness_data(
    participant_id="P001", scenario="resting", seed=1, number_of_windows=8,
)
```

The generator returns a profile dict (`participant_id`, `baseline_heart_rate`, `baseline_skin_response`, `baseline_temperature`) and a list of observation dicts (`timestamp`, `heart_rate`, `skin_response`, `temperature`, `activity_level`, `signal_quality`). It does not provide a maximum heart rate or a typical activity level, so classification below is based on how far a session's average heart rate sits above the participant's own baseline, not a fraction of some maximum.

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
- A session is classified as `resting` when the average heart rate is no more than 15 bpm above the participant's baseline heart rate and average activity is 0.30 or lower.
- A session is classified as `moderate activity` when the average heart rate is no more than 45 bpm above the participant's baseline heart rate.
- Sessions above this level are classified as `high activity`.

These thresholds are simple values I chose myself and checked against generator output; they are not values taken from inside `data_generator.py`.

## Installation and running

The project only uses the Python standard library, so no extra packages are required beyond the supplied `data_generator.py`, which must stay in the same folder as the other files.

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
Session report: Participant P001 - Resting session
============================================================
Observations used: 8 / 8
Classification:     resting
Recovery detected:  False

Heart rate (bpm):
  avg=64.12  min=60  max=67
Activity level (0-1):
  avg=0.13  min=0.05  max=0.19
============================================================

============================================================
Session report: Participant P004 - Activity followed by recovery
============================================================
Observations used: 8 / 8
Classification:     recovering
Recovery detected:  True

Heart rate (bpm):
  avg=101.62  min=72  max=126
Activity level (0-1):
  avg=0.46  min=0.06  max=0.85
============================================================

============================================================
Session report: Participant P005 - Poor-quality / invalid data
============================================================
Observations used: 0 / 8
Classification:     insufficient data
Recovery detected:  False

Heart rate (bpm):
  avg=None  min=None  max=None
Activity level (0-1):
  avg=None  min=None  max=None

Flagged/invalid observations: 8
  #1: missing heart_rate, signal_quality below usable threshold
  #2: heart_rate out of plausible range, signal_quality below usable threshold
  #3: activity_level outside 0-1, signal_quality below usable threshold
  #4: missing skin_response, signal_quality below usable threshold
  #5: missing heart_rate, signal_quality below usable threshold
  #6: heart_rate out of plausible range
  #7: activity_level outside 0-1, signal_quality below usable threshold
  #8: missing skin_response, signal_quality below usable threshold
============================================================
```

Running `python3 main.py` shows all five test scenarios. The poor-quality scenario reports 0 usable observations because the generator deliberately corrupts every window in that scenario, cycling through four different problems (missing heart rate, an impossible heart rate, an out-of-range activity level, missing skin response).

## Known limitations

- Recovery detection only compares averages from the first and second half of the session. It does not calculate a full trend over time.
- The classification thresholds are offsets I chose myself, not calibrated against real wearable-device data, and not derived from `data_generator.py`'s internal logic.
- Because the generator does not supply a maximum heart rate, "high activity" is only defined relative to how far above baseline a session runs, not as a percentage of a true physiological maximum.
- The program is intended as a simple fitness-session analysis example rather than a medical analysis tool.
