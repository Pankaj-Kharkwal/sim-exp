# Component Library Specification

> **Enterprise-Grade Component System for AI Automation Platform**
> Built with Tailwind CSS + ShadCN UI + Radix UI
> Version 2.0 | Updated: 2025-11-15

---

## 🔘 Buttons

### Variants

#### 1. Primary Button
**Usage**: Main CTAs, primary actions, workflow execution

```tsx
<Button variant="primary" size="md">
  Run Workflow
</Button>
```

**Styles**:
```css
.btn-primary {
  @apply h-10 px-4 rounded-lg;
  @apply bg-primary text-white;
  @apply hover:bg-primary-hover;
  @apply active:bg-primary-active;
  @apply disabled:opacity-50 disabled:cursor-not-allowed;
  @apply transition-colors duration-150;
  @apply font-medium text-sm;
  @apply shadow-sm;
}

.btn-primary:focus-visible {
  @apply outline-none ring-2 ring-primary ring-offset-2;
}
```

#### 2. Secondary Button
**Usage**: Secondary actions, cancellations

```tsx
<Button variant="secondary" size="md">
  Cancel
</Button>
```

**Styles**:
```css
.btn-secondary {
  @apply h-10 px-4 rounded-lg;
  @apply bg-surface-3 text-text-primary;
  @apply hover:bg-surface-4;
  @apply active:bg-surface-5;
  @apply border border-border;
  @apply transition-colors duration-150;
  @apply font-medium text-sm;
}
```

#### 3. Outline Button
**Usage**: Tertiary actions, filters, toggles

```tsx
<Button variant="outline" size="md">
  <Filter className="w-4 h-4 mr-2" />
  Filter
</Button>
```

**Styles**:
```css
.btn-outline {
  @apply h-10 px-4 rounded-lg;
  @apply bg-transparent text-text-primary;
  @apply border border-border;
  @apply hover:bg-surface-2;
  @apply active:bg-surface-3;
  @apply transition-colors duration-150;
  @apply font-medium text-sm;
}
```

#### 4. Ghost Button
**Usage**: Icon buttons, subtle actions, table row actions

```tsx
<Button variant="ghost" size="sm">
  <MoreHorizontal className="w-4 h-4" />
</Button>
```

**Styles**:
```css
.btn-ghost {
  @apply h-8 px-2 rounded-lg;
  @apply bg-transparent text-text-secondary;
  @apply hover:bg-surface-2 hover:text-text-primary;
  @apply active:bg-surface-3;
  @apply transition-colors duration-150;
}
```

#### 5. Destructive Button
**Usage**: Delete, remove, dangerous actions

```tsx
<Button variant="destructive" size="md">
  <Trash2 className="w-4 h-4 mr-2" />
  Delete Workflow
</Button>
```

**Styles**:
```css
.btn-destructive {
  @apply h-10 px-4 rounded-lg;
  @apply bg-error text-white;
  @apply hover:bg-red-600;
  @apply active:bg-red-700;
  @apply transition-colors duration-150;
  @apply font-medium text-sm;
}
```

### Sizes

```tsx
const buttonSizes = {
  xs: 'h-7 px-2 text-xs',       // Tiny actions, badges
  sm: 'h-8 px-3 text-sm',       // Compact UI, table actions
  md: 'h-10 px-4 text-sm',      // Default size
  lg: 'h-11 px-5 text-base',    // Prominent actions
  xl: 'h-12 px-6 text-base',    // Hero CTAs
}
```

### States

```tsx
// Loading state
<Button disabled>
  <Loader2 className="w-4 h-4 mr-2 animate-spin" />
  Processing...
</Button>

// Icon-only
<Button size="sm" variant="ghost">
  <Settings className="w-4 h-4" />
</Button>

// With icon
<Button>
  <Play className="w-4 h-4 mr-2" />
  Run
</Button>
```

### Full Component Code

