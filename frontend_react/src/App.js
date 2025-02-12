import React, { useEffect, useState } from 'react';

function App() {
  const [message, setMessage] = useState('Loading...');

  useEffect(() => {
    fetch('http://localhost:8080/api/test')
      .then(response => response.json())
      .then(data => setMessage(data.message))
      .catch(error => setMessage('Error: ' + error.message));
  }, []);

  return (
    <div style={{ textAlign: 'center', marginTop: '50px' }}>
      <h1>My Chinese App</h1>
      <p>{message}</p>
    </div>
  );
}

export default App;
