import { useState } from 'react';
import { evaluateAnswer } from './api';

const SAMPLE_QUESTION = "Discuss the significance of India's G20 Presidency in the context of Global South leadership. (150 words)";

export default function EvaluatorPage() {
  const [question, setQuestion] = useState(SAMPLE_QUESTION);
  const [answer, setAnswer] = useState('');
  const [wordLimit, setWordLimit] = useState(150);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const evaluate = async () => {
    if (!answer.trim()) return;
    setLoading(true);
    setError(null);
    try {
      const data = await evaluateAnswer(question, answer, wordLimit);
      setResult(data);
    } catch (e) {
      setError('Failed to evaluate. Make sure the backend is running.');
    } finally {
      setLoading(false);
    }
  };

  const wordCount = answer.trim().split(/\s+/).filter(Boolean).length;
  const gradeColors = { A: '#22c97a', B: '#4f8cff', C: '#f5a623', D: '#f04f5e' };

  return (
    <div className="page">
      <div className="page-header">
        <h2>UPSC Answer Evaluator</h2>
        <p>Get AI feedback on your Mains answers using actual UPSC criteria</p>
      </div>

      <label className="field-label">Question</label>
      <textarea
        className="text-input"
        rows={2}
        value={question}
        onChange={e => setQuestion(e.target.value)}
      />

      <div className="wl-row">
        <label className="field-label">Your Answer</label>
        <span className={`word-count ${wordCount > wordLimit ? 'over' : ''}`}>
          {wordCount} / {wordLimit} words
        </span>
        <select
          value={wordLimit}
          onChange={e => setWordLimit(Number(e.target.value))}
          className="wl-select">
          <option value={150}>150 words</option>
          <option value={250}>250 words</option>
        </select>
      </div>

      <textarea
        className="text-input answer-box"
        rows={8}
        placeholder="Write your UPSC answer here..."
        value={answer}
        onChange={e => setAnswer(e.target.value)}
      />

      <button
        onClick={evaluate}
        disabled={loading || !answer.trim()}
        className="btn-primary">
        {loading ? 'Evaluating with Amazon Nova...' : 'Evaluate Answer'}
      </button>

      {error && <div className="error-box">{error}</div>}

      {result && (
        <div className="eval-result">
          <div className="eval-header">
            <div className="score-circle"
              style={{ borderColor: gradeColors[result.overall_grade] }}>
              <span className="score-num">{result.total}</span>
              <span className="score-max">/ 10</span>
            </div>
            <div>
              <div className="grade"
                style={{ color: gradeColors[result.overall_grade] }}>
                Grade {result.overall_grade}
              </div>
              <div className="grade-reasoning">{result.grade_reasoning}</div>
            </div>
          </div>

          <div className="score-breakdown">
            {Object.entries(result.scores).map(([k, v]) => (
              <div key={k} className="score-row">
                <span className="score-label">{k.replace(/_/g, ' ')}</span>
                <div className="score-bar">
                  <div className="score-fill"
                    style={{ width: `${v * 33}%` }} />
                </div>
                <span className="score-val">{v}</span>
              </div>
            ))}
          </div>

          <div className="feedback-section">
            <h4>✅ Strengths</h4>
            <ul>{result.strengths?.map((s, i) => <li key={i}>{s}</li>)}</ul>

            <h4>🔧 Improvements</h4>
            <ul>{result.improvements?.map((s, i) => <li key={i}>{s}</li>)}</ul>

            {result.missed_points?.length > 0 && <>
              <h4>📌 Missed Points</h4>
              <ul>{result.missed_points.map((s, i) => <li key={i}>{s}</li>)}</ul>
            </>}

            <h4>💡 Model Introduction</h4>
            <p className="model-intro">{result.model_intro}</p>

            <div className="word-feedback">{result.word_limit_feedback}</div>
          </div>
        </div>
      )}
    </div>
  );
}