import React, { useState } from 'react';
import Navbar from './components/Navbar';
import SentimentForm from './components/SentimentForm';
import SentimentResult from './components/SentimentResult';

const App = () => {
  const [result, setResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleAnalyze = async (text) => {
    setIsLoading(true);
    setResult(null);
    setError(null);

    try {
      const response = await fetch('http://localhost:5000/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Gagal terhubung ke server');
      }

      setResult(data);
    } catch (err) {
      console.error('Error saat analisis sentimen:', err);
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 font-urbanist">
      <Navbar />

      <main className="flex flex-col md:flex-row justify-center items-start pt-32 pb-20 px-8 gap-10 max-w-6xl mx-auto w-full">
        <div className="w-full md:w-1/2">
          <SentimentForm
            onAnalyze={handleAnalyze}
            isLoading={isLoading}
          />
        </div>

        <div className="w-full md:w-1/2">
          <SentimentResult
            result={result}
            isLoading={isLoading}
            error={error}
          />
        </div>
      </main>
    </div>
  );
};

export default App;
