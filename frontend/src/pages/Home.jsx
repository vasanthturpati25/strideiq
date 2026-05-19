import React, { useState } from 'react';
import { v4 as uuidv4 } from 'uuid';
import VideoUploader from '../components/VideoUploader';
import ResultsPanel from '../components/ResultsPanel';
import { analyzeVideo } from '../utils/api';

const getSessionId = () => {
  let id = localStorage.getItem('strideiq_session');
  if (!id) { id = uuidv4(); localStorage.setItem('strideiq_session', id); }
  return id;
};

const TIPS = [
  'Film from the side at waist height',
  'Ensure your full body is visible',
  'Record 5–30 seconds of steady running',
  'Good lighting, stable camera',
  'Wear fitted clothing for better detection',
];

const Home = () => {
  const [loading, setLoading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);
  const [phase, setPhase] = useState('');

  const handleUpload = async (file) => {
    setLoading(true); setError(null); setResults(null); setPhase('uploading');
    const formData = new FormData();
    formData.append('video', file);
    formData.append('session_id', getSessionId());

    try {
      const resp = await analyzeVideo(formData, (e) => {
        const pct = Math.round((e.loaded / e.total) * 100);
        setProgress(pct);
        if (pct === 100) setPhase('processing');
      });
      setResults(resp.data);
    } catch (err) {
      setError(err.response?.data?.error || 'Analysis failed. Please try again.');
    } finally {
      setLoading(false); setPhase(''); setProgress(0);
    }
  };

  return (
    <div style={{ maxWidth: 1400, margin: '0 auto', padding: '2rem' }}>

      {/* Hero */}
      <div style={{ textAlign: 'center', padding: '2rem 0 2.5rem', animation: 'fadeIn 0.5s ease' }}>
        <h1 style={{ fontSize: 'clamp(1.8rem, 4vw, 2.8rem)', fontWeight: 800, lineHeight: 1.15, marginBottom: '0.9rem', letterSpacing: '-0.03em' }}>
          AI-Powered{' '}
          <span style={{ background: 'linear-gradient(90deg, var(--accent), var(--accent2))', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
            Running Form
          </span>{' '}
          Analysis
        </h1>
        <p style={{ color: 'var(--text-muted)', maxWidth: 520, margin: '0 auto', fontSize: '1rem' }}>
          Upload your running video — get instant biomechanical feedback, injury risk score, and coaching tips.
        </p>
      </div>

      {/* Two-column layout */}
      <div className="two-col" style={{ display: 'grid', gridTemplateColumns: '360px 1fr', gap: '1.5rem', alignItems: 'start' }}>

        {/* Left column */}
        <div>
          <div className="card" style={{ marginBottom: '1rem' }}>
            <h2 style={{ fontSize: '1rem', fontWeight: 700, marginBottom: '0.2rem' }}>Upload Video</h2>
            <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginBottom: '1.1rem' }}>
              Side-view · full body visible · 5–30 seconds
            </p>
            <VideoUploader onUpload={handleUpload} loading={loading} />

            {loading && (
              <div style={{ marginTop: '1rem' }}>
                <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginBottom: '0.4rem' }}>
                  {phase === 'uploading' ? `Uploading… ${progress}%` : '⚙️ Processing pose landmarks…'}
                </p>
                <div style={{ height: 6, background: 'var(--border)', borderRadius: 3, overflow: 'hidden' }}>
                  <div style={{ height: '100%', borderRadius: 3, transition: 'width 0.3s ease', background: 'linear-gradient(90deg, var(--accent), var(--accent2))', width: phase === 'processing' ? '100%' : `${progress}%` }} />
                </div>
              </div>
            )}

            {error && (
              <div style={{ marginTop: '1rem', padding: '0.7rem 1rem', background: '#7f1d1d30', border: '1px solid var(--red)', borderRadius: 8, color: 'var(--red)', fontSize: '0.83rem' }}>
                ⚠️ {error}
              </div>
            )}
          </div>

          <div className="card">
            <h3 style={{ fontSize: '0.88rem', fontWeight: 700, marginBottom: '0.8rem', color: 'var(--accent)' }}>📋 Recording Tips</h3>
            {TIPS.map((tip, i) => (
              <div key={i} style={{ display: 'flex', gap: '0.6rem', marginBottom: '0.45rem', alignItems: 'flex-start' }}>
                <span style={{ flexShrink: 0, width: 20, height: 20, borderRadius: '50%', background: 'var(--surface2)', border: '1px solid var(--border)', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '0.68rem', fontWeight: 700, color: 'var(--accent)' }}>{i + 1}</span>
                <span style={{ fontSize: '0.82rem', color: 'var(--text-muted)' }}>{tip}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Right column */}
        <div>
          {results ? (
            <ResultsPanel data={results} />
          ) : (
            <div style={{ textAlign: 'center', padding: '5rem 2rem', background: 'var(--surface)', border: '1px dashed var(--border)', borderRadius: 'var(--radius)' }}>
              <div style={{ fontSize: '4rem', marginBottom: '1rem' }}>🏃</div>
              <div style={{ fontWeight: 700, marginBottom: '0.4rem' }}>Your analysis will appear here</div>
              <div style={{ color: 'var(--text-muted)', fontSize: '0.88rem' }}>Upload a video to get started</div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Home;
