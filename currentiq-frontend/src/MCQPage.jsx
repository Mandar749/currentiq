import { useState } from 'react';
import { getMCQs } from './api';

export default function MCQPage({ exam }) {
  const [topic, setTopic] = useState('');
  const [loading, setLoading] = useState(false);
  const [mcqs, setMcqs] = useState(null);
  const [selected, setSelected] = useState({});
  const [revealed, setRevealed] = useState(false);
  const [error, setError] = useState(null);

  const generate = async () => {
    if (!topic.trim()) return;
    setLoading(true);
    setSelected({});
    setRevealed(false);
    setError(null);
    try {
      const data = await getMCQs(exam, topic, 5);
      setMcqs(data);
    } catch (e) {
      setError('Failed to generate MCQs. Make sure the backend is running.');
    } finally {
      setLoading(false);
    }
  };

  const score = () => {
    if (!mcqs) return 0;
    return mcqs.questions.filter(q => selected[q.id] === q.correct).length;
  };

  return (
    <div className="page">
      <div className="page-header">
        <h2>{exam.toUpperCase()} MCQ Generator</h2>
        <p>Practice questions in the exact exam pattern</p>
      </div>

      <div className="input-row">
        <input
          placeholder="Enter a topic (e.g. India Space Policy, G20 Summit)"
          value={topic}
          onChange={e => setTopic(e.target.value)}
          onKeyDown={e => e.key === 'Enter' && generate()}
          className="text-input"
        />
        <button onClick={generate} disabled={loading || !topic.trim()} className="btn-primary">
          {loading ? 'Generating...' : 'Generate 5 MCQs'}
        </button>
      </div>

      {error && <div className="error-box">{error}</div>}
      {loading && <div className="loading-box">Generating {exam.toUpperCase()} pattern questions with Amazon Nova...</div>}

      {mcqs && (
        <div className="mcq-output">
          <div className="digest-meta">
            {mcqs.exam_full_name} · {mcqs.powered_by}
          </div>
          {mcqs.questions?.map((q, i) => (
            <div key={q.id} className="mcq-card">
              <div className="mcq-question">
                <span className="mcq-num">Q{i + 1}</span> {q.question}
              </div>
              <div className="mcq-options">
                {Object.entries(q.options).map(([key, val]) => {
                  let cls = 'mcq-option';
                  if (selected[q.id] === key) cls += ' selected';
                  if (revealed) {
                    if (key === q.correct) cls += ' correct';
                    else if (selected[q.id] === key) cls += ' wrong';
                  }
                  return (
                    <button key={key} className={cls}
                      onClick={() => !revealed && setSelected(p => ({ ...p, [q.id]: key }))}>
                      <span className="opt-key">{key}</span> {val}
                    </button>
                  );
                })}
              </div>
              {revealed && (
                <div className="explanation">
                  <strong>Explanation:</strong> {q.explanation}
                </div>
              )}
            </div>
          ))}

          <div className="mcq-actions">
            {!revealed ? (
              <button className="btn-primary" onClick={() => setRevealed(true)}>
                Check Answers
              </button>
            ) : (
              <div className="score-display">
                Score: {score()} / {mcqs.questions.length}
                {score() === mcqs.questions.length && ' 🎉 Perfect!'}
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}