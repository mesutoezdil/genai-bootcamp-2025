import api from '@/lib/api'

export interface StudySession {
  id: number
  start_time: string
  duration_minutes: number
  focus_area: string
  notes: string
  created_at: string
  updated_at: string
}

export interface CreateStudySessionInput {
  start_time: string
  duration_minutes: number
  focus_area: string
  notes?: string
}

export interface UpdateStudySessionInput extends Partial<CreateStudySessionInput> {}

export interface StudySessionStats {
  total_sessions: number
  total_minutes: number
  average_duration: number
  focus_area_breakdown: Record<string, number>
}

const studySessionService = {
  getSessions: async () => {
    const response = await api.get<StudySession[]>('/sessions')
    return response.data
  },

  getSession: async (id: number) => {
    const response = await api.get<StudySession>(`/sessions/${id}`)
    return response.data
  },

  createSession: async (session: CreateStudySessionInput) => {
    const response = await api.post<StudySession>('/sessions', session)
    return response.data
  },

  updateSession: async (id: number, session: UpdateStudySessionInput) => {
    const response = await api.put<StudySession>(`/sessions/${id}`, session)
    return response.data
  },

  deleteSession: async (id: number) => {
    await api.delete(`/sessions/${id}`)
  },

  getStats: async () => {
    const response = await api.get<StudySessionStats>('/sessions/stats')
    return response.data
  },

  getRecentSessions: async (limit: number = 5) => {
    const response = await api.get<StudySession[]>(`/sessions/recent?limit=${limit}`)
    return response.data
  }
}

export default studySessionService
