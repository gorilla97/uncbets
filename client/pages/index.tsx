import React, { useEffect, useState } from 'react';

interface Bet {
  id: number;
  creator_id: number;
  acceptor_id: number;
  bet_worth: number;
  bet_body: string;
  bet_status: string;
}

function Index() {
  const [message, setMessage] = useState('Loading, hold up');
  const [people, setPeople] = useState<string[]>([]);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [bets, setBets] = useState<Bet[]>([]);
  const [newBet, setNewBet] = useState({
    creator_id: 1, // Assuming a default user ID for now
    acceptor_id: 2, // Assuming another default user ID for now
    bet_worth: 10,
    bet_body: '',
    bet_status: 'pending',
  });

  useEffect(() => {
    // Fetch home data
    fetch('http://localhost:8000/api/home')
      .then((response) => response.json())
      .then((data) => {
        setMessage(data.message);
        setPeople(data.people);
      });

    // Fetch all bets
    fetch('http://localhost:8000/api/bets')
      .then((response) => response.json())
      .then((data) => setBets(data.bets));
  }, []);

  const handleRegister = () => {
    // Handle user registration
    fetch('http://localhost:8000/api/register', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ username, password }),
    })
      .then((response) => response.json())
      .then((data) => setMessage(data.message));
  };

  const handleLogin = () => {
    // Handle user login
    fetch('http://localhost:8000/api/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ username, password }),
    })
      .then((response) => response.json())
      .then((data) => setMessage(data.message));
  };

  const handleCreateBet = () => {
    // Handle creating a new bet
    fetch('http://localhost:8000/api/bets', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(newBet),
    })
      .then((response) => response.json())
      .then((data) => {
        setMessage(data.message);
        // Fetch updated list of bets after creating a new bet
        fetch('http://localhost:8000/api/bets')
          .then((response) => response.json())
          .then((data) => setBets(data.bets));
      });
  };

  return (
    <div>
      <div> {message} </div>

      {/* User Registration */}
      <div>
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

      {/* User Login */}
      <div>
        <h2>User Login</h2>
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
        <button onClick={handleLogin}>Login</button>
      </div>

      {/* Create a new bet */}
      <div>
        <h2>Create a New Bet</h2>
        <input
          type="text"
          placeholder="Bet Body"
          value={newBet.bet_body}
          onChange={(e) => setNewBet({ ...newBet, bet_body: e.target.value })}
        />
        <button onClick={handleCreateBet}>Create Bet</button>
      </div>

      {/* Display all bets */}
      <div>
        <h2>All Bets</h2>
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
}

export default Index;