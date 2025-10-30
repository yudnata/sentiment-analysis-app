import React, { useState } from 'react';

const SentimentForm = ({ onAnalyze, isLoading }) => {
  const [text, setText] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!text.trim()) return; 
    onAnalyze(text);
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="bg-white border border-gray-200 p-10 rounded-3xl shadow-md flex flex-col gap-6 transition-all duration-300 h-[450px]"
    >
      <h2 className="text-2xl font-semibold text-gray-800">Analisis Sentimen</h2>
      <label className="text-lg font-medium text-gray-600">Masukkan Ulasan Produk:</label>

      <textarea
        className="w-full p-4 rounded-xl bg-gray-50 border border-gray-300 text-gray-800 resize-none focus:outline-none focus:ring-2 focus:ring-green-400 focus:border-transparent transition-all text-base"
        rows="6"
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Contoh: Saya setuju dengan kebijakan PPKM karena membantu menekan penyebaran COVID-19"
        required
        disabled={isLoading}
      />

      <button
        type="submit"
        className="bg-green-500 hover:bg-green-600 text-white font-semibold py-3 rounded-xl text-lg shadow-md transition-all disabled:bg-gray-400 disabled:cursor-not-allowed"
        disabled={isLoading}
      >
        {isLoading ? 'Menganalisis...' : 'Analisis'}
      </button>
    </form>
  );
};

export default SentimentForm;
