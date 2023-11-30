// newbet.tsx
import React, { useState } from 'react';
import styles from './styles.module.css';

const NewBet = () => {
  const [newBet, setNewBet] = useState({
    creator_id: 1, // Assuming a default user ID for now
    acceptor_id: 2, // Assuming another default user ID for now
    bet_worth: 10,
    bet_body: '',
    bet_status: 'pending',
  });

  const handleCreateBet = () => {
    // Handle creating a new bet
    fetch('http://localhost:8000/api/create_bet', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(newBet),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log(data.message);
        // Optionally, you can redirect or perform other actions after creating the bet
      })
      .catch((error) => {
        console.error('Error creating bet:', error);
      });
  };

  return (
    <div className={`${styles.body} ${styles.redBackground} ${styles.container}`}>
      <div className={styles.registerContainer}>
        <h2>Create a New Bet</h2>
        <input
          type="text"
          placeholder="Bet Body"
          value={newBet.bet_body}
          onChange={(e) => setNewBet({ ...newBet, bet_body: e.target.value })}
        />
        <button onClick={handleCreateBet}>Create Bet</button>
      </div>
    </div>
  );
};

export default NewBet;
