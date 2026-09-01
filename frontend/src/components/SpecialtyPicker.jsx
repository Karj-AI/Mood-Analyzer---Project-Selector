export default function SpecialtyPicker({ specialties, onSelect }) {
  return (
    <div className="pixel-panel">
      <div className="section-heading">Pick your specialty</div>
      {specialties.map((s) => (
        <button
          key={s.id}
          className="pixel-button"
          onClick={() => onSelect(s.id)}
        >
          {s.label}
        </button>
      ))}
    </div>
  );
}