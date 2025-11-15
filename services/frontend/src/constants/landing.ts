import { Blocks, LineChart, Shield, Workflow } from 'lucide-react'
import type { LucideIcon } from 'lucide-react'

export type NavLink = { label: string; href: string }
export type HeroStat = { label: string; value: string; helper: string; target: number }
export type FeatureCard = {
  id: string
  title: string
  description: string
  bullets: string[]
  icon: LucideIcon
}
export type ProductShowcase = {
  id: string
  eyebrow: string
  title: string
  description: string
  highlights: string[]
  gradient: string
}
export type BlockCategory = {
  title: string
  description: string
  metrics: { label: string; value: string }[]
}
export type WorkflowStage = {
  step: number
  title: string
  description: string
  badge: string
}
export type IntegrationPartner = { name: string; href: string }
export type PricingPlan = {
  id: string
  name: string
  price: string
  description: string
  cta: string
  highlighted?: boolean
  perks: string[]
}
export type Testimonial = {
  quote: string
  author: string
  role: string
  company: string
  highlight: string
}
export type DocsCard = { title: string; description: string; cta: string; code: string }
export type FooterColumn = { title: string; links: { label: string; href: string }[] }

export const navLinks: NavLink[] = [
  { label: 'Product', href: '#product' },
  { label: 'Blocks', href: '#blocks' },
  { label: 'Workflow Builder', href: '#workflow' },
  { label: 'Gluon Observability', href: '#gluon' },
  { label: 'Pricing', href: '#pricing' },
  { label: 'Docs', href: '#docs' },
]

export const heroStats: HeroStat[] = [
  { label: 'Latency', value: '84ms', helper: 'Streaming actions', target: 84 },
  { label: 'Coverage', value: '120+', helper: 'Native integrations', target: 120 },
  { label: 'Time saved', value: '37%', helper: 'Avg ops savings', target: 37 },
]

export const featureCards: FeatureCard[] = [
  {
    id: 'why-1',
    title: 'AI-native canvas',
    description:
      'Pair LLMs, tools, and enterprise APIs inside a tactile workflow builder with version history.',
    bullets: ['Composable agents', 'Branching logic', 'Human-in-the-loop controls'],
    icon: Workflow,
  },
  {
    id: 'why-2',
    title: 'Blocks Library',
    description: 'Search, remix, and publish building blocks built by your team and the community.',
    bullets: ['Secure sharing model', 'Semantic search', 'Usage analytics'],
    icon: Blocks,
  },
  {
    id: 'why-3',
    title: 'Observability with Gluon',
    description:
      'Trace every tool call, inspect spans, and fix regressions with guardrails and live dashboards.',
    bullets: ['Replay sessions', 'Guardrail alerts', 'PII stripping'],
    icon: LineChart,
  },
  {
    id: 'why-4',
    title: 'Enterprise ready',
    description: 'SSO, fine-grained permissions, custom SLAs, and regional data residency.',
    bullets: ['SOC 2 Type II', 'SAML + SCIM', 'On-prem connectors'],
    icon: Shield,
  },
]

export const productShowcases: ProductShowcase[] = [
  {
    id: 'product-home',
    eyebrow: 'Command Center',
    title: 'One console for every agent workflow',
    description:
      'Design branching logic, schedule runs, and preview API traffic with glass dashboards that stay in sync with production.',
    highlights: ['Live runbooks', 'Adaptive rate limits', 'Schema aware prompts'],
    gradient: 'from-brand-peacock via-brand-emerald to-brand-aqua',
  },
  {
    id: 'product-blocks',
    eyebrow: 'Blocks Library',
    title: 'Curate your private AI building blocks',
    description:
      'Package prompts, tools, memory stores, and evaluators as reusable blocks with semantic tagging and approvals.',
    highlights: ['Version pinning', 'Private marketplace', 'In-line metrics'],
    gradient: 'from-brand-emerald via-brand-aqua to-brand-royal',
  },
  {
    id: 'product-observability',
    eyebrow: 'Gluon Observability',
    title: 'Production visibility from day zero',
    description:
      'Every generation, API call, and human escalation is traceable, comparable, and exportable with Gluon.',
    highlights: ['Span explorer', 'Quality gates', 'Anomaly alerts'],
    gradient: 'from-brand-royal via-brand-peacock to-brand-emerald',
  },
]

export const blockCategories: BlockCategory[] = [
  {
    title: 'Retrieval & Memory',
    description: 'Pinecone, Weaviate, Supabase, AlloyDB, S3, Azure Blob, custom embeddings',
    metrics: [
      { label: 'Latency', value: '45ms p95' },
      { label: 'Documents', value: '18M' },
    ],
  },
  {
    title: 'Automation & Ops',
    description: 'Zendesk, Linear, Jira, Salesforce, Workday, Coupa',
    metrics: [
      { label: 'Runs/day', value: '42K' },
      { label: 'Savings', value: '37%' },
    ],
  },
  {
    title: 'Creative & Studio',
    description: 'Figma, Adobe Firefly, ElevenLabs, Runway, Midjourney control',
    metrics: [
      { label: 'Assets', value: '3.2M' },
      { label: 'Reviews', value: '1.1K' },
    ],
  },
  {
    title: 'Security & Trust',
    description: 'Okta, Azure AD, Duo, custom policy engines, human approvals',
    metrics: [
      { label: 'Approvals', value: '99.7%' },
      { label: 'Incidents', value: '0 critical' },
    ],
  },
]

