import React, { useState } from 'react';
import Navbar from './components/Navbar';
import SentimentForm from './components/SentimentForm';
import SentimentResult from './components/SentimentResult';

const App = () => {
  const [result, setResult] = useState(null);

  return (
    <div className="min-h-screen bg-slate-50 font-urbanist">
      <Navbar />

      <main className="flex flex-col md:flex-row justify-center items-start pt-32 pb-20 px-8 gap-10 max-w-6xl mx-auto w-full">
        {/* Form di sisi kiri */}
        <div className="w-full md:w-1/2">
          <SentimentForm setResult={setResult} />
        </div>

        {/* Card hasil di sisi kanan */}
        <div className="w-full md:w-1/2">
          <SentimentResult result={result} />
        </div>
      </main>
    </div>
  );
};

export default App;
