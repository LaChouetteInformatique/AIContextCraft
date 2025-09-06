import React, { useState, useEffect } from 'react';
import LoremDisplay from './components/LoremDisplay';
import { fetchLorem } from './utils/api';

function App() {
  const [loremText, setLoremText] = useState('');
  const [loading, setLoading] = useState(false);
  
  useEffect(() => {
    loadLorem();
  }, []);
  
  const loadLorem = async () => {
    setLoading(true);
    try {
      const text = await fetchLorem();
      setLoremText(text);
    } catch (error) {
      console.error('Failed to load lorem:', error);
    }
    setLoading(false);
  };
  
  return (
    <div className="app">
      <h1>Lorem Ipsum Generator</h1>
      {loading ? (
        <p>Loading...</p>
      ) : (
        <LoremDisplay text={loremText} />
      )}
      <button onClick={loadLorem}>Generate New</button>
    </div>
  );
}

export default App;
