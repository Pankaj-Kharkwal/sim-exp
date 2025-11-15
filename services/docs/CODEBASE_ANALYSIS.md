# Sim Monolith Codebase - Complete Feature Analysis

**Last Updated:** November 15, 2025  
**Analysis Focus:** Frontend app at `/apps/sim` - What's implemented vs. missing

---

## Executive Summary

The Sim application is a comprehensive **AI workflow builder and execution platform** with robust backend infrastructure. The frontend app structure is **INCOMPLETE** - several core features are implemented in backend/stores but **missing or inaccessible from the frontend UI**.

### Key Finding: Why Settings Returns 404
The Settings page exists in the **modal dialog** (SettingsModal component at `/w/components/sidebar/components-new/settings-modal`) but is **NOT accessible as a full route**. Instead, it's opened via a modal triggered from the sidebar footer.

---

## Part 1: Complete Feature List for Frontend App

### Core Features Implemented ✅

1. **Workflow Editor Canvas** 
   - React Flow-based visual workflow builder
   - Block drag-and-drop with 100+ block types
   - Edge connections between blocks
   - Loop and parallel block support
   - Auto-layout capability
   - Real-time collaborative editing

2. **Copilot (AI Assistant)**
   - Chat interface with streaming responses
   - Message history management
   - Context pills for workflow selection
   - File attachments support
   - Model selection (gpt-4o, gpt-4-turbo, etc.)
   - Mode selection (Build/Ask)
   - Tool calling with inline preview
   - Training data collection system

3. **Chat Interface**
   - Floating chat modal on canvas
   - Draggable and resizable
   - File upload/attachment support
   - Workflow output selection
   - Deployed chat pages (`/app/chat/[identifier]/`)
   - Voice interface support (ElevenLabs)
   - Auth options (password, email, SSO)

4. **Settings Modal**
   - General settings (UI preferences)
   - Environment variables management
   - Copilot API key management
   - Team/Organization settings
   - SSO configuration
   - Subscription management
   - Integration with settings store

5. **Templates**
   - Browse and search templates at `/workspace/[id]/templates`
   - Template categories (gallery, your, pending)
   - Star/favorite templates
   - Template details page with preview
   - Approve/reject workflow (superuser)

6. **Logs & Execution**
   - Execution logs page at `/workspace/[id]/logs`
   - Real-time execution monitoring
   - Log filtering and search
   - Workflow execution history
   - Terminal console output

7. **Knowledge Base**
   - Create and manage knowledge bases
   - Document upload and chunking
   - Vector search with embeddings
   - Tag-based filtering
   - Chunk editing interface
   - Knowledge page at `/workspace/[id]/knowledge/[id]`

8. **MCP (Model Context Protocol) Servers**
   - Server discovery and management
   - Tool selection from servers
   - Dynamic tool execution
   - Server health monitoring
   - Tool input/output handling

9. **Custom Tools**
   - Custom tool creation and management
   - Tool parameter configuration
   - Integration in tool-input component
   - Tool execution framework

10. **Workflow Management**
    - Create/edit/delete workflows
    - Workflow duplication
    - Folder organization
    - Workflow publishing
    - Webhook configuration

11. **Block Editor Panel**
    - Block configuration UI
    - Subblock editing
    - Code editor with Wand (AI generation)
    - Connection management
    - Advanced mode toggle
    - Documentation links

---

## Part 2: Key Feature Components Deep Dive

### 2.1 Copilot Implementation

#### Location
- **Main Component:** `/app/workspace/[workspaceId]/w/[workflowId]/components/panel-new/components/copilot/copilot.tsx`
- **UI Components:** `/app/workspace/[workspaceId]/w/[workflowId]/components/panel-new/components/copilot/components/`
  - `user-input/` - Message input with file attachment, mode/model selection
  - `copilot-message/` - Message display with markdown, streaming, reactions
  - `inline-tool-call/` - Tool execution preview and approval UI
  - `todo-list/` - Planning UI for multi-step operations
  - `welcome/` - Greeting screen with suggested prompts

