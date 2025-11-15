# Feature-by-Feature Migration Guide

## Overview

This document provides a detailed, feature-by-feature guide for migrating components from `apps/sim` to `services/frontend`.

---

## 🎯 Phase 1: Workflow Canvas (PRIORITY 1)

### Feature: Workflow Editor Canvas

**Original Location**: `apps/sim/app/workspace/[workspaceId]/w/[workflowId]/workflow.tsx`

**New Location**: `services/frontend/src/components/workflow/WorkflowCanvas.tsx`

#### Files to Migrate

```
SOURCE: apps/sim/app/workspace/[workspaceId]/w/[workflowId]/
├── workflow.tsx                              → WorkflowCanvas.tsx
├── page.tsx                                   → (Already migrated to WorkflowEditorPage.tsx)
└── layout.tsx                                 → (Not needed in new arch)
```

#### Key Dependencies

**React Flow**: Already installed in new frontend
```typescript
import ReactFlow, {
  Background,
  Controls,
  MiniMap,
  Node,
  Edge,
  ReactFlowProvider,
} from 'reactflow'
import 'reactflow/dist/style.css'
```

**Hooks to Migrate**:
```
hooks/use-current-workflow.ts        → services/frontend/src/hooks/workflow/useCurrentWorkflow.ts
hooks/use-workflow-execution.ts      → services/frontend/src/hooks/workflow/useWorkflowExecution.ts
hooks/use-auto-layout.ts             → services/frontend/src/hooks/workflow/useAutoLayout.ts
hooks/use-block-connections.ts       → services/frontend/src/hooks/workflow/useBlockConnections.ts
hooks/use-node-utilities.ts          → services/frontend/src/hooks/workflow/useNodeUtilities.ts
```

#### Component Structure

```typescript
// services/frontend/src/components/workflow/WorkflowCanvas.tsx

import { useState, useCallback, useRef, useEffect } from 'react'
import ReactFlow, {
  Background,
  Controls,
  MiniMap,
  Node,
  Edge,
  Connection,
  addEdge,
  useNodesState,
  useEdgesState,
} from 'reactflow'
import 'reactflow/dist/style.css'
import { useWorkflowStore } from '@/stores/workflowStore'
import { useParams } from 'react-router-dom'
import { BlockNode } from './BlockNode'
import { CustomEdge } from './CustomEdge'
import { BlockPanel } from './BlockPanel'

// Define custom node types
const nodeTypes = {
  block: BlockNode,
}

// Define custom edge types
const edgeTypes = {
  custom: CustomEdge,
}

export function WorkflowCanvas() {
  const { workflowId } = useParams()
  const { currentWorkflow, fetchWorkflow, updateWorkflow } = useWorkflowStore()
  const reactFlowWrapper = useRef<HTMLDivElement>(null)

  const [nodes, setNodes, onNodesChange] = useNodesState([])
  const [edges, setEdges, onEdgesChange] = useEdgesState([])

  // Load workflow data
  useEffect(() => {
    if (workflowId) {
      fetchWorkflow(workflowId)
    }
  }, [workflowId, fetchWorkflow])

  // Convert workflow blocks to nodes
  useEffect(() => {
    if (currentWorkflow) {
      const flowNodes = currentWorkflow.blocks.map((block) => ({
        id: block.id,
        type: 'block',
        position: block.position,
        data: block.data || {},
      }))
      setNodes(flowNodes)

      const flowEdges = currentWorkflow.edges.map((edge) => ({
        id: edge.id,
        source: edge.source,
        target: edge.target,
        type: 'custom',
      }))
      setEdges(flowEdges)
    }
  }, [currentWorkflow, setNodes, setEdges])

  // Handle new connections
  const onConnect = useCallback(
    (connection: Connection) => {
      setEdges((eds) => addEdge(connection, eds))
      // TODO: Save to backend
    },
    [setEdges]
  )

  // Handle node drag
  const onNodeDragStop = useCallback(
    (event: React.MouseEvent, node: Node) => {
      // TODO: Save position to backend
    },
    []
  )

  return (
    <div className="h-screen w-full">
      <ReactFlowProvider>
        <div ref={reactFlowWrapper} className="h-full w-full">
          <ReactFlow
            nodes={nodes}
            edges={edges}
            onNodesChange={onNodesChange}
            onEdgesChange={onEdgesChange}
            onConnect={onConnect}
            onNodeDragStop={onNodeDragStop}
            nodeTypes={nodeTypes}
            edgeTypes={edgeTypes}
            fitView
          >
            <Background />
            <Controls />
            <MiniMap />
          </ReactFlow>
        </div>
        <BlockPanel />
      </ReactFlowProvider>
    </div>
  )
}
```

