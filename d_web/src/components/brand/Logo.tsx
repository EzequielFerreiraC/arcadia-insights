import Image from 'next/image'

export function Logo({ className = 'h-6 w-6' }: { className?: string }) {
  return (
    <svg
      className={className}
      viewBox="0 0 32 32"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      aria-hidden="true"
    >
      {/* Body */}
      <path
        d="M16 6.5C16 6.5 15.4 9 15.4 15.5C15.4 22 16 25.5 16 25.5C16 25.5 16.6 22 16.6 15.5C16.6 9 16 6.5 16 6.5Z"
        fill="url(#bfly-body)"
      />
      {/* Left upper wing */}
      <path
        d="M15.2 14C15.2 14 11 6.5 6.5 6C3.2 5.6 2 8.5 3 11.5C4.2 15 9 16.5 15.2 15.2V14Z"
        fill="url(#bfly-wing)"
      />
      {/* Left lower wing */}
      <path
        d="M15.2 16.4C15.2 16.4 11.5 22.5 8 23.5C5.4 24.2 4 22.2 4.6 19.8C5.4 16.8 10.5 15.6 15.2 16.2V16.4Z"
        fill="url(#bfly-wing2)"
      />
      {/* Right upper wing */}
      <path
        d="M16.8 14C16.8 14 21 6.5 25.5 6C28.8 5.6 30 8.5 29 11.5C27.8 15 23 16.5 16.8 15.2V14Z"
        fill="url(#bfly-wing)"
      />
      {/* Right lower wing */}
      <path
        d="M16.8 16.4C16.8 16.4 20.5 22.5 24 23.5C26.6 24.2 28 22.2 27.4 19.8C26.6 16.8 21.5 15.6 16.8 16.2V16.4Z"
        fill="url(#bfly-wing2)"
      />
      <defs>
        <linearGradient id="bfly-wing" x1="3" y1="6" x2="16" y2="16" gradientUnits="userSpaceOnUse">
          <stop stopColor="#7fe0d9" />
          <stop offset="1" stopColor="#4ECDC4" />
        </linearGradient>
        <linearGradient id="bfly-wing2" x1="4" y1="24" x2="16" y2="16" gradientUnits="userSpaceOnUse">
          <stop stopColor="#4a8bab" />
          <stop offset="1" stopColor="#6db3d4" />
        </linearGradient>
        <linearGradient id="bfly-body" x1="16" y1="6" x2="16" y2="26" gradientUnits="userSpaceOnUse">
          <stop stopColor="#f6c67e" />
          <stop offset="1" stopColor="#f0a94e" />
        </linearGradient>
      </defs>
    </svg>
  )
}

/** Standalone decorative butterfly — the blue morpho from the series. */
export function Butterfly({ className = 'h-10 w-10' }: { className?: string }) {
  return (
    <Image
      src="/images/butterfly-icon.png"
      alt=""
      aria-hidden="true"
      width={512}
      height={512}
      priority={false}
      className={`object-contain ${className}`}
    />
  )
}
