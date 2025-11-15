# Implementation Guide

> **Step-by-step guide to implement the enterprise UI/UX redesign**

---

## 🗺️ Implementation Roadmap

### Timeline: 6 Weeks

**Week 1**: Foundation & Design Tokens
**Week 2**: Component Library
**Week 3-4**: Page Implementations
**Week 5**: Polish & Optimization
**Week 6**: Testing & Launch

---

## Week 1: Foundation

### Day 1-2: Design Tokens

#### Step 1: Update `globals.css`

Replace the entire color system in `/apps/sim/app/globals.css`:

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  /* Light Mode */
  :root {
    /* Backgrounds */
    --bg: #ffffff;
    --bg-subtle: #fafafa;
    --bg-muted: #f5f5f5;
    --bg-hover: #f0f0f0;
    --bg-active: #e5e5e5;

    /* Surfaces (15 levels) */
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
    --text-primary: #1b1b1b;
    --text-secondary: #404040;
    --text-tertiary: #555555;
    --text-muted: #737373;
    --text-subtle: #8a8a8a;

    /* Borders */
    --border: #dddddd;
    --border-secondary: #d1d1d1;
    --border-muted: #e5e5e5;
    --border-focus: #6366f1;

    /* Brand Colors */
    --primary: #6366f1;
    --primary-hover: #4f46e5;
    --primary-active: #4338ca;
    --primary-light: #eef2ff;

    --secondary: #8b5cf6;
    --secondary-hover: #7c3aed;
    --secondary-active: #6d28d9;
    --secondary-light: #f5f3ff;

    --accent: #3b82f6;
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
    --node-agent: #8b5cf6;
    --node-api: #3b82f6;
    --node-data: #22c55e;
    --node-logic: #f59e0b;
    --node-trigger: #ec4899;
    --node-integration: #06b6d4;

    /* Shadows */
    --shadow-xs: 0 1px 2px 0 rgb(0 0 0 / 0.05);
    --shadow-sm: 0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1);
    --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
    --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1);
    --shadow-xl: 0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1);
    --shadow-2xl: 0 25px 50px -12px rgb(0 0 0 / 0.25);
    --shadow-inner: inset 0 2px 4px 0 rgb(0 0 0 / 0.05);
    --shadow-focus: 0 0 0 3px var(--primary-light);

    /* Border Radius */
    --radius: 8px;
  }

  /* Dark Mode */
  .dark {
    /* Backgrounds */
    --bg: #1b1b1b;
    --bg-subtle: #1e1e1e;
    --bg-muted: #212121;
    --bg-hover: #252525;
    --bg-active: #2a2a2a;

    /* Surfaces */
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

    /* Text */
    --text-primary: #e6e6e6;
    --text-secondary: #b1b1b1;
    --text-tertiary: #aeaeae;
    --text-muted: #787878;
    --text-subtle: #7d7d7d;

    /* Borders */
    --border: #2c2c2c;
    --border-secondary: #303030;
    --border-muted: #393939;

    /* Primary colors stay same */

    /* Semantic states - darker backgrounds */
    --success-bg: #14532d;
    --success-border: #166534;

    --warning-bg: #451a03;
    --warning-border: #78350f;

    --error-bg: #450a0a;
    --error-border: #7f1d1d;

    --info-bg: #1e3a8a;
    --info-border: #1e40af;

    /* Stronger shadows */
    --shadow-xs: 0 1px 2px 0 rgb(0 0 0 / 0.3);
    --shadow-sm: 0 1px 3px 0 rgb(0 0 0 / 0.4), 0 1px 2px -1px rgb(0 0 0 / 0.4);
    --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.5), 0 2px 4px -2px rgb(0 0 0 / 0.5);
    --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.6), 0 4px 6px -4px rgb(0 0 0 / 0.6);
    --shadow-xl: 0 20px 25px -5px rgb(0 0 0 / 0.7), 0 8px 10px -6px rgb(0 0 0 / 0.7);
    --shadow-2xl: 0 25px 50px -12px rgb(0 0 0 / 0.8);
  }

  * {
    border-color: var(--border);
  }

  body {
    background-color: var(--bg);
    color: var(--text-primary);
  }
}

