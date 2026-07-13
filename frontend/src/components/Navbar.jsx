import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export default function Navbar() {
  const { isAuthenticated, user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  return (
    <nav className="sticky top-0 z-50 w-full" style={{ backgroundColor: 'var(--color-surface-nav)' }}>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link to={isAuthenticated ? '/dashboard' : '/'} className="flex items-center gap-2 no-underline">
            <div className="flex items-center gap-1.5">
              <svg width="28" height="28" viewBox="0 0 28 28" fill="none" xmlns="http://www.w3.org/2000/svg">
                <circle cx="14" cy="14" r="13" stroke="#14b8a6" strokeWidth="2"/>
                <path d="M10 8C10 8 14 12 14 14C14 16 10 20 10 20" stroke="#14b8a6" strokeWidth="2" strokeLinecap="round"/>
                <path d="M18 8C18 8 14 12 14 14C14 16 18 20 18 20" stroke="#f97316" strokeWidth="2" strokeLinecap="round"/>
                <circle cx="12" cy="11" r="1.5" fill="#14b8a6"/>
                <circle cx="16" cy="17" r="1.5" fill="#f97316"/>
                <circle cx="14" cy="14" r="1.5" fill="#0f766e"/>
              </svg>
              <span className="text-xl font-bold tracking-tight" style={{ color: 'var(--color-text-light)' }}>
                GEN<span style={{ color: 'var(--color-accent)' }}>Q</span>
              </span>
            </div>
          </Link>

          {/* Nav Links */}
          <div className="flex items-center gap-4">
            {isAuthenticated ? (
              <>
                <Link
                  to="/dashboard"
                  className="text-sm font-medium no-underline px-3 py-1.5 rounded-md transition-colors"
                  style={{ color: 'var(--color-text-muted)' }}
                  onMouseEnter={e => e.target.style.color = 'var(--color-text-light)'}
                  onMouseLeave={e => e.target.style.color = 'var(--color-text-muted)'}
                >
                  Dashboard
                </Link>
                <span className="text-sm" style={{ color: 'var(--color-text-muted)' }}>
                  {user?.username || user?.email}
                </span>
                <button
                  onClick={handleLogout}
                  className="text-sm font-medium px-3 py-1.5 rounded-md transition-colors cursor-pointer"
                  style={{
                    color: 'var(--color-text-muted)',
                    background: 'none',
                    border: 'none',
                  }}
                  onMouseEnter={e => {
                    e.target.style.color = '#ef4444';
                  }}
                  onMouseLeave={e => {
                    e.target.style.color = 'var(--color-text-muted)';
                  }}
                >
                  Log out
                </button>
              </>
            ) : (
              <>
                <Link
                  to="/login"
                  className="text-sm font-medium no-underline px-3 py-1.5 rounded-md transition-colors"
                  style={{ color: 'var(--color-text-muted)' }}
                  onMouseEnter={e => e.target.style.color = 'var(--color-text-light)'}
                  onMouseLeave={e => e.target.style.color = 'var(--color-text-muted)'}
                >
                  Log in
                </Link>
                <Link to="/signup" className="btn-primary no-underline text-sm" style={{ padding: '0.5rem 1rem' }}>
                  Sign Up
                </Link>
              </>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
}
