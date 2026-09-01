export async function fetchSpecialties() {
  const res = await fetch("/api/specialties");
  if (!res.ok) throw new Error("Failed to load specialties");
  return res.json();
}

export async function fetchQuiz() {
  const res = await fetch("/api/quiz");
  if (!res.ok) throw new Error("Failed to load quiz");
  return res.json();
}

export async function fetchHistory() {
  const res = await fetch("/api/history");
  if (!res.ok) throw new Error("Failed to load history");
  return res.json();
}

export async function markComplete({ projectId, projectTitle }) {
  const res = await fetch("/api/complete", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ project_id: projectId, project_title: projectTitle }),
  });
  if (!res.ok) throw new Error("Failed to mark complete");
  return res.json();
}

export async function submitQuiz({ specialty, answerIndexes, difficulty }) {
  const res = await fetch("/api/submit-quiz", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      specialty,
      answer_indexes: answerIndexes,
      difficulty,
    }),
  });

  if (!res.ok) {
    const errBody = await res.json().catch(() => ({}));
    throw new Error(errBody.error || "Failed to submit quiz");
  }

  return res.json();
}