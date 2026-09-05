# TurabIQ Logo — One-Page Quick Reference

## Logo Concept: "Stratified Intelligence"
**Three angled soil layers + ascending sensor signal waveform**  
*Represents: Earth monitoring + Data intelligence*

---

## 🎨 Core Colors

| Color | Hex | RGB | Use |
|-------|-----|-----|-----|
| **Warm Sand** | `#D4A574` | 212, 165, 116 | Primary layer, warm accent |
| **Deep Teal** | `#1B7B7F` | 27, 123, 127 | Signal line, tech accent |
| **Medium Clay** | `#C29A6B` | 194, 154, 107 | Secondary layer |
| **Dark Clay** | `#A0826D` | 160, 130, 109 | Deep foundation, dark text |
| **Off-White** | `#FAFAF8` | 250, 250, 248 | Background |
| **Charcoal** | `#2C2C2C` | 44, 44, 44 | Primary text |

---

## 📐 Logo Sizes

| Context | Size | File |
|---------|------|------|
| **Browser Tab** | 32–64px | `turabiq-favicon.svg` |
| **App Icon** | 192–512px | `turabiq-favicon.svg` |
| **Website Header** | 200–300px | `turabiq-logo-horizontal.svg` |
| **Pitch Deck** | 300–400px | `turabiq-logo-horizontal.svg` |
| **Business Card** | 40mm | `turabiq-logo-horizontal.svg` |
| **Print (High-Res)** | 300 DPI export | Any SVG → PDF |

---

## 📄 File Manifest

```
turabiq-logo-mark.svg          ← Icon only (120×120)
turabiq-logo-horizontal.svg    ← Wordmark horizontal (320×100)
turabiq-logo-stacked.svg       ← Wordmark vertical (140×160)
turabiq-favicon.svg            ← App icon (64×64)
```

**All files:** Vector SVG (scalable, editable)

---

## ✅ Quick Checklist

- [ ] File added to project
- [ ] Favicon updated in `index.html`
- [ ] Color palette imported to CSS
- [ ] Logo tested at multiple sizes
- [ ] Contrast verified (dark text on light background)
- [ ] No effects added (no shadows, gradients, or 3D)
- [ ] Social media og:image set to favicon
- [ ] Brand guidelines distributed to team

---

## 🚫 Don't

❌ Rotate, skew, or distort the mark  
❌ Add drop shadows, glows, or effects  
❌ Change colors (use hex values exactly)  
❌ Remove layers or signal line  
❌ Use at sizes below 64×64px (without favicon version)  
❌ Add additional decorative elements  

---

## 🎯 Quick Copy-Paste

### CSS Variables
```css
--turabiq-sand: #D4A574;
--turabiq-teal: #1B7B7F;
--turabiq-clay-m: #C29A6B;
--turabiq-clay-d: #A0826D;
--turabiq-bg: #FAFAF8;
--turabiq-text: #2C2C2C;
```

### HTML Meta (Favicon)
```html
<link rel="icon" type="image/svg+xml" href="/turabiq-favicon.svg">
<meta name="theme-color" content="#1B7B7F">
<meta property="og:image" content="https://yoursite.com/turabiq-favicon.svg">
```

### React Component
```jsx
import logo from '/turabiq-logo-horizontal.svg';
export default function Logo() {
  return <img src={logo} alt="TurabIQ" className="logo" />;
}
```

---

## 📚 Full Documentation

- `BRAND_GUIDELINES.md` — Complete design specifications
- `COLOR_PALETTE.md` — Detailed color reference (RGB, HSL, CMYK)
- `IMPLEMENTATION_CHECKLIST.md` — Step-by-step rollout guide
- `DESIGN_OVERVIEW.md` — Concept brief and design philosophy

---

**TurabIQ Branding Kit v1.0**  
*Ready to deploy: Web • Mobile • Print • Merchandise*

Last Updated: 2026-09-05