#### Store
- **Location:** `/stores/panel-new/copilot/store.ts`
- **State Management:** Zustand with devtools
- **Key Methods:**
  - `setWorkflowId()` - Select active workflow
  - `sendMessage()` - Stream message to API
  - `abortMessage()` - Cancel in-flight requests
  - `clearMessages()` - Reset chat history
  - `loadChats()` - Load previous conversations

#### API Endpoints
| Endpoint | Purpose |
|----------|---------|
| `POST /api/copilot/chat` | Send message & get streaming response |
| `POST /api/copilot/tools` | Execute copilot tool call |
| `GET /api/copilot/keys` | Fetch user's copilot API keys |
| `POST /api/copilot/keys` | Generate new copilot key |
| `DELETE /api/copilot/keys/[id]` | Revoke copilot key |
| `POST /api/copilot/train` | Submit training data |

#### UI Components Tree
```
Copilot (main)
├── Header (with history dropdown)
├── ScrollArea (messages)
│  ├── CopilotMessage[] (with streaming, reactions)
│  │  ├── SmoothStreamingText
│  │  ├── MarkdownRenderer
│  │  ├── FileAttachmentDisplay
│  │  └── InlineToolCall[] (with Run/Skip buttons)
│  ├── TodoList (optional)
│  └── Welcome (initial state)
└── UserInput
   ├── Textarea with @mentions
   ├── ContextPills
   ├── ModelSelector
   ├── ModeSelector
   ├── AttachedFilesDisplay
   └── SendButton
```

#### Features Implemented
✅ Message history with conversation grouping  
✅ File attachments (images, PDFs, text)  
✅ Context selection (@workflow, @file, @knowledge)  
✅ Streaming response with smooth text animation  
✅ Tool execution with inline approval  
✅ Model selection (different reasoning models)  
✅ Mode selection (Build vs Ask mode)  
✅ Training data collection  
✅ Conversation recovery on page reload  

---

### 2.2 Block Generation with AI (Wand)

#### Location
- **Hook:** `/app/workspace/[workspaceId]/w/[workflowId]/hooks/use-wand.ts`
- **API Route:** `/app/api/wand-generate/route.ts`
- **UI Integration:** `sub-block.tsx` - Inline Wand prompts in editors

#### How It Works
1. User clicks Wand icon (✨) in code/JSON editor
2. Opens inline prompt bar with context
3. Sends request to `/api/wand-generate`
4. Streams generated code/JSON back to editor
5. User can accept or modify

#### Supported Contexts
- JavaScript/Python code generation
- JSON schema generation
- JSON object body generation
- SQL query generation
- Markdown content
- Configuration files

#### Configuration
```typescript
wandConfig = {
  enabled: true,
  prompt: "You are an expert programmer...",
  generationType: 'javascript-function-body' | 'json-object' | 'python-function-body',
  maintainHistory: true,
  placeholder: "Describe what you need..."
}
```

#### API Details
- **POST** `/api/wand-generate`
- **Input:** `{ prompt, systemPrompt, history[], stream, workflowId }`
- **Output:** Streaming or single response with generated content
- **Cost Tracking:** Integrated with user stats & billing

---

### 2.3 Workflow Builder Canvas

#### Location
- **Main Component:** `/app/workspace/[workspaceId]/w/[workflowId]/workflow.tsx`
- **Dependencies:** ReactFlow v11, Zustand store

#### Key Features
✅ 100+ block types from registry  
✅ Drag-and-drop block placement  
✅ Custom edge rendering (WorkflowEdge)  
✅ Loop and parallel block support  
✅ Subblock components (branches)  
✅ Webhook/trigger configuration  
✅ Auto-layout with smart spacing  
✅ Zoom and pan controls  
✅ Block execution debugging  
✅ Diff mode for version comparison  

