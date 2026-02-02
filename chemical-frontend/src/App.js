import React, { useState, useEffect } from 'react';
import axios from 'axios';
import AuthPage from './components/AuthPage';
import Dashboard from './components/Dashboard';
import './App.css';

const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

function App() {
  const [authToken, setAuthToken] = useState(localStorage.getItem('authToken'));
  const [username, setUsername] = useState(localStorage.getItem('username'));
  const [message, setMessage] = useState('');
  const [messageType, setMessageType] = useState('');

  useEffect(() => {
    // Check if token is still valid on app load
    if (authToken) {
      verifyToken();
    }
  }, []);

  const verifyToken = async () => {
    try {
      await axios.get(`${API_BASE}/equipment/datasets/`, {
        headers: { Authorization: `Bearer ${authToken}` }
      });
    } catch (error) {
      // Token invalid, logout
      handleLogout();
    }
  };

  const showMessage = (msg, type) => {
    setMessage(msg);
    setMessageType(type);
    setTimeout(() => setMessage(''), 5000);
  };

  const handleLogin = async (loginUsername, loginPassword) => {
    try {
      const response = await axios.post(`${API_BASE}/auth/login/`, {
        username: loginUsername,
        password: loginPassword
      });
      const token = response.data.access;
      setAuthToken(token);
      setUsername(response.data.username);
      localStorage.setItem('authToken', token);
      localStorage.setItem('username', response.data.username);
      showMessage('Login successful!', 'success');
    } catch (error) {
      showMessage(error.response?.data?.error || 'Login failed: ' + error.message, 'error');
    }
  };

  const handleRegister = async (registerUsername, registerPassword) => {
    try {
      await axios.post(`${API_BASE}/auth/register/`, {
        username: registerUsername,
        password: registerPassword
      });
      showMessage('Registration successful! Now login with your credentials.', 'success');
      return true;
    } catch (error) {
      showMessage(error.response?.data?.error || 'Registration failed: ' + error.message, 'error');
      return false;
    }
  };

  const handleLogout = () => {
    setAuthToken(null);
    setUsername(null);
    localStorage.removeItem('authToken');
    localStorage.removeItem('username');
    showMessage('Logged out successfully', 'success');
  };

  if (!authToken) {
    return (
      <AuthPage
        onLogin={handleLogin}
        onRegister={handleRegister}
        message={message}
        messageType={messageType}
      />
    );
  }

  return (
    <Dashboard
      authToken={authToken}
      username={username}
      onLogout={handleLogout}
      message={message}
      messageType={messageType}
      showMessage={showMessage}
    />
  );
}

export default App;
