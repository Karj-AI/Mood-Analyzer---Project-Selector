const DIFFICULTIES = [
  { id: "easy", label: "Easy" },
  { id: "medium", label: "Medium" },
  { id: "hard", label: "Hard" },
];

export default function DifficultyPicker({ onSelect }) {
  return (
    <div className="pixel-panel">
      <div className="section-heading">Pick a difficulty</div>
      {DIFFICULTIES.map((d) => (
        <button
          key={d.id}
          className="pixel-button"
          onClick={() => onSelect(d.id)}
        >
          {d.label}
        </button>
      ))}
    </div>
  );
}