# Workspace Child Pages

> **Parent**: `/workspace/:workspaceId/*`
> **Pages**: Home, Workflows List, Templates, Tools, Knowledge, Logs, Settings

---

## 📑 Page 1: Workflows List Page

**Route**: `/workspace/:workspaceId/w`

### Layout

```
┌──────────────────────────────────────────────────────────────────┐
│  HEADER                                                          │
│  ┌───────────────────┐  [View: Grid/List]  [Sort]  [Filter]    │
│  │ Search workflows  │                                           │
│  └───────────────────────────────────────────────── [+ New]     │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  WORKFLOWS GRID                                                  │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐                │
│  │ Workflow 1 │  │ Workflow 2 │  │ Workflow 3 │                │
│  │            │  │            │  │            │                │
│  │ [Active]   │  │ [Paused]   │  │ [Draft]    │                │
│  │ 98% ✓      │  │ 85% ✓      │  │ --         │                │
│  └────────────┘  └────────────┘  └────────────┘                │
│                                                                  │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐                │
│  │ Workflow 4 │  │ + Create   │  │            │                │
│  └────────────┘  └────────────┘  └────────────┘                │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### Implementation

```tsx
// app/workspace/[workspaceId]/w/page.tsx
export default function WorkflowsListPage() {
  const [view, setView] = useState<'grid' | 'list'>('grid')
  const [searchQuery, setSearchQuery] = useState('')
  const { workflows, folders } = useWorkflows()

  return (
    <div className="h-full flex flex-col">
      {/* Header */}
      <div className="p-6 border-b border-border bg-bg">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h1 className="text-2xl font-bold text-text-primary">Workflows</h1>
            <p className="text-sm text-text-secondary mt-1">
              Manage and monitor your automation workflows
            </p>
          </div>
          <Button variant="primary" onClick={createWorkflow}>
            <Plus className="w-4 h-4 mr-2" />
            New Workflow
          </Button>
        </div>

        <div className="flex items-center gap-3">
          {/* Search */}
          <div className="flex-1 max-w-md">
            <Input
              type="search"
              placeholder="Search workflows..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full"
            />
          </div>

          {/* View Toggle */}
          <div className="flex items-center gap-1 p-1 bg-surface-2 rounded-lg">
            <Button
              variant={view === 'grid' ? 'secondary' : 'ghost'}
              size="sm"
              onClick={() => setView('grid')}
            >
              <LayoutGrid className="w-4 h-4" />
            </Button>
            <Button
              variant={view === 'list' ? 'secondary' : 'ghost'}
              size="sm"
              onClick={() => setView('list')}
            >
              <List className="w-4 h-4" />
            </Button>
          </div>

          {/* Sort */}
          <Select value={sortBy} onValueChange={setSortBy}>
            <SelectTrigger className="w-[180px]">
              <SelectValue placeholder="Sort by..." />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="updated">Last Updated</SelectItem>
              <SelectItem value="name">Name</SelectItem>
              <SelectItem value="created">Date Created</SelectItem>
              <SelectItem value="executions">Most Runs</SelectItem>
            </SelectContent>
          </Select>

          {/* Filter */}
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="outline">
                <Filter className="w-4 h-4 mr-2" />
                Filter
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end" className="w-56">
              <DropdownMenuLabel>Status</DropdownMenuLabel>
              <DropdownMenuCheckboxItem checked>
                Active
              </DropdownMenuCheckboxItem>
              <DropdownMenuCheckboxItem>
                Paused
              </DropdownMenuCheckboxItem>
              <DropdownMenuCheckboxItem>
                Draft
              </DropdownMenuCheckboxItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </div>
      </div>

      {/* Content */}
      <div className="flex-1 overflow-y-auto p-6">
        {view === 'grid' ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {/* Create Card */}
            <Card
              className="border-2 border-dashed border-border hover:border-primary hover:bg-primary/5 cursor-pointer transition-all group"
              onClick={createWorkflow}
            >
              <CardContent className="p-6 flex flex-col items-center justify-center h-[200px] text-center">
                <div className="w-12 h-12 rounded-full bg-surface-3 group-hover:bg-primary/10 flex items-center justify-center mb-3">
                  <Plus className="w-6 h-6 text-text-muted group-hover:text-primary" />
                </div>
                <p className="text-sm font-medium text-text-secondary group-hover:text-primary">
                  Create Workflow
                </p>
              </CardContent>
            </Card>

            {/* Workflow Cards */}
            {workflows.map((workflow) => (
              <WorkflowCard
                key={workflow.id}
                workflow={workflow}
                onClick={() => navigate(`/workspace/${workspaceId}/w/${workflow.id}`)}
              />
            ))}
          </div>
        ) : (
          <WorkflowsTable workflows={workflows} />
        )}
      </div>
    </div>
  )
}
```

### Workflow Card Component

```tsx
function WorkflowCard({ workflow, onClick }) {
  return (
    <Card
      className="hover:shadow-lg hover:border-primary/50 transition-all cursor-pointer group"
      onClick={onClick}
    >
      <CardHeader>
        <div className="flex items-start justify-between">
          <div className="flex-1">
            <CardTitle className="text-base group-hover:text-primary transition-colors">
              {workflow.name}
            </CardTitle>
            <CardDescription className="line-clamp-2 mt-1">
              {workflow.description || 'No description'}
            </CardDescription>
          </div>
          <DropdownMenu>
            <DropdownMenuTrigger asChild onClick={(e) => e.stopPropagation()}>
              <Button variant="ghost" size="xs">
                <MoreVertical className="w-4 h-4" />
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent>
              <DropdownMenuItem>
                <Play className="w-4 h-4 mr-2" />
                Run
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
        </div>
      </CardHeader>

      <CardContent className="space-y-3">
        {/* Status Badge */}
        <div className="flex items-center gap-2">
          <Badge
            variant={
              workflow.status === 'active'
                ? 'success'
                : workflow.status === 'paused'
                ? 'warning'
                : 'default'
            }
          >
            {workflow.status}
          </Badge>
          {workflow.successRate && (
            <span className="text-xs text-text-muted">
              {workflow.successRate}% success rate
            </span>
          )}
        </div>

        {/* Stats */}
        <div className="flex items-center justify-between text-xs text-text-secondary">
          <div className="flex items-center gap-1">
            <PlayCircle className="w-3 h-3" />
            <span>{workflow.totalRuns || 0} runs</span>
          </div>
          <div className="flex items-center gap-1">
            <Clock className="w-3 h-3" />
            <span>{formatDistance(workflow.updatedAt, new Date())} ago</span>
          </div>
        </div>

        {/* Mini preview of nodes */}
        <div className="flex items-center gap-1 pt-2 border-t border-border">
          <div className="flex items-center gap-1 overflow-hidden">
            {workflow.nodes?.slice(0, 5).map((node) => (
              <div
                key={node.id}
                className="w-6 h-6 rounded bg-surface-3 flex items-center justify-center shrink-0"
              >
                <Zap className="w-3 h-3 text-text-muted" />
              </div>
            ))}
            {workflow.nodes?.length > 5 && (
              <span className="text-xs text-text-muted ml-1">
                +{workflow.nodes.length - 5}
              </span>
            )}
          </div>
        </div>
      </CardContent>
    </Card>
  )
}
```

---

## 📑 Page 2: Templates Page

**Route**: `/workspace/:workspaceId/templates`

```tsx
export default function TemplatesPage() {
  const [category, setCategory] = useState('all')
  const [searchQuery, setSearchQuery] = useState('')

  return (
    <div className="h-full flex flex-col">
      {/* Header */}
      <div className="p-6 border-b border-border bg-bg">
        <h1 className="text-2xl font-bold text-text-primary">Templates</h1>
        <p className="text-sm text-text-secondary mt-1">
          Start with pre-built workflow templates
        </p>
      </div>

      {/* Category Tabs */}
      <div className="border-b border-border bg-surface-1">
        <div className="px-6">
          <Tabs value={category} onValueChange={setCategory}>
            <TabsList className="border-b-0">
              <TabsTrigger value="all">All Templates</TabsTrigger>
              <TabsTrigger value="ai">AI & ML</TabsTrigger>
              <TabsTrigger value="data">Data Processing</TabsTrigger>
              <TabsTrigger value="integration">Integrations</TabsTrigger>
              <TabsTrigger value="automation">Automation</TabsTrigger>
            </TabsList>
          </Tabs>
        </div>
      </div>

      {/* Content */}
      <div className="flex-1 overflow-y-auto p-6">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {templates
            .filter((t) => category === 'all' || t.category === category)
            .map((template) => (
              <TemplateCard
                key={template.id}
                template={template}
                onUse={createFromTemplate}
                onPreview={openTemplatePreview}
              />
            ))}
        </div>
      </div>
    </div>
  )
}

