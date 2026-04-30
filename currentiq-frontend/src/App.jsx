import { useState, useEffect } from 'react';
import DigestPage from './DigestPage';
import MCQPage from './MCQPage';
import EvaluatorPage from './EvaluatorPage';
import { getHeadlines } from './api';
import './App.css';

const TABS = [
  { id: 'digest',    label: 'Daily Digest' },
  { id: 'mcq',       label: 'MCQ Generator' },
  { id: 'evaluator', label: 'Answer Evaluator' },
];

const EXAMS = [
  { id: 'upsc',  label: 'UPSC',  color: '#4f8cff' },
  { id: 'nda',   label: 'NDA',   color: '#22c97a' },
  { id: 'cds',   label: 'CDS',   color: '#f5a623' },
  { id: 'afcat', label: 'AFCAT', color: '#1fd4b8' },
  { id: 'ssc',   label: 'SSC',   color: '#e85d9e' },
  { id: 'gate',  label: 'GATE',  color: '#7b5cf0' },
];

export default function App() {
  const [activeTab, setActiveTab]       = useState('digest');
  const [selectedExam, setSelectedExam] = useState('upsc');
  const [headlines, setHeadlines]       = useState([]);


  useEffect(() => {
    const loadHeadlines = async () => {
      try {
        const data = await getHeadlines();
        setHeadlines(data.headlines || []);
      } catch (e) {
        console.log('Headlines failed to load:', e);
      }
    };
    setTimeout(loadHeadlines, 1000);
  }, []);

  return (
    <div className="app">
      <header className="header">
      <div className="logo">
  <svg width="38" height="38" viewBox="0 0 38 38" fill="none" xmlns="http://www.w3.org/2000/svg">
    <rect width="38" height="38" rx="10" fill="url(#logoGrad)"/>
    <defs>
      <linearGradient id="logoGrad" x1="0" y1="0" x2="38" y2="38" gradientUnits="userSpaceOnUse">
        <stop offset="0%" stopColor="#0ea5e9"/>
        <stop offset="100%" stopColor="#06b6d4"/>
      </linearGradient>
    </defs>
    {/* Signal/radar arc lines */}
    <path d="M10 24 Q19 8 28 24" stroke="white" strokeWidth="2" strokeLinecap="round" fill="none" opacity="0.4"/>
    <path d="M13 26 Q19 13 25 26" stroke="white" strokeWidth="2" strokeLinecap="round" fill="none" opacity="0.7"/>
    <path d="M16 28 Q19 18 22 28" stroke="white" strokeWidth="2.5" strokeLinecap="round" fill="none"/>
    {/* Center dot */}
    <circle cx="19" cy="29" r="2.5" fill="white"/>
  </svg>
  <div className="logo-text-wrap">
    <span className="logo-text">CurrentIQ</span>
    <span className="logo-sub">AI Current Affairs Engine</span>
  </div>
</div>
        <div className="nova-badge">Powered by Amazon Nova 2 Lite</div>
        <nav className="tabs">
          {TABS.map(tab => (
            <button
              key={tab.id}
              className={`tab ${activeTab === tab.id ? 'active' : ''}`}
              onClick={() => setActiveTab(tab.id)}>
              {tab.label}
            </button>
          ))}
        </nav>
      </header>

      <div className="exam-selector">
        <span className="exam-label">Preparing for:</span>
        {EXAMS.map(e => (
          <button
            key={e.id}
            className={`exam-btn ${selectedExam === e.id ? 'active' : ''}`}
            style={{ '--exam-color': e.color }}
            onClick={() => setSelectedExam(e.id)}>
            {e.label}
          </button>
        ))}
      </div>

      <div className="main-layout">
        <main className="main-content">
          {activeTab === 'digest'    && <DigestPage    exam={selectedExam} />}
          {activeTab === 'mcq'       && <MCQPage       exam={selectedExam} />}
          {activeTab === 'evaluator' && <EvaluatorPage />}
        </main>

        <aside className="radar-panel">
          <h3>Today's Radar</h3>
          {headlines.length === 0 && (
            <p className="radar-empty">Loading headlines...</p>
          )}
          {headlines.map((h, i) => (
            <a key={i} href={h.link} target="_blank"
              rel="noreferrer" className="headline-item">
              <span className="hl-source">{h.source}</span>
              <span className="hl-title">{h.title}</span>
            </a>
          ))}
        </aside>
      </div>
    </div>
  );
}