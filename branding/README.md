# TurabIQ Branding Assets

## Welcome to the TurabIQ Brand Kit 🎨

This folder contains all design assets and brand guidelines for TurabIQ — a predictive monitoring system for aggregate/sand batching plants in the UAE.

---

## What's Inside

### 🎨 Logo Files (Vector SVG — Infinitely Scalable)

#### 1. **Logo Mark** — `turabiq-logo-mark.svg`
```
Icon only (no text)
120×120px canvas
Perfect for: favicon, app icon, profile picture, sticker
Standalone geometric mark = stratified soil layers + signal waveform
```

#### 2. **Logo Horizontal** — `turabiq-logo-horizontal.svg`
```
Mark + "TurabIQ" wordmark + "تراب" (Arabic)
320×100px canvas
Perfect for: website header, pitch deck, email signature, business card
Primary logo format for most use cases
```

#### 3. **Logo Stacked** — `turabiq-logo-stacked.svg`
```
Mark stacked above "TurabIQ" wordmark
140×160px canvas
Perfect for: vertical layouts, app icon containers, social media covers
Compact format for space-constrained contexts
```

#### 4. **Favicon** — `turabiq-favicon.svg`
```
Simplified mark (icon only)
64×64px canvas
Perfect for: browser tab, app icon, social avatar, favicon.ico
Already deployed to frontend/public/ and linked in index.html
```

---

## 📚 Documentation Files

### `QUICK_REFERENCE.md` ⭐ **START HERE**
One-page cheat sheet with:
- Core color hex codes
- Logo sizing guide
- File manifest
- Quick checklist
- Copy-paste CSS/HTML code

**Use:** Print this out, share with team, keep in Slack

### `BRAND_GUIDELINES.md` — The Master Document
Comprehensive specifications including:
- Design concept & visual metaphor
- Color palette (RGB, HSL, CMYK, usage rules)
- Logo versions & clear-space requirements
- Typography (Space Grotesk + Arabic typeface)
- Accessibility standards (WCAG contrast ratios)
- What NOT to do (common mistakes)
- iOS/Android app icon specifications
- Print & merchandise guidelines

**Use:** Reference for designers, developers, marketing team

### `COLOR_PALETTE.md` — Color Reference
Detailed color specifications:
- 3 core brand colors (Sand, Teal, Clay)
- 4 neutral colors (Off-white, Charcoal, Gray)
- RGB, HSL, CMYK values for each
- Web usage (CSS variables)
- Alert states & accessibility guidance

**Use:** Design tool setup, CSS implementation, print production

### `IMPLEMENTATION_CHECKLIST.md` — Rollout Guide
Step-by-step checklist for deploying branding:
- ✅ Web implementation (React favicon, CSS variables)
- ✅ Mobile apps (iOS/Android icon guidelines)
- ✅ Print collateral (business cards, letterhead, brochures)
- ✅ Social media (profile pics, cover images, og:meta tags)
- ✅ Merchandise (apparel, stickers, packaging)
- ✅ Quality assurance checklist

**Use:** Project management, team assignments, deployment phases

### `DESIGN_OVERVIEW.md` — Concept Brief
Strategic document explaining:
- Design philosophy: "Stratified Intelligence"
- Core concept: Soil layers + sensor signal
- Design decisions & why (not generic circuit boards or plants)
- Comparison with alternatives (why our approach wins)
- Brand personality (technical, industrial, local, intelligent)
- Visual references & design principles

**Use:** Pitching brand to investors, onboarding new team members, internal communication

---

## 🎯 Quick Start

### For Web Developers
1. Logo files already integrated into frontend
2. Favicon displays in browser tab (linked in `index.html`)
3. Copy `COLOR_PALETTE.md` hex codes to CSS variables
4. See `QUICK_REFERENCE.md` for HTML/React code snippets

### For Designers
1. Open any `.svg` file in Figma, Adobe Illustrator, or Sketch
2. Export to PNG for specific sizes (see `BRAND_GUIDELINES.md`)
3. Use exact hex colors from `COLOR_PALETTE.md`
4. Maintain clear space (1.5× letter-height around logo)
5. Never add effects (no shadows, gradients, or 3D)

### For Marketing / Business
1. Start with `QUICK_REFERENCE.md` (one-page overview)
2. Use `IMPLEMENTATION_CHECKLIST.md` to plan rollout
3. Share `BRAND_GUIDELINES.md` with design vendors
4. Pitch using `DESIGN_OVERVIEW.md` for strategic positioning

### For Mobile App Developers
1. Export `turabiq-favicon.svg` as PNG (512×512 for iOS, 192×512 for Android)
2. Follow instructions in `BRAND_GUIDELINES.md` (iOS/Android sections)
3. Use `turabiq-favicon.svg` as adaptive icon source
4. See `IMPLEMENTATION_CHECKLIST.md` for manifest.json setup

---

## 🎨 Design Philosophy: "Stratified Intelligence"

### The Concept
Three angled soil strata (geological cross-section) intersected by an ascending sensor signal waveform (data flow). This visual metaphor merges:
- **Physical domain** = Soil/aggregate monitoring (real-world grounding)
- **Digital domain** = Predictive analytics (cloud intelligence)

### Why It Works
- ✅ **Specific** — Not a generic IoT logo, clearly about soil/earth
- ✅ **Minimal** — Flat, geometric, no effects (timeless, premium)
- ✅ **Scalable** — Works at 16px favicon and 800px billboard
- ✅ **Memorable** — Single, confident mark with clear metaphor
- ✅ **Authentic** — Warm earth palette + cool tech teal = honest positioning

