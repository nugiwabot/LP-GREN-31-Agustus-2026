/* =========================================================================
 * GREN Propertykost — Design Tokens (Tailwind Play CDN config)
 * Load AFTER <script src="https://cdn.tailwindcss.com"></script>
 * ========================================================================= */
window.tailwind = window.tailwind || {};
tailwind.config = {
  theme: {
    extend: {
      colors: {
        brand: {
          50: '#F2F6F2',
          100: '#E2EBE3',
          200: '#C5D6C8',
          300: '#9DB8A2',
          400: '#6E9276',
          500: '#4A7253',
          600: '#335A3D',
          700: '#27482F',
          800: '#1D3825',
          900: '#142A1B',
          950: '#0A1A10'
        },
        accent: {
          50: '#FBF7EF',
          100: '#F5ECD9',
          200: '#EAD8B2',
          300: '#DCBE83',
          400: '#CBA45C',
          500: '#B68F43',
          600: '#977433',
          700: '#795B2A',
          800: '#5E4622',
          900: '#4A371C'
        },
        slate: {
          50: '#FAF9F6',
          100: '#F3F1EC',
          200: '#E7E4DD',
          300: '#D4D0C6',
          400: '#A9A69C',
          500: '#827F76',
          600: '#646258',
          700: '#4B4A43',
          800: '#2E2E29',
          850: '#23241F',
          900: '#191A16',
          950: '#0E0F0C'
        }
      },
      fontFamily: {
        sans: ['Manrope', 'ui-sans-serif', 'system-ui', 'sans-serif'],
        serif: ['Fraunces', 'Georgia', 'serif'],
        display: ['Fraunces', 'Georgia', 'serif']
      }
    }
  }
};
