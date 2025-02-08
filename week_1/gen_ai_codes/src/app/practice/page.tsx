"use client";

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';

interface Challenge {
    question: string;
    answer: string;
    hint: string;
    explanation: string;
    points: number;
    theme: string;
}

const allChallenges: Record<string, Challenge[]> = {
    "time-travel": [
        {
            question: "What dynasty is 明朝 (Míng cháo)?",
            answer: "Ming Dynasty",
            hint: "This dynasty ruled China from 1368-1644",
            explanation: "明朝 (Míng cháo) was one of China's most prosperous dynasties",
            points: 10,
            theme: "time-travel"
        },
        // ... more dynasty-related challenges
    ],
    "cooking": [
        {
            question: "What does 炒 (chǎo) mean in cooking?",
            answer: "stir fry",
            hint: "This is a common cooking method in Chinese cuisine",
            explanation: "炒 (chǎo) is the basic technique for wok cooking",
            points: 8,
            theme: "cooking"
        },
        // ... more cooking-related challenges
    ],
    // ... other themes
};

// Use a larger local dictionary instead
const chineseVocabulary = [
    // Numbers (1-10)
    { word: '一', pinyin: 'yī', meaning: 'one', category: 'numbers' },
    { word: '二', pinyin: 'èr', meaning: 'two', category: 'numbers' },
    { word: '三', pinyin: 'sān', meaning: 'three', category: 'numbers' },
    { word: '四', pinyin: 'sì', meaning: 'four', category: 'numbers' },
    { word: '五', pinyin: 'wǔ', meaning: 'five', category: 'numbers' },
    { word: '六', pinyin: 'liù', meaning: 'six', category: 'numbers' },
    { word: '七', pinyin: 'qī', meaning: 'seven', category: 'numbers' },
    { word: '八', pinyin: 'bā', meaning: 'eight', category: 'numbers' },
    { word: '九', pinyin: 'jiǔ', meaning: 'nine', category: 'numbers' },
    { word: '十', pinyin: 'shí', meaning: 'ten', category: 'numbers' },

    // Basic Verbs
    { word: '是', pinyin: 'shì', meaning: 'to be', category: 'verbs' },
    { word: '有', pinyin: 'yǒu', meaning: 'to have', category: 'verbs' },
    { word: '看', pinyin: 'kàn', meaning: 'to look/see', category: 'verbs' },
    { word: '听', pinyin: 'tīng', meaning: 'to listen', category: 'verbs' },
    { word: '说', pinyin: 'shuō', meaning: 'to speak', category: 'verbs' },
    { word: '吃', pinyin: 'chī', meaning: 'to eat', category: 'verbs' },
    { word: '喝', pinyin: 'hē', meaning: 'to drink', category: 'verbs' },
    { word: '睡觉', pinyin: 'shuì jiào', meaning: 'to sleep', category: 'verbs' },
    { word: '学习', pinyin: 'xué xí', meaning: 'to study', category: 'verbs' },
    { word: '工作', pinyin: 'gōng zuò', meaning: 'to work', category: 'verbs' },

    // Common Nouns
    { word: '水', pinyin: 'shuǐ', meaning: 'water', category: 'nouns' },
    { word: '茶', pinyin: 'chá', meaning: 'tea', category: 'nouns' },
    { word: '饭', pinyin: 'fàn', meaning: 'rice/meal', category: 'nouns' },
    { word: '书', pinyin: 'shū', meaning: 'book', category: 'nouns' },
    { word: '桌子', pinyin: 'zhuō zi', meaning: 'table', category: 'nouns' },
    { word: '椅子', pinyin: 'yǐ zi', meaning: 'chair', category: 'nouns' },
    { word: '电脑', pinyin: 'diàn nǎo', meaning: 'computer', category: 'nouns' },
    { word: '手机', pinyin: 'shǒu jī', meaning: 'mobile phone', category: 'nouns' },

    // Time Words
    { word: '今天', pinyin: 'jīn tiān', meaning: 'today', category: 'time' },
    { word: '明天', pinyin: 'míng tiān', meaning: 'tomorrow', category: 'time' },
    { word: '昨天', pinyin: 'zuó tiān', meaning: 'yesterday', category: 'time' },
    { word: '上午', pinyin: 'shàng wǔ', meaning: 'morning', category: 'time' },
    { word: '下午', pinyin: 'xià wǔ', meaning: 'afternoon', category: 'time' },
    { word: '晚上', pinyin: 'wǎn shang', meaning: 'evening', category: 'time' }
];

