import path from "path"
import react from "@vitejs/plugin-react"
import { defineConfig } from "vite"

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  server: {
    proxy: {
      "/api": {
        target: "http://localhost:5000",
        changeOrigin: true,
        secure: false, // Eğer HTTPS kullanmıyorsan, bağlantıyı zorlamaması için
        rewrite: (path) => path.replace(/^\/api/, ""), // API çağrılarını backend’e yönlendir
      },
    },
  },
  build: {
    outDir: "dist",
    sourcemap: true, // Daha iyi hata ayıklama için
  },
  define: {
    __APP_VERSION__: JSON.stringify("1.0.0"),
  },
})
