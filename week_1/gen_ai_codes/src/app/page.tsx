"use client";

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';

export default function IdeaScreen() {
  const router = useRouter();
  const [idea, setIdea] = useState('');
  const [isGlowing, setIsGlowing] = useState(false);

  // Add pulsing animation every second
  useEffect(() => {
    const interval = setInterval(() => {
      setIsGlowing(true);
      setTimeout(() => setIsGlowing(false), 500); // Glow for 500ms
    }, 1000);

    return () => clearInterval(interval);
  }, []);

  const handleGetRandomIdea = () => {
    const randomIdeas = [
      "A game that teaches Chinese characters through storytelling",
      "An app that matches Chinese idioms with their origin stories",
      "A virtual tour guide teaching daily Chinese conversations",
      "A Chinese cooking game that teaches food vocabulary",
      "A time-travel adventure learning Chinese dynasties",
      "A karaoke app for learning Chinese songs",
      "A puzzle game with Chinese radicals",
      "A shopping simulation to learn numbers and money"
    ];
    setIdea(randomIdeas[Math.floor(Math.random() * randomIdeas.length)]);
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (idea.trim()) {
      router.push(`/practice?idea=${encodeURIComponent(idea)}`);
    }
  };

  return (
    <div className="min-h-screen bg-black text-white flex items-center justify-center p-4">
      <div className={`
        w-[90%] max-w-[600px] p-8 
        border-2 border-[#ff6b6b]/30 rounded-2xl relative
        animate-border-glow
        transition-all duration-300
        hover:shadow-[0_0_20px_#ff6b6b33]
        ${isGlowing ? 'shadow-[0_0_30px_#ff6b6b40]' : ''}
      `}>
        <div className="text-center mb-2 text-3xl font-bold bg-gradient-to-r from-[#ff6b6b] to-[#ffd93d] bg-clip-text text-transparent flex items-center justify-center gap-2">
          Share Your Chinese Learning Idea! 🐲
        </div>

        <p className="text-center text-gray-400 mb-8">
          Let's innovate Chinese language education together! Share your idea for making learning Chinese more engaging.
        </p>

        <form onSubmit={handleSubmit} className="flex flex-col gap-5">
          <label className="text-center text-xl text-[#ff6b6b]">
            What Chinese learning concept should we explore?
            <span className="block text-sm text-gray-400 mt-1">
              让我们开始吧！(Let's begin!)
            </span>
          </label>

          <input
            type="text"
            value={idea}
            onChange={(e) => setIdea(e.target.value)}
            placeholder="Examples: character memorization games, pronunciation practice apps..."
            className="p-4 border-2 border-[#ff6b6b]/30 rounded-xl bg-transparent text-white 
                     focus:border-[#ff6b6b] focus:outline-none focus:ring-2 focus:ring-[#ff6b6b]/50
                     transition-all duration-300"
          />

          <div className="flex flex-col gap-3 mt-4">
            <button
              type="submit"
              disabled={!idea.trim()}
              className="px-8 py-4 bg-gradient-to-r from-[#ff6b6b] to-[#ffd93d] rounded-xl
                       hover:from-[#ff5252] hover:to-[#ffd21d] transition-all duration-300
                       font-semibold text-lg disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Continue 继续 →
            </button>

            <button
              type="button"
              onClick={handleGetRandomIdea}
              className="px-8 py-3 border border-[#ff6b6b]/30 rounded-xl
                       hover:bg-[#ff6b6b]/10 transition-all duration-300
                       text-white/70 hover:text-white"
            >
              Get Random Idea 随机想法 ✨
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
