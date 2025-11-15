# Workspace Shell Design

> **Route**: `/workspace/:workspaceId/*`
> **Type**: Application shell layout
> **Goal**: Consistent navigation and workspace management

---

## 🎯 Layout Overview

```
┌──────────────────────────────────────────────────────────────────┐
│  ┌────────┐  TOPBAR                                              │
│  │        │  Breadcrumbs • Search (⌘K) • Notifications • User   │
├──┤ SIDE   ├──────────────────────────────────────────────────────┤
│  │ BAR    │                                                      │
│  │        │                                                      │
│  │ • WS   │         PAGE CONTENT                                 │
│  │ • 🔍   │         (Dynamic based on route)                     │
│  │        │                                                      │
│  │ Wflow  │                                                      │
│  │ ├─ F1  │                                                      │
│  │ ├─ W1  │                                                      │
│  │ └─ W2  │                                                      │
│  │        │                                                      │
│  │ ------  │                                                      │
│  │ 📊 Logs │                                                      │
│  │ 📑 Tmpl │                                                      │
│  │ 📚 Know │                                                      │
│  │ ⚙️  Set │                                                      │
│  └────────┘                                                      │
└──────────────────────────────────────────────────────────────────┘
```

**Dimensions**:
- Sidebar: 280px (collapsed: 64px)
- Topbar: 56px height
- Content: flex-1

---

## 🧩 Component Breakdown

### 1. Workspace Sidebar

```tsx
// components/workspace/sidebar.tsx
export function WorkspaceSidebar() {
  const [isCollapsed, setIsCollapsed] = useState(false)
  const { workspaceId } = useParams()

  return (
    <aside
      className={cn(
        'flex flex-col h-screen border-r border-border bg-surface-1',
        'transition-all duration-200',
        isCollapsed ? 'w-16' : 'w-[280px]'
      )}
    >
      {/* Workspace Header */}
      <div className="h-14 px-4 flex items-center justify-between border-b border-border">
        {!isCollapsed && (
          <WorkspaceSwitcher workspaceId={workspaceId} />
        )}
        <Button
          variant="ghost"
          size="xs"
          onClick={() => setIsCollapsed(!isCollapsed)}
        >
          {isCollapsed ? (
            <ChevronsRight className="w-4 h-4" />
          ) : (
            <ChevronsLeft className="w-4 h-4" />
          )}
        </Button>
      </div>

      {/* Search */}
      <div className="p-3 border-b border-border">
        {isCollapsed ? (
          <Button
            variant="ghost"
            size="sm"
            className="w-full"
            onClick={openSearch}
          >
            <Search className="w-4 h-4" />
          </Button>
        ) : (
          <Button
            variant="ghost"
            className="w-full justify-start text-text-muted"
            onClick={openSearch}
          >
            <Search className="w-4 h-4 mr-2" />
            Search...
            <kbd className="ml-auto text-xs">⌘K</kbd>
          </Button>
        )}
      </div>

      {/* Workflows Section */}
      <div className="flex-1 overflow-y-auto p-3">
        <div className="space-y-1">
          {!isCollapsed && (
            <div className="flex items-center justify-between px-3 py-1">
              <span className="text-xs font-semibold text-text-muted uppercase tracking-wider">
                Workflows
              </span>
              <Button
                variant="ghost"
                size="xs"
                onClick={createWorkflow}
              >
                <Plus className="w-3 h-3" />
              </Button>
            </div>
          )}

          <WorkflowTree
            workspaceId={workspaceId}
            collapsed={isCollapsed}
          />
        </div>
      </div>

      {/* Usage Indicator (if billing enabled) */}
      {!isCollapsed && (
        <div className="px-3 py-2 border-t border-border">
          <UsageIndicator />
        </div>
      )}

      {/* Bottom Navigation */}
      <div className="border-t border-border p-2">
        <nav className="space-y-1">
          <SidebarLink
            href={`/workspace/${workspaceId}/logs`}
            icon={<ScrollText className="w-4 h-4" />}
            label="Logs"
            collapsed={isCollapsed}
          />
          <SidebarLink
            href={`/workspace/${workspaceId}/templates`}
            icon={<FileText className="w-4 h-4" />}
            label="Templates"
            collapsed={isCollapsed}
          />
          <SidebarLink
            href={`/workspace/${workspaceId}/knowledge`}
            icon={<Database className="w-4 h-4" />}
            label="Knowledge"
            collapsed={isCollapsed}
          />
          <Button
            variant="ghost"
            className={cn(
              'w-full',
              isCollapsed ? 'justify-center' : 'justify-start'
            )}
            onClick={openSettings}
          >
            <Settings className="w-4 h-4" />
            {!isCollapsed && <span className="ml-2">Settings</span>}
          </Button>
        </nav>
      </div>
    </aside>
  )
}
```

---

### 2. Workspace Switcher

