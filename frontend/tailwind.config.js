/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        "earth-blue": "#00B4FF",
        "earth-green": "#4ade80",
      }
    }
  },
  plugins: [],
}