#### State Management
- **Workflow Store:** `/stores/workflows/workflow/store.ts`
  - Blocks (nodes)
  - Edges (connections)
  - Loops and parallels
  - Execution state
  - Diff tracking

#### Node Types
```typescript
const nodeTypes = {
  workflowBlock: WorkflowBlock,      // Regular blocks
  subflowNode: SubflowNodeComponent,  // Loop/parallel
  noteBlock: NoteBlock,               // Documentation
}
```

#### Edge Types
```typescript
const edgeTypes = {
  default: WorkflowEdge,
  workflowEdge: WorkflowEdge,
}
```

---

### 2.4 Chat Interface/Chatbot Feature

#### Location A: Floating Chat on Canvas
- **Component:** `/app/workspace/[workspaceId]/w/[workflowId]/components/chat/chat.tsx`
- **Store:** `/stores/chat/store.ts`
- **Purpose:** Test workflows during development

#### Location B: Deployed Chat Pages
- **Component:** `/app/chat/[identifier]/chat.tsx`
- **Purpose:** Public-facing chat interface for deployed workflows

#### Features
✅ Draggable and resizable modal  
✅ File upload support (images, documents)  
✅ Workflow output selection  
✅ Message history per workflow  
✅ Voice input/output (ElevenLabs integration)  
✅ Multiple auth modes (public, password, email, SSO)  
✅ Real-time streaming responses  
✅ Conversation export (CSV)  

#### State Interfaces
```typescript
interface ChatMessage {
  id: string
  content: string | Record<string, unknown>
  workflowId: string
  type: 'user' | 'workflow'
  timestamp: string
  blockId?: string
  isStreaming?: boolean
  attachments?: ChatAttachment[]
}

interface ChatState {
  // UI State
  isChatOpen: boolean
  chatPosition: ChatPosition | null
  chatWidth: number
  chatHeight: number
  
  // Message State
  messages: ChatMessage[]
  selectedWorkflowOutputs: Record<string, string[]>
  conversationIds: Record<string, string>
  
  // Actions
  addMessage(message)
  clearChat(workflowId)
  setSelectedWorkflowOutput(workflowId, outputIds)
}
```

#### Workflow Execution Flow
1. User sends message in chat
2. Extracts selected workflow outputs
3. Prepares execution input with chat message + files
4. Calls workflow execution API
5. Streams response back to chat
6. Appends workflow output to message

---

### 2.5 Tools Management (MCP Servers & Custom Tools)

#### MCP Server Management

**Location:** `/app/api/mcp/` (backend routes)

**Store:** `/hooks/queries/mcp.ts`

**Tool Discovery Hook:** `/hooks/use-mcp-tools.ts`

**Features:**
✅ Server creation/deletion/update  
✅ Tool discovery from servers  
✅ Connection testing  
✅ Health monitoring  
✅ Caching with 5-minute auto-refresh  
✅ Dynamic tool schema loading  

**UI Components:**
- `MCP Server Selector` in tool-input
- `MCP Tool Selector` for picking specific tools
- `MCP Dynamic Args` for parameter configuration

#### Custom Tools

**Store Location:** `/stores/custom-tools/store.ts`

**Features:**
✅ Create custom tool definitions  
✅ Parameter schema validation  
✅ Tool execution via API proxy  
✅ Usage control (auto/manual)  

**Tool Selection Flow:**
```
ToolInput Component
├── Built-in Tools (100+ blocks)
├── MCP Tools (from servers)
├── Custom Tools (user-defined)
└── Search & Filter
```

#### API Endpoints
| Endpoint | Purpose |
|----------|---------|
| `GET /api/mcp/tools/discover?workspaceId=X` | List all tools |
| `POST /api/mcp/tools/execute` | Execute MCP tool |
| `GET /api/mcp/servers?workspaceId=X` | List servers |
| `POST /api/mcp/servers` | Create server |
| `DELETE /api/mcp/servers/[id]` | Delete server |
| `PUT /api/mcp/servers/[id]` | Update server |

