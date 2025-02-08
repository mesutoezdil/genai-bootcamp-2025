"use client";

import { useState } from 'react';

export default function IdeaScreen() {
  const [idea, setIdea] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // TODO: Handle form submission
    console.log('Submitted idea:', idea);
  };

  return (
    <div className="min-h-screen bg-black text-white flex items-center justify-center p-4">
      <div className="w-[90%] max-w-[600px] p-5 border-2 border-white rounded-lg">
        <div className="text-left mb-10 text-lg">
          SCREEN 1: IDEA SCREEN
        </div>

        <form onSubmit={handleSubmit} className="flex flex-col gap-5 p-5">
          <label className="text-center text-lg">
            TYPE YOUR IDEA:
          </label>

          <input
            type="text"
            value={idea}
            onChange={(e) => setIdea(e.target.value)}
            placeholder="Enter your idea here"
            className="p-2.5 border-2 border-white rounded bg-transparent text-white"
          />

          <button
            type="submit"
            className="mt-5 px-5 py-2.5 bg-white text-black rounded hover:bg-gray-200 transition-colors"
          >
            Continue
          </button>
        </form>
      </div>
    </div>
  );
}
