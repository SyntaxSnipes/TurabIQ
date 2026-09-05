# TurabIQ Branding Guidelines

## Logo Concept
**"Stratified Intelligence"** — An abstract mark combining three angled soil strata (representing layered earth/soil monitoring) with an ascending sensor signal waveform (representing data collection and predictive intelligence). This visual metaphor merges the physical domain (soil/aggregate) with the digital domain (IoT sensors, analytics).

---

## Color Palette

### Primary Colors
- **Warm Sand/Clay** — `#D4A574` (hex) — Represents soil, earth, materiality. Warm, inviting, grounded.
- **Deep Teal** — `#1B7B7F` (hex) — Represents technology, precision, data streams. Confident, professional, modern.

### Secondary Colors
- **Clay (Medium)** — `#C29A6B` (hex) — Layered earth tones, natural variation.
- **Clay (Dark)** — `#A0826D` (hex) — Depth, foundation, stability.
- **Off-White** — `#FAFAF8` (hex) — Clean background, high contrast.
- **Charcoal** — `#2C2C2C` (hex) — Text, strong contrast on light backgrounds.

### Accent Neutrals
- **Warm Gray** — `#E8DCC8` (hex) — Subtle dividers, borders, light accents.

**Rationale:** Warm earthy palette evokes UAE desert, aggregate/sand industry. Deep teal adds tech credibility without being cold. Total 3 core colors (sand, clay, teal) maintains minimalism.

---

## Logo Versions & Usage

### 1. **Logo Mark** (`turabiq-logo-mark.svg`)
- **Purpose:** Standalone icon for app, favicon, social avatars, stickers
- **Min Size:** 64×64px (favicon), 256×256px recommended
- **Background:** Works on any light or dark background with sufficient contrast
- **Files Available:** SVG (scalable), ready to export as PNG/PDF

### 2. **Logo Horizontal** (`turabiq-logo-horizontal.svg`)
- **Purpose:** Pitch decks, website headers, email signatures, business cards
- **Aspect Ratio:** ~3.2:1 (fits horizontal layouts)
- **Use Case:** Primary logo for marketing materials
- **Spacing:** Divider line separates mark from wordmark; maintain 1.5× letterheight as minimum clear space

### 3. **Logo Stacked** (`turabiq-logo-stacked.svg`)
- **Purpose:** Vertical layouts, app icon containers, social media covers
- **Aspect Ratio:** ~1:1.3 (square-friendly)
- **Use Case:** Secondary logo for space-constrained contexts

### 4. **Favicon** (`turabiq-favicon.svg`)
- **Purpose:** Browser tabs, iOS/Android app icon, social media profile picture
- **Sizes:** 16×16, 32×32, 64×64, 256×256px
- **Format:** Simplified mark-only (wordmark removed for legibility at tiny sizes)

---

## Typography

### English Wordmark
- **Font Family:** Space Grotesk (Google Fonts) or similar geometric sans-serif (Poppins, Inter, Sora)
- **Weight:** 600–700 (bold, confident)
- **Letter Spacing:** Tight (-0.5px to -0.3px) for geometric feel
- **Case:** Title case "TurabIQ" (no all-caps unless tagline)
- **Note:** Already embedded in SVG files; exports to PDF/print will need system font fallback

### Arabic Subtext
- **Text:** تراب (turab = soil)
- **Font Family:** Segoe UI, Arabic Typesetting, or modern Arabic geometric typeface
- **Weight:** 500 (medium, complements English)
- **Purpose:** Bilingual credibility, local market relevance (UAE context)
- **Placement:** Directly below or beside English wordmark, 40–50% relative size

---

## Clear Space & Sizing

### Minimum Clear Space
- **Desktop/Print:** 1.5× the height of the "T" in "TurabIQ"
- **Mobile/Web:** 8–12px padding on all sides
- Maintain space between logo and any other graphics, text, or borders

### Recommended Minimum Sizes
| Context | Min Width | Notes |
|---------|-----------|-------|
| Browser Tab | 32px | Mark only |
| App Icon | 64px | Mark only, rounded corner container (iOS) or square (Android) |
| Email Signature | 160px | Horizontal layout |
| Pitch Deck Slide | 280px | Horizontal or stacked, depending on layout |
| Business Card | 40mm | Horizontal, typically top-left or center |
| Website Header | 200–300px | Horizontal; adjust for responsive breakpoints |

---

## Color Variants

