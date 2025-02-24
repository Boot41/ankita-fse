/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        pastel: {
          blue: '#A8D8EA',
          pink: '#FFB6B9',
          mint: '#BDEDC1',
          yellow: '#FDFD96',
          purple: '#E7CEF2',
          gray: '#F0F0F0'
        }
      }
    },
  },
  plugins: [],
};