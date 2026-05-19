import React from 'react';
import { Link, useLocation } from 'react-router-dom';

const Navbar = () => {
  const { pathname } = useLocation();

  const link = (to, label) => (
    <Link
      to={to}
      style={{
        ...styles.link,
        color: pathname === to ? 'var(--accent)' : 'var(--text-muted)',
        borderBottom: pathname === to ? '2px solid var(--accent)' : '2px solid transparent',
      }}
    >
      {label}
    </Link>
  );

  return (
    <nav style={styles.nav}>
      <span style={styles.brand}>⚡ StrideIQ</span>
      <div style={styles.links}>
        {link('/', 'Analyze')}
        {link('/history', 'History')}
        {link('/about', 'About')}
      </div>
    </nav>
  );
};

const styles = {
  nav: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between',
    padding: '0.75rem 2rem',
    background: 'var(--surface)',
    borderBottom: '1px solid var(--border)',
    position: 'sticky',
    top: 0,
    zIndex: 100,
  },
  brand: { fontWeight: 800, fontSize: '1.1rem', letterSpacing: '-0.02em' },
  links: { display: 'flex', gap: '1.5rem' },
  link: {
    fontSize: '0.9rem',
    fontWeight: 600,
    paddingBottom: '2px',
    transition: 'color 0.15s',
  },
};

export default Navbar;