### Full Color (Primary)
- Mark: Layered warm earth tones + deep teal signal line
- Wordmark: Charcoal (#2C2C2C)
- Use on light backgrounds (off-white, light gray, light cream)

### Monochrome (For Constraints)
- **On Light:** All elements in Charcoal (#2C2C2C)
- **On Dark:** All elements in Off-White (#FAFAF8)
- **Linework Only:** Mark outlines only, no fills (useful for embroidery, etching)

### Single-Color Accent (Social Media)
- Deep Teal (#1B7B7F) with white/off-white for visibility on photo backgrounds
- Useful for Instagram stories, LinkedIn, Twitter profile pictures

---

## What NOT to Do

❌ Do NOT rotate, skew, or distort the mark  
❌ Do NOT add drop shadows, glows, or 3D effects  
❌ Do NOT change color to gradients or change the earth-tone palette  
❌ Do NOT remove or separate the stratified layers — they define the concept  
❌ Do NOT use at sizes below 64×64px without the simplified favicon version  
❌ Do NOT place on backgrounds with insufficient contrast (e.g., tan mark on tan background)  
❌ Do NOT add additional decorative elements (leaves, circuit boards, clouds, etc.)  

---

## Export Instructions

### For Web (CSS/Branding Sites)
```html
<link rel="icon" href="turabiq-favicon.svg" type="image/svg+xml">
<img src="turabiq-logo-horizontal.svg" alt="TurabIQ" width="300">
```

### For Print (High Resolution)
1. Open SVG in Adobe Illustrator / Figma
2. Export as **PDF** (vectors, preserves scalability) or **PNG** @ 300 DPI
3. Recommended canvas: 3000×2000px for print-quality PNG

### For iOS App
1. Export favicon SVG as **1024×1024 PNG**
2. Upload to App Store Connect (will auto-generate icon sizes: 120, 180, 1024px)
3. Use rounded corner mask (App Store requires 1:1 ratio with corner radius ~20%)

### For Android App
1. Export favicon SVG as square **512×512 PNG** (adaptive icon friendly)
2. Place in `res/mipmap-xxxhdpi/ic_launcher.png` folders
3. Android will auto-scale to 48, 72, 96, 144, 192, 512px variants

---

## Implementation Examples

### React (Favicon)
```jsx
// public/index.html
<link rel="icon" type="image/svg+xml" href="/turabiq-favicon.svg">

// src/App.jsx
import logo from '/turabiq-logo-horizontal.svg';
export default function App() {
  return <img src={logo} alt="TurabIQ" className="header-logo" />;
}
```

### CSS (Brand Colors)
```css
:root {
  --turabiq-sand: #D4A574;
  --turabiq-clay: #C29A6B;
  --turabiq-teal: #1B7B7F;
  --turabiq-text: #2C2C2C;
  --turabiq-bg: #FAFAF8;
}
```

---

## Design Rationale

**Visual Metaphor:**
- **Stratified layers** = layered soil profiles (geology/agriculture context) + hierarchical data analysis (tech context)
- **Ascending signal line** = sensor data flowing upward from soil to cloud platform
- **Warm earth + cool tech teal** = bridging physical and digital domains

**Style:**
- Flat, geometric = modern, scalable, printable at any size
- No gradients/shadows = clean, professional, premium
- Restrained color palette (3 colors) = confident, not over-designed
- Minimal line weights = works at favicon size and billboard size

**Market Position:**
- Avoids generic IoT/AI clichés (no circuit boards, network nodes, or glowing effects)
- Avoids agricultural clichés (no literal plants, leaves, or seedlings)
- Positions as precision engineering + hardware credibility (UAE startup aesthetic)
- Bilingual (English + Arabic) appeals to regional market without tokenism

---

## File Manifest

| File | Purpose | Dimensions | Format |
|------|---------|-----------|--------|
| `turabiq-logo-mark.svg` | Standalone icon | 120×120px | SVG (scalable) |
| `turabiq-logo-horizontal.svg` | Primary wordmark | 320×100px | SVG (scalable) |
| `turabiq-logo-stacked.svg` | Vertical wordmark | 140×160px | SVG (scalable) |
| `turabiq-favicon.svg` | App icon / favicon | 64×64px | SVG (scalable) |

All files are vector-based and can be scaled infinitely without quality loss. Export to PNG/PDF as needed for specific deliverables.

---

**Created for:** TurabIQ — Soil Intelligence Platform  
**Style:** Minimal, Geometric, Modern Industrial  
**Status:** Ready for implementation  
**Last Updated:** 2026-09-05
