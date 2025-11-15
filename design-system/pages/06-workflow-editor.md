# Workflow Editor Page Design

> **Route**: `/workspace/:workspaceId/w/:workflowId`
> **Type**: Core workflow builder interface
> **Goal**: Professional, n8n/Make/Langflow-inspired visual editor

---

## 🎯 Layout Overview

```
┌──────────────────────────────────────────────────────────────────────────┐
│  TOPBAR                                                                  │
│  [Workflow Name] • [Run] [Deploy] [Version] [Save] [...More]    [Close] │
├──────┬───────────────────────────────────────────────────────────┬───────┤
│      │                                                           │       │
│ NODE │                  CANVAS AREA                              │ INSP  │
│ PAL  │                                                           │ ECTOR │
│ ETTE │     Infinite canvas with nodes & connections             │       │
│      │                                                           │ Node  │
│ 🤖AI │  ┌────────┐        ┌────────┐        ┌────────┐          │ Props │
│ 🔌API│  │Trigger │───────▶│  AI    │───────▶│ Action │          │       │
│ 💾DB │  └────────┘        └────────┘        └────────┘          │ [Tabs]│
│ 🔧UT │                                                           │       │
│ ⚡TR │                                                           │ ┌───┐ │
│      │                                                           │ │   │ │
│ [AI  │                                                           │ │   │ │
│  Gen]│                                                           │ └───┘ │
│      │                                                           │       │
├──────┴───────────────────────────────────────────────────────────┴───────┤
│  FOOTER                                                                  │
│  Zoom: [-] [100%] [+] • Minimap • Variables: 3 • Execution: Idle        │
└──────────────────────────────────────────────────────────────────────────┘
```

**Dimensions**:
- Node Palette (Left): 280px (collapsible to 56px)
- Inspector (Right): 400px (collapsible)
- Topbar: 56px
- Footer: 40px
- Canvas: flex-1 (fills remaining space)

---

## 🧩 Component Breakdown

### 1. Topbar

```tsx
function WorkflowTopbar({ workflow, onRun, onDeploy }) {
  const [isSaving, setIsSaving] = useState(false)
  const [isEditing, setIsEditing] = useState(false)

  return (
    <header className="h-14 border-b border-border bg-bg flex items-center justify-between px-4 sticky top-0 z-50">
      {/* Left: Name + Status */}
      <div className="flex items-center gap-3">
        <Button
          variant="ghost"
          size="sm"
          asChild
        >
          <Link href={`/workspace/${workspaceId}/w`}>
            <X className="w-4 h-4" />
          </Link>
        </Button>

        {isEditing ? (
          <Input
            value={workflowName}
            onChange={(e) => setWorkflowName(e.target.value)}
            onBlur={() => setIsEditing(false)}
            onKeyDown={(e) => {
              if (e.key === 'Enter') setIsEditing(false)
            }}
            className="h-8 max-w-xs"
            autoFocus
          />
        ) : (
          <button
            className="text-lg font-semibold text-text-primary hover:text-primary transition-colors"
            onClick={() => setIsEditing(true)}
          >
            {workflow.name}
          </button>
        )}

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

        {isSaving && (
          <div className="flex items-center gap-2 text-xs text-text-muted">
            <Loader2 className="w-3 h-3 animate-spin" />
            Saving...
          </div>
        )}
      </div>

      {/* Center: Quick Actions */}
      <div className="flex items-center gap-2">
        <Button
          variant="primary"
          size="sm"
          onClick={onRun}
          disabled={!canExecute}
        >
          <Play className="w-4 h-4 mr-2" />
          Run
        </Button>

        <Button variant="outline" size="sm" onClick={onTest}>
          <TestTube className="w-4 h-4 mr-2" />
          Test
        </Button>

        <Button variant="outline" size="sm" onClick={onDeploy}>
          <Rocket className="w-4 h-4 mr-2" />
          Deploy
        </Button>

        <Separator orientation="vertical" className="h-6" />

        <Button variant="ghost" size="sm" onClick={undo} disabled={!canUndo}>
          <Undo className="w-4 h-4" />
        </Button>

        <Button variant="ghost" size="sm" onClick={redo} disabled={!canRedo}>
          <Redo className="w-4 h-4" />
        </Button>
      </div>

      {/* Right: Settings */}
      <div className="flex items-center gap-2">
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button variant="ghost" size="sm">
              <GitBranch className="w-4 h-4 mr-2" />
              v{workflow.version}
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent>
            <DropdownMenuItem>
              <History className="w-4 h-4 mr-2" />
              Version History
            </DropdownMenuItem>
            <DropdownMenuItem>
              <GitCompare className="w-4 h-4 mr-2" />
              Compare Versions
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>

        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button variant="ghost" size="sm">
              <MoreVertical className="w-4 h-4" />
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="end">
            <DropdownMenuItem>
              <Copy className="w-4 h-4 mr-2" />
              Duplicate
            </DropdownMenuItem>
            <DropdownMenuItem>
              <Download className="w-4 h-4 mr-2" />
              Export JSON
            </DropdownMenuItem>
            <DropdownMenuItem>
              <Share2 className="w-4 h-4 mr-2" />
              Share
            </DropdownMenuItem>
            <DropdownMenuSeparator />
            <DropdownMenuItem className="text-error">
              <Trash2 className="w-4 h-4 mr-2" />
              Delete
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>

        <Button
          variant="ghost"
          size="sm"
          onClick={openSettings}
        >
          <Settings className="w-4 h-4" />
        </Button>
      </div>
    </header>
  )
}
```

