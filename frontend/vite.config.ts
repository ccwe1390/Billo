import path from 'node:path'
import tailwindcss from '@tailwindcss/vite'
import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'

// The FastAPI backend (repo root: `py -m uvicorn app.main:app --port 8000`). In dev, the browser only talks to
// Vite; these paths are forwarded so the app calls `/evaluate` with no hostname, exactly as it will when FastAPI
// serves the built files on the OCI VM.
const BACKEND = 'http://127.0.0.1:8000'
const API_PATHS = ['/extract', '/evaluate', '/explain', '/packet', '/policy-cumberland.html']

// https://vite.dev/config/
export default defineConfig({
  plugins: [react(), tailwindcss()],
  resolve: {
    alias: { '@': path.resolve(import.meta.dirname, './src') },
  },
  server: {
    proxy: Object.fromEntries(API_PATHS.map((p) => [p, BACKEND])),
  },
})
