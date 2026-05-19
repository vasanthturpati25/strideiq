import React, { useRef, useState } from 'react';

const VideoUploader = ({ onUpload, loading }) => {
  const inputRef = useRef();
  const [dragOver, setDragOver] = useState(false);
  const [selected, setSelected] = useState(null);

  const handle = (file) => {
    if (!file) return;
    setSelected(file);
  };

  const onDrop = (e) => {
    e.preventDefault();
    setDragOver(false);
    handle(e.dataTransfer.files[0]);
  };

  const submit = () => { if (selected) onUpload(selected); };

  return (
    <div>
      <div
        style={{
          ...styles.dropzone,
          borderColor: dragOver ? 'var(--accent)' : 'var(--border)',
          background: dragOver ? '#00e5ff10' : 'var(--surface2)',
        }}
        onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
        onDragLeave={() => setDragOver(false)}
        onDrop={onDrop}
        onClick={() => inputRef.current.click()}
      >
        <div style={styles.icon}>🎬</div>
        <p style={styles.main}>
          {selected ? selected.name : 'Drop video here or click to browse'}
        </p>
        <p style={styles.sub}>MP4 · MOV · AVI · WebM — max 100 MB</p>
        <input
          ref={inputRef}
          type="file"
          accept="video/*"
          style={{ display: 'none' }}
          onChange={(e) => handle(e.target.files[0])}
        />
      </div>

      <button
        onClick={submit}
        disabled={!selected || loading}
        style={{ width: '100%', marginTop: '1rem', padding: '0.75rem' }}
      >
        {loading ? '⏳ Analyzing…' : '⚡ Analyze My Form'}
      </button>
    </div>
  );
};

const styles = {
  dropzone: {
    border: '2px dashed',
    borderRadius: 'var(--radius)',
    padding: '2rem',
    textAlign: 'center',
    cursor: 'pointer',
    transition: 'all 0.2s',
  },
  icon: { fontSize: '2.5rem', marginBottom: '0.75rem' },
  main: { fontWeight: 600, fontSize: '0.9rem', marginBottom: '0.3rem' },
  sub: { color: 'var(--text-muted)', fontSize: '0.78rem' },
};

export default VideoUploader;
