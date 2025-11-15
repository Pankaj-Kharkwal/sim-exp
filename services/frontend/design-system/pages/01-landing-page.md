# Landing Page Design

> **Route**: `/`
> **Type**: Public marketing page
> **Goal**: Convert visitors into users with clear value proposition

---

## 🎯 Layout Overview

```
┌─────────────────────────────────────────────────────────────┐
│  NAVIGATION BAR (sticky)                                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  HERO SECTION                                               │
│  - Main headline + subheadline                              │
│  - CTA buttons                                              │
│  - Product screenshot/demo                                  │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  SOCIAL PROOF                                               │
│  - Trusted by logos                                         │
│  - Stats (users, workflows, integrations)                   │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  FEATURES GRID                                              │
│  - 3x2 feature cards with icons                             │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  HOW IT WORKS                                               │
│  - 3-step process with visuals                              │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  WORKFLOW EXAMPLES                                          │
│  - Interactive workflow previews                            │
│  - Use case tabs                                            │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  INTEGRATIONS                                               │
│  - Tool logos grid                                          │
│  - 81+ integrations badge                                   │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  TESTIMONIALS                                               │
│  - Carousel with user quotes                                │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  PRICING (if applicable)                                    │
│  - 3 tier cards                                             │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  FINAL CTA                                                  │
│  - Strong headline + action                                 │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  FOOTER                                                     │
│  - Links, legal, social                                     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 🧩 Section Breakdown

### 1. Navigation Bar

**Position**: Sticky top, z-index 50
**Background**: Blur backdrop with border bottom

```tsx
<nav className="sticky top-0 z-50 backdrop-blur-xl bg-bg/80 border-b border-border">
  <div className="container max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
    {/* Logo */}
    <div className="flex items-center gap-8">
      <Logo />
      <div className="hidden md:flex items-center gap-6">
        <NavLink href="#features">Features</NavLink>
        <NavLink href="#integrations">Integrations</NavLink>
        <NavLink href="#pricing">Pricing</NavLink>
        <NavLink href="/docs">Docs</NavLink>
      </div>
    </div>

    {/* Actions */}
    <div className="flex items-center gap-3">
      <Button variant="ghost" asChild>
        <Link href="/login">Sign In</Link>
      </Button>
      <Button variant="primary" asChild>
        <Link href="/signup">Get Started</Link>
      </Button>
    </div>
  </div>
</nav>
```

**Styles**:
- Height: 64px (h-16)
- Background: `backdrop-blur-xl bg-bg/80`
- Border: 1px bottom, `border-border`
- Nav links: text-sm, text-text-secondary, hover:text-text-primary

---

### 2. Hero Section

**Layout**: Centered, max-width 1280px, py-20 md:py-32

```tsx
<section className="relative overflow-hidden py-20 md:py-32">
  {/* Background gradient */}
  <div className="absolute inset-0 bg-gradient-to-br from-primary/5 via-transparent to-secondary/5" />

  <div className="container max-w-6xl mx-auto px-6 relative z-10">
    <div className="text-center space-y-6 max-w-3xl mx-auto mb-12">
      {/* Badge */}
      <Badge variant="primary" className="inline-flex">
        <Sparkles className="w-3 h-3 mr-1" />
        AI-Powered Automation
      </Badge>

      {/* Headline */}
      <h1 className="text-5xl md:text-6xl lg:text-7xl font-bold tracking-tight text-text-primary">
        Build Powerful AI Workflows{' '}
        <span className="bg-gradient-to-r from-primary to-secondary bg-clip-text text-transparent">
          Without Code
        </span>
      </h1>

      {/* Subheadline */}
      <p className="text-xl md:text-2xl text-text-secondary max-w-2xl mx-auto">
        Connect AI agents, APIs, and tools with a visual workflow builder.
        Automate complex tasks in minutes.
      </p>

      {/* CTA Buttons */}
      <div className="flex flex-col sm:flex-row items-center justify-center gap-4 pt-4">
        <Button size="lg" variant="primary" className="w-full sm:w-auto">
          <Play className="w-5 h-5 mr-2" />
          Start Building Free
        </Button>
        <Button size="lg" variant="outline" className="w-full sm:w-auto">
          <Video className="w-5 h-5 mr-2" />
          Watch Demo
        </Button>
      </div>

      {/* Social Proof */}
      <p className="text-sm text-text-muted pt-4">
        Join 10,000+ teams automating workflows
      </p>
    </div>

    {/* Product Screenshot */}
    <div className="relative max-w-5xl mx-auto">
      <div className="rounded-xl border border-border shadow-2xl overflow-hidden bg-surface-1">
        <img
          src="/screenshots/workflow-editor.png"
          alt="Workflow Editor Interface"
          className="w-full h-auto"
        />
      </div>
      {/* Floating elements */}
      <div className="absolute -top-4 -left-4 w-72 h-72 bg-primary/20 rounded-full blur-3xl" />
      <div className="absolute -bottom-4 -right-4 w-72 h-72 bg-secondary/20 rounded-full blur-3xl" />
    </div>
  </div>
