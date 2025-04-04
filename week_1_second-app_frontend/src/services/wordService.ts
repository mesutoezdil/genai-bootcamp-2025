import api from '@/lib/api'

export interface Word {
  id: number
  character: string
  pinyin: string
  meaning: string
  level: string
  created_at: string
  updated_at: string
}

export interface CreateWordInput {
  character: string
  pinyin: string
  meaning: string
  level: string
}

export interface UpdateWordInput extends Partial<CreateWordInput> {}

const wordService = {
  getWords: async () => {
    const response = await api.get<Word[]>('/words')
    return response.data
  },

  getWord: async (id: number) => {
    const response = await api.get<Word>(`/words/${id}`)
    return response.data
  },

  createWord: async (word: CreateWordInput) => {
    const response = await api.post<Word>('/words', word)
    return response.data
  },

  updateWord: async (id: number, word: UpdateWordInput) => {
    const response = await api.put<Word>(`/words/${id}`, word)
    return response.data
  },

  deleteWord: async (id: number) => {
    await api.delete(`/words/${id}`)
  },

  searchWords: async (query: string) => {
    const response = await api.get<Word[]>(`/words/search?q=${encodeURIComponent(query)}`)
    return response.data
  },
}

export default wordService