```tsx
// components/ui/button.tsx
import { cva, type VariantProps } from 'class-variance-authority'
import { cn } from '@/lib/utils'
import { forwardRef } from 'react'

const buttonVariants = cva(
  'inline-flex items-center justify-center rounded-lg font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 disabled:opacity-50 disabled:pointer-events-none',
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

interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {}

const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, ...props }, ref) => {
    return (
      <button
        className={cn(buttonVariants({ variant, size, className }))}
        ref={ref}
        {...props}
      />
    )
  }
)

export { Button, buttonVariants }
```

---

## 📥 Inputs

### Text Input

```tsx
<Input
  type="text"
  placeholder="Enter workflow name..."
  label="Workflow Name"
/>
```

**Styles**:
```css
.input {
  @apply h-10 w-full rounded-lg;
  @apply px-3 py-2 text-sm;
  @apply bg-bg border border-border;
  @apply text-text-primary placeholder:text-text-muted;
  @apply focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent;
  @apply disabled:opacity-50 disabled:cursor-not-allowed;
  @apply transition-all duration-150;
}

.input-error {
  @apply border-error focus:ring-error;
}

.input-success {
  @apply border-success focus:ring-success;
}
```

### Full Input Component

```tsx
// components/ui/input.tsx
import { forwardRef } from 'react'
import { cn } from '@/lib/utils'

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string
  error?: string
  helperText?: string
}

const Input = forwardRef<HTMLInputElement, InputProps>(
  ({ className, label, error, helperText, ...props }, ref) => {
    return (
      <div className="w-full space-y-1.5">
        {label && (
          <label className="text-sm font-medium text-text-primary">
            {label}
          </label>
        )}
        <input
          className={cn(
            'flex h-10 w-full rounded-lg border border-border bg-bg px-3 py-2 text-sm',
            'placeholder:text-text-muted',
            'focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent',
            'disabled:cursor-not-allowed disabled:opacity-50',
            'transition-all duration-150',
            error && 'border-error focus:ring-error',
            className
          )}
          ref={ref}
          {...props}
        />
        {error && (
          <p className="text-xs text-error">{error}</p>
        )}
        {helperText && !error && (
          <p className="text-xs text-text-muted">{helperText}</p>
        )}
      </div>
    )
  }
)

export { Input }
```

### Textarea

```tsx
<Textarea
  placeholder="Enter description..."
  rows={4}
  label="Description"
/>
```

```tsx
// components/ui/textarea.tsx
const Textarea = forwardRef<HTMLTextAreaElement, TextareaProps>(
  ({ className, label, error, helperText, ...props }, ref) => {
    return (
      <div className="w-full space-y-1.5">
        {label && (
          <label className="text-sm font-medium text-text-primary">
            {label}
          </label>
        )}
        <textarea
          className={cn(
            'flex min-h-[80px] w-full rounded-lg border border-border bg-bg px-3 py-2 text-sm',
            'placeholder:text-text-muted',
            'focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent',
            'disabled:cursor-not-allowed disabled:opacity-50',
            'transition-all duration-150 resize-none',
            error && 'border-error focus:ring-error',
            className
          )}
          ref={ref}
          {...props}
        />
        {error && (
          <p className="text-xs text-error">{error}</p>
        )}
        {helperText && !error && (
          <p className="text-xs text-text-muted">{helperText}</p>
        )}
      </div>
    )
  }
)
```

---

## 🃏 Cards

### Basic Card

```tsx
<Card>
  <CardHeader>
    <CardTitle>Workflow Statistics</CardTitle>
    <CardDescription>Your workflow performance overview</CardDescription>
  </CardHeader>
  <CardContent>
    {/* Content here */}
  </CardContent>
  <CardFooter>
    <Button variant="outline">View Details</Button>
  </CardFooter>
</Card>
```