</section>
```

**Colors**:
- Headline: text-text-primary, gradient accent on key phrase
- Subheadline: text-text-secondary, text-xl
- Background: Subtle gradient overlay with primary/secondary colors at 5% opacity

**Typography**:
- H1: text-5xl md:text-6xl lg:text-7xl, font-bold
- Subheadline: text-xl md:text-2xl
- CTA: Button size-lg

**Spacing**:
- Section: py-20 md:py-32
- Inner gap: space-y-6
- Max width: 1280px (max-w-6xl)

---

### 3. Social Proof Section

```tsx
<section className="py-12 border-y border-border bg-surface-1">
  <div className="container max-w-6xl mx-auto px-6">
    {/* Stats */}
    <div className="grid grid-cols-2 md:grid-cols-4 gap-8 mb-12">
      <Stat value="10,000+" label="Active Users" />
      <Stat value="500K+" label="Workflows Run" />
      <Stat value="81+" label="Integrations" />
      <Stat value="99.9%" label="Uptime" />
    </div>

    {/* Trusted By Logos */}
    <div className="text-center">
      <p className="text-sm text-text-muted mb-6">Trusted by teams at</p>
      <div className="flex flex-wrap items-center justify-center gap-8 opacity-60 grayscale hover:opacity-100 hover:grayscale-0 transition-all">
        {/* Company logos */}
        <img src="/logos/company1.svg" className="h-8" />
        <img src="/logos/company2.svg" className="h-8" />
        {/* ... more logos */}
      </div>
    </div>
  </div>
</section>
```

---

### 4. Features Grid

```tsx
<section className="py-24">
  <div className="container max-w-6xl mx-auto px-6">
    {/* Section Header */}
    <div className="text-center max-w-3xl mx-auto mb-16">
      <h2 className="text-3xl md:text-4xl font-bold text-text-primary mb-4">
        Everything you need to automate
      </h2>
      <p className="text-lg text-text-secondary">
        Powerful features designed for modern automation workflows
      </p>
    </div>

    {/* Feature Grid */}
    <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
      <FeatureCard
        icon={<Zap className="w-6 h-6" />}
        title="Visual Workflow Builder"
        description="Drag-and-drop interface to build complex automation flows without coding"
        gradient="from-violet-500/10 to-purple-500/10"
      />
      <FeatureCard
        icon={<Brain className="w-6 h-6" />}
        title="AI Agent Integration"
        description="Connect GPT-4, Claude, and custom AI models to your workflows"
        gradient="from-blue-500/10 to-cyan-500/10"
      />
      <FeatureCard
        icon={<Boxes className="w-6 h-6" />}
        title="81+ Integrations"
        description="Pre-built connectors for APIs, databases, and popular tools"
        gradient="from-green-500/10 to-emerald-500/10"
      />
      <FeatureCard
        icon={<Code className="w-6 h-6" />}
        title="Custom Code Blocks"
        description="Write JavaScript, Python, or SQL when you need full control"
        gradient="from-amber-500/10 to-orange-500/10"
      />
      <FeatureCard
        icon={<Shield className="w-6 h-6" />}
        title="Enterprise Security"
        description="SOC 2 compliant with end-to-end encryption and audit logs"
        gradient="from-red-500/10 to-pink-500/10"
      />
      <FeatureCard
        icon={<Gauge className="w-6 h-6" />}
        title="Real-time Monitoring"
        description="Track execution logs, performance metrics, and errors live"
        gradient="from-indigo-500/10 to-violet-500/10"
      />
    </div>
  </div>