---

### 2. Node Palette (Left Sidebar)

```tsx
function NodePalette({ onAddNode }) {
  const [collapsed, setCollapsed] = useState(false)
  const [searchQuery, setSearchQuery] = useState('')
  const [category, setCategory] = useState('all')

  const nodeCategories = [
    { id: 'ai', label: 'AI & Agents', icon: Brain, color: 'violet' },
    { id: 'api', label: 'API', icon: Globe, color: 'blue' },
    { id: 'database', label: 'Database', icon: Database, color: 'green' },
    { id: 'logic', label: 'Logic', icon: GitBranch, color: 'amber' },
    { id: 'trigger', label: 'Triggers', icon: Zap, color: 'pink' },
    { id: 'integration', label: 'Integrations', icon: Boxes, color: 'cyan' },
  ]

  return (
    <aside
      className={cn(
        'border-r border-border bg-surface-1 flex flex-col transition-all duration-200',
        collapsed ? 'w-14' : 'w-[280px]'
      )}
    >
      {/* Header */}
      <div className="h-12 px-3 flex items-center justify-between border-b border-border">
        {!collapsed && (
          <h3 className="font-semibold text-sm text-text-primary">Add Node</h3>
        )}
        <Button
          variant="ghost"
          size="xs"
          onClick={() => setCollapsed(!collapsed)}
        >
          {collapsed ? (
            <ChevronsRight className="w-4 h-4" />
          ) : (
            <ChevronsLeft className="w-4 h-4" />
          )}
        </Button>
      </div>

      {!collapsed && (
        <>
          {/* Search */}
          <div className="p-3 border-b border-border">
            <Input
              type="search"
              placeholder="Search nodes..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="h-9"
            />
          </div>

          {/* Categories */}
          <div className="p-2 border-b border-border">
            <div className="grid grid-cols-2 gap-1">
              <Button
                variant={category === 'all' ? 'secondary' : 'ghost'}
                size="sm"
                className="justify-start text-xs"
                onClick={() => setCategory('all')}
              >
                All
              </Button>
              {nodeCategories.map((cat) => (
                <Button
                  key={cat.id}
                  variant={category === cat.id ? 'secondary' : 'ghost'}
                  size="sm"
                  className="justify-start text-xs"
                  onClick={() => setCategory(cat.id)}
                >
                  <cat.icon className="w-3 h-3 mr-1.5" />
                  {cat.label}
                </Button>
              ))}
            </div>
          </div>

          {/* Node List */}
          <div className="flex-1 overflow-y-auto p-2">
            <div className="space-y-4">
              {nodeCategories
                .filter((cat) => category === 'all' || category === cat.id)
                .map((cat) => (
                  <div key={cat.id}>
                    <h4 className="text-xs font-semibold text-text-muted uppercase tracking-wider px-2 mb-2">
                      {cat.label}
                    </h4>
                    <div className="space-y-1">
                      {getNodesByCategory(cat.id).map((node) => (
                        <NodePaletteItem
                          key={node.id}
                          node={node}
                          category={cat}
                          onAdd={onAddNode}
                        />
                      ))}
                    </div>
                  </div>
                ))}
            </div>
          </div>

          {/* AI Builder */}
          <div className="p-3 border-t border-border">
            <Button
              variant="primary"
              className="w-full"
              onClick={openAIBuilder}
            >
              <Sparkles className="w-4 h-4 mr-2" />
              AI Builder
            </Button>
          </div>
        </>
      )}

      {/* Collapsed View */}
      {collapsed && (
        <div className="flex-1 p-2 space-y-2">
          {nodeCategories.map((cat) => (
            <Tooltip key={cat.id} content={cat.label}>
              <Button
                variant="ghost"
                size="sm"
                className="w-full"
                onClick={() => {
                  setCategory(cat.id)
                  setCollapsed(false)
                }}
              >
                <cat.icon className="w-4 h-4" />
              </Button>
            </Tooltip>
          ))}
        </div>
      )}
    </aside>
  )
}

function NodePaletteItem({ node, category, onAdd }) {
  return (
    <button
      className="w-full text-left px-2 py-2 rounded-lg hover:bg-surface-2 transition-colors group flex items-start gap-2"
      onClick={() => onAdd(node)}
      draggable
      onDragStart={(e) => {
        e.dataTransfer.setData('application/reactflow', JSON.stringify(node))
        e.dataTransfer.effectAllowed = 'move'
      }}
    >
      <div
        className={cn(
          'w-8 h-8 rounded-lg flex items-center justify-center shrink-0',
          `bg-${category.color}-500/10`
        )}
      >
        {node.icon || <category.icon className="w-4 h-4" />}
      </div>
      <div className="flex-1 min-w-0">
        <p className="text-sm font-medium text-text-primary truncate">
          {node.label}
        </p>
        <p className="text-xs text-text-muted line-clamp-1">
          {node.description}
        </p>
      </div>
    </button>
  )
}
```