export const workflowStages: WorkflowStage[] = [
  {
    step: 1,
    title: 'Model Orchestration',
    description: 'Blend GPT-4.1, Claude, Krutrim, and fine-tuned mini models with fallback logic.',
    badge: 'Multi-LLM mesh',
  },
  {
    step: 2,
    title: 'Tool + API Calls',
    description: 'Securely inject keys, throttle requests, and log structured responses.',
    badge: 'Safe actions',
  },
  {
    step: 3,
    title: 'Human Review',
    description: 'Escalate edge cases to reviewers with context-rich sidecars and auto-summaries.',
    badge: 'Featherlight inbox',
  },
  {
    step: 4,
    title: 'Gluon Analytics',
    description: 'Trace anomalies, compare cohorts, and feed evals back into training.',
    badge: 'Adaptive learning',
  },
]

export const integrationPartners: IntegrationPartner[] = [
  { name: 'Slack', href: '#' },
  { name: 'Gmail', href: '#' },
  { name: 'Outlook', href: '#' },
  { name: 'Pinecone', href: '#' },
  { name: 'Notion', href: '#' },
  { name: 'Stripe', href: '#' },
  { name: 'Jira', href: '#' },
  { name: 'Linear', href: '#' },
  { name: 'Discord', href: '#' },
  { name: 'Supabase', href: '#' },
  { name: 'Airtable', href: '#' },
  { name: 'Zendesk', href: '#' },
]

export const pricingPlans: PricingPlan[] = [
  {
    id: 'starter',
    name: 'Feather',
    price: '$69',
    description: 'Launch your first AI agents with collaborative tooling.',
    cta: 'Start free',
    perks: ['3 workspaces', '50K workflow runs', '75 blocks', 'Community support'],
  },
  {
    id: 'growth',
    name: 'Flight',
    price: '$249',
    description: 'Scale teams with observability, RBAC, and premium integrations.',
    cta: 'Talk to sales',
    highlighted: true,
    perks: [
      'Unlimited workspaces',
      'Priority pipelines',
      'Gluon observability',
      'SOC 2 & regional hosting',
    ],
  },
  {
    id: 'enterprise',
    name: 'Constellation',
    price: 'Custom',
    description: 'White-glove support, air-gapped deployments, and co-build sprints.',
    cta: 'Book a call',
    perks: ['Dedicated TAM', 'Private block registry', 'Custom SLAs', 'On-prem connectors'],
  },
]

export const testimonials: Testimonial[] = [
  {
    quote:
      'Pankh AI is the first platform that let our data science and GTM teams compose agents together. Shipping RAG experiences now feels like live prototyping.',
    author: 'Sonal Arora',
    role: 'Head of Product Automation',
    company: 'Nirvana Health',
    highlight: '+28 point CSAT',
  },
  {
    quote:
      'We replaced six brittle workflows with one adaptive mesh inside Pankh. Gluon saved us days of debugging every sprint.',
    author: 'Felix Ortega',
    role: 'VP Engineering',
    company: 'Northwind Systems',
    highlight: '42k automated ops',
  },
  {
    quote:
      'Blocks Library turned our best automations into a curated marketplace. The governance model is perfect for enterprise teams.',
    author: 'Kim Wei',
    role: 'Director of Strategy',
    company: 'Aravalli Finance',
    highlight: '14 countries onboarded',
  },
]

export const docsCards: DocsCard[] = [
  {
    title: 'Getting started',
    description: 'Spin up your workspace, invite teams, and deploy your first agent in 10 minutes.',
    cta: 'Read guide',
    code: `sim init
sim connect slack --scopes=write
sim deploy workflow.yml`,
  },
  {
    title: 'Blocks SDK',
    description: 'Author secure custom tools with TypeScript or Python. Publish to private registries.',
    cta: 'View SDK',
    code: `import { defineBlock } from '@pankh/sdk'

export const sentiment = defineBlock({
  input: z.object({ message: z.string() }),
  async run({ input, llm }) {
    return llm.classify(input.message, { labels: ['pos','neg','neutral'] })
  }
})`,
  },
]

export const footerColumns: FooterColumn[] = [
  {
    title: 'Product',
    links: [
      { label: 'Why Pankh', href: '#why' },
      { label: 'Workflow Builder', href: '#workflow' },
      { label: 'Blocks Library', href: '#blocks' },
      { label: 'Gluon Observability', href: '#gluon' },
    ],
  },
  {
    title: 'Resources',
    links: [
      { label: 'Docs', href: '#docs' },
      { label: 'Templates', href: '#product' },
      { label: 'Status', href: '#' },
      { label: 'Security', href: '#' },
    ],
  },
  {
    title: 'Company',
    links: [
      { label: 'About', href: '#' },
      { label: 'Blog', href: '#' },
      { label: 'Careers', href: '#' },
      { label: 'Contact', href: '#' },
    ],
  },
  {
    title: 'Legal',
    links: [
      { label: 'Privacy', href: '/privacy' },
      { label: 'Terms', href: '/terms' },
      { label: 'GDPR', href: '#' },
    ],
  },
]
