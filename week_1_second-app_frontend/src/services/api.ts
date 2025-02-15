const API_BASE_URL = 'http://localhost:5000';

// Group types
export interface Group {
  id: number;
  group_name: string;
  word_count: number;
}

export interface GroupsResponse {
  groups: Group[];
  total_pages: number;
  current_page: number;
}

// Word types
export interface WordGroup {
  id: number;
  name: string;
}

export interface Word {
  id: number;
  hanzi: string;
  pinyin: string;
  english: string;
  correct_count: number;
  wrong_count: number;
  groups: WordGroup[];
}

export interface WordsResponse {
  words: Word[];
  total_pages: number;
  current_page: number;
  total_words: number;
}

// Study Session types
export interface StudySession {
  id: number;
  group_id: number;
  group_name: string;
  activity_id: number;
  activity_name: string;
  start_time: string;
  end_time: string;
  review_items_count: number;
}

export interface WordReview {
  word_id: number;
  is_correct: boolean;
}

// Dashboard types
export interface RecentSession {
  id: number;
  group_id: number;
  activity_name: string;
  created_at: string;
  correct_count: number;
  wrong_count: number;
}

export interface StudyStats {
  total_vocabulary: number;
  total_words_studied: number;
  mastered_words: number;
  success_rate: number;
  total_sessions: number;
  active_groups: number;
  current_streak: number;
}

// Utility function for handling fetch requests
async function fetchData<T>(url: string, options?: RequestInit): Promise<T> {
  const response = await fetch(url, options);
  if (!response.ok) {
    throw new Error(`API Error: ${response.statusText}`);
  }
  return response.json();
}

// Group API
export const fetchGroups = async (
  page: number = 1,
  sortBy: string = 'name',
  order: 'asc' | 'desc' = 'asc'
): Promise<GroupsResponse> => {
  return fetchData<GroupsResponse>(
    `${API_BASE_URL}/groups?page=${page}&sort_by=${sortBy}&order=${order}`
  );
};

export interface GroupDetails {
  id: number;
  group_name: string;
  word_count: number;
}

export const fetchGroupDetails = async (groupId: number): Promise<GroupDetails> => {
  return fetchData<GroupDetails>(`${API_BASE_URL}/groups/${groupId}`);
};

export const fetchGroupWords = async (
  groupId: number,
  page: number = 1,
  sortBy: string = 'hanzi',
  order: 'asc' | 'desc' = 'asc'
): Promise<WordsResponse> => {
  return fetchData<WordsResponse>(
    `${API_BASE_URL}/groups/${groupId}/words?page=${page}&sort_by=${sortBy}&order=${order}`
  );
};

// Word API
export const fetchWords = async (
  page: number = 1,
  sortBy: string = 'hanzi',
  order: 'asc' | 'desc' = 'asc'
): Promise<WordsResponse> => {
  return fetchData<WordsResponse>(
    `${API_BASE_URL}/words?page=${page}&sort_by=${sortBy}&order=${order}`
  );
};

export const fetchWordDetails = async (wordId: number): Promise<Word> => {
  return fetchData<Word>(`${API_BASE_URL}/words/${wordId}`);
};

// Study Session API
export const createStudySession = async (
  groupId: number,
  studyActivityId: number
): Promise<{ session_id: number }> => {
  return fetchData<{ session_id: number }>(`${API_BASE_URL}/study_sessions`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ group_id: groupId, study_activity_id: studyActivityId }),
  });
};

export const submitStudySessionReview = async (
  sessionId: number,
  reviews: WordReview[]
): Promise<void> => {
  await fetchData(`${API_BASE_URL}/study_sessions/${sessionId}/review`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ reviews }),
  });
};

export interface StudySessionsResponse {
  study_sessions: StudySession[];
  total_pages: number;
  current_page: number;
}

export const fetchStudySessions = async (
  page: number = 1,
  perPage: number = 10
): Promise<StudySessionsResponse> => {
  return fetchData<StudySessionsResponse>(
    `${API_BASE_URL}/study-sessions?page=${page}&per_page=${perPage}`
  );
};

export const fetchGroupStudySessions = async (
  groupId: number,
  page: number = 1,
  sortBy: string = 'created_at',
  order: 'asc' | 'desc' = 'desc'
): Promise<StudySessionsResponse> => {
  return fetchData<StudySessionsResponse>(
    `${API_BASE_URL}/groups/${groupId}/study_sessions?page=${page}&sort_by=${sortBy}&order=${order}`
  );
};

// Dashboard API
export const fetchRecentStudySession = async (): Promise<RecentSession | null> => {
  return fetchData<RecentSession | null>(`${API_BASE_URL}/dashboard/recent-session`);
};

export const fetchStudyStats = async (): Promise<StudyStats> => {
  return fetchData<StudyStats>(`${API_BASE_URL}/dashboard/stats`);
};
