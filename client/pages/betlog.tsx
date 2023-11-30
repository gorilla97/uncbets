// betlog.tsx
import React, { useEffect, useState } from 'react';
import styles from './styles.module.css';

interface Bet {
  id: number;
  creator_id: number;
  acceptor_id: number;
  bet_worth: number;
  bet_body: string;
  bet_status: string;
}

const BetLog = () => {
  const [bets, setBets] = useState<Bet[]>([]);

  useEffect(() => {
    // Fetch bet log data
    fetch('http://localhost:8000/api/betlog') // Replace with your actual API endpoint
      .then((response) => response.json())
      .then((data) => setBets(data.bets));
  }, []);

  return (
    <div className={`${styles.body} ${styles.redBackground} ${styles.container}`}>
      <div className={styles.registerContainer}>
        <h2>Bet Log</h2>
        {bets.map((bet) => (
          <div key={bet.id}>
            <p>{`Bet ID: ${bet.id}`}</p>
            <p>{`Creator ID: ${bet.creator_id}`}</p>
            <p>{`Acceptor ID: ${bet.acceptor_id}`}</p>
            <p>{`Bet Worth: ${bet.bet_worth}`}</p>
            <p>{`Bet Body: ${bet.bet_body}`}</p>
            <p>{`Bet Status: ${bet.bet_status}`}</p>
            <hr />
          </div>
        ))}
      </div>
    </div>
  );
};

export default BetLog;
