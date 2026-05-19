import React from 'react';
import {
  RadarChart, Radar, PolarGrid, PolarAngleAxis,
  ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, Cell,
} from 'recharts';

const METRIC_LABELS = {
  cadence: 'Cadence',
  knee_drive_angle: 'Knee Drive',
  forward_lean: 'Forward Lean',
  foot_strike_offset: 'Foot Strike',
  arm_crossing_index: 'Arm Crossing',
};

const METRIC_UNITS = {
  cadence: ' spm',
  knee_drive_angle: '°',
  forward_lean: '°',
  foot_strike_offset: '',
  arm_crossing_index: '',
};

const RISK = {
  Low:    { color: 'var(--green)',  emoji: '✅', text: 'Great form! Low injury risk.' },
  Medium: { color: 'var(--yellow)', emoji: '⚠️', text: 'Some areas need attention.' },
  High:   { color: 'var(--red)',    emoji: '🚨', text: 'High injury risk detected.' },
};

const BAR_COLORS = ['#00e5ff', '#7c3aed', '#22c55e', '#f59e0b', '#ef4444'];

const ResultsPanel = ({ data }) => {
  if (!data) return null;

  const {
    risk_level, overall_score,
    scores = {}, metrics = {},
    injuries = [], feedback = [],
    shap_values = {}, probabilities = {},
    annotated_url,
  } = data;

  const cfg = RISK[risk_level] || RISK.Medium;

  const radarData = Object.entries(scores).map(([k, v]) => ({
    metric: METRIC_LABELS[k] || k, score: v,
  }));

  const shapData = Object.entries(shap_values)
    .map(([k, v]) => ({ name: METRIC_LABELS[k] || k, importance: +(v * 100).toFixed(1) }))
    .sort((a, b) => b.importance - a.importance);

  return (
    <div style={{ animation: 'fadeIn 0.6s ease' }}>

      {/* Score card */}
      <div className="card" style={{ textAlign: 'center', marginBottom: '1rem' }}>
        <div style={{ ...styles.badge, background: cfg.color + '22', border: `2px solid ${cfg.color}`, color: cfg.color }}>
          {cfg.emoji} {risk_level} Risk
        </div>
        <div>
          <span style={{ fontSize: '3.5rem', fontWeight: 800, color: cfg.color, fontFamily: 'var(--font-mono)' }}>
            {overall_score}
          </span>
          <span style={{ color: 'var(--text-muted)', fontSize: '1.1rem' }}>/100</span>
        </div>
        <p style={{ color: 'var(--text-muted)', fontSize: '0.88rem', marginBottom: '1rem' }}>{cfg.text}</p>

        {Object.keys(probabilities).length > 0 && (
          <div style={{ textAlign: 'left' }}>
            {Object.entries(probabilities).map(([lvl, prob]) => (
              <div key={lvl} style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '0.4rem' }}>
                <span style={{ width: 60, fontSize: '0.78rem', color: 'var(--text-muted)', fontWeight: 600 }}>{lvl}</span>
                <div style={{ flex: 1, height: 6, background: 'var(--border)', borderRadius: 3, overflow: 'hidden' }}>
                  <div style={{ width: `${(prob * 100).toFixed(0)}%`, height: '100%', background: RISK[lvl]?.color || 'var(--accent)', borderRadius: 3, transition: 'width 0.6s ease' }} />
                </div>
                <span style={{ width: 36, fontSize: '0.78rem', color: 'var(--text-muted)', textAlign: 'right' }}>{(prob * 100).toFixed(0)}%</span>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Metric scores */}
      <div className="card" style={{ marginBottom: '1rem' }}>
        <h3 style={styles.sectionTitle}>📊 Metric Scores</h3>
        {Object.entries(scores).map(([key, score]) => {
          const color = score >= 80 ? 'var(--green)' : score >= 60 ? 'var(--yellow)' : 'var(--red)';
          return (
            <div key={key} style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '0.65rem' }}>
              <div style={{ width: 130, flexShrink: 0 }}>
                <div style={{ fontSize: '0.83rem', fontWeight: 600 }}>{METRIC_LABELS[key]}</div>
                {metrics[key] !== undefined && (
                  <div style={{ fontSize: '0.73rem', color: 'var(--text-muted)', fontFamily: 'var(--font-mono)' }}>
                    {typeof metrics[key] === 'number' ? metrics[key].toFixed(2) : metrics[key]}{METRIC_UNITS[key] || ''}
                  </div>
                )}
              </div>
              <div style={{ flex: 1, height: 8, background: 'var(--border)', borderRadius: 4, overflow: 'hidden' }}>
                <div style={{ width: `${score}%`, height: '100%', background: color, borderRadius: 4, transition: 'width 0.8s ease' }} />
              </div>
              <span style={{ width: 32, fontFamily: 'var(--font-mono)', fontWeight: 700, fontSize: '0.88rem', color, textAlign: 'right' }}>{score}</span>
            </div>
          );
        })}
      </div>

      {/* Charts */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))', gap: '1rem', marginBottom: '1rem' }}>
        <div className="card">
          <h3 style={styles.sectionTitle}>🕸 Form Radar</h3>
          <ResponsiveContainer width="100%" height={220}>
            <RadarChart data={radarData}>
              <PolarGrid stroke="var(--border)" />
              <PolarAngleAxis dataKey="metric" tick={{ fill: 'var(--text-muted)', fontSize: 11 }} />
              <Radar dataKey="score" stroke="var(--accent)" fill="var(--accent)" fillOpacity={0.25} dot />
            </RadarChart>
          </ResponsiveContainer>
        </div>
        <div className="card">
          <h3 style={styles.sectionTitle}>🔬 Feature Importance</h3>
          <ResponsiveContainer width="100%" height={220}>
            <BarChart data={shapData} layout="vertical" margin={{ left: 8, right: 16 }}>
              <XAxis type="number" tick={{ fill: 'var(--text-muted)', fontSize: 11 }} domain={[0, 100]} />
              <YAxis dataKey="name" type="category" tick={{ fill: 'var(--text-muted)', fontSize: 11 }} width={96} />
              <Tooltip contentStyle={{ background: 'var(--surface2)', border: '1px solid var(--border)', borderRadius: 8 }} />
              <Bar dataKey="importance" radius={4}>
                {shapData.map((_, i) => <Cell key={i} fill={BAR_COLORS[i % BAR_COLORS.length]} />)}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Injuries */}
      {injuries.length > 0 && (
        <div className="card" style={{ marginBottom: '1rem' }}>
          <h3 style={styles.sectionTitle}>🚑 Injury Risk Flags</h3>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem' }}>
            {injuries.map((inj, i) => (
              <span key={i} style={{ padding: '0.3rem 0.9rem', background: '#7f1d1d30', border: '1px solid var(--red)', borderRadius: 999, color: 'var(--red)', fontSize: '0.8rem', fontWeight: 600 }}>
                {inj}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Feedback */}
      {feedback.length > 0 && (
        <div className="card" style={{ marginBottom: '1rem' }}>
          <h3 style={styles.sectionTitle}>💡 Actionable Feedback</h3>
          {feedback.map((fb, i) => (
            <div key={i} style={{ background: 'var(--surface2)', border: '1px solid var(--border)', borderRadius: 8, padding: '0.9rem 1.1rem', marginBottom: '0.6rem' }}>
              <div style={{ display: 'flex', gap: '0.75rem', marginBottom: '0.4rem' }}>
                <span style={{ fontWeight: 700, fontSize: '0.88rem' }}>{fb.label}</span>
                <span style={{ color: 'var(--red)', fontSize: '0.8rem', fontWeight: 600 }}>→ {fb.injury}</span>
              </div>
              <p style={{ fontSize: '0.83rem', color: 'var(--text-muted)', marginBottom: '0.4rem', lineHeight: 1.5 }}>{fb.explanation}</p>
              <p style={{ fontSize: '0.83rem', lineHeight: 1.5 }}><span style={{ color: 'var(--accent)', fontWeight: 700 }}>Fix: </span>{fb.fix}</p>
            </div>
          ))}
        </div>
      )}

      {/* Annotated video */}
      {annotated_url && (
        <div className="card">
          <h3 style={styles.sectionTitle}>🎥 Annotated Video</h3>
          <video src={annotated_url} controls style={{ width: '100%', borderRadius: 8, marginTop: '0.75rem' }} />
        </div>
      )}
    </div>
  );
};

const styles = {
  badge: { display: 'inline-block', padding: '0.35rem 1rem', borderRadius: 999, fontWeight: 800, fontSize: '0.85rem', marginBottom: '0.75rem' },
  sectionTitle: { fontSize: '0.95rem', fontWeight: 700, marginBottom: '1rem' },
};

export default ResultsPanel;
