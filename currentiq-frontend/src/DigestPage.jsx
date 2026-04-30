import { useState } from 'react';
import { getDigest } from './api';

export default function DigestPage({ exam }) {
  const [loading, setLoading] = useState(false);
  const [digest, setDigest] = useState(null);
  const [topic, setTopic] = useState('');
  const [error, setError] = useState(null);

  const generate = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await getDigest(exam, 1, topic || null);
      setDigest(data);
    } catch (e) {
      setError('Failed to generate digest. Make sure the backend is running.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page">
      <div className="page-header">
        <h2>{exam.toUpperCase()} Current Affairs Digest</h2>
        <p>Today's news repackaged specifically for your exam</p>
      </div>

      <div className="input-row">
        <input
          placeholder="Optional: filter by topic (e.g. India-China relations)"
          value={topic}
          onChange={e => setTopic(e.target.value)}
          className="text-input"
        />
        <button onClick={generate} disabled={loading} className="btn-primary">
          {loading ? 'Generating...' : 'Generate Digest'}
        </button>
      </div>

      {error && <div className="error-box">{error}</div>}
      {loading && <div className="loading-box">Fetching news and analysing with Amazon Nova...</div>}

      {digest && (
        <div className="digest-output">
          <div className="digest-meta">
            Sources: {digest.sources_used?.join(', ')} · {digest.article_count} articles analysed · {digest.powered_by}
          </div>
          {digest.digest_items?.map((item, i) => (
            <div key={i} className="digest-card">
              <div className="digest-card-header">
                <h3>{item.headline}</h3>
                <div className="tags">
                  {item.gs_paper && <span className="tag tag-blue">{item.gs_paper}</span>}
                  {item.topic_tag && <span className="tag tag-green">{item.topic_tag}</span>}
                  {item.topic && <span className="tag tag-green">{item.topic}</span>}
                </div>
              </div>
              <p className="digest-summary">{item.summary}</p>
              {item.upsc_angle && (
                <div className="upsc-angle">
                  <strong>UPSC Angle:</strong> {item.upsc_angle}
                </div>
              )}
              {item.one_liner && (
                <div className="upsc-angle">
                  <strong>Summary:</strong> {item.one_liner}
                </div>
              )}
              {item.key_facts && (
                <ul className="key-facts">
                  {item.key_facts.map((f, j) => <li key={j}>{f}</li>)}
                </ul>
              )}
              {item.mains_relevance && (
                <div className="mains-rel">
                  <strong>Mains:</strong> {item.mains_relevance}
                </div>
              )}
              {item.exam_tip && (
                <div className="mains-rel">
                  <strong>Exam Tip:</strong> {item.exam_tip}
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}