export interface Word {
  id: string
  chinese: string
  pinyin: string
  english: string
  difficulty: 'easy' | 'medium' | 'hard'
  lastReviewed?: Date
}

export interface StudySession {
  id: string
  date: Date
  wordsStudied: number
  correctAnswers: number
  durationMinutes: number
}

export interface User {
  id: string
  name: string
  email: string
  streakDays: number
  totalWordsLearned: number
}