</section>
```

**FeatureCard Component**:
```tsx
function FeatureCard({ icon, title, description, gradient }) {
  return (
    <Card className="group hover:shadow-lg transition-all duration-300 cursor-pointer border-border">
      <CardContent className="p-6">
        <div className={`inline-flex p-3 rounded-lg bg-gradient-to-br ${gradient} mb-4`}>
          {icon}
        </div>
        <h3 className="text-lg font-semibold text-text-primary mb-2">
          {title}
        </h3>
        <p className="text-sm text-text-secondary leading-relaxed">
          {description}
        </p>
      </CardContent>
    </Card>
  )
}
```

---

### 5. How It Works

```tsx
<section className="py-24 bg-surface-1">
  <div className="container max-w-6xl mx-auto px-6">
    <div className="text-center max-w-3xl mx-auto mb-16">
      <h2 className="text-3xl md:text-4xl font-bold text-text-primary mb-4">
        Start automating in 3 steps
      </h2>
    </div>

    <div className="grid md:grid-cols-3 gap-8 relative">
      {/* Connection lines */}
      <div className="hidden md:block absolute top-1/4 left-1/3 right-1/3 h-0.5 bg-gradient-to-r from-primary via-secondary to-primary opacity-30" />

      <StepCard
        number="01"
        title="Choose a Template"
        description="Start with pre-built workflows or create from scratch"
        icon={<FileText className="w-8 h-8" />}
      />
      <StepCard
        number="02"
        title="Connect Your Tools"
        description="Authenticate and configure your integrations"
        icon={<Link2 className="w-8 h-8" />}
      />
      <StepCard
        number="03"
        title="Deploy & Monitor"
        description="Activate your workflow and track executions in real-time"
        icon={<Rocket className="w-8 h-8" />}
      />
    </div>
  </div>
</section>
```

---

### 6. Workflow Examples

```tsx
<section className="py-24">
  <div className="container max-w-6xl mx-auto px-6">
    <div className="text-center max-w-3xl mx-auto mb-12">
      <h2 className="text-3xl md:text-4xl font-bold text-text-primary mb-4">
        Built for every use case
      </h2>
    </div>

    {/* Tabs */}
    <Tabs defaultValue="customer-support" className="w-full">
      <TabsList className="grid grid-cols-3 max-w-md mx-auto mb-8">
        <TabsTrigger value="customer-support">Support</TabsTrigger>
        <TabsTrigger value="data-processing">Data</TabsTrigger>
        <TabsTrigger value="marketing">Marketing</TabsTrigger>
      </TabsList>

      <TabsContent value="customer-support">
        <WorkflowPreview
          title="AI Customer Support Agent"
          description="Automatically respond to support tickets using GPT-4"
          nodes={['Trigger: New Ticket', 'AI Agent: Classify', 'Condition', 'Send Response']}
          screenshot="/workflows/support.png"
        />
      </TabsContent>
      {/* More tabs... */}
    </Tabs>
  </div>
</section>
```

---

### 7. Integrations Grid

```tsx
<section className="py-24 bg-surface-1">
  <div className="container max-w-6xl mx-auto px-6">
    <div className="text-center max-w-3xl mx-auto mb-12">
      <h2 className="text-3xl md:text-4xl font-bold text-text-primary mb-4">
        Connect everything
      </h2>
      <p className="text-lg text-text-secondary">
        81+ pre-built integrations and counting
      </p>
    </div>

    {/* Integration logos */}
    <div className="grid grid-cols-4 md:grid-cols-6 lg:grid-cols-8 gap-6">
      {integrations.map((integration) => (
        <div
          key={integration.id}
          className="flex items-center justify-center p-4 rounded-lg bg-bg border border-border hover:border-primary hover:shadow-md transition-all group"
        >
          <img
            src={integration.logo}
            alt={integration.name}
            className="w-10 h-10 object-contain grayscale group-hover:grayscale-0 transition-all"
          />
        </div>
      ))}
    </div>

    <div className="text-center mt-8">
      <Button variant="outline">
        View All Integrations
        <ArrowRight className="w-4 h-4 ml-2" />
      </Button>
    </div>
  </div>
</section>
```

---

### 8. Testimonials

```tsx
<section className="py-24">
  <div className="container max-w-6xl mx-auto px-6">
    <div className="text-center max-w-3xl mx-auto mb-12">
      <h2 className="text-3xl md:text-4xl font-bold text-text-primary mb-4">
        Loved by teams worldwide
      </h2>
    </div>

    {/* Testimonial Carousel */}
    <div className="grid md:grid-cols-3 gap-8">
      <TestimonialCard
        quote="Pankh AI reduced our automation time by 80%. The visual builder is incredibly intuitive."
        author="Sarah Chen"
        role="Engineering Lead"
        company="TechCorp"
        avatar="/avatars/sarah.jpg"
      />
      {/* More testimonials */}
    </div>
  </div>
</section>
```

---

### 9. Final CTA

```tsx
<section className="py-24 bg-gradient-to-br from-primary/10 via-bg to-secondary/10">
  <div className="container max-w-4xl mx-auto px-6 text-center">
    <h2 className="text-4xl md:text-5xl font-bold text-text-primary mb-6">
      Ready to automate your workflows?
    </h2>
    <p className="text-xl text-text-secondary mb-8">
      Join thousands of teams building with Pankh AI
    </p>
    <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
      <Button size="xl" variant="primary">
        Start Free Trial
      </Button>
      <Button size="xl" variant="outline">
        Talk to Sales
      </Button>
    </div>
    <p className="text-sm text-text-muted mt-6">
      No credit card required • Free forever plan available
    </p>
  </div>
