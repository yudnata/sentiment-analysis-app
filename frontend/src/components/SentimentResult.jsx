import React from 'react';

const SentimentResult = ({ result }) => {
  const color =
    result?.sentiment === 'positif'
      ? 'text-green-500'
      : result?.sentiment === 'negatif'
      ? 'text-red-500'
      : 'text-yellow-500';

  return (
    <div className="bg-white border border-gray-200 p-10 rounded-3xl shadow-md h-[450px] flex flex-col justify-center items-center transition-all duration-300">
      {!result ? (
        <div className="text-gray-400 italic text-center text-lg">
          Hasil analisis akan muncul di sini setelah Anda mengirim opini
        </div>
      ) : (
        <>
          <h2 className="text-2xl font-semibold text-gray-800 mb-3">Hasil Analisis Sentimen</h2>
          <p
            className={`mt-6 text-5xl font-extrabold tracking-wide ${color} transition-all duration-300`}
          >
            {result.sentiment.toUpperCase()}
          </p>
          <p className="mt-5 text-gray-500 text-base italic">
            Probabilitas: <span className="font-medium text-gray-700">{result.probability}</span>
          </p>

          <div className="mt-8 w-full bg-gray-100 rounded-xl h-3 overflow-hidden">
            <div
              className={`h-3 ${
                result?.sentiment === 'positif'
                  ? 'bg-green-500'
                  : result?.sentiment === 'negatif'
                  ? 'bg-red-500'
                  : 'bg-yellow-400'
              }`}
              style={{ width: `${Math.round(result.probability * 100)}%` }}
            ></div>
          </div>
        </>
      )}
    </div>
  );
};

export default SentimentResult;
