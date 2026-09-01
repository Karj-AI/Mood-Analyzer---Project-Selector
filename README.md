# 🎮 Mood Project Picker

A mood-based coding project recommender. Answer a short quiz about how you're
feeling, pick a specialty and difficulty, and get matched to a real project
idea to build — picked using weighted vector similarity, not a random
generator or hardcoded lookup table.

## Features

- 🧭 **Specialty selection** — Software, Cybersecurity, Data (Power BI/SQL), Azure/Cloud, or Game Development
- 🧠 **Mood inference engine** — a 7-question quiz maps answers to a 3-axis mood vector (energy, creativity, challenge)
- 🎯 **Weighted recommendation matching** — Euclidean distance between your mood and each project's ideal mood profile, filtered by difficulty
- 🎡 **Animated roulette wheel** — eased spin animation with weighted randomness, so results feel intentional, not arbitrary
- 📋 **Full project output** — description, tech stack, build steps, and stretch goals for every result
- 📊 **History + analytics tracking** — logs every pick and completion locally, viewable in-app
- 🎨 **Custom pixel-art theme** — pink/purple retro aesthetic built with a dedicated design system

## Technology Stack

| Layer | Technology |
|---|---|
| Frontend | React 18 + Vite |
| Styling | Custom CSS (pixel theme, no framework) |
| Backend | Flask (Python) |
| Matching Logic | Pure Python — vector math, no ML dependencies |
| Data Storage | Local JSON file (analytics log) |
| Fonts | Press Start 2P, VT323 |

## How Mood Matching Works

```
User answers 7 quiz questions
        ↓
Each answer nudges a mood axis (energy / creativity / challenge)
        ↓
Final mood vector, clamped to [-2, 2] per axis
        ↓
Filter project bank by specialty + difficulty
        ↓
Score every candidate: Euclidean distance to mood vector
        ↓
Weighted random selection (closer matches more likely, not guaranteed)
        ↓
Animated wheel settles on the backend-selected project
        ↓
Full project brief + one-line match reason displayed
```

This is intentionally **not** machine learning. With a 3-dimensional
input space and a small, hand-tagged project bank, a weighted nearest-
neighbor approach is the honest, explainable tool for the job — it's
easy to reason about, doesn't require fabricated training data, and
scales cleanly if more mood axes or projects are added later.

## Project Bank

275 total projects, 55 per specialty, each tagged with:
- a difficulty (`easy` / `medium` / `hard`)
- a mood-fit vector on the same 3 axes as the quiz
- tech stack, build steps, and stretch goals

A handful of projects per specialty currently have fully custom,
hand-written steps and stretch goals; the rest use a generated
template pending further content passes.

## Installation

```bash
# Clone the project
git clone <your-repo-url>
cd mood-project-picker

# --- Backend setup ---
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
pip install flask

# --- Frontend setup ---
cd frontend
npm install
```

## Running Locally

Two terminals required — Flask serves the API, Vite serves the UI.

**Terminal 1 (backend):**
```bash
venv\Scripts\activate
python app.py
```
Runs on `http://127.0.0.1:5000`

**Terminal 2 (frontend):**
```bash
cd frontend
npm run dev
```
Runs on `http://localhost:5173` — open this in your browser.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/specialties` | List of available specialties |
| GET | `/api/quiz` | The 7 quiz questions and options |
| POST | `/api/submit-quiz` | Submit answers + difficulty, get a matched project |
| GET | `/api/history` | Past picks with completion status |
| POST | `/api/complete` | Mark a project as completed |

## Limitations

- Only 10 of 275 projects have fully custom build steps; the rest use generated template text
- Analytics/history are stored in a local JSON file, not a real database — data doesn't persist across different machines or deployments
- No user accounts — history is shared across anyone using the same local instance
- Not yet deployed; runs locally only

## Project Structure

```
mood-project-picker/
├── app.py                    ← Flask entry point, all API routes
├── main.py                   ← Original terminal-only test harness
├── models/
│   ├── mood_axes.py          ← Mood axis definitions + clamping
│   ├── quiz_data.py          ← 7 quiz questions
│   ├── specialty_data.py     ← Specialty list
│   └── *_projects.py         ← 5 project banks (55 each)
├── logic/
│   ├── scoring.py            ← Quiz answers → mood vector
│   └── matcher.py            ← Distance scoring + weighted wheel selection
├── analytics/
│   └── tracker.py            ← Pick/completion logging + history
└── frontend/
    └── src/
        ├── App.jsx           ← Step machine orchestrating the flow
        ├── api.js            ← Fetch helpers for the Flask API
        ├── index.css         ← Pixel theme design system
        └── components/
            ├── SpecialtyPicker.jsx
            ├── Quiz.jsx
            ├── DifficultyPicker.jsx
            ├── Wheel.jsx
            ├── ProjectResult.jsx
            └── History.jsx
```

## Future Improvements

- [ ] Hand-write custom steps/stretch goals for the remaining ~265 projects
- [ ] Deploy backend + frontend (e.g. Render + Vercel) for a live demo link
- [ ] Move analytics from local JSON to a real database (SQLite/PostgreSQL)
- [ ] User accounts so history isn't shared across a shared instance
- [ ] Sound effects on the wheel spin
- [ ] GitHub starter template links per project
