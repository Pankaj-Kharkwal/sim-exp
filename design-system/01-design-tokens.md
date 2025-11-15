# Design System — Core Tokens

> **Enterprise-Grade Design System for AI Automation Platform**
> Version 2.0 | Updated: 2025-11-15

---

## 📐 Spacing System

### Base Unit: 4px Grid

All spacing follows a strict **4px increment** system for consistency across the platform.

```typescript
const spacing = {
  0: '0px',
  0.5: '2px',   // 0.5 × 4 = 2px
  1: '4px',     // 1 × 4 = 4px
  1.5: '6px',   // 1.5 × 4 = 6px
  2: '8px',     // 2 × 4 = 8px
  3: '12px',    // 3 × 4 = 12px
  4: '16px',    // 4 × 4 = 16px
  5: '20px',    // 5 × 4 = 20px
  6: '24px',    // 6 × 4 = 24px
  8: '32px',    // 8 × 4 = 32px
  10: '40px',   // 10 × 4 = 40px
  12: '48px',   // 12 × 4 = 48px
  16: '64px',   // 16 × 4 = 64px
  20: '80px',   // 20 × 4 = 80px
  24: '96px',   // 24 × 4 = 96px
}
```

### Component-Specific Spacing

```typescript
const componentSpacing = {
  // Cards & Panels
  card: {
    padding: '24px',        // p-6
    gap: '16px',            // gap-4
  },
  panel: {
    padding: '16px',        // p-4
    gap: '12px',            // gap-3
  },
  section: {
    padding: '32px',        // p-8
    gap: '24px',            // gap-6
  },

  // Form Elements
  input: {
    padding: '8px 12px',    // px-3 py-2
    height: '40px',         // h-10
  },
  button: {
    sm: '6px 12px',         // px-3 py-1.5
    md: '8px 16px',         // px-4 py-2
    lg: '10px 20px',        // px-5 py-2.5
  },

  // Layout
  container: {
    maxWidth: '1440px',
    padding: '0 24px',      // px-6
  },
  grid: {
    columns: 12,
    gap: '24px',            // gap-6
  },
}
```

---

## 🎨 Color System

### Semantic Color Tokens

#### Light Mode

```css
:root {
  /* Backgrounds */
  --bg: #ffffff;
  --bg-subtle: #fafafa;
  --bg-muted: #f5f5f5;
  --bg-hover: #f0f0f0;
  --bg-active: #e5e5e5;

  /* Surfaces (15 levels for layering) */
  --surface-1: #fafafa;
  --surface-2: #f5f5f5;
  --surface-3: #f0f0f0;
  --surface-4: #ebebeb;
  --surface-5: #e6e6e6;
  --surface-6: #e0e0e0;
  --surface-7: #dbdbdb;
  --surface-8: #d6d6d6;
  --surface-9: #d1d1d1;
  --surface-10: #cfcfcf;

  /* Text Hierarchy */
  --text-primary: #1b1b1b;      /* High emphasis - headers, key content */
  --text-secondary: #404040;    /* Medium emphasis - body text */
  --text-tertiary: #555555;     /* Low emphasis - labels */
  --text-muted: #737373;        /* Very low emphasis - placeholders */
  --text-subtle: #8a8a8a;       /* Disabled, hints */

  /* Borders */
  --border-primary: #dddddd;
  --border-secondary: #d1d1d1;
  --border-muted: #e5e5e5;
  --border-focus: #6366f1;      /* Focus rings */

  /* Brand Colors */
  --primary: #6366f1;           /* Indigo - primary actions */
  --primary-hover: #4f46e5;
  --primary-active: #4338ca;
  --primary-light: #eef2ff;

  --secondary: #8b5cf6;         /* Violet - secondary actions */
  --secondary-hover: #7c3aed;
  --secondary-active: #6d28d9;
  --secondary-light: #f5f3ff;

  --accent: #3b82f6;            /* Blue - highlights, links */
  --accent-hover: #2563eb;
  --accent-light: #eff6ff;

  /* Semantic States */
  --success: #22c55e;
  --success-bg: #f0fdf4;
  --success-border: #86efac;

  --warning: #f59e0b;
  --warning-bg: #fffbeb;
  --warning-border: #fcd34d;

  --error: #ef4444;
  --error-bg: #fef2f2;
  --error-border: #fca5a5;

  --info: #3b82f6;
  --info-bg: #eff6ff;
  --info-border: #93c5fd;

  /* Workflow Node Colors */
  --node-agent: #8b5cf6;        /* Violet */
  --node-api: #3b82f6;          /* Blue */
  --node-data: #22c55e;         /* Green */
  --node-logic: #f59e0b;        /* Amber */
  --node-trigger: #ec4899;      /* Pink */
  --node-integration: #06b6d4;  /* Cyan */
}
```

