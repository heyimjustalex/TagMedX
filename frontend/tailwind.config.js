import {nextui} from '@nextui-org/react';

/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/**/*.{js,ts,jsx,tsx,mdx}',
    './node_modules/@nextui-org/theme/dist/**/*.{js,ts,jsx,tsx}'
  ],
  theme: {
    extend: {
      width: {
        '2-el': 'calc((100% - 1rem) / 2)',
        '3-el': 'calc((100% - 2rem) / 3)',
        '4-el': 'calc((100% - 3rem) / 4)',
        '5-el': 'calc((100% - 4rem) / 5)'
      }
    },
  },
  darkMode: 'class',
  plugins: [nextui()],
}