**Styles**:
```css
.card {
  @apply rounded-lg border border-border bg-surface-1 shadow-sm;
  @apply transition-all duration-150;
}

.card-hover {
  @apply hover:shadow-md hover:border-border-secondary;
  @apply cursor-pointer;
}

.card-header {
  @apply p-6 space-y-1.5;
}

.card-title {
  @apply text-xl font-semibold text-text-primary;
}

.card-description {
  @apply text-sm text-text-muted;
}

.card-content {
  @apply p-6 pt-0;
}

.card-footer {
  @apply p-6 pt-0 flex items-center gap-3;
}
```

### Full Card Component

```tsx
// components/ui/card.tsx
import { cn } from '@/lib/utils'

const Card = ({ className, ...props }: React.HTMLAttributes<HTMLDivElement>) => (
  <div
    className={cn(
      'rounded-lg border border-border bg-surface-1 shadow-sm',
      className
    )}
    {...props}
  />
)

const CardHeader = ({ className, ...props }: React.HTMLAttributes<HTMLDivElement>) => (
  <div className={cn('flex flex-col space-y-1.5 p-6', className)} {...props} />
)

const CardTitle = ({ className, ...props }: React.HTMLAttributes<HTMLHeadingElement>) => (
  <h3
    className={cn('text-xl font-semibold leading-none tracking-tight text-text-primary', className)}
    {...props}
  />
)

const CardDescription = ({ className, ...props }: React.HTMLAttributes<HTMLParagraphElement>) => (
  <p className={cn('text-sm text-text-muted', className)} {...props} />
)

const CardContent = ({ className, ...props }: React.HTMLAttributes<HTMLDivElement>) => (
  <div className={cn('p-6 pt-0', className)} {...props} />
)

const CardFooter = ({ className, ...props }: React.HTMLAttributes<HTMLDivElement>) => (
  <div className={cn('flex items-center p-6 pt-0', className)} {...props} />
)

export { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter }
```

### Workflow Card (Special)

```tsx
<WorkflowCard
  title="Customer Onboarding"
  description="Automated workflow for new customer setup"
  status="active"
  lastRun="2 hours ago"
  successRate={98.5}
  onClick={() => navigate('/workflow/123')}
/>
```

---

## 🏷️ Badges

### Variants

```tsx
// Status badges
<Badge variant="success">Active</Badge>
<Badge variant="warning">Paused</Badge>
<Badge variant="error">Failed</Badge>
<Badge variant="info">Running</Badge>
<Badge variant="default">Draft</Badge>
```

**Styles**:
```css
.badge {
  @apply inline-flex items-center px-2.5 py-0.5 rounded-md;
  @apply text-xs font-medium;
  @apply transition-colors duration-150;
}

.badge-default {
  @apply bg-surface-3 text-text-secondary border border-border;
}

.badge-success {
  @apply bg-success-bg text-green-700 border border-success-border;
}

.badge-warning {
  @apply bg-warning-bg text-amber-700 border border-warning-border;
}

.badge-error {
  @apply bg-error-bg text-red-700 border border-error-border;
}

.badge-info {
  @apply bg-info-bg text-blue-700 border border-info-border;
}

.badge-primary {
  @apply bg-primary text-white;
}
```

### Full Badge Component

```tsx
// components/ui/badge.tsx
import { cva, type VariantProps } from 'class-variance-authority'
import { cn } from '@/lib/utils'

const badgeVariants = cva(
  'inline-flex items-center rounded-md px-2.5 py-0.5 text-xs font-medium transition-colors',
  {
    variants: {
      variant: {
        default: 'bg-surface-3 text-text-secondary border border-border',
        success: 'bg-success-bg text-green-700 border border-success-border',
        warning: 'bg-warning-bg text-amber-700 border border-warning-border',
        error: 'bg-error-bg text-red-700 border border-error-border',
        info: 'bg-info-bg text-blue-700 border border-info-border',
        primary: 'bg-primary text-white',
      },
    },
    defaultVariants: {
      variant: 'default',
    },
  }
)

interface BadgeProps
  extends React.HTMLAttributes<HTMLDivElement>,
    VariantProps<typeof badgeVariants> {}

function Badge({ className, variant, ...props }: BadgeProps) {
  return <div className={cn(badgeVariants({ variant }), className)} {...props} />
}

export { Badge, badgeVariants }
```

