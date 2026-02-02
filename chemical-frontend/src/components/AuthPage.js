import React, { useState } from 'react';
import './AuthPage.css';

function AuthPage({ onLogin, onRegister, message, messageType }) {
  const [showRegister, setShowRegister] = useState(false);
  const [loginUsername, setLoginUsername] = useState('');
  const [loginPassword, setLoginPassword] = useState('');
  const [registerUsername, setRegisterUsername] = useState('');
  const [registerPassword, setRegisterPassword] = useState('');
  const [loading, setLoading] = useState(false);

  const handleLoginSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    await onLogin(loginUsername, loginPassword);
    setLoginUsername('');
    setLoginPassword('');
    setLoading(false);
  };

  const handleRegisterSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    const success = await onRegister(registerUsername, registerPassword);
    if (success) {
      setRegisterUsername('');
      setRegisterPassword('');
      setShowRegister(false);
    }
    setLoading(false);
  };

  return (
    <div className="auth-container">
      <div className="card">
        <div className="logo">
          <h1>⚗️ Chemical Visualizer</h1>
          <p>Analyze equipment data with ease</p>
        </div>

        {message && (
          <div className={`message ${messageType}`}>
            {message}
          </div>
        )}

        {!showRegister ? (
          <form onSubmit={handleLoginSubmit}>
            <h2>Login</h2>
            <div className="form-group">
              <label htmlFor="loginUsername">Username</label>
              <input
                id="loginUsername"
                type="text"
                value={loginUsername}
                onChange={(e) => setLoginUsername(e.target.value)}
                placeholder="Enter your username"
                required
                disabled={loading}
              />
            </div>
            <div className="form-group">
              <label htmlFor="loginPassword">Password</label>
              <input
                id="loginPassword"
                type="password"
                value={loginPassword}
                onChange={(e) => setLoginPassword(e.target.value)}
                placeholder="Enter your password"
                required
                disabled={loading}
              />
            </div>
            <button type="submit" disabled={loading}>
              {loading ? 'Logging in...' : 'Login'}
            </button>
            <div className="toggle-form">
              Don't have an account?{' '}
              <button
                type="button"
                onClick={() => setShowRegister(true)}
                disabled={loading}
              >
                Register
              </button>
            </div>
          </form>
        ) : (
          <form onSubmit={handleRegisterSubmit}>
            <h2>Register</h2>
            <div className="form-group">
              <label htmlFor="registerUsername">Username</label>
              <input
                id="registerUsername"
                type="text"
                value={registerUsername}
                onChange={(e) => setRegisterUsername(e.target.value)}
                placeholder="Choose a username"
                required
                disabled={loading}
              />
            </div>
            <div className="form-group">
              <label htmlFor="registerPassword">Password</label>
              <input
                id="registerPassword"
                type="password"
                value={registerPassword}
                onChange={(e) => setRegisterPassword(e.target.value)}
                placeholder="Create a password"
                required
                disabled={loading}
              />
            </div>
            <button type="submit" disabled={loading}>
              {loading ? 'Registering...' : 'Register'}
            </button>
            <div className="toggle-form">
              Already have an account?{' '}
              <button
                type="button"
                onClick={() => setShowRegister(false)}
                disabled={loading}
              >
                Login
              </button>
            </div>
          </form>
        )}
      </div>
    </div>
  );
}

export default AuthPage;