#### Migration Steps

1. Create directory structure:
```bash
mkdir -p services/frontend/src/components/workflow
mkdir -p services/frontend/src/hooks/workflow
```

2. Copy and adapt workflow.tsx:
   - Remove Next.js specific imports
   - Replace `useRouter` with `useNavigate` from react-router-dom
   - Update store imports to use new workflow store
   - Remove server components logic
   - Adapt API calls to use new API layer

3. Create BlockNode component (see below)

4. Create CustomEdge component (see below)

5. Update WorkflowEditorPage.tsx to use WorkflowCanvas

#### Testing Checklist

- [ ] Canvas renders correctly
- [ ] Blocks display on canvas
- [ ] Connections between blocks work
- [ ] Drag and drop blocks works
- [ ] Zoom and pan work
- [ ] Auto-layout works
- [ ] Save workflow updates to backend

---

## 🧩 Phase 2: Block Components

### Feature: Block Node Component

**Original Location**: `apps/sim/app/workspace/[workspaceId]/w/[workflowId]/components/workflow-node/*`

**New Location**: `services/frontend/src/components/workflow/BlockNode.tsx`

#### Component Structure

```typescript
// services/frontend/src/components/workflow/BlockNode.tsx

import { memo } from 'react'
import { Handle, Position, NodeProps } from 'reactflow'
import { Card } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Settings, Play, Trash2 } from 'lucide-react'

export const BlockNode = memo(({ data, selected }: NodeProps) => {
  const blockType = data.type || 'unknown'
  const blockName = data.name || 'Unnamed Block'

  return (
    <Card
      className={`
        min-w-[200px] max-w-[300px] p-4
        ${selected ? 'ring-2 ring-primary' : ''}
        transition-all hover:shadow-lg
      `}
    >
      {/* Input Handle */}
      <Handle
        type="target"
        position={Position.Top}
        className="!bg-primary"
      />

      {/* Block Header */}
      <div className="flex items-start justify-between mb-2">
        <div className="flex-1">
          <h3 className="font-semibold text-sm">{blockName}</h3>
          <Badge variant="secondary" className="text-xs mt-1">
            {blockType}
          </Badge>
        </div>
        <div className="flex gap-1">
          <button className="p-1 hover:bg-muted rounded">
            <Settings className="h-3 w-3" />
          </button>
          <button className="p-1 hover:bg-muted rounded">
            <Play className="h-3 w-3" />
          </button>
          <button className="p-1 hover:bg-red-50 rounded">
            <Trash2 className="h-3 w-3 text-red-600" />
          </button>
        </div>
      </div>

      {/* Block Description */}
      {data.description && (
        <p className="text-xs text-muted-foreground line-clamp-2">
          {data.description}
        </p>
      )}

      {/* Output Handle */}
      <Handle
        type="source"
        position={Position.Bottom}
        className="!bg-primary"
      />
    </Card>
  )
})

BlockNode.displayName = 'BlockNode'
```

#### Files to Reference

```
apps/sim/app/workspace/[workspaceId]/w/[workflowId]/components/
├── workflow-node/                    → Reference for node styling
├── note-block/                       → Special note node type
└── subflows/                         → Loop/parallel node types
```

---

## 📚 Phase 3: Block Palette

### Feature: Block Library Sidebar

**Original Location**: `apps/sim/blocks/blocks/*` (for block metadata)
**New Location**: `services/frontend/src/components/blocks/BlockPalette.tsx`

#### Component Structure