function TemplateCard({ template, onUse, onPreview }) {
  return (
    <Card className="hover:shadow-lg hover:border-primary/50 transition-all">
      <CardHeader>
        <div className="flex items-start gap-3">
          <div className="w-12 h-12 rounded-lg bg-gradient-to-br from-primary/10 to-secondary/10 flex items-center justify-center shrink-0">
            {template.icon}
          </div>
          <div className="flex-1">
            <CardTitle className="text-base">{template.name}</CardTitle>
            <div className="flex items-center gap-2 mt-1">
              <Badge variant="default" className="text-xs">
                {template.category}
              </Badge>
              <div className="flex items-center gap-1 text-xs text-text-muted">
                <Download className="w-3 h-3" />
                {template.uses}
              </div>
            </div>
          </div>
        </div>
      </CardHeader>

      <CardContent className="space-y-3">
        <p className="text-sm text-text-secondary line-clamp-2">
          {template.description}
        </p>

        <div className="flex flex-wrap gap-1">
          {template.tags.map((tag) => (
            <span
              key={tag}
              className="text-xs px-2 py-0.5 rounded bg-surface-3 text-text-muted"
            >
              {tag}
            </span>
          ))}
        </div>
      </CardContent>

      <CardFooter className="gap-2">
        <Button
          variant="outline"
          size="sm"
          className="flex-1"
          onClick={() => onPreview(template)}
        >
          <Eye className="w-4 h-4 mr-2" />
          Preview
        </Button>
        <Button
          variant="primary"
          size="sm"
          className="flex-1"
          onClick={() => onUse(template)}
        >
          <Plus className="w-4 h-4 mr-2" />
          Use Template
        </Button>
      </CardFooter>
    </Card>
  )
}
```

---

## 📑 Page 3: Knowledge Page

**Route**: `/workspace/:workspaceId/knowledge`

```tsx
export default function KnowledgePage() {
  const [view, setView] = useState<'grid' | 'list'>('list')

  return (
    <div className="h-full flex">
      {/* Document List */}
      <div className="flex-1 flex flex-col border-r border-border">
        {/* Header */}
        <div className="p-6 border-b border-border">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h1 className="text-2xl font-bold text-text-primary">
                Knowledge Base
              </h1>
              <p className="text-sm text-text-secondary mt-1">
                Vector database for AI context
              </p>
            </div>
            <Button variant="primary" onClick={uploadDocument}>
              <Upload className="w-4 h-4 mr-2" />
              Upload
            </Button>
          </div>

          <Input
            type="search"
            placeholder="Search documents..."
            className="w-full"
          />
        </div>

        {/* Documents Table */}
        <div className="flex-1 overflow-y-auto">
          <DataTable
            columns={documentsColumns}
            data={documents}
            searchable={false}
          />
        </div>
      </div>

      {/* Document Preview */}
      <aside className="w-[400px] flex flex-col bg-surface-1">
        {selectedDocument ? (
          <>
            <div className="p-6 border-b border-border">
              <h3 className="font-semibold text-text-primary">
                {selectedDocument.name}
              </h3>
              <div className="flex items-center gap-4 mt-2 text-xs text-text-muted">
                <span>{selectedDocument.size}</span>
                <span>•</span>
                <span>{selectedDocument.chunks} chunks</span>
                <span>•</span>
                <Badge
                  variant={
                    selectedDocument.status === 'embedded'
                      ? 'success'
                      : 'warning'
                  }
                >
                  {selectedDocument.status}
                </Badge>
              </div>
            </div>

            <div className="flex-1 overflow-y-auto p-6 space-y-4">
              {/* Metadata */}
              <div>
                <h4 className="text-sm font-medium text-text-secondary mb-2">
                  Metadata
                </h4>
                <dl className="space-y-2 text-sm">
                  <div className="flex justify-between">
                    <dt className="text-text-muted">Type</dt>
                    <dd className="text-text-primary">{selectedDocument.type}</dd>
                  </div>
                  <div className="flex justify-between">
                    <dt className="text-text-muted">Uploaded</dt>
                    <dd className="text-text-primary">
                      {formatDate(selectedDocument.createdAt)}
                    </dd>
                  </div>
                </dl>
              </div>

              {/* AI Search */}
              <div>
                <h4 className="text-sm font-medium text-text-secondary mb-2">
                  Search in Document
                </h4>
                <Input
                  type="search"
                  placeholder="Ask a question..."
                  onKeyDown={(e) => {
                    if (e.key === 'Enter') {
                      performSemanticSearch(e.currentTarget.value)
                    }
                  }}
                />
              </div>

              {/* Preview */}
              <div>
                <h4 className="text-sm font-medium text-text-secondary mb-2">
                  Preview
                </h4>
                <div className="rounded-lg border border-border p-4 bg-bg text-sm text-text-secondary max-h-96 overflow-y-auto">
                  {selectedDocument.preview}
                </div>
              </div>
            </div>
          </>
        ) : (
          <div className="flex-1 flex items-center justify-center text-center p-6">
            <div>
              <FileText className="w-12 h-12 text-text-muted mx-auto mb-3" />
              <p className="text-sm text-text-muted">
                Select a document to view details
              </p>
            </div>
          </div>
        )}
      </aside>
    </div>
  )
}
```

---

## 📑 Page 4: Logs Page

**Route**: `/workspace/:workspaceId/logs`

```tsx
export default function LogsPage() {
  const [severity, setSeverity] = useState('all')
  const [autoRefresh, setAutoRefresh] = useState(true)

  return (
    <div className="h-full flex flex-col">
      {/* Header */}
      <div className="p-6 border-b border-border bg-bg">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h1 className="text-2xl font-bold text-text-primary">Logs</h1>
            <p className="text-sm text-text-secondary mt-1">
              Real-time execution logs and monitoring
            </p>
          </div>
          <div className="flex items-center gap-2">
            <div className="flex items-center gap-2">
              <Switch
                checked={autoRefresh}
                onCheckedChange={setAutoRefresh}
                id="auto-refresh"
              />
              <label
                htmlFor="auto-refresh"
                className="text-sm text-text-secondary"
              >
                Auto-refresh
              </label>
            </div>
            <Button variant="outline" size="sm" onClick={clearLogs}>
              <Trash2 className="w-4 h-4 mr-2" />
              Clear
            </Button>
            <Button variant="outline" size="sm" onClick={exportLogs}>
              <Download className="w-4 h-4 mr-2" />
              Export
            </Button>
          </div>
        </div>

        {/* Filters */}
        <div className="flex items-center gap-3">
          <Input
            type="search"
            placeholder="Search logs..."
            className="flex-1 max-w-md"
          />

          <Select value={severity} onValueChange={setSeverity}>
            <SelectTrigger className="w-[150px]">
              <SelectValue placeholder="Severity" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All Levels</SelectItem>
              <SelectItem value="info">Info</SelectItem>
              <SelectItem value="warning">Warning</SelectItem>
              <SelectItem value="error">Error</SelectItem>
            </SelectContent>
          </Select>

          <Popover>
            <PopoverTrigger asChild>
              <Button variant="outline">
                <Calendar className="w-4 h-4 mr-2" />
                Date Range
              </Button>
            </PopoverTrigger>
            <PopoverContent>
              <DateRangePicker />
            </PopoverContent>
          </Popover>
        </div>
      </div>

      {/* Logs Stream */}
      <div className="flex-1 overflow-hidden">
        <div className="h-full overflow-y-auto font-mono text-sm">
          {logs.map((log, index) => (
            <LogEntry key={`${log.id}-${index}`} log={log} />
          ))}
        </div>
      </div>
    </div>
  )
}