---

### 2.6 Knowledge Base Management

#### Location
- **Page:** `/app/workspace/[workspaceId]/knowledge/[id]/base.tsx`
- **Store:** `/stores/knowledge/store.ts`
- **Hook:** `/hooks/use-knowledge.ts`
- **API:** `/app/api/knowledge/`

#### Features
✅ Create knowledge bases  
✅ Upload documents (PDF, TXT, DOCX, etc.)  
✅ Automatic chunking with configurable size  
✅ Vector embeddings (text-embedding-3-small)  
✅ Semantic search with vector similarity  
✅ Tag-based filtering (7 tag slots)  
✅ Document/chunk management UI  
✅ Token counting  
✅ Processing status tracking  

#### Knowledge Block in Workflows
```typescript
// Search by query
knowledge_search({
  knowledgeBaseId: string,
  query?: string,
  topK?: number,  // 1-100
  tagFilters?: { tagName, tagValue }[]
})
```

#### API Endpoints
| Endpoint | Purpose |
|----------|---------|
| `GET /api/knowledge` | List user's knowledge bases |
| `POST /api/knowledge` | Create knowledge base |
| `GET /api/knowledge/[id]` | Get knowledge base details |
| `PUT /api/knowledge/[id]` | Update knowledge base |
| `DELETE /api/knowledge/[id]` | Delete knowledge base |
| `POST /api/knowledge/[id]/documents` | Upload document |
| `POST /api/knowledge/search` | Search knowledge base |

---

### 2.7 Settings Page Implementation

#### Location (MODAL)
- **Modal Component:** `/app/workspace/[workspaceId]/w/components/sidebar/components-new/settings-modal/settings-modal.tsx`
- **Triggered from:** Footer navigation in sidebar
- **Access Point:** `FooterNavigation` component

#### Settings Sections

| Section | Component Location | Features |
|---------|-------------------|----------|
| **General** | `settings-modal/components/general/` | UI toggles, theme, display settings |
| **Environment** | `settings-modal/components/environment/` | Env var management |
| **Copilot** | `settings-modal/components/copilot/` | API key management |
| **Team/Org** | `settings-modal/components/organization/` | Team member management |
| **SSO** | `settings-modal/components/sso/` | Single sign-on config |
| **Subscription** | `settings-modal/components/subscription/` | Billing & plan info |

#### Why "Settings" Returns 404 as a Route
- **Settings is NOT a page route** (`/workspace/[id]/settings`)
- **It's a modal dialog** triggered from sidebar footer
- **Access:** Click gear icon in footer → Opens SettingsModal
- **Navigation Items:** Stored in `FooterNavigation` component
- **Pages Actually Available:**
  - ✅ `/workspace/[id]/` (workspace home)
  - ✅ `/workspace/[id]/w` (workflow list)
  - ✅ `/workspace/[id]/w/[id]` (workflow editor)
  - ✅ `/workspace/[id]/logs` (execution logs)
  - ✅ `/workspace/[id]/knowledge` (knowledge bases)
  - ✅ `/workspace/[id]/knowledge/[id]` (knowledge base detail)
  - ✅ `/workspace/[id]/templates` (workspace templates)
  - ❌ `/workspace/[id]/settings` (DOES NOT EXIST - use modal instead)

---

### 2.8 Workflow Execution & Logs

#### Execution System

**Hook:** `/app/workspace/[workspaceId]/w/[workflowId]/hooks/use-workflow-execution.ts`

**Executor:** `/executor/` directory with block execution logic

**Features:**
✅ Single workflow execution  
✅ Step-by-step debugging  
✅ Resume/pause execution  
✅ Variable tracking  
✅ Block output inspection  
✅ Execution timing  
✅ Error handling & recovery  

