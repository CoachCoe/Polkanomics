/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'polkadot': {
          pink: '#E6007A',
          'pink-dark': '#C4006A',
        }
      }
    },
  },
  plugins: [],
  safelist: [
    'bg-polkadot-pink',
    'bg-polkadot-pink-dark',
    'text-polkadot-pink',
    'ring-polkadot-pink',
    'hover:bg-polkadot-pink-dark',
    'focus:ring-polkadot-pink'
  ],
  variants: {
    extend: {
      opacity: ['disabled'],
      cursor: ['disabled']
    }
  }
} 