---

## 📊 Tables

### Data Table Component

```tsx
<DataTable
  columns={workflowColumns}
  data={workflows}
  searchable
  searchPlaceholder="Search workflows..."
  sortable
  pagination
/>
```

**Table Styles**:
```css
.table-container {
  @apply w-full overflow-auto rounded-lg border border-border;
}

.table {
  @apply w-full text-sm;
}

.table-header {
  @apply bg-surface-2 border-b border-border;
}

.table-header-row {
  @apply transition-colors;
}

.table-head {
  @apply h-11 px-4 text-left align-middle font-medium text-text-secondary;
  @apply sticky top-0 bg-surface-2;
}

.table-head-sortable {
  @apply cursor-pointer select-none hover:text-text-primary;
}

.table-body {
  @apply divide-y divide-border;
}

.table-row {
  @apply transition-colors hover:bg-surface-2;
  @apply cursor-pointer;
}

.table-row-selected {
  @apply bg-surface-3;
}

.table-cell {
  @apply p-4 align-middle;
}
```

### Full DataTable Component

```tsx
// components/ui/data-table.tsx
import {
  flexRender,
  getCoreRowModel,
  getSortedRowModel,
  getFilteredRowModel,
  getPaginationRowModel,
  useReactTable,
  type ColumnDef,
} from '@tanstack/react-table'
import { Input } from './input'
import { Button } from './button'
import { ChevronLeft, ChevronRight, ChevronsLeft, ChevronsRight } from 'lucide-react'

interface DataTableProps<TData, TValue> {
  columns: ColumnDef<TData, TValue>[]
  data: TData[]
  searchable?: boolean
  searchPlaceholder?: string
  pagination?: boolean
}

export function DataTable<TData, TValue>({
  columns,
  data,
  searchable = false,
  searchPlaceholder = 'Search...',
  pagination = true,
}: DataTableProps<TData, TValue>) {
  const table = useReactTable({
    data,
    columns,
    getCoreRowModel: getCoreRowModel(),
    getSortedRowModel: getSortedRowModel(),
    getFilteredRowModel: getFilteredRowModel(),
    getPaginationRowModel: getPaginationRowModel(),
  })

  return (
    <div className="space-y-4">
      {searchable && (
        <Input
          placeholder={searchPlaceholder}
          value={(table.getColumn('name')?.getFilterValue() as string) ?? ''}
          onChange={(e) => table.getColumn('name')?.setFilterValue(e.target.value)}
          className="max-w-sm"
        />
      )}

      <div className="rounded-lg border border-border overflow-hidden">
        <table className="w-full">
          <thead className="bg-surface-2 border-b border-border">
            {table.getHeaderGroups().map((headerGroup) => (
              <tr key={headerGroup.id}>
                {headerGroup.headers.map((header) => (
                  <th
                    key={header.id}
                    className="h-11 px-4 text-left align-middle font-medium text-text-secondary text-sm"
                  >
                    {flexRender(header.column.columnDef.header, header.getContext())}
                  </th>
                ))}
              </tr>
            ))}
          </thead>
          <tbody className="divide-y divide-border">
            {table.getRowModel().rows.map((row) => (
              <tr
                key={row.id}
                className="transition-colors hover:bg-surface-2"
              >
                {row.getVisibleCells().map((cell) => (
                  <td key={cell.id} className="p-4 align-middle">
                    {flexRender(cell.column.columnDef.cell, cell.getContext())}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {pagination && (
        <div className="flex items-center justify-between">
          <div className="text-sm text-text-muted">
            {table.getFilteredSelectedRowModel().rows.length} of{' '}
            {table.getFilteredRowModel().rows.length} row(s) selected.
          </div>
          <div className="flex items-center gap-2">
            <Button
              variant="outline"
              size="sm"
              onClick={() => table.setPageIndex(0)}
              disabled={!table.getCanPreviousPage()}
            >
              <ChevronsLeft className="w-4 h-4" />
            </Button>
            <Button
              variant="outline"
              size="sm"
              onClick={() => table.previousPage()}
              disabled={!table.getCanPreviousPage()}
            >
              <ChevronLeft className="w-4 h-4" />
            </Button>
            <span className="text-sm text-text-secondary">
              Page {table.getState().pagination.pageIndex + 1} of {table.getPageCount()}
            </span>
            <Button
              variant="outline"
              size="sm"
              onClick={() => table.nextPage()}
              disabled={!table.getCanNextPage()}
            >
              <ChevronRight className="w-4 h-4" />
            </Button>
            <Button
              variant="outline"
              size="sm"
              onClick={() => table.setPageIndex(table.getPageCount() - 1)}
              disabled={!table.getCanNextPage()}
            >
              <ChevronsRight className="w-4 h-4" />
            </Button>
          </div>
        </div>
      )}
    </div>
  )
}
```