/* Custom animations */
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

@keyframes dash-flow {
  to { stroke-dashoffset: -20; }
}

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

/* Accessibility */
*:focus-visible {
  outline: 2px solid var(--border-focus);
  outline-offset: 2px;
}

*:focus:not(:focus-visible) {
  outline: none;
}

/* Reduced motion */
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}

/* High contrast mode */
@media (prefers-contrast: high) {
  :root {
    --border: #000000;
    --text-primary: #000000;
  }

  .dark {
    --border: #ffffff;
    --text-primary: #ffffff;
  }
}
```

#### Step 2: Update Tailwind Config

Update `/apps/sim/tailwind.config.ts`:

```typescript
import type { Config } from 'tailwindcss'

export default {
  darkMode: ['class'],
  content: [
    './app/**/*.{ts,tsx}',
    './components/**/*.{ts,tsx}',
    './blocks/**/*.{ts,tsx}',
  ],
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
          DEFAULT: 'var(--border)',
          secondary: 'var(--border-secondary)',
          muted: 'var(--border-muted)',
          focus: 'var(--border-focus)',
        },
        primary: {
          DEFAULT: 'var(--primary)',
          hover: 'var(--primary-hover)',
          active: 'var(--primary-active)',
          light: 'var(--primary-light)',
        },
        secondary: {
          DEFAULT: 'var(--secondary)',
          hover: 'var(--secondary-hover)',
          active: 'var(--secondary-active)',
          light: 'var(--secondary-light)',
        },
        accent: {
          DEFAULT: 'var(--accent)',
          hover: 'var(--accent-hover)',
          light: 'var(--accent-light)',
        },
        success: {
          DEFAULT: 'var(--success)',
          bg: 'var(--success-bg)',
          border: 'var(--success-border)',
        },
        warning: {
          DEFAULT: 'var(--warning)',
          bg: 'var(--warning-bg)',
          border: 'var(--warning-border)',
        },
        error: {
          DEFAULT: 'var(--error)',
          bg: 'var(--error-bg)',
          border: 'var(--error-border)',
        },
        info: {
          DEFAULT: 'var(--info)',
          bg: 'var(--info-bg)',
          border: 'var(--info-border)',
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
      boxShadow: {
        xs: 'var(--shadow-xs)',
        sm: 'var(--shadow-sm)',
        md: 'var(--shadow-md)',
        lg: 'var(--shadow-lg)',
        xl: 'var(--shadow-xl)',
        '2xl': 'var(--shadow-2xl)',
        inner: 'var(--shadow-inner)',
        focus: 'var(--shadow-focus)',
      },
      borderRadius: {
        lg: 'var(--radius)',
        md: 'calc(var(--radius) - 2px)',
        sm: 'calc(var(--radius) - 4px)',
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'Consolas', 'monospace'],
      },
      fontSize: {
        xs: ['12px', '16px'],
        sm: ['14px', '20px'],
        base: ['16px', '24px'],
        lg: ['18px', '28px'],
        xl: ['20px', '28px'],
        '2xl': ['24px', '32px'],
        '3xl': ['30px', '38px'],
        '4xl': ['36px', '44px'],
        '5xl': ['48px', '56px'],
        '6xl': ['60px', '68px'],
      },
      animation: {
        'fade-in': 'fade-in 0.2s ease-out',
        'slide-up': 'slide-up 0.3s ease-out',
        'slide-down': 'slide-down 0.3s ease-out',
        'scale-in': 'scale-in 0.2s ease-out',
        'shimmer': 'shimmer 2s linear infinite',
        'pulse-ring': 'pulse-ring 2s ease-in-out infinite',
      },
    },
  },
  plugins: [
    require('@tailwindcss/typography'),
    require('tailwindcss-animate'),
  ],
} satisfies Config
```

#### Step 3: Install & Configure Fonts

Update `/apps/sim/app/layout.tsx`:

```typescript
import { Inter, JetBrains_Mono } from 'next/font/google'

