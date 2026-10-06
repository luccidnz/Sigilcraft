import type { Config } from 'tailwindcss';

export default {
  content: ['./index.html', './src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        navy: {
          50: '#f3f4f6',
          100: '#e5e7eb',
          200: '#d1d5db',
          400: '#9ca3af',
          600: '#4b5563',
          700: '#1f2937',
          800: '#111827',
          900: '#0b1220',
          950: '#050914'
        },
        chapter: '#0b1220',
        violet: {
          50: '#f5f3ff',
          100: '#ede9fe',
          200: '#ddd6fe',
          300: '#c4b5fd',
          400: '#a78bfa',
          500: '#8b5cf6',
          600: '#7c3aed',
          700: '#6d28d9',
          800: '#5b21b6',
          900: '#4c1d95',
          950: '#2e1065'
        },
        gold: {
          50: '#fffbeb',
          100: '#fef3c7',
          200: '#fde68a',
          300: '#fcd34d',
          400: '#fbbf24',
          500: '#f59e0b',
          600: '#d97706',
          700: '#b45309',
          800: '#92400e',
          900: '#78350f'
        }
      },
      fontFamily: {
        display: ['"Cinzel"', 'serif'],
        mono: ['"Orbitron"', 'ui-monospace', 'monospace']
      },
      backgroundImage: {
        'cosmos': 'linear-gradient(135deg, #0b1220 0%, #111827 45%, #1f2937 100%)'
      },
      boxShadow: {
        'sigil': '0 20px 50px -12px rgba(0,0,0,0.8), 0 0 0 1px rgba(139,92,246,0.35)'
      }
    }
  },
  plugins: []
} satisfies Config;
