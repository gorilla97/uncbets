// register.tsx
import React, { useState } from 'react';
import styles from './styles.module.css';

const Register = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleRegister = async () => {
    // Add your registration logic here
    // Example: Call an API to register a new user
    try {
      const response = await fetch('http://localhost:8000/api/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password }),
      });

      const data = await response.json();

      // Handle the response from the server, e.g., show a success message or handle errors
      console.log(data.message);
    } catch (error) {
      console.error('Error during registration:', error);
    }
  };

  return (
    <div className={`${styles.body} ${styles.redBackground} ${styles.container}`}>
      <div className={styles.registerContainer}>
        <h2>User Registration</h2>
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button onClick={handleRegister}>Register</button>
      </div>
    </div>
  );
};

export default Register;