#### Dark Mode

```css
.dark {
  /* Backgrounds */
  --bg: #1b1b1b;
  --bg-subtle: #1e1e1e;
  --bg-muted: #212121;
  --bg-hover: #252525;
  --bg-active: #2a2a2a;

  /* Surfaces (15 levels for layering) */
  --surface-1: #1e1e1e;
  --surface-2: #212121;
  --surface-3: #252525;
  --surface-4: #292929;
  --surface-5: #2d2d2d;
  --surface-6: #313131;
  --surface-7: #353535;
  --surface-8: #3d3d3d;
  --surface-9: #4a4a4a;
  --surface-10: #5a5a5a;

  /* Text Hierarchy */
  --text-primary: #e6e6e6;
  --text-secondary: #b1b1b1;
  --text-tertiary: #aeaeae;
  --text-muted: #787878;
  --text-subtle: #7d7d7d;

  /* Borders */
  --border-primary: #2c2c2c;
  --border-secondary: #303030;
  --border-muted: #393939;
  --border-focus: #6366f1;

  /* Brand Colors (same as light, adjusted for dark backgrounds) */
  --primary: #6366f1;
  --primary-hover: #818cf8;
  --primary-active: #a5b4fc;
  --primary-light: #1e1b4b;

  --secondary: #8b5cf6;
  --secondary-hover: #a78bfa;
  --secondary-active: #c4b5fd;
  --secondary-light: #2e1065;

  --accent: #3b82f6;
  --accent-hover: #60a5fa;
  --accent-light: #1e3a8a;

  /* Semantic States */
  --success: #22c55e;
  --success-bg: #14532d;
  --success-border: #166534;

  --warning: #f59e0b;
  --warning-bg: #451a03;
  --warning-border: #78350f;

  --error: #ef4444;
  --error-bg: #450a0a;
  --error-border: #7f1d1d;

  --info: #3b82f6;
  --info-bg: #1e3a8a;
  --info-border: #1e40af;

  /* Workflow Node Colors (same) */
  --node-agent: #8b5cf6;
  --node-api: #3b82f6;
  --node-data: #22c55e;
  --node-logic: #f59e0b;
  --node-trigger: #ec4899;
  --node-integration: #06b6d4;
}
```

### Tailwind Config Extension

```typescript
// tailwind.config.ts
export default {
  theme: {
    extend: {
      colors: {
        bg: {
          DEFAULT: 'var(--bg)',
          subtle: 'var(--bg-subtle)',
          muted: 'var(--bg-muted)',
          hover: 'var(--bg-hover)',
          active: 'var(--bg-active)',
        },
        surface: {
          1: 'var(--surface-1)',
          2: 'var(--surface-2)',
          3: 'var(--surface-3)',
          4: 'var(--surface-4)',
          5: 'var(--surface-5)',
          6: 'var(--surface-6)',
          7: 'var(--surface-7)',
          8: 'var(--surface-8)',
          9: 'var(--surface-9)',
          10: 'var(--surface-10)',
        },
        text: {
          primary: 'var(--text-primary)',
          secondary: 'var(--text-secondary)',
          tertiary: 'var(--text-tertiary)',
          muted: 'var(--text-muted)',
          subtle: 'var(--text-subtle)',
        },
        border: {
          DEFAULT: 'var(--border-primary)',
          secondary: 'var(--border-secondary)',
          muted: 'var(--border-muted)',
          focus: 'var(--border-focus)',
        },
        node: {
          agent: 'var(--node-agent)',
          api: 'var(--node-api)',
          data: 'var(--node-data)',
          logic: 'var(--node-logic)',
          trigger: 'var(--node-trigger)',
          integration: 'var(--node-integration)',
        },
      },
    },
  },
}
```