function LogEntry({ log }) {
  const [expanded, setExpanded] = useState(false)

  return (
    <div
      className={cn(
        'border-b border-border hover:bg-surface-1 transition-colors',
        log.severity === 'error' && 'bg-error-bg/50',
        log.severity === 'warning' && 'bg-warning-bg/50'
      )}
    >
      <div
        className="flex items-start gap-3 p-3 cursor-pointer"
        onClick={() => setExpanded(!expanded)}
      >
        {/* Severity Badge */}
        <Badge
          variant={
            log.severity === 'error'
              ? 'error'
              : log.severity === 'warning'
              ? 'warning'
              : 'info'
          }
          className="shrink-0 mt-0.5"
        >
          {log.severity}
        </Badge>

        {/* Timestamp */}
        <span className="text-xs text-text-muted shrink-0 w-32">
          {formatTime(log.timestamp)}
        </span>

        {/* Message */}
        <div className="flex-1">
          <p className="text-sm text-text-primary">{log.message}</p>
          {log.workflow && (
            <p className="text-xs text-text-muted mt-1">
              Workflow: {log.workflow.name}
            </p>
          )}
        </div>

        {/* Expand Icon */}
        {log.details && (
          <ChevronDown
            className={cn(
              'w-4 h-4 text-text-muted transition-transform',
              expanded && 'rotate-180'
            )}
          />
        )}
      </div>

      {/* Expanded Details */}
      {expanded && log.details && (
        <div className="px-3 pb-3 pl-[180px]">
          <div className="rounded-lg bg-surface-3 p-4 text-xs">
            <pre className="overflow-x-auto">
              {JSON.stringify(log.details, null, 2)}
            </pre>
          </div>
        </div>
      )}
    </div>
  )
}
```

---

## 📑 Page 5: Tools Page

**Route**: Typically a modal, but can be standalone

```tsx
export default function ToolsPage() {
  const [category, setCategory] = useState('all')
  const [searchQuery, setSearchQuery] = useState('')

  return (
    <div className="h-full flex flex-col">
      {/* Header */}
      <div className="p-6 border-b border-border">
        <h1 className="text-2xl font-bold text-text-primary">Tools</h1>
        <p className="text-sm text-text-secondary mt-1">
          81+ integrations and tools for your workflows
        </p>
      </div>

      {/* Search & Categories */}
      <div className="p-6 border-b border-border bg-surface-1">
        <Input
          type="search"
          placeholder="Search tools..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="mb-4"
        />

        <div className="flex flex-wrap gap-2">
          <Badge
            variant={category === 'all' ? 'primary' : 'default'}
            className="cursor-pointer"
            onClick={() => setCategory('all')}
          >
            All Tools
          </Badge>
          <Badge
            variant={category === 'ai' ? 'primary' : 'default'}
            className="cursor-pointer"
            onClick={() => setCategory('ai')}
          >
            AI & ML
          </Badge>
          <Badge
            variant={category === 'api' ? 'primary' : 'default'}
            className="cursor-pointer"
            onClick={() => setCategory('api')}
          >
            APIs
          </Badge>
          <Badge
            variant={category === 'database' ? 'primary' : 'default'}
            className="cursor-pointer"
            onClick={() => setCategory('database')}
          >
            Databases
          </Badge>
          <Badge
            variant={category === 'cloud' ? 'primary' : 'default'}
            className="cursor-pointer"
            onClick={() => setCategory('cloud')}
          >
            Cloud
          </Badge>
        </div>
      </div>

      {/* Tools Grid */}
      <div className="flex-1 overflow-y-auto p-6">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
          {tools
            .filter((t) => category === 'all' || t.category === category)
            .filter((t) =>
              t.name.toLowerCase().includes(searchQuery.toLowerCase())
            )
            .map((tool) => (
              <ToolCard key={tool.id} tool={tool} />
            ))}
        </div>
      </div>
    </div>
  )
}