// Convert vocabulary to challenges
const languageChallenges: Challenge[] = chineseVocabulary.map(word => ({
    question: `What does '${word.word}' (${word.pinyin}) mean?`,
    answer: word.meaning,
    hint: `Category: ${word.category}`,
    explanation: `${word.word} (${word.pinyin}) means '${word.meaning}' in Chinese`,
    points: 5
}));

export default function PracticeScreen() {
    const router = useRouter();
    const [userAnswer, setUserAnswer] = useState('');
    const [timeLeft, setTimeLeft] = useState(60);
    const [iterationCount, setIterationCount] = useState(1);
    const [isTimerRunning, setIsTimerRunning] = useState(false);
    const [currentChallenge, setCurrentChallenge] = useState<Challenge | null>(null);
    const [feedback, setFeedback] = useState<'correct' | 'incorrect' | null>(null);
    const [showSolution, setShowSolution] = useState(false);
    const [totalPoints, setTotalPoints] = useState(0);
    const [progress, setProgress] = useState(0);
    const [currentTheme, setCurrentTheme] = useState<string>('');

    const challenges: Challenge[] = [
        {
            question: "Translate: 我是中国人 (Wǒ shì zhōngguó rén)",
            answer: "I am Chinese",
            hint: "Focus on the basic sentence structure: Subject + 是 (to be) + Nationality",
            explanation: "'我' means 'I', '是' means 'am', '中国人' means 'Chinese person'",
            points: 10
        },
        {
            question: "Write the pinyin for: 谢谢",
            answer: "xiexie",
            hint: "This is a common way to say 'thank you'",
            explanation: "谢谢 (xièxiè) is one of the most basic and important phrases in Chinese",
            points: 5
        },
        {
            question: "What does '龙' mean?",
            answer: "dragon",
            hint: "This is a legendary creature in Chinese culture",
            explanation: "龙 (lóng) is the Chinese dragon, a symbol of power and good fortune",
            points: 8
        }
    ];

    // Timer color calculation
    const getTimerColor = () => {
        if (timeLeft > 40) return 'text-green-400';
        if (timeLeft > 20) return 'text-yellow-400';
        return 'text-red-400';
    };

    useEffect(() => {
        // Get theme from URL
        const params = new URLSearchParams(window.location.search);
        const theme = params.get('theme') || 'time-travel';
        setCurrentTheme(theme);
    }, []);

    useEffect(() => {
        if (isTimerRunning && timeLeft > 0) {
            const timer = setInterval(() => {
                setTimeLeft((prev) => {
                    if (prev <= 1) {
                        // When timer hits 0, show timeout message
                        setFeedback('incorrect');
                        setShowSolution(true);
                        return 0;
                    }
                    return prev - 1;
                });
            }, 1000);
            return () => clearInterval(timer);
        }
    }, [isTimerRunning, timeLeft]);

    const getRandomChallenge = () => {
        const randomChallenge = languageChallenges[
            Math.floor(Math.random() * languageChallenges.length)
        ];
        setCurrentChallenge(randomChallenge);
        setIsTimerRunning(true);
        setFeedback(null);
        setShowSolution(false);
        setUserAnswer('');
        setTimeLeft(60);
        setProgress((iterationCount / 5) * 100);
    };

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        try {
            if (!currentChallenge) return;
            const isCorrect = userAnswer.toLowerCase().trim() === currentChallenge.answer.toLowerCase();
            setFeedback(isCorrect ? 'correct' : 'incorrect');

            if (isCorrect) {
                setTotalPoints(prev => prev + currentChallenge.points);
                setIterationCount((prev) => prev + 1);
                getRandomChallenge();
            }
        } catch (err) {
            console.error('Something went wrong. Please try again.');
        }
    };

    return (
        <div className="min-h-screen bg-black text-white relative overflow-hidden">
            {/* Static Chinese Characters */}
            {[
                '学', '习', '中', '文', '加', '油', '好', '棒', '语', '言',
                '我', '你', '他', '她', '它', '们', '的', '是', '在', '有'
            ].map((char, index) => (
                <div
                    key={index}
                    className="fixed text-[#ff6b6b] text-8xl opacity-[0.03]"
                    style={{
                        left: `${(index * 10) % 100}%`,
                        top: `${Math.floor(index / 10) * 20}%`,
                        transform: `rotate(${Math.random() * 45}deg)`,
                    }}
                >
                    {char}
                </div>
            ))}

            {/* Main container with back button just above it */}
            <div className="relative z-10 min-h-screen flex flex-col items-center justify-center p-4">
                {/* Back button moved closer to main container */}
                <div className="mb-4">
                    <button
                        onClick={() => router.push('/')}
                        className="text-[#ff6b6b] hover:text-white flex items-center gap-2 transition-colors duration-300"
                    >
                        ← Back to Step 1 返回
                    </button>
                </div>

                <div className="w-[90%] max-w-[600px] p-8 border-2 border-[#ff6b6b]/30 rounded-2xl">
                    <div className="text-center mb-2 text-3xl font-bold bg-gradient-to-r from-[#ff6b6b] to-[#ffd93d] bg-clip-text text-transparent flex items-center justify-center gap-2">
                        Step 2: Practice & Iterate <span>💫</span>
                    </div>

                    <div className="flex justify-between items-center mb-4">
                        <div className="text-xl font-bold text-[#ffd93d]">
                            Points: {totalPoints} ⭐
                        </div>
                        <div className={`text-xl font-bold text-[#22c55e]`}>
                            Time Left: <span className="text-[#22c55e]">{timeLeft}s</span>
                        </div>
                    </div>

                    <div className="text-center text-2xl font-bold text-[#ffd93d] mb-4">
                        Challenge #{iterationCount}
                    </div>

                    <form onSubmit={handleSubmit} className="flex flex-col gap-5">
                        {currentChallenge ? (
                            <>
                                <div className="p-6 border-2 border-[#ff6b6b]/30 rounded-xl bg-transparent text-white text-center">
                                    <p className="text-xl mb-3">{currentChallenge.question}</p>
                                    <p className="text-sm text-gray-400">{currentChallenge.hint}</p>
                                </div>

                                <input
                                    type="text"
                                    value={userAnswer}
                                    onChange={(e) => setUserAnswer(e.target.value)}
                                    placeholder="Type your answer here..."
                                    className="p-4 border-2 border-[#ff6b6b]/30 rounded-xl bg-transparent text-white 
                                             focus:border-[#ff6b6b] focus:outline-none focus:ring-2 focus:ring-[#ff6b6b]/50
                                             transition-all duration-300"
                                />

                                {feedback && (
                                    <div className={`text-center p-4 rounded-lg ${feedback === 'correct'
                                            ? 'bg-green-500/20 text-green-400 animate-bounce'
                                            : 'bg-orange-500/20 text-orange-400'
                                        }`}>
                                        {feedback === 'correct'
                                            ? `正确 Excellent! +${currentChallenge.points} points! 🎉`
                                            : 'Almost there! Keep trying! 加油! 💪'}
                                    </div>
                                )}
                            </>
                        )}
                    </form>
                </div>
            </div>
        </div>
    );
}