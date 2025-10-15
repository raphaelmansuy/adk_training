import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      // Proxy API requests to backend
      // Forwards /api/copilotkit to http://localhost:8000/api/copilotkit
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        // Don't rewrite the path - keep /api prefix
        configure: (proxy) => {
          // Log proxy requests for debugging
          proxy.on('proxyReq', (proxyReq, req) => {
            console.log(`[Vite Proxy] ${req.method} ${req.url} → ${proxyReq.path}`)
          })
          proxy.on('error', (err, req, res) => {
            console.error('[Vite Proxy Error]', err)
          })
        },
      },
    },
  },
})
