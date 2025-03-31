# Chinese Learning App - Frontend

Welcome to the **Chinese Learning App** frontend! Built with **React**, **TypeScript**, and **Vite**, this application offers a **fast** and **interactive** interface for learners to explore and practice Chinese language content. The project is configured with **ESLint**, **Prettier**, **React Query**, **Tailwind CSS**, and **React Router** to ensure a robust and maintainable codebase.

---

## Table of Contents

1. [Overview](#1-overview)  
2. [Tech Stack](#2-tech-stack)  
3. [Project Setup](#3-project-setup)  
   1. [Cloning the Repository](#31-cloning-the-repository)  
   2. [Installing Dependencies](#32-installing-dependencies)  
4. [Development](#4-development)  
   1. [Local Development Server](#41-local-development-server)  
   2. [Production Build](#42-production-build)  
5. [ESLint & Code Quality](#5-eslint--code-quality)  
   1. [Type-Aware ESLint Configuration](#51-type-aware-eslint-configuration)  
   2. [React ESLint Plugin](#52-react-eslint-plugin)  
6. [Styling](#6-styling)  
7. [API Integration](#7-api-integration)  
8. [Project Structure](#8-project-structure)  
9. [Contributing](#9-contributing)  
10. [License](#10-license)  
11. [Additional Tips](#11-additional-tips)

---

## 1. Overview

This **React + TypeScript** application serves as the **frontend** for a comprehensive Chinese learning platform, communicating with a **Flask**-based backend. By leveraging **Vite** for lightning-fast development and bundling, the app provides a seamless environment for building interactive language lessons, exercises, and progress tracking features.

**Key Advantages**:
- **Fast Iterations**: Vite ensures minimal compile times and instant HMR (Hot Module Replacement).
- **Strict Type-Checking**: TypeScript reduces runtime errors by catching type issues during development.
- **Maintained Code Style**: ESLint & Prettier enforce consistent coding patterns and formatting.

---

## 2. Tech Stack

- **React 18**  
  Core library for building user interfaces, with **React Router** for client-side navigation.
- **TypeScript**  
  Ensures type safety and clarity in the codebase.
- **Vite**  
  Lightning-fast development server and build tool.
- **Tailwind CSS**  
  Utility-first CSS framework for rapid UI prototyping.
- **React Query**  
  Simplifies data fetching, caching, and state synchronization with the backend.
- **ESLint & Prettier**  
  Automated code checks and formatting for a consistent developer experience.

---

## 3. Project Setup

### 3.1 Cloning the Repository

```bash
git clone https://github.com/your-repo/chinese-learning-app.git
cd chinese-learning-app-frontend
```

### 3.2 Installing Dependencies

Install the required packages:

```bash
npm install
```

> **Tip**: If you prefer **Yarn** or **pnpm**, simply adapt the commands accordingly.

---

## 4. Development

### 4.1 Local Development Server

Launch the local dev server:

```bash
npm run dev
```

- The application becomes accessible at **`http://localhost:5173`** (by default).
- Vite’s **HMR** ensures immediate UI updates as you save files.

### 4.2 Production Build

Generate an optimized build for production deployment:

```bash
npm run build
```

- The output is placed in the `dist/` directory.
- You can serve this build via any static hosting solution or integrate it into a Node.js/Flask server for a comprehensive deployment.

---

## 5. ESLint & Code Quality

### 5.1 Type-Aware ESLint Configuration

For robust type-aware linting, **enable project-based parser settings** in your ESLint config (e.g., `eslint.config.js` or `.eslintrc.js`):

```js
export default tseslint.config({
  languageOptions: {
    parserOptions: {
      project: ['./tsconfig.node.json', './tsconfig.app.json'],
      tsconfigRootDir: import.meta.dirname,
    },
  },
})
```

**Recommended**: Switch from `tseslint.configs.recommended` to `tseslint.configs.recommendedTypeChecked`, optionally including `...tseslint.configs.stylisticTypeChecked` for stricter style checks.

### 5.2 React ESLint Plugin

**eslint-plugin-react** helps catch React-specific issues:

```bash
npm install eslint-plugin-react --save-dev
```

Then update `eslint.config.js`:

```js
import react from 'eslint-plugin-react'

export default tseslint.config({
  settings: { react: { version: '18.3' } },
  plugins: { react },
  rules: {
    ...react.configs.recommended.rules,
    ...react.configs['jsx-runtime'].rules,
  },
})
```

This approach ensures your React code follows recommended best practices.

---

## 6. Styling

**Tailwind CSS** accelerates UI styling with utility classes:

1. **Install**:
   ```bash
   npm install -D tailwindcss postcss autoprefixer
   npx tailwindcss init -p
   ```
2. **Configuration** (`tailwind.config.js`):
   ```js
   module.exports = {
     content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
     theme: {
       extend: {},
     },
     plugins: [],
   }
   ```
3. **Import**: In your primary CSS (e.g., `src/styles/index.css`):
   ```css
   @tailwind base;
   @tailwind components;
   @tailwind utilities;
   ```
  
**Tip**: Combine Tailwind with design systems or custom themes to achieve a consistent look across pages.

---

## 7. API Integration

By default, the app communicates with a **Flask backend** at `http://localhost:5000/api/`. Customize your **Vite** proxy settings in `vite.config.ts`:

```ts
server: {
  proxy: {
    '/api': {
      target: 'http://localhost:5000',
      changeOrigin: true,
      rewrite: (path) => path.replace(/^\/api/, ''),
    },
  },
},
```

This setup allows you to make calls like `fetch('/api/lessons')` in your React code without manually specifying the server domain.

---

## 8. Project Structure

Below is a recommended folder structure:

```
chinese-learning-app-frontend/
├── src/
│   ├── assets/          # Static assets (images, icons, fonts)
│   ├── components/      # Reusable UI components (e.g., Button, Card, Navbar)
│   ├── pages/           # Page-level components (Home, Lessons, Profile, etc.)
│   ├── hooks/           # Custom hooks (e.g., useFetchLessons, useUserAuth)
│   ├── styles/          # Global or modular CSS (Tailwind entry, overrides)
│   ├── api/             # API interaction functions (fetch words, exercises)
│   ├── routes.tsx       # React Router configuration
│   ├── App.tsx          # Main App component
│   └── main.tsx         # Entry point for rendering React
├── public/
│   ├── index.html       # HTML template
│   ├── site.webmanifest # PWA manifest (optional)
│   └── icons/           # App icons/favicons
├── .eslintrc.js         # ESLint configuration
├── .prettierrc          # Prettier configuration
├── tailwind.config.js   # Tailwind CSS config
├── tsconfig.json        # TypeScript configuration
├── vite.config.ts       # Vite configuration
└── package.json         # Dependencies and npm scripts
```

> **Note**: For larger teams, you may wish to separate feature modules or define an architecture that structures pages and components in domain-specific directories.

---

## 9. Contributing

We gladly accept contributions to improve this frontend:

1. **Fork** the repository on GitHub.  
2. **Create a new branch** (e.g., `git checkout -b feature/some-new-feature`).  
3. **Commit** your changes with a descriptive message.  
4. **Push** to your fork (`git push origin feature/some-new-feature`).  
5. **Open a Pull Request** – include details about improvements or bug fixes, possibly with screenshots or logs.

---

## 10. License

This project is licensed under the **MIT License**, granting you permission to copy, modify, and distribute the application. See the `LICENSE` file for exact terms.

---

## 11. Additional Tips

- **React Query** Usage:  
  Create a central `QueryClient` in `main.tsx` and wrap the app with `<QueryClientProvider>`. Then define `useQuery` hooks for fetching data from the API. This simplifies caching, refetching, and error handling.

- **Testing & QA**:  
  Implement unit/integration tests using **Jest** or **Vitest**. For end-to-end tests, consider **Cypress**.

- **Type Safety**:  
  Maintain TypeScript types for all components, props, and API responses. This fosters reliable code and reduces runtime bugs.

- **Deployment**:  
  Vite’s production build can be served by static hosting solutions (Netlify, Vercel, GitHub Pages) or integrated into a Docker container for a multi-service setup with the Flask backend.