```typescript
// services/frontend/src/components/blocks/BlockPalette.tsx

import { useState, useEffect } from 'react'
import { Input } from '@/components/ui/input'
import { ScrollArea } from '@/components/ui/scroll-area'
import { Card } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Search, Blocks as BlocksIcon } from 'lucide-react'
import * as api from '@/lib/api'

interface Block {
  type: string
  name: string
  description: string
  category: string
  icon?: string
}

export function BlockPalette() {
  const [blocks, setBlocks] = useState<Block[]>([])
  const [searchQuery, setSearchQuery] = useState('')
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  // Fetch blocks from backend
  useEffect(() => {
    const fetchBlocks = async () => {
      try {
        setIsLoading(true)
        const response = await api.listBlocks()
        setBlocks(response)
      } catch (error) {
        console.error('Failed to fetch blocks:', error)
      } finally {
        setIsLoading(false)
      }
    }
    fetchBlocks()
  }, [])

  // Filter blocks
  const filteredBlocks = blocks.filter((block) => {
    const matchesSearch = block.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      block.description.toLowerCase().includes(searchQuery.toLowerCase())
    const matchesCategory = !selectedCategory || block.category === selectedCategory
    return matchesSearch && matchesCategory
  })

  // Get unique categories
  const categories = Array.from(new Set(blocks.map((b) => b.category)))

  // Handle drag start
  const onDragStart = (event: React.DragEvent, block: Block) => {
    event.dataTransfer.setData('application/reactflow', block.type)
    event.dataTransfer.effectAllowed = 'move'
  }

  return (
    <div className="w-80 h-full border-l bg-background flex flex-col">
      {/* Header */}
      <div className="p-4 border-b">
        <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
          <BlocksIcon className="h-5 w-5" />
          Block Library
        </h2>

        {/* Search */}
        <div className="relative mb-4">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
          <Input
            placeholder="Search blocks..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="pl-10"
          />
        </div>

        {/* Categories */}
        <div className="flex flex-wrap gap-2">
          <Badge
            variant={selectedCategory === null ? 'default' : 'outline'}
            className="cursor-pointer"
            onClick={() => setSelectedCategory(null)}
          >
            All
          </Badge>
          {categories.map((category) => (
            <Badge
              key={category}
              variant={selectedCategory === category ? 'default' : 'outline'}
              className="cursor-pointer"
              onClick={() => setSelectedCategory(category)}
            >
              {category}
            </Badge>
          ))}
        </div>
      </div>

      {/* Block List */}
      <ScrollArea className="flex-1">
        <div className="p-4 space-y-2">
          {isLoading && (
            <div className="text-center text-muted-foreground py-8">
              Loading blocks...
            </div>
          )}

          {!isLoading && filteredBlocks.length === 0 && (
            <div className="text-center text-muted-foreground py-8">
              No blocks found
            </div>
          )}

          {!isLoading && filteredBlocks.map((block) => (
            <Card
              key={block.type}
              className="p-3 cursor-move hover:bg-muted/50 transition-colors"
              draggable
              onDragStart={(e) => onDragStart(e, block)}
            >
              <div className="flex items-start gap-3">
                <div className="h-10 w-10 rounded-lg bg-primary/10 flex items-center justify-center flex-shrink-0">
                  {block.icon || <BlocksIcon className="h-5 w-5 text-primary" />}
                </div>
                <div className="flex-1 min-w-0">
                  <h3 className="font-medium text-sm mb-1">{block.name}</h3>
                  <p className="text-xs text-muted-foreground line-clamp-2">
                    {block.description}
                  </p>
                </div>
              </div>
            </Card>
          ))}
        </div>
      </ScrollArea>
    </div>
  )
}
```

#### API Integration

Uses backend endpoint:
```
GET /api/v1/blocks
GET /api/v1/blocks/category/{category}
GET /api/v1/blocks/{block_type}
```

The backend already has these endpoints implemented with all 90 blocks!

---

## 🤖 Phase 4: Copilot Integration

### Feature: AI Copilot Sidebar

**Original Location**: `apps/sim/lib/copilot/` and `apps/sim/app/workspace/[workspaceId]/w/[workflowId]/components/panel-new/components/copilot/`

**New Location**:
- `services/frontend/src/lib/copilot/` (copy from apps/sim)
- `services/frontend/src/components/copilot/`

#### Files to Copy

```
SOURCE: apps/sim/lib/copilot/
├── prompts.ts                        → services/frontend/src/lib/copilot/prompts.ts
├── tools/                            → services/frontend/src/lib/copilot/tools/
├── api.ts                            → services/frontend/src/lib/copilot/api.ts (ADAPT)
└── types.ts                          → services/frontend/src/lib/copilot/types.ts

SOURCE: apps/sim/app/workspace/[workspaceId]/w/[workflowId]/components/panel-new/components/copilot/
├── components/
│   ├── copilot-message/              → services/frontend/src/components/copilot/Message/
│   ├── user-input/                   → services/frontend/src/components/copilot/UserInput/
│   └── copilot-suggestions/          → services/frontend/src/components/copilot/Suggestions/
├── hooks/
│   └── use-copilot.ts                → services/frontend/src/hooks/copilot/useCopilot.ts
└── copilot.tsx                       → services/frontend/src/components/copilot/CopilotPanel.tsx
```

#### Backend Requirements

Need to create these endpoints:
```python
# services/backend/app/api/v1/copilot.py

POST /api/v1/copilot/chat
  Request: { "message": string, "workflow_id": string, "context": {...} }
  Response: { "message": string, "suggestions": [...] }

POST /api/v1/copilot/generate-block
  Request: { "description": string, "workflow_id": string }
  Response: { "block": {...}, "explanation": string }

POST /api/v1/copilot/suggest-workflow
  Request: { "description": string }
  Response: { "workflow": {...}, "blocks": [...] }
```