---

## 🔤 Typography

### Font Family

```css
:root {
  --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
  --font-mono: 'JetBrains Mono', 'Fira Code', 'Consolas', monospace;
}
```

**Primary Font**: Inter (Variable)
- **Usage**: All UI text, headings, body copy
- **Weights**: 400 (Regular), 500 (Medium), 600 (Semibold), 700 (Bold)
- **Load**: `@fontsource/inter` or Google Fonts with variable weight axis

**Monospace Font**: JetBrains Mono
- **Usage**: Code blocks, JSON viewers, logs, terminal
- **Weights**: 400, 500, 600
- **Features**: Ligatures enabled for code

### Type Scale

```typescript
const typography = {
  // Display (Marketing pages only)
  display: {
    fontSize: '56px',
    lineHeight: '64px',
    fontWeight: 700,
    letterSpacing: '-0.02em',
  },

  // Headings
  h1: {
    fontSize: '48px',
    lineHeight: '56px',
    fontWeight: 700,
    letterSpacing: '-0.02em',
  },
  h2: {
    fontSize: '30px',
    lineHeight: '38px',
    fontWeight: 600,
    letterSpacing: '-0.01em',
  },
  h3: {
    fontSize: '24px',
    lineHeight: '32px',
    fontWeight: 600,
  },
  h4: {
    fontSize: '20px',
    lineHeight: '28px',
    fontWeight: 600,
  },
  h5: {
    fontSize: '16px',
    lineHeight: '24px',
    fontWeight: 600,
  },
  h6: {
    fontSize: '14px',
    lineHeight: '20px',
    fontWeight: 600,
  },

  // Body
  body: {
    fontSize: '16px',
    lineHeight: '24px',
    fontWeight: 400,
  },
  bodySm: {
    fontSize: '14px',
    lineHeight: '20px',
    fontWeight: 400,
  },
  bodyXs: {
    fontSize: '12px',
    lineHeight: '16px',
    fontWeight: 400,
  },

  // Labels & UI
  label: {
    fontSize: '14px',
    lineHeight: '20px',
    fontWeight: 500,
  },
  labelSm: {
    fontSize: '12px',
    lineHeight: '16px',
    fontWeight: 500,
  },

  // Code
  code: {
    fontSize: '14px',
    lineHeight: '20px',
    fontWeight: 400,
    fontFamily: 'var(--font-mono)',
  },
  codeSm: {
    fontSize: '12px',
    lineHeight: '18px',
    fontWeight: 400,
    fontFamily: 'var(--font-mono)',
  },
}
```

### Tailwind Typography Classes

```css
/* Custom text utilities */
.text-display { @apply text-[56px] leading-[64px] font-bold tracking-tight; }
.text-h1 { @apply text-5xl leading-[56px] font-bold tracking-tight; }
.text-h2 { @apply text-3xl leading-[38px] font-semibold tracking-tight; }
.text-h3 { @apply text-2xl leading-8 font-semibold; }
.text-h4 { @apply text-xl leading-7 font-semibold; }
.text-h5 { @apply text-base leading-6 font-semibold; }
.text-h6 { @apply text-sm leading-5 font-semibold; }

.text-body { @apply text-base leading-6; }
.text-body-sm { @apply text-sm leading-5; }
.text-body-xs { @apply text-xs leading-4; }

.text-label { @apply text-sm leading-5 font-medium; }
.text-label-sm { @apply text-xs leading-4 font-medium; }

.text-code { @apply font-mono text-sm leading-5; }
.text-code-sm { @apply font-mono text-xs leading-[18px]; }
```

---

## 📏 Border Radius

### Standard Radius Scale

