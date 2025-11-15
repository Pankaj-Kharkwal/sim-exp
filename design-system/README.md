# Enterprise UI/UX Design System

> **Complete redesign documentation for AI Automation Platform**
> Version 2.0 | Created: 2025-11-15

---

## 📚 Documentation Structure

```
design-system/
├── README.md                      # This file
├── 01-design-tokens.md            # Core design system (colors, spacing, typography)
├── 02-component-library.md        # All UI components with code samples
├── pages/
│   ├── 01-landing-page.md         # Public landing page
│   ├── 02-auth-pages.md           # Login & Signup
│   ├── 03-chat-page.md            # Standalone chat interface
│   ├── 04-workspace-shell.md      # App shell & navigation
│   ├── 05-workspace-pages.md      # Workflows, Templates, Logs, Knowledge, Tools, Settings
│   └── 06-workflow-editor.md      # Core node-based workflow builder
└── IMPLEMENTATION.md              # Step-by-step implementation guide
```

---

## 🎯 Design Philosophy

This redesign follows **world-class enterprise design standards** inspired by:
- **n8n** - Visual workflow builder UX
- **Linear** - Clean, performant interface
- **Vercel** - Subtle gradients and spacing
- **Notion** - Information hierarchy
- **Figma** - Canvas interactions

### Core Principles

1. **Consistency Over Creativity**
   - Use the 4px spacing grid everywhere
   - Maintain semantic color tokens
   - Follow established component patterns

2. **Performance First**
   - Optimize animations for 60fps
   - Lazy load heavy components
   - Use CSS variables for theming

3. **Accessibility by Default**
   - WCAG 2.2 AA compliance
   - Keyboard navigation support
   - Screen reader optimization

4. **Professional, Not Playful**
   - Subtle shadows (no heavy drop shadows)
   - Consistent border radius (8-12px)
   - Enterprise-appropriate iconography

---

## 🎨 Design System Overview

### Color System
- **Light Mode**: Clean whites and grays with indigo/violet accents
- **Dark Mode**: Slate backgrounds with enhanced accents
- **Semantic Tokens**: `--text-primary`, `--bg-surface-2`, `--border`, etc.

### Typography
- **Primary Font**: Inter (Variable)
- **Monospace**: JetBrains Mono
- **Scale**: 12px → 14px → 16px → 20px → 24px → 30px → 48px
- **Line Height**: 1.5 for body, 1.2 for headings

### Spacing
- **Base Unit**: 4px grid
- **Component Spacing**:
  - Cards: `p-6` (24px)
  - Panels: `p-4` (16px)
  - Sections: `p-8` (32px)

### Border Radius
- **Small**: 4px (badges, tags)
- **Medium**: 8px (buttons, inputs)
- **Large**: 12px (cards, panels)
- **XL**: 16px (modals, dialogs)

---

## 📄 Page-by-Page Guide

### Public Pages

#### 1. Landing Page (`/`)
- Hero section with product screenshot
- Feature grid (3x2 cards)
- Social proof & testimonials
- Pricing tiers
- Clear CTAs throughout

**Key Files**: `apps/sim/app/(landing)/landing.tsx`

#### 2. Login & Signup (`/login`, `/signup`)
- Split layout (form + visual)
- OAuth buttons (GitHub, Google)
- Email/password with validation
- Password strength indicator

**Key Files**: `apps/sim/app/(auth)/login/`, `apps/sim/app/(auth)/signup/`

---

### Application Pages

#### 3. Workspace Shell
- Collapsible sidebar (280px → 64px)
- Workflow tree navigation
- Command palette (⌘K)
- Breadcrumbs
- User menu & notifications

**Key Files**: `apps/sim/app/workspace/[workspaceId]/layout.tsx`

#### 4. Workflow Editor ⭐ (Most Important)
- Node palette (left, 280px)
- Infinite canvas (ReactFlow)
- Inspector panel (right, 400px)
- Topbar with run/deploy actions
- Footer with zoom & stats

