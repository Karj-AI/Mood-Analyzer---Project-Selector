import { useEffect, useState } from "react";
import SpecialtyPicker from "./components/SpecialtyPicker.jsx";
import Quiz from "./components/Quiz.jsx";
import DifficultyPicker from "./components/DifficultyPicker.jsx";
import Wheel from "./components/Wheel.jsx";
import ProjectResult from "./components/ProjectResult.jsx";
import History from "./components/History.jsx";
import { fetchSpecialties, fetchQuiz, submitQuiz } from "./api.js";

const STEPS = {
  SPECIALTY: "specialty",
  QUIZ: "quiz",
  DIFFICULTY: "difficulty",
  SPINNING: "spinning",
  RESULT: "result",
  HISTORY: "history",
};

export default function App() {
  const [step, setStep] = useState(STEPS.SPECIALTY);
  const [previousStep, setPreviousStep] = useState(STEPS.SPECIALTY);
  const [specialties, setSpecialties] = useState([]);
  const [questions, setQuestions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const [specialty, setSpecialty] = useState(null);
  const [answerIndexes, setAnswerIndexes] = useState(null);
  const [difficulty, setDifficulty] = useState(null);
  const [quizResult, setQuizResult] = useState(null);

  useEffect(() => {
    Promise.all([fetchSpecialties(), fetchQuiz()])
      .then(([specialtiesData, quizData]) => {
        setSpecialties(specialtiesData);
        setQuestions(quizData);
      })
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  function handleSpecialtySelect(id) {
    setSpecialty(id);
    setStep(STEPS.QUIZ);
  }

  function handleQuizComplete(indexes) {
    setAnswerIndexes(indexes);
    setStep(STEPS.DIFFICULTY);
  }

  async function handleDifficultySelect(diff) {
    setDifficulty(diff);
    setError(null);
    setStep(STEPS.SPINNING);

    try {
      const data = await submitQuiz({
        specialty,
        answerIndexes,
        difficulty: diff,
      });
      setQuizResult(data);
    } catch (err) {
      setError(err.message);
      setStep(STEPS.DIFFICULTY);
    }
  }

  function handleWheelFinished() {
    setStep(STEPS.RESULT);
  }

  function handleRestart() {
    setSpecialty(null);
    setAnswerIndexes(null);
    setDifficulty(null);
    setQuizResult(null);
    setError(null);
    setStep(STEPS.SPECIALTY);
  }

  function openHistory() {
    setPreviousStep(step);
    setStep(STEPS.HISTORY);
  }

  function closeHistory() {
    setStep(previousStep);
  }

  return (
    <div className="app-container">
      <div className="app-title">MOOD PROJECT PICKER</div>
      <div className="app-subtitle">find your next build, by vibe</div>

      {step !== STEPS.HISTORY && (
        <div className="top-nav">
          <button className="top-nav-link" onClick={openHistory}>
            View History
          </button>
        </div>
      )}

      {error && <div className="error-box">{error}</div>}

      {loading && <div className="loading-text">Loading...</div>}

      {!loading && step === STEPS.SPECIALTY && (
        <SpecialtyPicker
          specialties={specialties}
          onSelect={handleSpecialtySelect}
        />
      )}

      {!loading && step === STEPS.QUIZ && (
        <Quiz questions={questions} onComplete={handleQuizComplete} />
      )}

      {!loading && step === STEPS.DIFFICULTY && (
        <DifficultyPicker onSelect={handleDifficultySelect} />
      )}

      {step === STEPS.SPINNING && quizResult && (
        <Wheel
          candidates={quizResult.candidates}
          result={quizResult.result}
          onFinished={handleWheelFinished}
        />
      )}

      {step === STEPS.RESULT && quizResult && (
        <ProjectResult
          moodDescription={quizResult.mood_description}
          result={quizResult.result}
          reason={quizResult.reason}
          onRestart={handleRestart}
        />
      )}

      {step === STEPS.HISTORY && <History onBack={closeHistory} />}
    </div>
  );
}