```typescript
const borderRadius = {
  none: '0px',
  sm: '4px',      // Small elements (badges, tags)
  md: '8px',      // Default (buttons, inputs, cards)
  lg: '12px',     // Large cards, panels
  xl: '16px',     // Modals, dialogs
  full: '9999px', // Pills, avatars
}
```

### Component-Specific Radius

```typescript
const componentRadius = {
  button: '8px',
  input: '8px',
  card: '12px',
  modal: '16px',
  badge: '4px',
  avatar: '9999px',
  dropdown: '8px',
  tooltip: '6px',
  node: '8px',        // Workflow nodes
  minimap: '6px',
}
```

---

## 🎭 Elevation & Shadows

### Shadow Scale

```css
:root {
  /* Subtle elevation for cards */
  --shadow-xs: 0 1px 2px 0 rgb(0 0 0 / 0.05);
  --shadow-sm: 0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1);
  --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
  --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1);
  --shadow-xl: 0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1);

  /* For modals, popovers */
  --shadow-2xl: 0 25px 50px -12px rgb(0 0 0 / 0.25);

  /* Inner shadows for inputs */
  --shadow-inner: inset 0 2px 4px 0 rgb(0 0 0 / 0.05);

  /* Focus ring */
  --shadow-focus: 0 0 0 3px var(--primary-light);
}

.dark {
  /* Stronger shadows in dark mode */
  --shadow-xs: 0 1px 2px 0 rgb(0 0 0 / 0.3);
  --shadow-sm: 0 1px 3px 0 rgb(0 0 0 / 0.4), 0 1px 2px -1px rgb(0 0 0 / 0.4);
  --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.5), 0 2px 4px -2px rgb(0 0 0 / 0.5);
  --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.6), 0 4px 6px -4px rgb(0 0 0 / 0.6);
  --shadow-xl: 0 20px 25px -5px rgb(0 0 0 / 0.7), 0 8px 10px -6px rgb(0 0 0 / 0.7);
  --shadow-2xl: 0 25px 50px -12px rgb(0 0 0 / 0.8);
}
```

### Component Shadow Usage

```typescript
const componentShadows = {
  card: 'var(--shadow-sm)',
  cardHover: 'var(--shadow-md)',
  dropdown: 'var(--shadow-lg)',
  modal: 'var(--shadow-2xl)',
  tooltip: 'var(--shadow-md)',
  popover: 'var(--shadow-lg)',
  input: 'var(--shadow-inner)',
  focusRing: 'var(--shadow-focus)',
}
```

---

## ⚡ Transitions & Animations

### Duration Scale

```css
:root {
  --duration-75: 75ms;
  --duration-100: 100ms;
  --duration-150: 150ms;
  --duration-200: 200ms;
  --duration-300: 300ms;
  --duration-500: 500ms;
}
```

### Easing Functions

```css
:root {
  --ease-in: cubic-bezier(0.4, 0, 1, 1);
  --ease-out: cubic-bezier(0, 0, 0.2, 1);
  --ease-in-out: cubic-bezier(0.4, 0, 0.2, 1);
  --ease-bounce: cubic-bezier(0.68, -0.55, 0.265, 1.55);
  --ease-smooth: cubic-bezier(0.25, 0.1, 0.25, 1);
}
```

### Standard Transitions

```css
/* Default transitions for all interactive elements */
.transition-default {
  transition: all 150ms cubic-bezier(0.4, 0, 0.2, 1);
}

.transition-colors {
  transition: color 150ms, background-color 150ms, border-color 150ms;
}

.transition-transform {
  transition: transform 200ms cubic-bezier(0.4, 0, 0.2, 1);
}

.transition-opacity {
  transition: opacity 150ms cubic-bezier(0.4, 0, 0.2, 1);
}
```

### Custom Animations

```css
@keyframes fade-in {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes slide-up {
  from {
    opacity: 0;
    transform: translateY(8px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes slide-down {
  from {
    opacity: 0;
    transform: translateY(-8px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes scale-in {
  from {
    opacity: 0;
    transform: scale(0.95);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

@keyframes shimmer {
  0% { background-position: -1000px 0; }
  100% { background-position: 1000px 0; }
}

/* For workflow connections */
@keyframes dash-flow {
  to { stroke-dashoffset: -20; }
}

/* For loading states */
@keyframes pulse-ring {
  0%, 100% {
    opacity: 1;
    transform: scale(1);
  }
  50% {
    opacity: 0.5;
    transform: scale(1.1);
  }
}
```