**Key Files**: `apps/sim/app/workspace/[workspaceId]/w/[workflowId]/workflow.tsx`

#### 5. Other Workspace Pages
- **Workflows List**: Grid/list view with search & filters
- **Templates**: Category tabs with template cards
- **Logs**: Real-time stream with severity filters
- **Knowledge**: Document table + preview panel
- **Tools**: Searchable grid of 81+ integrations
- **Settings**: Modal with sectioned navigation

---

## 🧩 Component Library

### Core Components
- **Button** (5 variants: primary, secondary, outline, ghost, destructive)
- **Input** (with label, error, helper text)
- **Card** (with header, content, footer)
- **Badge** (6 variants for status indicators)
- **Table** (sortable, filterable, paginated)
- **Modal/Dialog** (with backdrop blur)
- **Dropdown** (menu, select, popover)
- **Toast** (4 variants: success, error, warning, info)

### Advanced Components
- **DataTable** (TanStack Table integration)
- **Command Palette** (⌘K search)
- **Workflow Node** (custom ReactFlow node)
- **Code Block** (syntax highlighted with copy button)
- **File Upload** (drag & drop with preview)

**Full Specs**: See `02-component-library.md`

---

## 🚀 Quick Start

### 1. Install Dependencies
```bash
# Core UI libraries
bun add @radix-ui/react-dialog @radix-ui/react-dropdown-menu
bun add class-variance-authority clsx tailwind-merge
bun add lucide-react

# Workflow editor
bun add reactflow

# Data tables
bun add @tanstack/react-table

# Charts
bun add recharts
```

### 2. Update Tailwind Config
```typescript
// tailwind.config.ts
import type { Config } from 'tailwindcss'

export default {
  darkMode: ['class'],
  content: [
    './app/**/*.{ts,tsx}',
    './components/**/*.{ts,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        bg: 'var(--bg)',
        'text-primary': 'var(--text-primary)',
        primary: 'var(--primary)',
        // ... see 01-design-tokens.md for full config
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
      },
    },
  },
} satisfies Config
```

### 3. Update Global Styles
```css
/* apps/sim/app/globals.css */
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  :root {
    --bg: #ffffff;
    --text-primary: #1b1b1b;
    --primary: #6366f1;
    /* ... see 01-design-tokens.md for full variables */
  }

  .dark {
    --bg: #1b1b1b;
    --text-primary: #e6e6e6;
    /* ... dark mode overrides */
  }
}
```

### 4. Create Component Library
```bash
# Use ShadCN CLI to scaffold components
npx shadcn-ui@latest add button
npx shadcn-ui@latest add input
npx shadcn-ui@latest add card
npx shadcn-ui@latest add dialog
npx shadcn-ui@latest add dropdown-menu
npx shadcn-ui@latest add table
```

### 5. Implement Pages
Follow the page-specific guides in `pages/` directory, starting with:
1. Update design tokens in `globals.css`
2. Create/update components in `components/ui/`
3. Implement pages in `app/` directory
4. Test in both light and dark modes

---

## ✅ Implementation Checklist

### Phase 1: Foundation (Week 1)
- [ ] Update `globals.css` with new CSS variables
- [ ] Configure Tailwind with extended theme
- [ ] Load Inter & JetBrains Mono fonts
- [ ] Set up dark mode with `next-themes`
- [ ] Create base components (Button, Input, Card)

### Phase 2: Components (Week 2)
- [ ] Implement all 40+ UI components
- [ ] Create component variants with CVA
- [ ] Add accessibility features (focus states, ARIA)
- [ ] Test components in Storybook
- [ ] Document usage examples

### Phase 3: Pages (Week 3-4)
- [ ] Redesign Landing Page with new sections
- [ ] Update Login & Signup pages
- [ ] Implement Workspace Shell & Navigation
- [ ] Rebuild Workflow Editor with ReactFlow
- [ ] Update all workspace child pages