```tsx
function WorkspaceSwitcher({ workspaceId }) {
  const workspaces = useWorkspaces()
  const currentWorkspace = workspaces.find((w) => w.id === workspaceId)

  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button variant="ghost" className="w-full justify-between px-2">
          <div className="flex items-center gap-2 overflow-hidden">
            <div className="w-8 h-8 rounded-lg bg-primary flex items-center justify-center shrink-0">
              <span className="text-white font-semibold text-sm">
                {currentWorkspace?.name?.[0] || 'W'}
              </span>
            </div>
            <div className="flex-1 text-left overflow-hidden">
              <p className="text-sm font-medium text-text-primary truncate">
                {currentWorkspace?.name}
              </p>
              <p className="text-xs text-text-muted">
                {currentWorkspace?.plan || 'Free'}
              </p>
            </div>
          </div>
          <ChevronsUpDown className="w-4 h-4 text-text-muted" />
        </Button>
      </DropdownMenuTrigger>

      <DropdownMenuContent align="start" className="w-64">
        <DropdownMenuLabel>Workspaces</DropdownMenuLabel>
        <DropdownMenuSeparator />
        {workspaces.map((workspace) => (
          <DropdownMenuItem
            key={workspace.id}
            onClick={() => navigate(`/workspace/${workspace.id}/w`)}
          >
            <div className="flex items-center gap-2">
              <div className="w-6 h-6 rounded bg-primary flex items-center justify-center">
                <span className="text-white text-xs font-semibold">
                  {workspace.name[0]}
                </span>
              </div>
              <span>{workspace.name}</span>
            </div>
            {workspace.id === workspaceId && (
              <Check className="w-4 h-4 ml-auto" />
            )}
          </DropdownMenuItem>
        ))}
        <DropdownMenuSeparator />
        <DropdownMenuItem onClick={createWorkspace}>
          <Plus className="w-4 h-4 mr-2" />
          Create Workspace
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  )
}
```

---

### 3. Workflow Tree

```tsx
function WorkflowTree({ workspaceId, collapsed }) {
  const { folders, workflows } = useWorkflows(workspaceId)

  if (collapsed) {
    return workflows.slice(0, 5).map((workflow) => (
      <Tooltip key={workflow.id} content={workflow.name}>
        <Button
          variant="ghost"
          size="sm"
          className="w-full justify-center"
          asChild
        >
          <Link href={`/workspace/${workspaceId}/w/${workflow.id}`}>
            <Zap className="w-4 h-4" />
          </Link>
        </Button>
      </Tooltip>
    ))
  }

  return (
    <div className="space-y-0.5">
      {folders.map((folder) => (
        <FolderItem key={folder.id} folder={folder} workspaceId={workspaceId} />
      ))}
      {workflows
        .filter((w) => !w.folderId)
        .map((workflow) => (
          <WorkflowItem
            key={workflow.id}
            workflow={workflow}
            workspaceId={workspaceId}
          />
        ))}
    </div>
  )
}

function WorkflowItem({ workflow, workspaceId }) {
  const pathname = usePathname()
  const isActive = pathname.includes(workflow.id)

  return (
    <Link
      href={`/workspace/${workspaceId}/w/${workflow.id}`}
      className={cn(
        'flex items-center gap-2 px-3 py-2 rounded-lg',
        'text-sm text-text-secondary',
        'hover:bg-surface-2 hover:text-text-primary',
        'transition-colors group',
        isActive && 'bg-surface-3 text-text-primary font-medium'
      )}
    >
      <Zap className="w-4 h-4 shrink-0" />
      <span className="flex-1 truncate">{workflow.name}</span>
      <DropdownMenu>
        <DropdownMenuTrigger asChild>
          <Button
            variant="ghost"
            size="xs"
            className="opacity-0 group-hover:opacity-100"
            onClick={(e) => e.preventDefault()}
          >
            <MoreVertical className="w-3 h-3" />
          </Button>
        </DropdownMenuTrigger>
        <DropdownMenuContent>
          <DropdownMenuItem>
            <Edit className="w-4 h-4 mr-2" />
            Rename
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
    </Link>
  )
}
```

---

### 4. Topbar

```tsx
function WorkspaceTopbar() {
  const pathname = usePathname()

  return (
    <header className="h-14 border-b border-border bg-bg sticky top-0 z-40">
      <div className="h-full px-4 flex items-center justify-between">
        {/* Left: Breadcrumbs */}
        <Breadcrumbs />

        {/* Right: Actions */}
        <div className="flex items-center gap-2">
          {/* Search */}
          <Button
            variant="ghost"
            size="sm"
            onClick={openCommandPalette}
          >
            <Search className="w-4 h-4" />
          </Button>

          {/* Notifications */}
          <Popover>
            <PopoverTrigger asChild>
              <Button variant="ghost" size="sm" className="relative">
                <Bell className="w-4 h-4" />
                {hasUnread && (
                  <span className="absolute top-1 right-1 w-2 h-2 bg-error rounded-full" />
                )}
              </Button>
            </PopoverTrigger>
            <PopoverContent className="w-80 p-0" align="end">
              <NotificationsPanel />
            </PopoverContent>
          </Popover>

          {/* Help */}
          <Button variant="ghost" size="sm" onClick={openHelp}>
            <HelpCircle className="w-4 h-4" />
          </Button>

          {/* User Menu */}
          <UserMenu />
        </div>
      </div>
    </header>
  )
}
```

