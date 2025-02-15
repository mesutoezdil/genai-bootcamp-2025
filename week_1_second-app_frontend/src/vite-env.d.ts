/// <reference types="vite/client" />

// Ensures TypeScript recognizes `.env` variables from Vite
interface ImportMetaEnv {
    readonly VITE_API_URL: string;
    readonly VITE_APP_NAME: string;
}

interface ImportMeta {
    readonly env: ImportMetaEnv;
}
