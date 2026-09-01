"""
7 quiz questions. Each option has an 'effect' dict that nudges the mood
axes defined in mood_axes.py. Feel free to rebalance these numbers once
you see how they play out in testing.
"""

QUESTIONS = [
    {
        "id": "q1",
        "text": "How's your energy right now?",
        "options": [
            {"label": "Running on empty", "effect": {"energy": -2}},
            {"label": "Steady, could go either way", "effect": {"energy": 0}},
            {"label": "Wired and ready to go", "effect": {"energy": 2}},
        ],
    },
    {
        "id": "q2",
        "text": "Do you want to make something or solve something?",
        "options": [
            {"label": "Make something fun or visual", "effect": {"creativity": 2}},
            {"label": "Solve a tricky logic problem", "effect": {"creativity": -2, "challenge": 1}},
        ],
    },
    {
        "id": "q3",
        "text": "How much patience do you have for debugging today?",
        "options": [
            {"label": "None, I want something that just works", "effect": {"challenge": -2}},
            {"label": "Some, I don't mind a little struggle", "effect": {"challenge": 0}},
            {"label": "Bring on the hard bugs", "effect": {"challenge": 2}},
        ],
    },
    {
        "id": "q4",
        "text": "Pick a vibe.",
        "options": [
            {"label": "Cozy and chill", "effect": {"energy": -1, "creativity": 1}},
            {"label": "Fast and intense", "effect": {"energy": 2, "challenge": 1}},
            {"label": "Curious and exploratory", "effect": {"creativity": 1, "challenge": 0}},
        ],
    },
    {
        "id": "q5",
        "text": "How much time do you realistically have this week?",
        "options": [
            {"label": "Barely any, small wins only", "effect": {"challenge": -1, "energy": -1}},
            {"label": "A decent chunk", "effect": {"challenge": 0}},
            {"label": "Lots, I want to sink my teeth into something", "effect": {"challenge": 2}},
        ],
    },
    {
        "id": "q6",
        "text": "Which sounds more appealing right now?",
        "options": [
            {"label": "Drawing, music, or visuals", "effect": {"creativity": 2, "energy": 1}},
            {"label": "Data, systems, or numbers", "effect": {"creativity": -1, "challenge": 1}},
        ],
    },
    {
        "id": "q7",
        "text": "How are you feeling about coding today, honestly?",
        "options": [
            {"label": "Kind of tired of it, need something light", "effect": {"energy": -2, "challenge": -1}},
            {"label": "Neutral, just want to build", "effect": {"energy": 0}},
            {"label": "Excited, let's do something ambitious", "effect": {"energy": 2, "challenge": 2}},
        ],
    },
]