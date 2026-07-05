import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

const srcPath = new URL('./src', import.meta.url).pathname

export default defineConfig({
  plugins: [react()],

  resolve: {
    alias: {
      '@': srcPath,
    },
  },

  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },

  build: {
    outDir: 'dist',
    sourcemap: true,
  },
})