const inter = Inter({
  subsets: ['latin'],
  variable: '--font-sans',
  display: 'swap',
})

const jetbrainsMono = JetBrains_Mono({
  subsets: ['latin'],
  variable: '--font-mono',
  display: 'swap',
})

export default function RootLayout({ children }) {
  return (
    <html lang="en" className={`${inter.variable} ${jetbrainsMono.variable}`}>
      <body className="font-sans antialiased">{children}</body>
    </html>
  )
}
```

---

## Week 2: Component Library

### Install ShadCN UI Components

```bash
npx shadcn-ui@latest init

# Install all core components
npx shadcn-ui@latest add button
npx shadcn-ui@latest add input
npx shadcn-ui@latest add textarea
npx shadcn-ui@latest add card
npx shadcn-ui@latest add badge
npx shadcn-ui@latest add dialog
npx shadcn-ui@latest add dropdown-menu
npx shadcn-ui@latest add popover
npx shadcn-ui@latest add select
npx shadcn-ui@latest add switch
npx shadcn-ui@latest add slider
npx shadcn-ui@latest add tabs
npx shadcn-ui@latest add table
npx shadcn-ui@latest add toast
npx shadcn-ui@latest add tooltip
npx shadcn-ui@latest add separator
npx shadcn-ui@latest add avatar
npx shadcn-ui@latest add checkbox
npx shadcn-ui@latest add radio-group
npx shadcn-ui@latest add command
```

### Customize Button Component

Update `/apps/sim/components/ui/button.tsx` to match design system:

```typescript
import { cva, type VariantProps } from 'class-variance-authority'

const buttonVariants = cva(
  'inline-flex items-center justify-center rounded-lg font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary focus-visible:ring-offset-2 disabled:opacity-50 disabled:pointer-events-none',
  {
    variants: {
      variant: {
        primary: 'bg-primary text-white hover:bg-primary-hover active:bg-primary-active shadow-sm',
        secondary: 'bg-surface-3 text-text-primary border border-border hover:bg-surface-4 active:bg-surface-5',
        outline: 'border border-border bg-transparent hover:bg-surface-2 active:bg-surface-3',
        ghost: 'hover:bg-surface-2 hover:text-text-primary',
        destructive: 'bg-error text-white hover:bg-red-600 active:bg-red-700',
        link: 'text-primary underline-offset-4 hover:underline',
      },
      size: {
        xs: 'h-7 px-2 text-xs',
        sm: 'h-8 px-3 text-sm',
        md: 'h-10 px-4 text-sm',
        lg: 'h-11 px-5 text-base',
        xl: 'h-12 px-6 text-base',
      },
    },
    defaultVariants: {
      variant: 'primary',
      size: 'md',
    },
  }
)

// ... rest of component
```

---

## Week 3-4: Page Implementations

### Priority Order

1. **Workflow Editor** (most complex, most important)
2. **Workspace Shell** (foundation for all pages)
3. **Workflows List Page**
4. **Login & Signup**
5. **Templates, Logs, Knowledge, Tools**
6. **Landing Page**

### Example: Implementing Workflow Editor

#### Install ReactFlow

```bash
bun add reactflow
```

#### Create Node Types

```typescript
// app/workspace/[workspaceId]/w/[workflowId]/nodes/custom-node.tsx
import { memo } from 'react'
import { Handle, Position } from 'reactflow'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'

export const CustomNode = memo(({ id, data, selected }) => {
  return (
    <div
      className={cn(
        'min-w-[240px] rounded-lg bg-surface-1 border-2 transition-all',
        selected ? 'border-primary shadow-lg' : 'border-border'
      )}
    >
      {/* Implementation from design spec */}
    </div>
  )
})
```

#### Create Main Editor

```typescript
// app/workspace/[workspaceId]/w/[workflowId]/page.tsx
'use client'