</section>
```

---

### 10. Footer

```tsx
<footer className="border-t border-border bg-surface-1 py-12">
  <div className="container max-w-6xl mx-auto px-6">
    <div className="grid grid-cols-2 md:grid-cols-4 gap-8 mb-8">
      <div>
        <h4 className="font-semibold text-text-primary mb-4">Product</h4>
        <ul className="space-y-2 text-sm text-text-secondary">
          <li><Link href="/features">Features</Link></li>
          <li><Link href="/integrations">Integrations</Link></li>
          <li><Link href="/pricing">Pricing</Link></li>
          <li><Link href="/changelog">Changelog</Link></li>
        </ul>
      </div>
      <div>
        <h4 className="font-semibold text-text-primary mb-4">Resources</h4>
        <ul className="space-y-2 text-sm text-text-secondary">
          <li><Link href="/docs">Documentation</Link></li>
          <li><Link href="/templates">Templates</Link></li>
          <li><Link href="/blog">Blog</Link></li>
          <li><Link href="/support">Support</Link></li>
        </ul>
      </div>
      <div>
        <h4 className="font-semibold text-text-primary mb-4">Company</h4>
        <ul className="space-y-2 text-sm text-text-secondary">
          <li><Link href="/about">About</Link></li>
          <li><Link href="/careers">Careers</Link></li>
          <li><Link href="/contact">Contact</Link></li>
        </ul>
      </div>
      <div>
        <h4 className="font-semibold text-text-primary mb-4">Legal</h4>
        <ul className="space-y-2 text-sm text-text-secondary">
          <li><Link href="/privacy">Privacy</Link></li>
          <li><Link href="/terms">Terms</Link></li>
          <li><Link href="/security">Security</Link></li>
        </ul>
      </div>
    </div>

    <div className="flex flex-col md:flex-row items-center justify-between pt-8 border-t border-border">
      <p className="text-sm text-text-muted">
        © 2025 Pankh AI. All rights reserved.
      </p>
      <div className="flex items-center gap-4 mt-4 md:mt-0">
        <Link href="https://twitter.com" className="text-text-muted hover:text-text-primary">
          <Twitter className="w-5 h-5" />
        </Link>
        <Link href="https://github.com" className="text-text-muted hover:text-text-primary">
          <Github className="w-5 h-5" />
        </Link>
        <Link href="https://linkedin.com" className="text-text-muted hover:text-text-primary">
          <Linkedin className="w-5 h-5" />
        </Link>
      </div>
    </div>
  </div>
</footer>
```

---

## 🎨 Design Tokens Used

**Colors**:
- Primary gradient: from-primary to-secondary
- Background layers: bg, surface-1, surface-2
- Text hierarchy: text-primary, text-secondary, text-muted
- Borders: border-border

**Spacing**:
- Section padding: py-20 md:py-32 (hero), py-24 (standard)
- Container: max-w-6xl mx-auto px-6
- Card gaps: gap-8
- Element spacing: space-y-6

**Typography**:
- Hero H1: text-5xl md:text-6xl lg:text-7xl
- Section H2: text-3xl md:text-4xl
- Body: text-lg, text-xl
- Small: text-sm

**Shadows**:
- Cards: shadow-sm, hover:shadow-lg
- Hero image: shadow-2xl
- Buttons: shadow-sm (primary variant)

---

## ♿ Accessibility

- [ ] All images have descriptive alt text
- [ ] Proper heading hierarchy (h1 → h2 → h3)
- [ ] Focus states on all interactive elements
- [ ] ARIA labels on icon-only buttons
- [ ] Skip to content link for keyboard users
- [ ] Color contrast meets WCAG 2.2 AA standards

---

## 📱 Responsive Breakpoints

- **Mobile** (< 640px): Single column, stacked CTAs
- **Tablet** (640px - 1024px): 2-column grids, side-by-side CTAs
- **Desktop** (> 1024px): Full 3-column grids, max-width constraints

---

## ✨ Interactions

- **Scroll animations**: Fade-in-up for sections (Framer Motion)
- **Parallax**: Subtle background movement on hero
- **Hover effects**: Scale 1.05 on feature cards
- **Smooth scroll**: Anchor links with smooth behavior
- **Lazy loading**: Images load on viewport entry

---

**Implementation File**: `/apps/sim/app/(landing)/landing.tsx`
