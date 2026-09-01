"""
Defines the mood axes the whole system scores against.
Each axis ranges from -2 to +2. Add more axes here later if you want,
just make sure quiz_data.py effects and projects_data.py mood_fit use
the same keys.
"""

MOOD_AXES = ["energy", "creativity", "challenge"]

AXIS_MIN = -2
AXIS_MAX = 2


def empty_mood_vector():
    return {axis: 0 for axis in MOOD_AXES}


def clamp(value, low=AXIS_MIN, high=AXIS_MAX):
    return max(low, min(high, value))


def clamp_vector(vector):
    return {axis: clamp(vector.get(axis, 0)) for axis in MOOD_AXES}


def describe_mood(vector):
    """Turns a numeric mood vector into a human readable label, purely for display."""
    energy = vector.get("energy", 0)
    creativity = vector.get("creativity", 0)
    challenge = vector.get("challenge", 0)

    energy_word = "low energy" if energy < 0 else "high energy" if energy > 0 else "steady energy"
    creativity_word = "structured" if creativity < 0 else "creative" if creativity > 0 else "balanced"
    challenge_word = "relaxed" if challenge < 0 else "challenge seeking" if challenge > 0 else "neutral"

    return f"{energy_word}, {creativity_word}, {challenge_word}"