#### Logs Page

**Location:** `/app/workspace/[workspaceId]/logs/`

**Components:**
- `dashboard.tsx` - Overview with charts
- `logs.tsx` - Detailed log list
- `hooks/` - Log queries and filters

**Features:**
✅ Filter by workflow, status, date  
✅ Search logs by content  
✅ Real-time log streaming  
✅ Execution time metrics  
✅ Error stack traces  
✅ Export logs  

#### Console Output

**Store:** `/stores/logs/` (or panel store)

**Display:** Terminal-like console in execution view

**Features:**
✅ Real-time output streaming  
✅ Syntax highlighting  
✅ Error/warning/info levels  
✅ Copyable output  
✅ Clear console  

---

### 2.9 Templates Browsing

#### Location
- **Workspace Templates:** `/workspace/[id]/templates/`
- **Public Templates:** `/templates/`
- **Template Detail:** `/templates/[id]/`

#### Features
✅ Browse approved templates  
✅ Filter by category/tags  
✅ Search templates  
✅ Star/favorite templates  
✅ View template details  
✅ Quick-start from template  
✅ Clone template to workspace  
✅ Superuser approval workflow  

#### Data Structure
```typescript
interface Template {
  id: string
  workflowId: string
  name: string
  description?: string
  details?: { tagline?: string; about?: string }
  creator?: { name: string; avatar?: string }
  views: number
  stars: number
  status: 'approved' | 'pending' | 'rejected'
  tags?: string[]
  requiredCredentials?: string[]
  state: WorkflowState  // Full workflow definition
  isStarred: boolean
}
```

#### API Endpoints
| Endpoint | Purpose |
|----------|---------|
| `GET /api/templates` | List templates with filters |
| `GET /api/templates/[id]` | Get template details |
| `POST /api/templates` | Create/publish template |
| `POST /api/templates/[id]/star` | Star template |
| `DELETE /api/templates/[id]/star` | Unstar template |
| `PUT /api/templates/[id]/approve` | Approve (superuser) |

---

## Part 3: Architecture & Routes Analysis

### 3.1 Frontend Route Structure

```
/workspace/
├── [workspaceId]/
│   ├── page.tsx ..................... Workspace home
│   ├── w/ (workflows)
│   │   ├── page.tsx ................ List workflows
│   │   ├── [workflowId]/
│   │   │   ├── page.tsx ........... Workflow editor
│   │   │   ├── workflow.tsx ....... Canvas component
│   │   │   ├── components/
│   │   │   │   ├── control-bar/ .. Save/Run/Deploy controls
│   │   │   │   ├── panel-new/ ... Right panel (Copilot/Editor/Toolbar)
│   │   │   │   ├── chat/ ........ Floating chat modal
│   │   │   │   └── ...
│   │   │   └── hooks/
│   │   ├── layout.tsx .............. Layout wrapper
│   │   └── providers/
│   ├── logs/
│   │   ├── page.tsx ................ Execution logs page
│   │   ├── dashboard.tsx ......... Log dashboard
│   │   └── components/
│   ├── knowledge/
│   │   ├── page.tsx ................ Knowledge base list
│   │   └── [id]/
│   │       ├── base.tsx ........... Knowledge base editor
│   │       └── components/
│   ├── templates/
│   │   ├── page.tsx ................ Workspace templates
│   │   └── templates.tsx ......... Template list component
│   └── layout.tsx ................. Workspace layout (with sidebar)
├── layout.tsx ................... Global layout
└── page.tsx ................... Workspace selector

/chat/
├── [identifier]/
│   ├── page.tsx .................. Deployed chat page
│   └── chat.tsx .................. Chat client component

/templates/
├── page.tsx ..................... Public templates
├── [id]/
│   └── page.tsx ................. Template detail

/settings/
└── (NOT A ROUTE - Use modal instead)
```

### 3.2 Backend API Routes (Most Relevant)

