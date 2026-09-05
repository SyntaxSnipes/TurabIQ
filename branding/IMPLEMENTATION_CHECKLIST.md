# TurabIQ Logo Implementation Checklist

Quick reference for adding TurabIQ branding across all platforms and materials.

---

## 🌐 Web Implementation

### Frontend (React/Vite)
- [ ] **Favicon** — Added to `public/turabiq-favicon.svg` ✓
- [ ] **index.html** — Updated with favicon link + meta tags ✓
- [ ] **Dashboard Header** — Add horizontal logo to navigation bar
  ```jsx
  <img src="/turabiq-logo-horizontal.svg" alt="TurabIQ" className="logo" />
  ```
- [ ] **CSS Variables** — Add TurabIQ color palette (see COLOR_PALETTE.md)
  ```css
  :root {
    --turabiq-sand: #D4A574;
    --turabiq-teal: #1B7B7F;
    --turabiq-text: #2C2C2C;
    --turabiq-bg: #FAFAF8;
  }
  ```
- [ ] **Browser Tab** — Verify favicon displays (Ctrl+F5 to refresh cache)

### Website / Landing Page
- [ ] **Hero Section** — Feature horizontal logo + tagline "Soil Intelligence"
- [ ] **Footer** — Stacked logo with copyright notice
- [ ] **Social Meta** — Use favicon for Open Graph image tag
  ```html
  <meta property="og:image" content="https://turabiq.io/turabiq-favicon.svg" />
  ```

---

## 📱 Mobile & App Implementation

### iOS App
- [ ] **App Icon** — Export `turabiq-favicon.svg` as 1024×1024 PNG
- [ ] **Upload to App Store Connect** — Icon will auto-scale to:
  - 120px (iPhone Spotlight, Settings)
  - 180px (iPhone App Library)
  - 1024px (App Store display)
- [ ] **Rounded Corners** — iOS requires corner radius ~20% of icon size
- [ ] **Safe Zone** — Keep mark within inner 75% of canvas

### Android App
- [ ] **Launcher Icon** — Export as 512×512 PNG (adaptive icon format)
- [ ] **Place in directories:**
  ```
  res/mipmap-mdpi/ic_launcher.png (48×48)
  res/mipmap-hdpi/ic_launcher.png (72×72)
  res/mipmap-xhdpi/ic_launcher.png (96×96)
  res/mipmap-xxhdpi/ic_launcher.png (144×144)
  res/mipmap-xxxhdpi/ic_launcher.png (192×192)
  ```