### Phase 4: Polish (Week 5)
- [ ] Add animations & transitions
- [ ] Optimize performance (lazy loading, code splitting)
- [ ] Test accessibility (keyboard nav, screen readers)
- [ ] Cross-browser testing
- [ ] Mobile responsiveness

### Phase 5: Launch (Week 6)
- [ ] Final QA testing
- [ ] Update documentation
- [ ] Deploy to staging
- [ ] User acceptance testing
- [ ] Production deployment

---

## 📐 Grid System

All layouts use a **12-column grid** with **24px gaps**:

```tsx
<div className="container max-w-7xl mx-auto px-6">
  <div className="grid grid-cols-12 gap-6">
    <div className="col-span-12 md:col-span-8 lg:col-span-9">
      {/* Main content */}
    </div>
    <div className="col-span-12 md:col-span-4 lg:col-span-3">
      {/* Sidebar */}
    </div>
  </div>
</div>
```

---

## 🎭 Animations

### Standard Transitions
```css
.transition-default {
  transition: all 150ms cubic-bezier(0.4, 0, 0.2, 1);
}
```

### Hover Effects
```tsx
<Card className="hover:shadow-lg hover:-translate-y-0.5 transition-all" />
```

### Loading States
```tsx
<Button disabled>
  <Loader2 className="w-4 h-4 mr-2 animate-spin" />
  Loading...
</Button>
```

---

## ♿ Accessibility

### Focus States
All interactive elements have visible focus rings:
```css
*:focus-visible {
  outline: 2px solid var(--primary);
  outline-offset: 2px;
}
```

### Keyboard Navigation
- **Tab**: Navigate between elements
- **Enter/Space**: Activate buttons
- **Escape**: Close modals/dropdowns
- **Arrow Keys**: Navigate lists/menus

### Screen Readers
```tsx
<Button aria-label="Close dialog">
  <X className="w-4 h-4" />
</Button>
```

---

## 📱 Responsive Breakpoints

```typescript
const breakpoints = {
  sm: '640px',   // Mobile landscape
  md: '768px',   // Tablet
  lg: '1024px',  // Desktop
  xl: '1280px',  // Large desktop
  '2xl': '1440px', // Max container width
}
```

### Mobile-First Approach
```tsx
<div className="flex flex-col md:flex-row gap-4">
  {/* Stacks on mobile, side-by-side on desktop */}
</div>
```

---

## 🔍 Testing

### Visual Regression
```bash
bun run test:visual
```

### Accessibility
```bash
bun run test:a11y
```

### Component Tests
```bash
bun run test:components
```

---

## 📚 Resources

### Design Inspiration
- [n8n.io](https://n8n.io) - Workflow builder UX
- [linear.app](https://linear.app) - Clean interface design
- [vercel.com](https://vercel.com) - Subtle gradients
- [figma.com](https://figma.com) - Canvas interactions

### Component Libraries
- [ShadCN UI](https://ui.shadcn.com) - Base components
- [Radix UI](https://radix-ui.com) - Primitives
- [Lucide Icons](https://lucide.dev) - Icon system

### Tools
- [Tailwind CSS](https://tailwindcss.com) - Utility CSS
- [CVA](https://cva.style) - Component variants
- [ReactFlow](https://reactflow.dev) - Node editor
- [TanStack Table](https://tanstack.com/table) - Data tables

---

## 🤝 Contributing

When implementing new components or pages:

1. **Follow the design system** - Use tokens, not hardcoded values
2. **Mobile-first** - Design for mobile, enhance for desktop
3. **Accessibility** - Test with keyboard and screen readers
4. **Performance** - Optimize for fast load times
5. **Documentation** - Add examples and usage notes

---

## 📞 Support

For questions or clarifications about this design system:
- Review the detailed page specifications in `pages/`
- Check component examples in `02-component-library.md`
- Refer to design tokens in `01-design-tokens.md`

---

**Last Updated**: 2025-11-15
**Version**: 2.0
**Status**: ✅ Ready for Implementation
