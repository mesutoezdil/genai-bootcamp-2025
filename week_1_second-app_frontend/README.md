# 🏠 Chinese Learning App - Frontend 🏠

This is the frontend for the **Chinese Learning App**, built with **React, TypeScript, and Vite**. It provides a fast, interactive, and modern interface for language learners.

## 🚀 **Tech Stack**
- **React 18** + **Vite**
- **TypeScript**
- **ESLint & Prettier**
- **React Router**
- **React Query** for API calls
- **Tailwind CSS** for styling

## 🛠 **Project Setup**
To get started, clone the repository and install dependencies:

```sh
git clone https://github.com/your-repo/chinese-learning-app.git
cd chinese-learning-app-frontend
npm install
```

## 🔥 **Run the Development Server**
Start the local development server:

```sh
npm run dev
```

The app will be available at **`http://localhost:5173`**.

## 🖥 **Production Build**
To generate a production build:

```sh
npm run build
```

This will create an optimized `dist/` folder.

## ⚙ **ESLint & Code Quality**
This project uses ESLint and Prettier for **code consistency**. To enable **type-aware linting**, update the ESLint configuration as follows:

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

Replace:

- `tseslint.configs.recommended` → `tseslint.configs.recommendedTypeChecked`
- Optionally add `...tseslint.configs.stylisticTypeChecked`

### 🔹 **React ESLint Plugin**
Install and configure **eslint-plugin-react**:

```sh
npm install eslint-plugin-react --save-dev
```

Then, update `eslint.config.js`:

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

## 🌈 **Styling**
We use **Tailwind CSS** for fast and responsive UI development.

To start with Tailwind, install it:

```sh
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

Then, add the following to your `tailwind.config.js`:

```js
module.exports = {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

## 🌍 **API Integration**
The frontend communicates with the **Flask backend** at `http://localhost:5000/api/`.

To change the API base URL, update `vite.config.ts`:

```typescript
server: {
  proxy: {
    "/api": {
      target: "http://localhost:5000",
      changeOrigin: true,
      rewrite: (path) => path.replace(/^\/api/, ""),
    },
  },
},
```

## 💁 **Project Structure**
```
chinese-learning-app-frontend/
├── src/
│   ├── assets/          # Static assets (images, icons, fonts)
│   ├── components/      # Reusable UI components
│   ├── pages/           # Page components (Home, Lessons, etc.)
│   ├── hooks/           # Custom hooks (API calls, utilities)
│   ├── styles/          # Tailwind global styles
│   ├── api/             # API functions (fetch words, exercises)
│   ├── routes.tsx       # React Router setup
│   ├── App.tsx          # Main App component
│   └── main.tsx         # Entry point
├── public/
│   ├── index.html       # HTML template
│   ├── site.webmanifest # PWA manifest
│   └── icons/           # App icons
├── .eslintrc.js         # ESLint configuration
├── .prettierrc          # Prettier configuration
├── tailwind.config.js   # Tailwind CSS configuration
├── tsconfig.json        # TypeScript configuration
├── vite.config.ts       # Vite configuration
└── package.json         # Dependencies and scripts
```

## 🌟 **Contributing**
If you'd like to contribute:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature-name`)
3. Commit your changes (`git commit -m "Added new feature"`)
4. Push to the branch (`git push origin feature-name`)
5. Open a Pull Request 🚀

## 🐝 **License**
This project is licensed under the MIT License.

---

🎯 **Happy Learning! 努力! 🚀**