- [ ] **Adaptive Icon Background** — Deep teal (#1B7B7F) or off-white (#FAFAF8)
- [ ] **Test on multiple devices** — Verify appearance across screen sizes

### Progressive Web App (PWA)
- [ ] **manifest.json** — Add icon declarations
  ```json
  "icons": [
    {"src": "turabiq-favicon-192.png", "sizes": "192×192", "type": "image/png"},
    {"src": "turabiq-favicon-512.png", "sizes": "512×512", "type": "image/png"}
  ],
  "theme_color": "#1B7B7F",
  "background_color": "#FAFAF8"
  ```
- [ ] **Export favicon as PNG** — Generate 192×192 and 512×512 variants

---

## 📄 Print & Documents

### Business Cards
- [ ] **Placement** — Top-left corner or centered, 40mm width
- [ ] **Stock** — Matte finish recommended (reduces gloss, looks premium)
- [ ] **Format** — Use horizontal logo version
- [ ] **Bleeds** — 3mm safety margin from card edge
- [ ] **Color Mode** — Export as CMYK (not RGB)
  ```
  Sand: CMYK (0, 22, 45, 17)
  Teal: CMYK (79, 3, 0, 50)
  ```

### Pitch Deck / Presentations
- [ ] **Title Slide** — Horizontal logo centered, 280–400px width
- [ ] **Logo Variations:**
  - Light background → Full color (sand + teal)
  - Photo background → White or teal mark only
  - Busy background → Stacked version (less visual weight)
- [ ] **Brand Slide** — Showcase all logo versions + color palette
- [ ] **Footer** — Small horizontal logo (100px) on every slide

### Stationery / Letterhead
- [ ] **Letterhead** — Horizontal logo, top-left or center (50–80mm)
- [ ] **Envelope** — Small logo, top-left corner
- [ ] **PDF Export** — Use 300 DPI, CMYK color mode
- [ ] **Consistent Placement** — Maintain 1.5× letter-height clear space

### Brochures / Marketing Materials
- [ ] **Cover** — Feature logo prominently (200–300px)
- [ ] **Interior Pages** — Smaller instances (80–120px) for credibility
- [ ] **Color Consistency** — Use TurabIQ brand colors throughout
- [ ] **Typography** — Pair with Space Grotesk or similar geometric sans-serif

---

## 🎨 Social Media & Digital Assets

### Social Media Profiles
- [ ] **Profile Picture** — Favicon (512×512 PNG)
- [ ] **Cover Image** — Horizontal logo + tagline (1200×630px recommended)
  - LinkedIn: 1200×627px
  - Twitter/X: 1500×500px
  - Facebook: 1200×628px
  - Instagram: 1080×1350px
- [ ] **Consistency** — Use same branding across all platforms

### Blog / Content Headers
- [ ] **Featured Image** — Logo + topic text (1200×630px)
- [ ] **Favicon** — Appears in browser tab auto-magically ✓
- [ ] **Byline Image** — Small logo + company name (100×100px)

### Email Template
- [ ] **Header Logo** — Horizontal version, 200–250px width
- [ ] **Footer Logo** — Stacked version, 100–120px width
- [ ] **Signature** — Favicon + "TurabIQ" text, right-aligned (inline)
  ```html
  <img src="https://turabiq.io/favicon.svg" width="24" alt=""> TurabIQ
  ```

### Advertisements
- [ ] **Display Ads** — Logo should occupy <15% of ad space (avoid clutter)
- [ ] **Video Intro/Outro** — 2–3 second fade-in of logo mark (1–2 sec hold)
- [ ] **Color Variants** — Test full-color and monochrome on different backgrounds

---

## 📦 Marketing Collateral

### Merchandise / Apparel
- [ ] **T-shirts / Hoodies** — Mark-only (80–120mm), centered
- [ ] **Caps / Hats** — Small mark (40–60mm), embroidered or printed
- [ ] **Stickers / Decals** — Mark-only, 50–100mm diameter
- [ ] **Format for Vendor** — Provide PNG (transparent background) + color specifications

### Packaging / Product Labels
- [ ] **Logo Size** — Proportional to package size (80–150mm for boxes)
- [ ] **Material Considerations:**
  - Embroidery → Use mark-only, high-contrast colors
  - Screen Printing → Solid colors, avoid thin lines (<1.5pt)
  - Digital Printing → Full color acceptable, maintain color palette
- [ ] **QR Code** — If adding QR to packaging, maintain 10mm+ clear space from logo

### Vehicle Wraps / Signage
- [ ] **Scale** — Logo should be visible from 20m+ distance
- [ ] **Placement** — Horizontal logo on vehicle sides (500–800mm width)
- [ ] **Contrast** — Ensure 7:1 contrast ratio with vehicle color
- [ ] **Large Format Export** — Provide as high-res PDF (300 DPI minimum)

---

## 🔐 Brand Asset Management

### File Organization
```
/branding/
├── turabiq-logo-mark.svg          ← Icon only
├── turabiq-logo-horizontal.svg    ← Primary wordmark
├── turabiq-logo-stacked.svg       ← Vertical layout
├── turabiq-favicon.svg            ← App icon
├── BRAND_GUIDELINES.md            ← This document
├── COLOR_PALETTE.md               ← Color reference
└── PNG_EXPORTS/                   ← Raster versions
    ├── logo-mark-256px.png
    ├── logo-horizontal-1024px.png
    ├── favicon-192px.png
    └── favicon-512px.png
```

### Export Formats (When Needed)
- **Web:** SVG (preferred), PNG 1–2× screen density
- **Print:** PDF (vectors) or PNG @ 300 DPI
- **Social:** PNG 1200×630px (og:image standard)
- **App:** SVG + PNG (192×192, 512×512 for manifest)

### Version Control
- All SVG files stored in `/branding/` folder
- PNG exports generated from SVG on-demand (no permanent storage needed)
- Keep master SVG files as single source of truth
- Color values locked to COLOR_PALETTE.md

---

## ✅ Quality Checklist

Before using logo in any medium:

- [ ] **Minimum Size** — Logo is at least 64×64px (favicon) or 100px (horizontal)
- [ ] **Clear Space** — 1.5× letter-height margin maintained on all sides
- [ ] **Contrast** — Background contrast ≥4.5:1 (WCAG AA minimum)
- [ ] **Color Accuracy** — Uses exact hex codes from COLOR_PALETTE.md
- [ ] **No Distortion** — Logo not rotated, skewed, or stretched
- [ ] **No Effects** — No drop shadows, glows, gradients, or outlines added
- [ ] **Font Matching** — Wordmark uses Space Grotesk or approved geometric sans-serif
- [ ] **Arabic Alignment** — "تراب" properly right-to-left rendered (if applicable)

---

## 🎯 Quick Links

| Purpose | File | Size | Format |
|---------|------|------|--------|
| Browser Tab | `turabiq-favicon.svg` | 64×64px | SVG |
| App Icon | `turabiq-favicon.svg` | 512×512px | PNG export |
| Pitch Deck | `turabiq-logo-horizontal.svg` | 300–400px | SVG/PDF |
| Business Card | `turabiq-logo-horizontal.svg` | 40mm | PDF |
| Social Media | `turabiq-favicon.svg` | 1200×630px | PNG |
| Website Header | `turabiq-logo-horizontal.svg` | 200–300px | SVG |
| Print (High-Res) | Any SVG file | Export to PDF @ 300 DPI | PDF |

---

**Last Updated:** 2026-09-05  
**Status:** Ready for Implementation  
**Questions?** See BRAND_GUIDELINES.md for detailed specifications