```
/api/
├── copilot/
│   ├── chat .................... LLM chat endpoint
│   ├── tools ................... Tool execution
│   ├── keys .................... Key management
│   └── train ................... Training data
├── workflows/
│   ├── [id]/autolayout ....... Auto-layout canvas
│   ├── [id]/publish .......... Publish workflow
│   ├── [id]/preview .......... Preview deployment
│   ├── [id]/logs ............. Execution logs
│   └── yaml/convert .......... YAML generation
├── knowledge/
│   ├── search .................. Vector search
│   ├── [id]/documents ........ Document management
│   └── [id]/chunks ........... Chunk management
├── mcp/
│   ├── tools/discover ....... Find MCP tools
│   ├── tools/execute ........ Run MCP tool
│   └── servers ............... Server management
├── chat/
│   ├── config ................. Get chat config
│   └── [identifier] .......... Chat execution
├── templates/
│   ├── [id]/star ............ Star/unstar
│   ├── [id]/approve ........ Template approval
│   └── [id]/clone .......... Clone to workspace
├── execution/
│   ├── [id]/run ............. Execute workflow
│   ├── [id]/debug/step ..... Debug step
│   └── logs .................. Fetch logs
├── wand-generate .............. AI generation
├── files/ .................... File upload
└── [many more]
```

### 3.3 Store Architecture (State Management)

```
/stores/
├── workflows/
│   ├── workflow/ .............. Current workflow state
│   ├── registry/ .............. Workspace workflows list
│   └── subblock/ .............. Loop/parallel blocks
├── panel-new/
│   ├── copilot/ ............... Copilot chat state
│   ├── editor/ ................ Block editor state
│   └── panel/ ................. Panel open/close state
├── chat/ ....................... Floating chat state
├── logs/ ....................... Execution logs
├── settings/
│   ├── general/ ............... User settings
│   ├── copilot/ ............... Copilot keys
│   └── organization/ .......... Team settings
├── knowledge/ .................. Knowledge base state
├── custom-tools/ ............... Custom tool definitions
├── execution/ .................. Workflow execution state
└── [many more]
```

---

## Part 4: What's Implemented vs. Missing

### ✅ Fully Implemented

| Feature | Status | Notes |
|---------|--------|-------|
| Copilot Chat | ✅ Complete | Full UI, streaming, file attachments |
| Block Editor | ✅ Complete | 100+ blocks, subflows, connections |
| Workflow Canvas | ✅ Complete | ReactFlow-based, auto-layout |
| Execution/Debugging | ✅ Complete | Step-by-step, variable tracking |
| Chat Interface | ✅ Complete | Floating + deployed pages |
| Settings Modal | ✅ Complete | All tabs: general, env, copilot, etc. |
| Logs Page | ✅ Complete | Dashboard, filtering, export |
| Knowledge Base | ✅ Complete | Upload, search, chunking, tagging |
| Templates | ✅ Complete | Browse, star, approve |
| MCP Tools | ✅ Complete | Discovery, execution, management |
| Custom Tools | ✅ Complete | Creation, integration |
| Wand (AI Gen) | ✅ Complete | Code, JSON, inline in editors |
| Folder Organization | ✅ Complete | Nested folders in sidebar |
| Workflow Publishing | ✅ Complete | Deploy, webhook, chat endpoints |

### ⚠️ Partially Implemented

| Feature | Status | Details |
|---------|--------|---------|
| Training Controls | ⚠️ Optional | Gated behind env var, for copilot training |
| Voice Chat | ⚠️ Optional | ElevenLabs integration, in chat pages |
| SSO Settings | ⚠️ Partial | UI exists, backend varies by deployment |
| Templates Approval | ⚠️ Superuser Only | Limited to superuser accounts |

### ❌ Missing / Not Accessible

