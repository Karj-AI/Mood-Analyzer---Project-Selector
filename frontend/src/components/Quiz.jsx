import { useState } from "react";

export default function Quiz({ questions, onComplete }) {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [answers, setAnswers] = useState([]);

  const question = questions[currentIndex];

  function handleAnswer(optionIndex) {
    const nextAnswers = [...answers, optionIndex];

    if (currentIndex + 1 < questions.length) {
      setAnswers(nextAnswers);
      setCurrentIndex(currentIndex + 1);
    } else {
      onComplete(nextAnswers);
    }
  }

  return (
    <div className="pixel-panel">
      <div className="progress-label">
        Question {currentIndex + 1} / {questions.length}
      </div>
      <div className="question-text">{question.text}</div>
      {question.options.map((opt, i) => (
        <button
          key={i}
          className="pixel-button"
          onClick={() => handleAnswer(i)}
        >
          {opt.label}
        </button>
      ))}
    </div>
  );
}