---

### 3. Canvas (ReactFlow Integration)

```tsx
function WorkflowCanvas({ workflowId }) {
  const [nodes, setNodes, onNodesChange] = useNodesState([])
  const [edges, setEdges, onEdgesChange] = useEdgesState([])
  const [selectedNode, setSelectedNode] = useState(null)

  const onConnect = useCallback((connection) => {
    setEdges((eds) => addEdge({
      ...connection,
      type: 'smoothstep',
      animated: true,
      style: { stroke: 'var(--primary)', strokeWidth: 2 },
    }, eds))
  }, [])

  const onNodeClick = useCallback((event, node) => {
    setSelectedNode(node)
  }, [])

  const onDrop = useCallback((event) => {
    event.preventDefault()
    const nodeData = JSON.parse(
      event.dataTransfer.getData('application/reactflow')
    )
    const position = reactFlowInstance.project({
      x: event.clientX,
      y: event.clientY,
    })
    addNode({ ...nodeData, position })
  }, [])

  return (
    <div className="flex-1 bg-surface-1 relative">
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onConnect={onConnect}
        onNodeClick={onNodeClick}
        onDrop={onDrop}
        onDragOver={(e) => e.preventDefault()}
        nodeTypes={nodeTypes}
        edgeTypes={edgeTypes}
        fitView
        snapToGrid
        snapGrid={[16, 16]}
        defaultEdgeOptions={{
          type: 'smoothstep',
          animated: true,
        }}
        className="workflow-canvas"
      >
        <Background
          gap={16}
          color="var(--border)"
          variant="dots"
        />
        <Controls
          className="!bg-surface-2 !border-border"
          showInteractive={false}
        />
        <MiniMap
          className="!bg-surface-2 !border-border"
          nodeColor={(node) => getNodeColor(node.type)}
          maskColor="var(--bg-muted)"
        />
        <Panel position="top-right">
          <div className="bg-surface-2 border border-border rounded-lg p-2 flex items-center gap-2">
            <Button variant="ghost" size="xs" onClick={autoLayout}>
              <LayoutGrid className="w-4 h-4" />
            </Button>
            <Button variant="ghost" size="xs" onClick={resetView}>
              <Maximize className="w-4 h-4" />
            </Button>
          </div>
        </Panel>
      </ReactFlow>
    </div>
  )
}
```

---

### 4. Custom Node Component