import ReactFlow, { Background, Controls, MiniMap } from 'reactflow'
import 'reactflow/dist/style.css'

export default function WorkflowEditorPage() {
  // Implementation from design spec
}
```

---

## Week 5: Polish & Optimization

### Performance Optimizations

#### 1. Code Splitting
```typescript
import dynamic from 'next/dynamic'

const WorkflowEditor = dynamic(
  () => import('@/components/workflow/editor'),
  { ssr: false, loading: () => <LoadingSkeleton /> }
)
```

#### 2. Image Optimization
```typescript
import Image from 'next/image'

<Image
  src="/hero.png"
  alt="Workflow Editor"
  width={1200}
  height={800}
  priority
  quality={90}
/>
```

#### 3. Font Optimization
Already done with `next/font/google`

### Animations

Add subtle animations:

```typescript
import { motion } from 'framer-motion'

<motion.div
  initial={{ opacity: 0, y: 20 }}
  animate={{ opacity: 1, y: 0 }}
  transition={{ duration: 0.3 }}
>
  {content}
</motion.div>
```

---

## Week 6: Testing & Launch

### Accessibility Testing

```bash
# Install testing tools
bun add -D @axe-core/react
bun add -D @testing-library/react
bun add -D @testing-library/jest-dom
```

### Visual Regression Testing

```bash
# Use Playwright for screenshots
bun add -D @playwright/test
```

### Checklist Before Launch

- [ ] All pages render correctly in light/dark mode
- [ ] No console errors or warnings
- [ ] Keyboard navigation works on all pages
- [ ] Screen reader testing completed
- [ ] Performance scores > 90 (Lighthouse)
- [ ] Mobile responsiveness verified
- [ ] Cross-browser testing (Chrome, Firefox, Safari, Edge)
- [ ] Load testing for workflow editor with 50+ nodes

---

## 🎯 Common Patterns

### Pattern 1: Page Layout

```typescript
export default function Page() {
  return (
    <div className="h-full flex flex-col">
      {/* Header */}
      <header className="p-6 border-b border-border">
        <h1 className="text-2xl font-bold">Page Title</h1>
      </header>

      {/* Content */}
      <main className="flex-1 overflow-y-auto p-6">
        {/* Content here */}
      </main>
    </div>
  )
}
```

### Pattern 2: Loading States

```typescript
{isLoading ? (
  <div className="flex items-center justify-center h-64">
    <Loader2 className="w-8 h-8 animate-spin text-primary" />
  </div>
) : (
  <Content />
)}
```

### Pattern 3: Empty States

```typescript
{items.length === 0 ? (
  <div className="flex flex-col items-center justify-center h-64 text-center">
    <FileQuestion className="w-12 h-12 text-text-muted mb-3" />
    <h3 className="text-lg font-semibold text-text-primary mb-1">
      No items found
    </h3>
    <p className="text-sm text-text-muted mb-4">
      Get started by creating your first item
    </p>
    <Button onClick={createItem}>
      <Plus className="w-4 h-4 mr-2" />
      Create Item
    </Button>
  </div>
) : (
  <ItemsList />
)}
```

---

## 🐛 Troubleshooting

### Issue: Colors not applying
**Solution**: Ensure CSS variables are defined in `globals.css` and imported in layout

### Issue: Fonts not loading
**Solution**: Check `layout.tsx` has font variables applied to `<html>` tag

### Issue: Dark mode not working
**Solution**: Verify `next-themes` is installed and ThemeProvider wraps app

### Issue: Components look different from design
**Solution**: Clear browser cache, rebuild Tailwind (`bun run build`)

---

## 📚 Additional Resources

- Full design specs: See `pages/` directory
- Component library: See `02-component-library.md`
- Design tokens: See `01-design-tokens.md`
- Main README: See `README.md`

---

**Ready to start implementation? Begin with Week 1, Day 1!**
