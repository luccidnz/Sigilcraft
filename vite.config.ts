import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0',
    hmr: false,
    allowedHosts: ['localhost', '127.0.0.1', '5173-i3yimsxed48x2c1vuuwxp.e2b.app'],
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:5000',
        changeOrigin: true,
        ws: false,
        on: {
          proxyReq: (proxyReq, req, res) => {
            console.log('proxying /api', req.url)
          }
        }
      }
    }
  },
  build: {
    outDir: 'dist',
    rollupOptions: {
      input: {
        main: 'index.html'
      }
    }
  }
});