### What We Avoided
- ❌ Generic "plant sprouting" (overused in AgriTech)
- ❌ Circuit board patterns (dated tech cliché)
- ❌ Network nodes / AI symbols (meaningless)
- ❌ Gradients/effects (makes small sizes illegible)
- ❌ Overly cute or "stock icon" feel (not premium)

---

## 🎨 Color Palette at a Glance

| Color | Hex | Purpose |
|-------|-----|---------|
| 🟠 **Warm Sand** | `#D4A574` | Earth tone, primary layer |
| 🔵 **Deep Teal** | `#1B7B7F` | Tech accent, signal line |
| 🟤 **Clay (Medium)** | `#C29A6B` | Secondary layer |
| 🟫 **Clay (Dark)** | `#A0826D` | Foundation, text |
| ⚪ **Off-White** | `#FAFAF8` | Background |
| ⬛ **Charcoal** | `#2C2C2C` | Primary text |

**Strategy:** Warm (soil context) + Cool (tech context) = visual tension representing physical + digital fusion.

---

## 📱 Cross-Platform Usage

### ✅ Deployed & Ready
- [x] Browser favicon (frontend/index.html)
- [x] Meta tags for social media
- [x] SVG files ready for export to any format
- [x] Color codes ready for CSS/design tools

### 🚀 Next Steps
- [ ] Export PNG variants for app stores (192×192, 512×512)
- [ ] Add color palette to CSS custom properties
- [ ] Create Figma design system (reusable components)
- [ ] Design business card template (40mm × 90mm)
- [ ] Create email signature template
- [ ] Design social media cover images (1200×630px templates)

---

## 📋 File Checklist

- [x] `turabiq-logo-mark.svg` — Icon only
- [x] `turabiq-logo-horizontal.svg` — Wordmark (primary)
- [x] `turabiq-logo-stacked.svg` — Vertical layout
- [x] `turabiq-favicon.svg` — App icon
- [x] `QUICK_REFERENCE.md` — One-page guide ⭐ START HERE
- [x] `BRAND_GUIDELINES.md` — Complete specs
- [x] `COLOR_PALETTE.md` — Color reference
- [x] `IMPLEMENTATION_CHECKLIST.md` — Rollout steps
- [x] `DESIGN_OVERVIEW.md` — Concept brief
- [x] `README.md` — This file

---

## 🔗 Quick Links

| Need | File | Description |
|------|------|-------------|
| **One-page overview** | `QUICK_REFERENCE.md` | Print-friendly cheat sheet |
| **Design specs** | `BRAND_GUIDELINES.md` | Complete design guide |
| **Color codes** | `COLOR_PALETTE.md` | RGB/HSL/CMYK values |
| **Deployment steps** | `IMPLEMENTATION_CHECKLIST.md` | Phase-by-phase rollout |
| **Brand story** | `DESIGN_OVERVIEW.md` | Concept + positioning |
| **Icon only** | `turabiq-logo-mark.svg` | Avatar, favicon, sticker |
| **Main logo** | `turabiq-logo-horizontal.svg` | Website, pitch deck |
| **App icon** | `turabiq-favicon.svg` | Mobile, browser tab |

---

## 💡 Pro Tips

1. **Always use SVG** — Infinitely scalable, editable, lightweight
2. **Maintain clear space** — 1.5× letter-height margin around logo
3. **Test contrast** — Ensure 4.5:1 contrast on backgrounds (WCAG AA)
4. **Don't rotate/skew** — Logo should never be distorted
5. **Export at 300 DPI** — For print materials (PDF recommended)
6. **Use exact hex codes** — Never approximate colors
7. **No effects** — Never add shadows, glows, gradients, or 3D
8. **Bilingual branding** — Keep English + Arabic text together (local market)

---

## ❓ FAQ

**Q: Can I change the colors?**  
A: No. Use exact hex values from COLOR_PALETTE.md. Consistency = brand recognition.

**Q: Can I simplify the logo for small sizes?**  
A: Yes, use `turabiq-favicon.svg` (simplified mark-only version) at sizes below 64×64px.

**Q: Which file for a website header?**  
A: `turabiq-logo-horizontal.svg` at 200–300px width.

**Q: How do I export to PNG?**  
A: Open SVG in Figma/Illustrator, export as PNG at desired size. For print, export as PDF @ 300 DPI.

**Q: Can I use this on a photo background?**  
A: Yes, but ensure contrast. Use monochrome (all teal or all white) if color mark doesn't contrast.

**Q: Is the logo bilingual?**  
A: Yes. English "TurabIQ" + Arabic "تراب" (turab = soil). Both should appear together.

**Q: What's the minimum size?**  
A: 64×64px (favicon version). At smaller sizes, readability suffers.

---

## 📞 Questions or Issues?

- **Design questions?** → See `BRAND_GUIDELINES.md`
- **Color codes?** → See `COLOR_PALETTE.md`
- **Implementation steps?** → See `IMPLEMENTATION_CHECKLIST.md`
- **Concept/strategy?** → See `DESIGN_OVERVIEW.md`
- **Quick help?** → See `QUICK_REFERENCE.md`

---

**TurabIQ Branding Kit v1.0**  
Created: 2026-09-05  
Status: Ready for Implementation  

*Stratified Intelligence — Where Earth Meets Data*
