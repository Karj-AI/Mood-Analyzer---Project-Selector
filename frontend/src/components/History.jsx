import { useEffect, useState } from "react";
import { fetchHistory } from "../api.js";

export default function History({ onBack }) {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchHistory()
      .then(setItems)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="pixel-panel">
      <div className="section-heading">Your Project History</div>

      {loading && <div className="loading-text">Loading...</div>}
      {error && <div className="error-box">{error}</div>}

      {!loading && items.length === 0 && (
        <div className="loading-text">
          No projects picked yet. Go spin the wheel!
        </div>
      )}

      {!loading &&
        items.map((item, i) => (
          <div key={i} className="history-item">
            <div className="history-title">{item.project_title}</div>
            <div className="history-meta">
              {item.specialty} • {item.difficulty} •{" "}
              {new Date(item.timestamp).toLocaleDateString()}
            </div>
            {item.completed && (
              <div className="history-completed">✓ Completed</div>
            )}
          </div>
        ))}

      <button className="pixel-button pixel-button-primary" onClick={onBack}>
        Back
      </button>
    </div>
  );
}