# TurabIQ Color Palette Reference

## Core Colors

### 1. Warm Sand — `#D4A574`
```
RGB: (212, 165, 116)
HSL: (29°, 53%, 64%)
CMYK: (0, 22, 45, 17)
Use: Primary earth tone, layer fills, warm accents
```

### 2. Deep Teal — `#1B7B7F`
```
RGB: (27, 123, 127)
HSL: (182°, 65%, 30%)
CMYK: (79, 3, 0, 50)
Use: Signal lines, tech accents, interactive elements
```

### 3. Medium Clay — `#C29A6B`
```
RGB: (194, 154, 107)
HSL: (29°, 38%, 59%)
Use: Secondary earth tone, layer shading
```

### 4. Dark Clay — `#A0826D`
```
RGB: (160, 130, 109)
HSL: (22°, 19%, 53%)
Use: Deep foundation, layered depth, text on light
```

## Neutral Palette

### Off-White Background — `#FAFAF8`
```
RGB: (250, 250, 248)
HSL: (30°, 100%, 98%)
Use: Clean backgrounds, high contrast with dark text
```

### Charcoal Text — `#2C2C2C`
```
RGB: (44, 44, 44)
HSL: (0°, 0%, 17%)
Use: Primary text, headlines, strong contrast on light
```

### Warm Gray Dividers — `#E8DCC8`
```
RGB: (232, 220, 200)
HSL: (29°, 44%, 85%)
Use: Subtle borders, divider lines, light accents
```

---

## Usage Guidelines

### Dashboard / UI
```css
/* Main background */
background-color: #FAFAF8;

/* Text */
color: #2C2C2C;

/* Accent buttons, active states */
accent-color: #1B7B7F;

/* Chart fills (layered data) */
--layer-1: #D4A574;
--layer-2: #C29A6B;
--layer-3: #A0826D;
```

### Alert States
```css
/* Success / Normal */
color: #1B7B7F;    /* Teal */

/* Warning */
color: #D4A574;    /* Warm sand */

/* Critical / High Alert */
color: #A0826D;    /* Dark clay */
```

### Accessibility
- **Dark text (#2C2C2C) on light background (#FAFAF8):** WCAG AAA ✓
- **Teal (#1B7B7F) text on white:** WCAG AA ✓ (avoid for small text)
- **Warm sand (#D4A574) on white:** WCAG AA ✓ (fair contrast)
- For small text (<14px), use dark clay (#A0826D) or charcoal (#2C2C2C)

---

## Color Hex Codes (Quick Copy)

```
Sand:     #D4A574
Teal:     #1B7B7F
Clay-M:   #C29A6B
Clay-D:   #A0826D
Off-Wh:   #FAFAF8
Charcoal: #2C2C2C
Gray:     #E8DCC8
```

## RGB Values (For Design Tools)

```
Sand:     212, 165, 116
Teal:     27,  123, 127
Clay-M:   194, 154, 107
Clay-D:   160, 130, 109
Off-Wh:   250, 250, 248
Charcoal: 44,  44,  44
Gray:     232, 220, 200
```

---

**Palette Strategy:** Warm earth (sand/clay) + cool tech (teal) creates visual tension between "soil monitoring" and "tech intelligence." Restrained 3-color core + 4 neutrals maintains premium, minimal aesthetic.
