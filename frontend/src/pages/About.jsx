import React from 'react';

const METRICS = [
  { name: 'Cadence',           range: '170–180 spm', injury: 'Shin Splints, Knee Pain' },
  { name: 'Knee Drive Angle',  range: '55–75°',      injury: 'IT Band Syndrome' },
  { name: 'Forward Lean',      range: '5–10°',       injury: 'Lower Back Pain, Hamstring Strain' },
  { name: 'Foot Strike Offset',range: '0.02–0.06',   injury: 'Knee Pain (Overstriding)' },
  { name: 'Arm Crossing Index',range: '0.05–0.15',   injury: 'Hip Rotational Stress' },
];

const About = () => (
  <div style={{ maxWidth: 780, margin: '0 auto', padding: '2rem' }}>
    <h1 style={{ fontSize: '1.8rem', fontWeight: 800, marginBottom: '0.5rem' }}>About StrideIQ</h1>
    <p style={{ color: 'var(--text-muted)', marginBottom: '2rem', lineHeight: 1.7 }}>
      StrideIQ uses MediaPipe pose estimation + a Random Forest classifier to analyse your running biomechanics
      and flag injury risks in seconds.
    </p>

    <div className="card" style={{ marginBottom: '1.5rem' }}>
      <h2 style={{ fontSize: '1rem', fontWeight: 700, marginBottom: '1rem' }}>📐 Biomechanical Metrics</h2>
      <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.85rem' }}>
        <thead>
          <tr>
            {['Metric', 'Optimal Range', 'Related Injury'].map((h) => (
              <th key={h} style={{ textAlign: 'left', padding: '0.5rem 0.75rem', borderBottom: '1px solid var(--border)', color: 'var(--text-muted)', fontWeight: 600 }}>{h}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {METRICS.map((m) => (
            <tr key={m.name}>
              <td style={{ padding: '0.55rem 0.75rem', borderBottom: '1px solid var(--border)', fontWeight: 600 }}>{m.name}</td>
              <td style={{ padding: '0.55rem 0.75rem', borderBottom: '1px solid var(--border)', fontFamily: 'var(--font-mono)', color: 'var(--accent)' }}>{m.range}</td>
              <td style={{ padding: '0.55rem 0.75rem', borderBottom: '1px solid var(--border)', color: 'var(--text-muted)' }}>{m.injury}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>

    <div className="card">
      <h2 style={{ fontSize: '1rem', fontWeight: 700, marginBottom: '0.75rem' }}>🧠 How It Works</h2>
      {[
        ['1. Pose Extraction', 'MediaPipe Pose detects 33 body landmarks per frame from your video.'],
        ['2. Biomechanics', 'Rule-based engine scores each metric against sports-science benchmarks.'],
        ['3. ML Classification', 'A Random Forest classifier predicts Low / Medium / High injury risk.'],
        ['4. Feedback', 'Personalised coaching tips are generated for each flagged metric.'],
      ].map(([title, desc]) => (
        <div key={title} style={{ marginBottom: '0.9rem' }}>
          <div style={{ fontWeight: 700, fontSize: '0.88rem', marginBottom: '0.2rem' }}>{title}</div>
          <div style={{ color: 'var(--text-muted)', fontSize: '0.84rem', lineHeight: 1.6 }}>{desc}</div>
        </div>
      ))}
    </div>
  </div>
);

export default About;
