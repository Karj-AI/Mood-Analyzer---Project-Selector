from models.mood_axes import empty_mood_vector, clamp_vector


def calculate_mood(selected_effects):
    """
    selected_effects: list of 'effect' dicts, one per answered question
    e.g. [{"energy": -2}, {"creativity": 2, "challenge": 1}, ...]

    Returns a clamped mood vector like {"energy": -1, "creativity": 2, "challenge": 0}
    """
    total = empty_mood_vector()

    for effect in selected_effects:
        for axis, value in effect.items():
            if axis in total:
                total[axis] += value

    return clamp_vector(total)