---

## 🔲 Z-Index Scale

```typescript
const zIndex = {
  base: 0,
  dropdown: 1000,
  sticky: 1020,
  fixed: 1030,
  modalBackdrop: 1040,
  modal: 1050,
  popover: 1060,
  tooltip: 1070,
  notification: 1080,
  commandPalette: 1090,
  max: 9999,
}
```

---

## 📐 Layout Grid

### 12-Column Grid System

```css
.container {
  max-width: 1440px;
  margin: 0 auto;
  padding: 0 24px;
}

.grid-12 {
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  gap: 24px;
}

/* Responsive breakpoints */
@media (max-width: 640px) {
  .container { padding: 0 16px; }
  .grid-12 { gap: 16px; }
}
```

### Breakpoints

```typescript
const breakpoints = {
  xs: '475px',
  sm: '640px',
  md: '768px',
  lg: '1024px',
  xl: '1280px',
  '2xl': '1440px',
}
```

---

## ♿ Accessibility

### Focus States

```css
/* Visible focus ring for keyboard navigation */
*:focus-visible {
  outline: 2px solid var(--border-focus);
  outline-offset: 2px;
}

/* Remove default outline */
*:focus:not(:focus-visible) {
  outline: none;
}

/* Custom focus ring for buttons */
.btn:focus-visible {
  outline: 2px solid var(--border-focus);
  outline-offset: 2px;
}
```

### High Contrast Mode

```css
@media (prefers-contrast: high) {
  :root {
    --border-primary: #000000;
    --text-primary: #000000;
  }

  .dark {
    --border-primary: #ffffff;
    --text-primary: #ffffff;
  }
}
```

### Reduced Motion

```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

---

## 📦 Component Variants

### Button Sizes

```typescript
const buttonSizes = {
  xs: 'h-7 px-2 text-xs',
  sm: 'h-8 px-3 text-sm',
  md: 'h-10 px-4 text-sm',
  lg: 'h-11 px-5 text-base',
  xl: 'h-12 px-6 text-base',
}
```

### Input Sizes

```typescript
const inputSizes = {
  sm: 'h-8 px-3 text-sm',
  md: 'h-10 px-3 text-sm',
  lg: 'h-11 px-4 text-base',
}
```

---

## 🎯 Usage Guidelines

### Do's ✅

- **Always use the 4px spacing grid** for margins and padding
- **Use semantic color tokens** (e.g., `text-primary`, `bg-surface-2`) instead of raw hex values
- **Apply consistent border radius** (8px for most UI, 12px for cards, 16px for modals)
- **Use subtle shadows** (shadow-sm or shadow-md) — avoid heavy drop shadows
- **Maintain strong visual hierarchy** with typography scale
- **Ensure WCAG 2.2 AA contrast ratios** for all text

### Don'ts ❌

- **Don't use arbitrary spacing values** outside the 4px grid
- **Don't use raw color values** in components (always use CSS variables)
- **Don't use excessive border radius** (max 16px, except pills/avatars)
- **Don't use heavy, childish shadows** or glows
- **Don't mix font families** (Inter for UI, JetBrains Mono for code only)
- **Don't create new color variants** without adding to the design system

---

## 📚 Implementation Checklist

- [ ] Update `globals.css` with new CSS variable system
- [ ] Configure Tailwind with extended theme tokens
- [ ] Load Inter and JetBrains Mono fonts (variable weights)
- [ ] Set up dark mode with `next-themes`
- [ ] Create reusable Tailwind classes for typography
- [ ] Implement focus-visible styles for accessibility
- [ ] Add reduced-motion media query support
- [ ] Test color contrast ratios in both light/dark modes
- [ ] Document all tokens in Storybook or design docs
- [ ] Create component variant utilities with CVA (Class Variance Authority)

---

**Next Steps**: Proceed to **02-component-library.md** for detailed component specifications.