function ToolCard({ tool }) {
  return (
    <Card className="hover:shadow-md hover:border-primary/50 transition-all cursor-pointer">
      <CardContent className="p-4">
        <div className="flex items-start gap-3">
          <div className="w-10 h-10 rounded-lg bg-surface-3 flex items-center justify-center shrink-0">
            {tool.icon || <Boxes className="w-5 h-5" />}
          </div>
          <div className="flex-1 min-w-0">
            <h3 className="font-medium text-sm text-text-primary truncate">
              {tool.name}
            </h3>
            <p className="text-xs text-text-muted line-clamp-2 mt-1">
              {tool.description}
            </p>
            <div className="flex items-center gap-2 mt-2">
              <Badge variant="default" className="text-xs">
                {tool.category}
              </Badge>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}
```

---

## 📑 Page 6: Settings Page

**Route**: Modal-based

```tsx
export default function SettingsModal() {
  const [section, setSection] = useState('general')

  return (
    <Dialog open={isOpen} onOpenChange={setIsOpen}>
      <DialogContent className="max-w-4xl h-[80vh] p-0">
        <div className="flex h-full">
          {/* Sidebar */}
          <aside className="w-64 border-r border-border p-4 overflow-y-auto">
            <h2 className="font-semibold text-text-primary mb-4">Settings</h2>
            <nav className="space-y-1">
              <SettingsNavItem
                icon={<Settings className="w-4 h-4" />}
                label="General"
                active={section === 'general'}
                onClick={() => setSection('general')}
              />
              <SettingsNavItem
                icon={<Key className="w-4 h-4" />}
                label="API Keys"
                active={section === 'api-keys'}
                onClick={() => setSection('api-keys')}
              />
              <SettingsNavItem
                icon={<Users className="w-4 h-4" />}
                label="Team"
                active={section === 'team'}
                onClick={() => setSection('team')}
              />
              <SettingsNavItem
                icon={<CreditCard className="w-4 h-4" />}
                label="Billing"
                active={section === 'billing'}
                onClick={() => setSection('billing')}
              />
            </nav>
          </aside>

          {/* Content */}
          <div className="flex-1 overflow-y-auto p-6">
            {section === 'general' && <GeneralSettings />}
            {section === 'api-keys' && <APIKeysSettings />}
            {section === 'team' && <TeamSettings />}
            {section === 'billing' && <BillingSettings />}
          </div>
        </div>
      </DialogContent>
    </Dialog>
  )
}
```

---

**Implementation Files**:
- `/apps/sim/app/workspace/[workspaceId]/w/page.tsx`
- `/apps/sim/app/workspace/[workspaceId]/templates/page.tsx`
- `/apps/sim/app/workspace/[workspaceId]/knowledge/page.tsx`
- `/apps/sim/app/workspace/[workspaceId]/logs/page.tsx`
