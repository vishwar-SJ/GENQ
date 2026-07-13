import { createContext, useContext, useState, useEffect } from 'react';
import api from '../api/axios';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check for existing token on mount
    const token = localStorage.getItem('genq_token');
    const email = localStorage.getItem('genq_email');
    const username = localStorage.getItem('genq_username');
    if (token && email) {
      setUser({ token, email, username: username || email });
    }
    setLoading(false);
  }, []);

  const login = async (email, password) => {
    const res = await api.post('/auth/login', { email, password });
    const { access_token, email: userEmail, username } = res.data;
    localStorage.setItem('genq_token', access_token);
    localStorage.setItem('genq_email', userEmail);
    localStorage.setItem('genq_username', username);
    setUser({ token: access_token, email: userEmail, username });
    return res.data;
  };

  const signup = async (username, email, password) => {
    const res = await api.post('/auth/signup', { username, email, password });
    const { access_token, email: userEmail, username: uname } = res.data;
    localStorage.setItem('genq_token', access_token);
    localStorage.setItem('genq_email', userEmail);
    localStorage.setItem('genq_username', uname);
    setUser({ token: access_token, email: userEmail, username: uname });
    return res.data;
  };

  const logout = () => {
    localStorage.removeItem('genq_token');
    localStorage.removeItem('genq_email');
    localStorage.removeItem('genq_username');
    setUser(null);
  };

  const isAuthenticated = !!user;

  return (
    <AuthContext.Provider value={{ user, login, signup, logout, isAuthenticated, loading }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error('useAuth must be used within AuthProvider');
  return ctx;
}

export default AuthContext;
