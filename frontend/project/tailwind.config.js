/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#f0f7ff',
          100: '#e6f3ff',
          200: '#bae0ff',
          300: '#8eccff',
          400: '#62b8ff',
          500: '#36a4ff',
          600: '#2b83cc',
          700: '#206299',
          800: '#164266',
          900: '#0b2133'
        },
        pastel: {
          pink: '#ffd6e0',
          blue: '#c5e1ff',
          green: '#c9f4d9',
          yellow: '#fff3c5',
          purple: '#e7d6ff',
          orange: '#ffe0cc'
        }
      }
    },
  },
  plugins: [],
};