---

## 📱 Modals & Dialogs

### Standard Dialog

```tsx
<Dialog open={isOpen} onOpenChange={setIsOpen}>
  <DialogContent>
    <DialogHeader>
      <DialogTitle>Delete Workflow</DialogTitle>
      <DialogDescription>
        Are you sure you want to delete this workflow? This action cannot be undone.
      </DialogDescription>
    </DialogHeader>
    <DialogFooter>
      <Button variant="outline" onClick={() => setIsOpen(false)}>
        Cancel
      </Button>
      <Button variant="destructive" onClick={handleDelete}>
        Delete
      </Button>
    </DialogFooter>
  </DialogContent>
</Dialog>
```

**Styles**:
```css
.dialog-overlay {
  @apply fixed inset-0 z-50 bg-black/60;
  @apply data-[state=open]:animate-in data-[state=closed]:animate-out;
  @apply data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0;
}

.dialog-content {
  @apply fixed left-1/2 top-1/2 z-50 -translate-x-1/2 -translate-y-1/2;
  @apply w-full max-w-lg rounded-xl;
  @apply bg-surface-1 border border-border shadow-2xl;
  @apply data-[state=open]:animate-in data-[state=closed]:animate-out;
  @apply data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0;
  @apply data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95;
  @apply data-[state=closed]:slide-out-to-left-1/2 data-[state=closed]:slide-out-to-top-[48%];
  @apply data-[state=open]:slide-in-from-left-1/2 data-[state=open]:slide-in-from-top-[48%];
}

.dialog-header {
  @apply flex flex-col space-y-1.5 p-6;
}

.dialog-title {
  @apply text-xl font-semibold text-text-primary;
}

.dialog-description {
  @apply text-sm text-text-muted;
}

.dialog-footer {
  @apply flex justify-end gap-3 p-6 pt-0;
}
```

---

## 🎯 Dropdowns & Popovers

### Dropdown Menu

```tsx
<DropdownMenu>
  <DropdownMenuTrigger asChild>
    <Button variant="ghost" size="sm">
      <MoreHorizontal className="w-4 h-4" />
    </Button>
  </DropdownMenuTrigger>
  <DropdownMenuContent align="end">
    <DropdownMenuItem>
      <Edit className="w-4 h-4 mr-2" />
      Edit
    </DropdownMenuItem>
    <DropdownMenuItem>
      <Copy className="w-4 h-4 mr-2" />
      Duplicate
    </DropdownMenuItem>
    <DropdownMenuSeparator />
    <DropdownMenuItem className="text-error">
      <Trash2 className="w-4 h-4 mr-2" />
      Delete
    </DropdownMenuItem>
  </DropdownMenuContent>
</DropdownMenu>
```

