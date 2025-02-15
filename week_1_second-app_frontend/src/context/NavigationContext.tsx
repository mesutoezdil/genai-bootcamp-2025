import React, { createContext, useContext, useState, useCallback } from "react";
import type { GroupDetails, Word } from "../services/api";

interface StudyActivity {
  id: number;
  title: string;
  launch_url: string;
  preview_url: string;
}

interface NavigationContextType {
  currentGroup: GroupDetails | null;
  setCurrentGroup: (group: GroupDetails | null) => void;
  currentWord: Word | null;
  setCurrentWord: (word: Word | null) => void;
  currentStudyActivity: StudyActivity | null;
  setCurrentStudyActivity: (activity: StudyActivity | null) => void;
}

// Create context
const NavigationContext = createContext<NavigationContextType | undefined>(undefined);

export const NavigationProvider = React.memo(({ children }: { children: React.ReactNode }) => {
  const [currentGroup, setCurrentGroup] = useState<GroupDetails | null>(null);
  const [currentWord, setCurrentWord] = useState<Word | null>(null);
  const [currentStudyActivity, setCurrentStudyActivity] = useState<StudyActivity | null>(null);

  // Memoize state setters to avoid unnecessary renders
  const handleSetCurrentGroup = useCallback((group: GroupDetails | null) => {
    setCurrentGroup(group);
  }, []);

  const handleSetCurrentWord = useCallback((word: Word | null) => {
    setCurrentWord(word);
  }, []);

  const handleSetCurrentStudyActivity = useCallback((activity: StudyActivity | null) => {
    setCurrentStudyActivity(activity);
  }, []);

  return (
    <NavigationContext.Provider
      value={{
        currentGroup,
        setCurrentGroup: handleSetCurrentGroup,
        currentWord,
        setCurrentWord: handleSetCurrentWord,
        currentStudyActivity,
        setCurrentStudyActivity: handleSetCurrentStudyActivity,
      }}
    >
      {children}
    </NavigationContext.Provider>
  );
});

export function useNavigation() {
  const context = useContext(NavigationContext);
  if (!context) {
    throw new Error("useNavigation must be used within a NavigationProvider");
  }
  return context;
}
