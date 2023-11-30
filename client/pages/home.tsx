// home.tsx
import React from 'react';
import Link from 'next/link';
import styles from './styles.module.css';

const Home = () => {
  return (
    <div className={`${styles.body} ${styles.redBackground}`}>
      <header className={styles.header}>
        <nav className={styles.nav}>
          <Link href="/betlog">
            <a className={styles.link}>Bet Log</a>
          </Link>
          <Link href="/newbet">
            <a className={styles.link}>New Bet</a>
          </Link>
        </nav>
      </header>
      <div className={styles.container}>
        <div className={styles.registerContainer}>
          <h2>Welcome to the Home Page</h2>
        </div>
      </div>
    </div>
  );
};

export default Home;
