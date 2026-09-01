import { useState } from "react";
import { markComplete } from "../api.js";

export default function ProjectResult({ moodDescription, result, reason, onRestart }) {
  const [completed, setCompleted] = useState(false);
  const [saving, setSaving] = useState(false);

  async function handleComplete() {
    setSaving(true);
    try {
      await markComplete({ projectId: result.id, projectTitle: result.title });
      setCompleted(true);
    } catch (err) {
      // non-critical, fail silently in UI but don't block the user
      console.error(err);
    } finally {
      setSaving(false);
    }
  }

  return (
    <div className="pixel-panel">
      <div className="mood-summary">Your mood: {moodDescription}</div>
      <div className="result-title">{result.title}</div>
      <div className="result-description">{result.description}</div>
      {reason && <div className="reason-text">{reason}</div>}

      <div className="subheading">Tech Stack</div>
      <div>
        {result.tech_stack.map((t) => (
          <span key={t} className="tech-tag">
            {t}
          </span>
        ))}
      </div>

      <div className="subheading">Steps</div>
      <ul className="step-list">
        {result.steps.map((step, i) => (
          <li key={i}>{step}</li>
        ))}
      </ul>

      <div className="subheading">Stretch Goals</div>
      <ul className="step-list">
        {result.stretch_goals.map((goal, i) => (
          <li key={i}>{goal}</li>
        ))}
      </ul>

      <button
        className="pixel-button"
        onClick={handleComplete}
        disabled={completed || saving}
      >
        {completed ? "Marked as completed!" : saving ? "Saving..." : "Mark as Completed"}
      </button>

      <button className="pixel-button pixel-button-primary" onClick={onRestart}>
        Spin Again
      </button>
    </div>
  );
}