| Feature | Status | Why |
|---------|--------|-----|
| Settings as Route | ❌ N/A | Only available as modal dialog |
| Standalone Settings Page | ❌ Not Built | Use modal from `/w/` pages |
| Advanced Diff Mode | ⚠️ Limited | Exists but not fully exposed |

---

## Part 5: Why Core Features Aren't "Visible"

### Problem 1: Settings Returning 404
**Root Cause:** Settings isn't a route, it's a modal dialog.

**Current Flow:**
```
User in /workspace/[id]/w/[workflowId]
  → Clicks gear icon in sidebar footer
  → Triggers SettingsModal (dialog)
  → Opens full-screen settings overlay
```

**Why Not a Route:**
- Workflow editor needs persistent state
- Modal preserves workflow state while settings are open
- Design choice to keep as part of workspace layout

**Solution If Wanting a Route:**
Would need to create `/workspace/[id]/settings/` page with layout preservation

### Problem 2: Copilot Not Visible on Landing
**Root Cause:** Copilot only appears inside workflow editor.

**Access Path:**
1. Go to workspace
2. Create or open workflow
3. Click "Copilot" tab in right panel
4. Copilot interface appears

**Why Not on Landing:**
- Copilot needs active workflow context
- Doesn't make sense without workflow to edit
- Intentional design

### Problem 3: Chat Seems Hidden
**Root Cause:** There are TWO different chat interfaces.

**1. Floating Chat (Development):**
- Location: Workflow canvas
- Click chat bubble icon → opens floating modal
- For testing workflows

**2. Deployed Chat (Public):**
- Location: `/chat/[identifier]/`
- Accessed via public URL
- After workflow is deployed with "Chat" deployment

### Problem 4: Templates and Logs Need Navigation
**Root Cause:** These are separate pages requiring navigation.

**Access:**
- From sidebar footer: Click database/layout icons
- Or direct URL: `/workspace/[id]/logs` or `/workspace/[id]/templates`

---

## Part 6: Block Registry (100+ Blocks)

### Block Categories

```
Triggers:
  - start (unified trigger)
  - api_trigger (webhook)
  - schedule_trigger
  - email_trigger
  - chat_trigger (legacy)

Actions:
  - api (HTTP requests)
  - function (JavaScript/Python)
  - condition (if/else)
  - loop (iterate)
  - parallel (concurrent)
  - human_in_the_loop

Integrations (100+):
  - slack, gmail, teams, discord
  - stripe, airtable, notion
  - google_docs, google_sheets, google_drive
  - github, jira, asana
  - openai, anthropic, huggingface
  - supabase, firebase, mongodb
  - zapier, make, n8n
  - ... and many more

Data:
  - knowledge (vector search)
  - file (upload/process)
  - database (SQL query)

Output:
  - response (return value)
  - log (console output)
```

### Registry Location
- **File:** `/blocks/registry.ts`
- **Block Definitions:** `/blocks/blocks/[block-type].ts`
- **Block Types:** `/blocks/types.ts`

---

## Part 7: Key Implementation Details

### Streaming Responses

**Copilot Messages:**
```typescript
// Server sends chunked text responses
// Client uses:
// - SmoothStreamingText for animated rendering
// - Real-time HTML parsing for markdown
// - Type-safe chunk handling
```

**Wand Generation:**
```typescript
// POST /api/wand-generate
// Returns: { content: string } or stream
// Updates editor in real-time
```

### Vector Search (Knowledge Base)

```typescript
// Automatic embedding on upload:
// 1. Chunk document (smart sizing)
// 2. Embed each chunk (OpenAI text-embedding-3-small)
// 3. Store in pgvector
// 4. Enable semantic search

// Search query:
knowledge_search({
  knowledgeBaseId: "kb_xyz",
  query: "user question",
  topK: 10,  // return top 10 similar chunks
  tagFilters: [{ tag1: "category", tagValue: "product" }]
})
```

### Workflow Publishing

