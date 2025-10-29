import React from 'react';
import { FaGithub, FaSyncAlt, FaMoon, FaUserCircle } from 'react-icons/fa';

const Navbar = () => {
  const handleRefresh = () => {
    window.location.reload();
  };

  return (
    <header className="flex justify-between items-center px-12 py-4 bg-white/80 backdrop-blur-md shadow-sm fixed top-0 left-0 right-0 z-50">

      <h1 className="text-2xl font-bold text-green-600 tracking-tight">
        Sentiment<span className="text-gray-800">Analysis.</span>
      </h1>

      <nav className="flex items-center gap-6 text-gray-700">
        <a
          href="https://github.com/"
          target="_blank"
          rel="noopener noreferrer"
          className="flex items-center gap-2 hover:text-green-600 transition-colors"
        >
          <FaGithub size={20} />
          <span>GitHub</span>
        </a>

        <button
          onClick={handleRefresh}
          className="flex items-center gap-2 hover:text-green-600 transition-colors"
        >
          <FaSyncAlt size={18} />
          <span>Refresh</span>
        </button>

        <div className="flex items-center gap-2 ml-4 text-gray-800 font-medium">
          <FaUserCircle
            size={22}
            className="text-green-600"
          />
          <span>2305551142</span>
        </div>
      </nav>
    </header>
  );
};

export default Navbar;
