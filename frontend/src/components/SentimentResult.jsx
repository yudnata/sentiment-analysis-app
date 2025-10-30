import React from 'react';
import { FaSpinner } from 'react-icons/fa';

const SentimentResult = ({ result, isLoading, error }) => {

  if (isLoading) {
    return (
      <div className="bg-white border border-gray-200 p-10 rounded-3xl shadow-md h-[450px] flex flex-col justify-center items-center">
        <FaSpinner
          className="animate-spin text-green-500"
          size={60}
        />
        <p className="mt-4 text-gray-500 text-lg">Menganalisis...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-white border border-gray-200 p-10 rounded-3xl shadow-md h-[450px] flex flex-col justify-center items-center">
        <h3 className="text-2xl font-semibold text-red-500">Terjadi Error</h3>
        <p className="mt-4 text-gray-600 text-center">{error}</p>
      </div>
    );
  }

  if (result) {
    const color =
      result.sentiment === 'POSITIF'
        ? 'text-green-500'
        : 'text-red-500'

    const bgColor =
      result.sentiment === 'POSITIF'
        ? 'bg-green-500'
        : 'bg-red-500'

    const probabilityPercent = Math.round(result.probability);

    return (
      <div className="bg-white border border-gray-200 p-10 rounded-3xl shadow-md h-[450px] flex flex-col justify-center items-center transition-all duration-300">
        <h2 className="text-2xl font-semibold text-gray-800 mb-3">Hasil Analisis Sentimen</h2>
        <p
          className={`mt-6 text-5xl font-extrabold tracking-wide ${color} transition-all duration-300`}
        >
          {result.sentiment.toUpperCase()}
        </p>
        <p className="mt-5 text-gray-500 text-base italic">
          Probabilitas: <span className="font-medium text-gray-700">{probabilityPercent}%</span>
        </p>
        <div className="mt-8 w-full bg-gray-100 rounded-xl h-3 overflow-hidden">
          <div
            className={`h-3 ${bgColor}`}
            style={{ width: `${probabilityPercent}%` }}
          ></div>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white border border-gray-200 p-10 rounded-3xl shadow-md h-[450px] flex flex-col justify-center items-center transition-all duration-300">
      <div className="text-gray-400 italic text-center text-lg">
        Hasil analisis akan muncul di sini setelah Anda mengirim opini
      </div>
    </div>
  );
};

export default SentimentResult;