#### Copilot Store

Already exists at: `services/frontend/src/stores/copilot/store.ts`

Needs to be connected to backend API.

---

## 📊 Phase 5: Additional Features

### 5.1 Knowledge Base

**Status**: Page exists (`KnowledgePage.tsx`), needs enhancement

**Features Needed**:
- File upload component
- Document list
- Vector search interface
- Document viewer

**Backend**: Endpoints already implemented

### 5.2 Templates

**Status**: Page exists (`TemplatesPage.tsx`), needs templates data

**Features Needed**:
- Template gallery
- Template preview
- "Use Template" button
- Template categories

**Backend**: Needs template endpoints

### 5.3 Execution Logs

**Status**: Page exists (`LogsPage.tsx`), needs real-time updates

**Features Needed**:
- Real-time log streaming (Socket.IO)
- Log filtering
- Execution timeline
- Error highlighting

**Backend**: Endpoints exist, Socket.IO implemented

---

## 🔌 API Integration Checklist

### Required API Calls (services/frontend/src/lib/api.ts)

Already Implemented ✅:
```typescript
// Workflows
export async function listWorkflows(): Promise<Workflow[]>
export async function getWorkflow(id: string): Promise<Workflow>
export async function createWorkflow(data: {...}): Promise<Workflow>
export async function updateWorkflow(id: string, data: {...}): Promise<Workflow>
export async function deleteWorkflow(id: string): Promise<void>
export async function executeWorkflow(id: string, data?: {...}): Promise<ExecutionResult>
```

Need to Implement ⏳:
```typescript
// Blocks
export async function listBlocks(): Promise<Block[]>
export async function getBlock(type: string): Promise<BlockDetails>
export async function getBlocksByCategory(category: string): Promise<Block[]>

// Copilot
export async function sendCopilotMessage(message: string, workflowId: string): Promise<CopilotResponse>
export async function generateBlock(description: string): Promise<GeneratedBlock>
export async function suggestWorkflow(description: string): Promise<WorkflowSuggestion>

// Templates
export async function listTemplates(): Promise<Template[]>
export async function getTemplate(id: string): Promise<Template>
export async function useTemplate(id: string): Promise<Workflow>

// Knowledge
export async function uploadDocument(file: File): Promise<Document>
export async function searchKnowledge(query: string): Promise<SearchResult[]>
```

---

## 📋 Migration Priority Order

### Week 1: Core Workflow Features
1. ✅ Docker setup
2. ✅ Environment configuration
3. ✅ Documentation
4. ⏳ **Workflow Canvas** (12-15 hours)
5. ⏳ **Block Palette** (8-10 hours)

### Week 2: AI Features
1. **Copilot Integration** (10-12 hours)
2. **Block Generation** (6-8 hours)
3. Test end-to-end workflows

### Week 3: Polish & Enhancement
1. Knowledge Base enhancement (8-10 hours)
2. Templates implementation (6-8 hours)
3. Real-time logs (8-10 hours)
4. Full E2E testing

---

## 🧪 Testing Strategy

### For Each Component

1. **Unit Tests**: Test component in isolation
2. **Integration Tests**: Test with stores and API
3. **E2E Tests**: Test complete user flows
4. **Visual Regression**: Test UI doesn't break

### Example Test

```typescript
// services/frontend/src/components/workflow/__tests__/WorkflowCanvas.test.tsx

import { render, screen } from '@testing-library/react'
import { WorkflowCanvas } from '../WorkflowCanvas'
import { ReactFlowProvider } from 'reactflow'

describe('WorkflowCanvas', () => {
  it('renders the canvas', () => {
    render(
      <ReactFlowProvider>
        <WorkflowCanvas />
      </ReactFlowProvider>
    )
    expect(screen.getByRole('region')).toBeInTheDocument()
  })

  it('loads workflow data', async () => {
    // Test implementation
  })
})
```

---

## 🎯 Success Metrics

### Phase Complete When:

**Workflow Canvas**:
- [ ] Canvas renders
- [ ] Blocks can be added
- [ ] Blocks can be connected
- [ ] Blocks can be configured
- [ ] Workflows save to backend
- [ ] Workflows execute successfully

**Block Palette**:
- [ ] All 90 blocks display
- [ ] Search works
- [ ] Category filter works
- [ ] Drag & drop works
- [ ] Blocks appear on canvas

**Copilot**:
- [ ] Chat interface works
- [ ] Messages send/receive
- [ ] Block generation works
- [ ] Suggestions display
- [ ] Integrates with workflow

---

**Last Updated**: November 15, 2025
**Next Feature**: Workflow Canvas Migration
**Estimated Completion**: 2-3 weeks