```tsx
function CustomNode({ id, data, selected }) {
  const nodeColor = getNodeColor(data.type)

  return (
    <div
      className={cn(
        'min-w-[240px] rounded-lg bg-surface-1 border-2 transition-all',
        selected
          ? 'border-primary shadow-lg ring-2 ring-primary/20'
          : 'border-border hover:border-border-secondary hover:shadow-md'
      )}
    >
      {/* Header */}
      <div
        className={cn(
          'flex items-center gap-2 px-4 py-3 border-b border-border',
          'bg-gradient-to-r',
          `from-${nodeColor}-500/10 to-${nodeColor}-600/10`,
          `border-l-4 border-l-${nodeColor}-500`
        )}
      >
        <div className={cn(
          'w-8 h-8 rounded-lg flex items-center justify-center',
          `bg-${nodeColor}-500/20`
        )}>
          {data.icon}
        </div>
        <div className="flex-1 min-w-0">
          <p className="text-sm font-semibold text-text-primary truncate">
            {data.label}
          </p>
          {data.subtitle && (
            <p className="text-xs text-text-muted truncate">
              {data.subtitle}
            </p>
          )}
        </div>
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button variant="ghost" size="xs">
              <MoreVertical className="w-3 h-3" />
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent>
            <DropdownMenuItem>
              <Copy className="w-4 h-4 mr-2" />
              Duplicate
            </DropdownMenuItem>
            <DropdownMenuItem className="text-error">
              <Trash2 className="w-4 h-4 mr-2" />
              Delete
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      </div>

      {/* Body */}
      <div className="p-4 space-y-2">
        {data.config && (
          <div className="text-xs space-y-1">
            {Object.entries(data.config).slice(0, 3).map(([key, value]) => (
              <div key={key} className="flex justify-between">
                <span className="text-text-muted">{key}:</span>
                <span className="text-text-primary font-medium truncate max-w-[120px]">
                  {String(value)}
                </span>
              </div>
            ))}
          </div>
        )}

        {/* Status Badge */}
        {data.status && (
          <Badge
            variant={
              data.status === 'success'
                ? 'success'
                : data.status === 'error'
                ? 'error'
                : 'default'
            }
            className="text-xs"
          >
            {data.status}
          </Badge>
        )}
      </div>

      {/* Input Handles */}
      {data.inputs > 0 && (
        <Handle
          type="target"
          position={Position.Left}
          className="!w-3 !h-3 !bg-primary !border-2 !border-surface-1"
        />
      )}

      {/* Output Handles */}
      {data.outputs > 0 && (
        <Handle
          type="source"
          position={Position.Right}
          className="!w-3 !h-3 !bg-primary !border-2 !border-surface-1"
        />
      )}
    </div>
  )
}
```

---

### 5. Inspector Panel (Right)

```tsx
function InspectorPanel({ selectedNode, onUpdate, onClose }) {
  if (!selectedNode) {
    return (
      <aside className="w-[400px] border-l border-border bg-surface-1 flex items-center justify-center p-6">
        <div className="text-center">
          <MousePointer className="w-12 h-12 text-text-muted mx-auto mb-3" />
          <p className="text-sm text-text-muted">
            Select a node to configure
          </p>
        </div>
      </aside>
    )
  }

  return (
    <aside className="w-[400px] border-l border-border bg-surface-1 flex flex-col">
      {/* Header */}
      <div className="p-4 border-b border-border flex items-center justify-between">
        <div className="flex items-center gap-2">
          {selectedNode.data.icon}
          <div>
            <h3 className="font-semibold text-sm text-text-primary">
              {selectedNode.data.label}
            </h3>
            <p className="text-xs text-text-muted">{selectedNode.type}</p>
          </div>
        </div>
        <Button variant="ghost" size="xs" onClick={onClose}>
          <X className="w-4 h-4" />
        </Button>
      </div>

      {/* Tabs */}
      <Tabs defaultValue="config" className="flex-1 flex flex-col">
        <TabsList className="px-4 py-2 border-b border-border">
          <TabsTrigger value="config">Config</TabsTrigger>
          <TabsTrigger value="data">Data</TabsTrigger>
          <TabsTrigger value="test">Test</TabsTrigger>
        </TabsList>

        {/* Config Tab */}
        <TabsContent value="config" className="flex-1 overflow-y-auto p-4 space-y-4">
          <NodeConfigForm
            node={selectedNode}
            onUpdate={onUpdate}
          />
        </TabsContent>

        {/* Data Tab */}
        <TabsContent value="data" className="flex-1 overflow-y-auto p-4">
          <div className="space-y-4">
            <div>
              <h4 className="text-sm font-medium text-text-secondary mb-2">
                Input Schema
              </h4>
              <div className="rounded-lg bg-surface-3 p-3 font-mono text-xs">
                <pre>{JSON.stringify(selectedNode.data.inputSchema, null, 2)}</pre>
              </div>
            </div>

            <div>
              <h4 className="text-sm font-medium text-text-secondary mb-2">
                Output Schema
              </h4>
              <div className="rounded-lg bg-surface-3 p-3 font-mono text-xs">
                <pre>{JSON.stringify(selectedNode.data.outputSchema, null, 2)}</pre>
              </div>
            </div>
          </div>
        </TabsContent>

        {/* Test Tab */}
        <TabsContent value="test" className="flex-1 overflow-y-auto p-4 space-y-4">
          <div>
            <Button
              variant="primary"
              className="w-full"
              onClick={() => testNode(selectedNode.id)}
            >
              <Play className="w-4 h-4 mr-2" />
              Test Node
            </Button>
          </div>

          {testResult && (
            <div className="rounded-lg bg-surface-3 p-4">
              <h4 className="text-sm font-medium text-text-secondary mb-2">
                Test Result
              </h4>
              <div className="font-mono text-xs">
                <pre>{JSON.stringify(testResult, null, 2)}</pre>
              </div>
            </div>
          )}
        </TabsContent>
      </Tabs>
    </aside>
  )
}
```