**Styles**:
```css
.dropdown-content {
  @apply z-50 min-w-[8rem] overflow-hidden rounded-lg;
  @apply bg-surface-1 border border-border shadow-lg;
  @apply p-1;
  @apply data-[state=open]:animate-in data-[state=closed]:animate-out;
  @apply data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0;
  @apply data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95;
}

.dropdown-item {
  @apply relative flex cursor-pointer select-none items-center;
  @apply rounded-md px-2 py-1.5 text-sm;
  @apply text-text-primary;
  @apply hover:bg-surface-3;
  @apply focus:bg-surface-3 focus:outline-none;
  @apply transition-colors duration-100;
}

.dropdown-separator {
  @apply -mx-1 my-1 h-px bg-border;
}
```

---

## 🔔 Notifications & Toasts

### Toast Component

```tsx
// Show toast
toast({
  title: 'Workflow Created',
  description: 'Your workflow has been created successfully.',
  variant: 'success',
})

// Error toast
toast({
  title: 'Error',
  description: 'Failed to create workflow. Please try again.',
  variant: 'error',
})
```

**Styles**:
```css
.toast {
  @apply flex w-full max-w-md items-start gap-3;
  @apply rounded-lg border border-border bg-surface-1 p-4 shadow-lg;
  @apply data-[state=open]:animate-in data-[state=closed]:animate-out;
  @apply data-[state=closed]:fade-out-80 data-[state=open]:fade-in-0;
  @apply data-[state=closed]:slide-out-to-right-full data-[state=open]:slide-in-from-right-full;
}

.toast-success {
  @apply border-success-border bg-success-bg;
}

.toast-error {
  @apply border-error-border bg-error-bg;
}

.toast-warning {
  @apply border-warning-border bg-warning-bg;
}
```

---

## 🧭 Navigation Components

### Sidebar

```tsx
<Sidebar>
  <SidebarHeader>
    <WorkspaceSwitcher />
    <SearchButton />
  </SidebarHeader>

  <SidebarContent>
    <SidebarSection title="Workflows">
      <SidebarItem icon={Zap} label="All Workflows" href="/workflows" />
      <SidebarItem icon={Folder} label="My Folder" href="/folder/123" />
    </SidebarSection>
  </SidebarContent>

  <SidebarFooter>
    <SidebarItem icon={Settings} label="Settings" onClick={openSettings} />
  </SidebarFooter>
</Sidebar>
```

**Styles**:
```css
.sidebar {
  @apply flex h-screen w-64 flex-col;
  @apply bg-surface-1 border-r border-border;
}

.sidebar-header {
  @apply flex flex-col gap-3 p-4 border-b border-border;
}

.sidebar-content {
  @apply flex-1 overflow-y-auto p-4 space-y-6;
}

.sidebar-section-title {
  @apply px-3 py-2 text-xs font-semibold text-text-muted uppercase tracking-wider;
}

.sidebar-item {
  @apply flex items-center gap-3 px-3 py-2 rounded-lg;
  @apply text-sm text-text-secondary;
  @apply hover:bg-surface-3 hover:text-text-primary;
  @apply transition-colors duration-150;
  @apply cursor-pointer;
}

.sidebar-item-active {
  @apply bg-surface-3 text-text-primary font-medium;
}

.sidebar-footer {
  @apply p-4 border-t border-border;
}
```

### Breadcrumbs

```tsx
<Breadcrumbs>
  <BreadcrumbItem href="/workspace/123">Workspace</BreadcrumbItem>
  <BreadcrumbSeparator />
  <BreadcrumbItem href="/workspace/123/workflows">Workflows</BreadcrumbItem>
  <BreadcrumbSeparator />
  <BreadcrumbItem active>Customer Onboarding</BreadcrumbItem>
</Breadcrumbs>
```

---

## 📈 Charts & Data Visualization

### Recommended Library: Recharts