**Chat Deployment:**
```typescript
// Creates public endpoint: /chat/[identifier]
// Configuration:
{
  identifier: string,        // Public URL
  title: string,            // Chat window title
  authType: 'public' | 'password' | 'email' | 'sso',
  selectedOutputBlocks: string[],  // Which outputs to show
  welcomeMessage: string
}
```

### Custom Tool Integration

```typescript
// Tool execution flow:
1. Tool selected in block config
2. Parameters mapped to block inputs
3. At runtime: tools/index.ts routes execution
4. For MCP tools: /api/mcp/tools/execute
5. For custom tools: Custom handler
6. Results returned to workflow
```

---

## Part 8: Dependencies & Tech Stack

### Frontend
- **Framework:** Next.js 15 (App Router)
- **UI:** React 19, TypeScript
- **Canvas:** ReactFlow v11
- **State:** Zustand with devtools
- **Styling:** Tailwind CSS
- **Components:** Shadcn/ui (custom components in `/components/ui`)
- **Markdown:** Multiple renderers for different contexts
- **Forms:** React Hook Form, Zod validation
- **HTTP:** Fetch API, streaming support

### Backend Integration
- **Streaming:** ReadableStream API
- **Authentication:** Next-auth v5
- **Database:** Drizzle ORM with PostgreSQL
- **Vector DB:** pgvector extension
- **LLM APIs:** OpenAI, Azure OpenAI, Anthropic, Hugging Face
- **File Upload:** Multipart form data
- **Webhooks:** Custom handlers per block type

---

## Part 9: Recommended Improvements

### If Adding Settings as a Route
```
/workspace/[id]/settings/
├── page.tsx ................... Settings page
├── layout.tsx ................. Settings layout (with nav sidebar)
├── general/ ................... General settings
├── environment/ ............... Env vars
├── copilot/ ................... Copilot keys
├── organization/ .............. Team
├── sso/ ....................... SSO config
└── subscription/ .............. Billing
```

### If Making Copilot Standalone
- Would need workflow selection dropdown
- History panel for past conversations
- Could be modal OR page

### If Improving Discovery
- Add onboarding tour
- Highlight features in first-time user flow
- Contextual help (? icons)
- Feature flags for beta features

---

## Part 10: File Structure Summary

```
/apps/sim/
├── app/ (Next.js App Router)
│   ├── api/ (Backend routes)
│   ├── workspace/ (Main app)
│   ├── chat/ (Public chat)
│   ├── templates/ (Template browsing)
│   ├── (auth)/ (Login/signup)
│   └── (landing)/ (Marketing)
├── blocks/ (Block definitions)
├── components/ (React components)
├── contexts/ (React contexts)
├── executor/ (Workflow execution)
├── hooks/ (React hooks)
├── lib/ (Utilities)
│   ├── workflows/
│   ├── knowledge/
│   ├── mcp/
│   ├── auth/
│   └── ...
├── providers/ (Next.js providers)
├── serializer/ (JSON serialization)
├── services/ (Business logic)
├── socket-server/ (WebSockets)
├── stores/ (Zustand stores)
├── tools/ (Tool definitions)
├── triggers/ (Trigger types)
└── public/ (Static files)
```

---

## Conclusion

The Sim frontend app is **feature-complete for core functionality**. The apparent "missing" features (Settings, Copilot visibility, Chat) are actually:

1. **Settings** - Accessible via modal, not as a route
2. **Copilot** - Intentionally contextual to workflow editor
3. **Chat** - Two separate UIs (dev floating, public deployed)
4. **Templates/Logs** - Available but require navigation

All infrastructure exists for:
- ✅ AI-powered workflow building
- ✅ Real-time execution & debugging  
- ✅ Vector search (knowledge bases)
- ✅ Tool integration (MCP + custom)
- ✅ Public deployment & chat
- ✅ Team collaboration

The codebase is well-organized, properly typed, and follows React best practices throughout.
