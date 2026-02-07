/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./src/**/*.{js,ts,jsx,tsx,mdx}'],
  theme: {
    extend: {
      colors: {
        bg: {
          DEFAULT: '#0a0e12',
          subtle: '#0e131a',
          elevated: '#141b23',
          overlay: '#1c2530',
        },
        line: {
          DEFAULT: 'rgba(255,255,255,0.08)',
          strong: 'rgba(255,255,255,0.14)',
        },
        content: {
          primary: 'rgba(247,244,238,0.95)',
          secondary: 'rgba(247,244,238,0.62)',
          tertiary: 'rgba(247,244,238,0.42)',
          faint: 'rgba(247,244,238,0.30)',
        },
        // Butterfly teal — the signature blue morpho
        teal: {
          DEFAULT: '#4ECDC4',
          soft: '#7fe0d9',
          dim: '#2a9d94',
        },
        // Golden-hour light over Arcadia Bay
        amber: {
          DEFAULT: '#f0a94e',
          soft: '#f6c67e',
          dim: '#c47f2e',
        },
        // Pacific sunset
        sunset: {
          DEFAULT: '#e07a5f',
          soft: '#ec9d86',
          dim: '#b85940',
        },
        // Coastal sky
        sky: {
          DEFAULT: '#6db3d4',
          soft: '#98cce3',
          dim: '#4a8bab',
        },
        violet: {
          DEFAULT: '#8b5cf6',
          soft: '#a78bfa',
          dim: '#6d28d9',
        },
      },
      fontFamily: {
        sans: [
          'Inter',
          'system-ui',
          '-apple-system',
          'BlinkMacSystemFont',
          'Segoe UI',
          'Roboto',
          'sans-serif',
        ],
        display: ['Fraunces', 'Georgia', 'Cambria', 'Times New Roman', 'serif'],
      },
      fontSize: {
        '2xs': ['0.6875rem', { lineHeight: '1rem', letterSpacing: '0.02em' }],
      },
      letterSpacing: {
        tightest: '-0.045em',
      },
      maxWidth: {
        content: '1180px',
      },
      borderRadius: {
        xl: '0.875rem',
        '2xl': '1.25rem',
      },
      boxShadow: {
        glow: '0 0 60px -12px rgba(240,169,78,0.28)',
        'glow-teal': '0 0 70px -18px rgba(78,205,196,0.32)',
        'glow-sunset': '0 0 80px -20px rgba(224,122,95,0.30)',
        polaroid: '0 18px 40px -12px rgba(0,0,0,0.55), 0 4px 10px -4px rgba(0,0,0,0.4)',
      },
      animation: {
        aurora: 'aurora 18s ease-in-out infinite',
        shimmer: 'shimmer 2s linear infinite',
        float: 'float 7s ease-in-out infinite',
        'float-slow': 'float 11s ease-in-out infinite',
        flutter: 'flutter 4.5s ease-in-out infinite',
        'fade-up': 'fadeUp 0.7s cubic-bezier(0.22,1,0.36,1) both',
      },
      keyframes: {
        aurora: {
          '0%, 100%': { transform: 'translate(0,0) scale(1)', opacity: '0.5' },
          '33%': { transform: 'translate(4%,-6%) scale(1.1)', opacity: '0.7' },
          '66%': { transform: 'translate(-4%,4%) scale(0.95)', opacity: '0.4' },
        },
        shimmer: {
          '0%': { backgroundPosition: '-200% 0' },
          '100%': { backgroundPosition: '200% 0' },
        },
        float: {
          '0%, 100%': { transform: 'translateY(0) rotate(-1deg)' },
          '50%': { transform: 'translateY(-14px) rotate(1.5deg)' },
        },
        flutter: {
          '0%, 100%': { transform: 'translateY(0) translateX(0) rotate(0deg)' },
          '25%': { transform: 'translateY(-10px) translateX(6px) rotate(4deg)' },
          '50%': { transform: 'translateY(-4px) translateX(-4px) rotate(-3deg)' },
          '75%': { transform: 'translateY(-12px) translateX(4px) rotate(3deg)' },
        },
        fadeUp: {
          '0%': { opacity: '0', transform: 'translateY(16px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
      },
    },
  },
  plugins: [],
}