---

### 6. Footer Controls

```tsx
function WorkflowFooter() {
  const [zoom, setZoom] = useState(100)

  return (
    <footer className="h-10 border-t border-border bg-surface-1 px-4 flex items-center justify-between text-xs text-text-secondary">
      {/* Left: Zoom Controls */}
      <div className="flex items-center gap-2">
        <Button variant="ghost" size="xs" onClick={() => zoomOut()}>
          <Minus className="w-3 h-3" />
        </Button>
        <span className="w-12 text-center font-mono">{zoom}%</span>
        <Button variant="ghost" size="xs" onClick={() => zoomIn()}>
          <Plus className="w-3 h-3" />
        </Button>
        <Separator orientation="vertical" className="h-4 mx-2" />
        <Button variant="ghost" size="xs" onClick={() => fitView()}>
          <Maximize className="w-3 h-3 mr-1" />
          Fit
        </Button>
      </div>

      {/* Center: Stats */}
      <div className="flex items-center gap-4">
        <span>Nodes: {nodeCount}</span>
        <span>•</span>
        <span>Connections: {edgeCount}</span>
        <span>•</span>
        <span>Variables: {variableCount}</span>
      </div>

      {/* Right: Execution Status */}
      <div className="flex items-center gap-2">
        <div className={cn(
          'w-2 h-2 rounded-full',
          executionStatus === 'running' ? 'bg-success animate-pulse' : 'bg-surface-5'
        )} />
        <span className="capitalize">{executionStatus}</span>
      </div>
    </footer>
  )
}
```

---

## 🎨 Design Tokens Used

**Node Colors** (by category):
- AI/Agent: violet-500
- API: blue-500
- Database: green-500
- Logic: amber-500
- Trigger: pink-500
- Integration: cyan-500

**Layout**:
- Node min-width: 240px
- Node padding: p-4
- Handle size: 12px (w-3 h-3)
- Border radius: rounded-lg (8px)

**Colors**:
- Selected node: border-primary, ring-2 ring-primary/20
- Canvas background: surface-1
- Node background: surface-1
- Headers: gradient from node color at 10% opacity

**Spacing**:
- Node gaps: space-y-2, space-y-4
- Panel padding: p-4
- Inspector sections: space-y-4

---

## ⚡ Interactions & Animations

### Connection Animation
```css
.react-flow__edge-path {
  stroke: var(--primary);
  stroke-width: 2px;
  animation: dash-flow 20s linear infinite;
}

@keyframes dash-flow {
  to {
    stroke-dashoffset: -20;
  }
}
```

### Node Hover
```css
.react-flow__node:hover {
  filter: drop-shadow(0 10px 15px rgb(0 0 0 / 0.1));
  transform: translateY(-2px);
  transition: all 150ms ease-out;
}
```

### Handle Hover
```css
.react-flow__handle:hover {
  transform: scale(1.3);
  transition: transform 100ms ease-out;
}
```

---

## ♿ Accessibility

- [ ] Keyboard navigation for canvas (arrow keys)
- [ ] Tab through nodes in order
- [ ] Screen reader labels for all handles
- [ ] Undo/Redo shortcuts (Cmd+Z, Cmd+Shift+Z)
- [ ] Delete node shortcut (Delete/Backspace)
- [ ] Copy/Paste shortcuts (Cmd+C, Cmd+V)

---

## 🎹 Keyboard Shortcuts

```typescript
const shortcuts = {
  'Cmd+Z': 'Undo',
  'Cmd+Shift+Z': 'Redo',
  'Cmd+C': 'Copy node',
  'Cmd+V': 'Paste node',
  'Cmd+D': 'Duplicate node',
  'Delete': 'Delete node',
  'Cmd+S': 'Save workflow',
  'Cmd+Enter': 'Run workflow',
  'Cmd+K': 'Open command palette',
  'Cmd+F': 'Search nodes',
  'Space': 'Pan canvas (hold)',
}
```

---

**Implementation File**: `/apps/sim/app/workspace/[workspaceId]/w/[workflowId]/workflow.tsx`
