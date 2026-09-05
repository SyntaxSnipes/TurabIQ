function Logo({ size = 40 }) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 100 100"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      role="img"
      aria-label="TurabIQ"
    >
      <rect x="6" y="20" width="88" height="12" fill="var(--sand)" />
      <rect x="14" y="38" width="72" height="12" fill="var(--clay)" />
      <rect x="22" y="56" width="56" height="12" fill="var(--dark-clay)" />
      <polyline
        points="0,26 24,26 30,10 38,42 46,26 100,26"
        stroke="var(--accent)"
        strokeWidth="4.2"
        fill="none"
        strokeLinejoin="round"
        strokeLinecap="round"
      />
      <rect x="30" y="74" width="40" height="8" fill="var(--sand)" />
    </svg>
  )
}

export default Logo
