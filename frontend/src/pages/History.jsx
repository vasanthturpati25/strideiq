import React, { useEffect, useState } from 'react';
import { fetchHistory } from '../utils/api';

const RISK_COLOR = { Low: 'var(--green)', Medium: 'var(--yellow)', High: 'var(--red)' };

const History = () => {
  const [records, setRecords] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const sid = localStorage.getItem('strideiq_session');
    if (!sid) { setLoading(false); return; }

    fetchHistory(sid)
      .then((r) => setRecords(r.data.history || []))
      .catch(() => setError('Failed to load history.'))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <p style={styles.msg}>Loading…</p>;
  if (error)   return <p style={{ ...styles.msg, color: 'var(--red)' }}>{error}</p>;
  if (!records.length) return (
    <div style={styles.page}>
      <h1 style={styles.title}>Analysis History</h1>
      <p style={styles.msg}>No analyses yet. Upload a video on the home page!</p>
    </div>
  );

  return (
    <div style={styles.page}>
      <h1 style={styles.title}>Analysis History</h1>
      <div style={styles.grid}>
        {records.map((r) => (
          <div key={r.id} className="card" style={styles.card}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '0.75rem' }}>
              <span style={{ fontWeight: 700, fontSize: '0.9rem', wordBreak: 'break-all' }}>{r.filename}</span>
              <span style={{ color: RISK_COLOR[r.risk_level], fontWeight: 700, fontSize: '0.82rem', marginLeft: '0.5rem', flexShrink: 0 }}>
                {r.risk_level} Risk
              </span>
            </div>
            <div style={{ fontSize: '2rem', fontWeight: 800, color: RISK_COLOR[r.risk_level], fontFamily: 'var(--font-mono)', marginBottom: '0.4rem' }}>
              {r.overall_score}
              <span style={{ fontSize: '0.9rem', color: 'var(--text-muted)', fontFamily: 'var(--font)', fontWeight: 400 }}>/100</span>
            </div>
            {r.injuries?.length > 0 && (
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.4rem', marginBottom: '0.5rem' }}>
                {r.injuries.slice(0, 3).map((inj, i) => (
                  <span key={i} style={{ padding: '0.2rem 0.6rem', background: '#7f1d1d20', border: '1px solid var(--red)', borderRadius: 999, color: 'var(--red)', fontSize: '0.74rem' }}>
                    {inj}
                  </span>
                ))}
              </div>
            )}
            <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
              {new Date(r.created_at).toLocaleString()}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
};

const styles = {
  page: { maxWidth: 1200, margin: '0 auto', padding: '2rem' },
  title: { fontSize: '1.6rem', fontWeight: 800, marginBottom: '1.5rem' },
  msg: { textAlign: 'center', padding: '3rem', color: 'var(--text-muted)' },
  grid: { display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))', gap: '1rem' },
  card: { transition: 'border-color 0.15s' },
};

export default History;