```tsx
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'

<ResponsiveContainer width="100%" height={300}>
  <LineChart data={executionData}>
    <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" />
    <XAxis
      dataKey="date"
      stroke="var(--text-muted)"
      style={{ fontSize: 12 }}
    />
    <YAxis
      stroke="var(--text-muted)"
      style={{ fontSize: 12 }}
    />
    <Tooltip
      contentStyle={{
        backgroundColor: 'var(--surface-2)',
        border: '1px solid var(--border)',
        borderRadius: '8px',
        padding: '12px',
      }}
    />
    <Line
      type="monotone"
      dataKey="executions"
      stroke="var(--primary)"
      strokeWidth={2}
      dot={{ fill: 'var(--primary)', r: 4 }}
    />
  </LineChart>
</ResponsiveContainer>
```

---

## 🎨 Workflow Node Components

### Node Card

```tsx
<WorkflowNode
  type="agent"
  title="OpenAI Agent"
  description="GPT-4 powered AI agent"
  status="active"
  connections={{ inputs: 1, outputs: 2 }}
/>
```

**Styles**:
```css
.workflow-node {
  @apply min-w-[240px] rounded-lg;
  @apply bg-surface-1 border-2 border-border;
  @apply shadow-sm hover:shadow-md;
  @apply transition-all duration-150;
}

.workflow-node-selected {
  @apply border-primary shadow-lg ring-2 ring-primary/20;
}

.workflow-node-header {
  @apply flex items-center gap-2 px-4 py-3;
  @apply border-b border-border;
  @apply bg-gradient-to-r;
}

.workflow-node-agent {
  @apply from-violet-500/10 to-purple-500/10;
  @apply border-l-4 border-l-violet-500;
}

.workflow-node-api {
  @apply from-blue-500/10 to-cyan-500/10;
  @apply border-l-4 border-l-blue-500;
}

.workflow-node-body {
  @apply p-4 space-y-2;
}

.workflow-node-port {
  @apply absolute w-3 h-3 rounded-full;
  @apply border-2 border-surface-1 bg-primary;
  @apply hover:scale-125 transition-transform;
}
```

---

## 🔍 Search & Command Palette

### Command Palette (⌘K)

```tsx
<CommandDialog open={open} onOpenChange={setOpen}>
  <CommandInput placeholder="Type a command or search..." />
  <CommandList>
    <CommandEmpty>No results found.</CommandEmpty>
    <CommandGroup heading="Quick Actions">
      <CommandItem onSelect={() => createWorkflow()}>
        <Plus className="w-4 h-4 mr-2" />
        Create Workflow
      </CommandItem>
      <CommandItem onSelect={() => openTemplates()}>
        <FileText className="w-4 h-4 mr-2" />
        Browse Templates
      </CommandItem>
    </CommandGroup>
    <CommandSeparator />
    <CommandGroup heading="Recent Workflows">
      {recentWorkflows.map((workflow) => (
        <CommandItem key={workflow.id} onSelect={() => navigate(workflow.id)}>
          <Zap className="w-4 h-4 mr-2" />
          {workflow.name}
        </CommandItem>
      ))}
    </CommandGroup>
  </CommandList>
</CommandDialog>
```

---

## ✅ Implementation Checklist

- [ ] Install ShadCN UI components: `npx shadcn-ui@latest add button input card badge table dialog dropdown-menu toast`
- [ ] Create custom component variants with CVA
- [ ] Set up Radix UI primitives for advanced interactions
- [ ] Implement data table with TanStack Table
- [ ] Create workflow node components with ReactFlow
- [ ] Set up toast notification system
- [ ] Implement command palette with ⌘K shortcut
- [ ] Test all components in light and dark modes
- [ ] Verify accessibility (keyboard navigation, ARIA labels)
- [ ] Document component usage in Storybook

---

**Next Steps**: Proceed to **03-page-designs/** folder for individual page specifications.
