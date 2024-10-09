import React, { useState } from 'react';
import './App.css';

function App() {
  const [file, setFile] = useState(null);

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    if (!file) {
      alert('Please select a PDF file!');
      return;
    }
    // Handle the file upload logic here
    console.log('File to upload:', file);
  };

  return (
    <div className="App">
      <h1>Upload PDF and Generate Video</h1>
      <form onSubmit={handleSubmit}>
        <input type="file" accept=".pdf" onChange={handleFileChange} />
        <button type="submit">Upload and Process</button>
      </form>
    </div>
  );
}

export default App;