---

### 5. Breadcrumbs

```tsx
function Breadcrumbs() {
  const pathname = usePathname()
  const { workspaceId, workflowId } = useParams()

  const workspace = useWorkspace(workspaceId)
  const workflow = useWorkflow(workflowId)

  const segments = [
    { label: workspace?.name || 'Workspace', href: `/workspace/${workspaceId}/w` },
  ]

  if (pathname.includes('/workflows')) {
    segments.push({ label: 'Workflows', href: `/workspace/${workspaceId}/w` })
    if (workflow) {
      segments.push({
        label: workflow.name,
        href: `/workspace/${workspaceId}/w/${workflowId}`,
      })
    }
  } else if (pathname.includes('/templates')) {
    segments.push({ label: 'Templates', href: `/workspace/${workspaceId}/templates` })
  } else if (pathname.includes('/logs')) {
    segments.push({ label: 'Logs', href: `/workspace/${workspaceId}/logs` })
  } else if (pathname.includes('/knowledge')) {
    segments.push({ label: 'Knowledge', href: `/workspace/${workspaceId}/knowledge` })
  }

  return (
    <nav className="flex items-center gap-2 text-sm">
      {segments.map((segment, index) => (
        <div key={segment.href} className="flex items-center gap-2">
          {index > 0 && <ChevronRight className="w-4 h-4 text-text-muted" />}
          {index === segments.length - 1 ? (
            <span className="text-text-primary font-medium">{segment.label}</span>
          ) : (
            <Link
              href={segment.href}
              className="text-text-secondary hover:text-text-primary"
            >
              {segment.label}
            </Link>
          )}
        </div>
      ))}
    </nav>
  )
}
```

---

### 6. Command Palette (⌘K)

```tsx
function CommandPalette() {
  const [open, setOpen] = useState(false)

  useEffect(() => {
    const down = (e: KeyboardEvent) => {
      if (e.key === 'k' && (e.metaKey || e.ctrlKey)) {
        e.preventDefault()
        setOpen((open) => !open)
      }
    }
    document.addEventListener('keydown', down)
    return () => document.removeEventListener('keydown', down)
  }, [])

  return (
    <CommandDialog open={open} onOpenChange={setOpen}>
      <CommandInput placeholder="Type a command or search..." />
      <CommandList>
        <CommandEmpty>No results found.</CommandEmpty>

        <CommandGroup heading="Quick Actions">
          <CommandItem onSelect={createWorkflow}>
            <Plus className="w-4 h-4 mr-2" />
            Create Workflow
          </CommandItem>
          <CommandItem onSelect={openTemplates}>
            <FileText className="w-4 h-4 mr-2" />
            Browse Templates
          </CommandItem>
          <CommandItem onSelect={openLogs}>
            <ScrollText className="w-4 h-4 mr-2" />
            View Logs
          </CommandItem>
        </CommandGroup>

        <CommandSeparator />

        <CommandGroup heading="Recent Workflows">
          {recentWorkflows.map((workflow) => (
            <CommandItem
              key={workflow.id}
              onSelect={() => navigate(workflow.id)}
            >
              <Zap className="w-4 h-4 mr-2" />
              {workflow.name}
            </CommandItem>
          ))}
        </CommandGroup>

        <CommandSeparator />

        <CommandGroup heading="Settings">
          <CommandItem onSelect={openSettings}>
            <Settings className="w-4 h-4 mr-2" />
            Workspace Settings
          </CommandItem>
        </CommandGroup>
      </CommandList>
    </CommandDialog>
  )
}
```

---

## 🎨 Design Tokens Used

**Layout**:
- Sidebar: w-[280px] (collapsed: w-16)
- Topbar: h-14
- Content: flex-1

**Colors**:
- Sidebar: bg-surface-1, border-border
- Topbar: bg-bg, border-border
- Active item: bg-surface-3, text-text-primary

**Typography**:
- Nav items: text-sm
- Section headers: text-xs uppercase tracking-wider
- Breadcrumbs: text-sm

**Spacing**:
- Sidebar padding: p-3
- Nav items: px-3 py-2
- Topbar padding: px-4

---

## ♿ Accessibility

- [ ] Skip navigation link
- [ ] Keyboard shortcuts documented (⌘K, etc.)
- [ ] ARIA labels on icon-only buttons
- [ ] Focus trap in command palette
- [ ] Collapsible sidebar accessible via keyboard

---

## 📱 Responsive Design

**Mobile (< 1024px)**:
- Sidebar hidden by default (overlay when opened)
- Hamburger menu in topbar
- Full-width content

**Desktop (>= 1024px)**:
- Persistent sidebar
- Collapsible to icon-only mode
- Fixed layout

---

**Implementation Files**:
- `/apps/sim/app/workspace/[workspaceId]/layout.tsx`
- `/apps/sim/app/workspace/[workspaceId]/w/components/sidebar/sidebar-new.tsx`
