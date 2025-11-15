# Comprehensive Migration Plan: apps/sim → services/

## Executive Summary

This document outlines the complete migration strategy for moving from the monolithic **Sim** application to the microservices-based **Pankh.AI** platform.

---

## Current Status

### ✅ Completed (Backend)
- FastAPI backend with 80+ endpoints
- 90/90 workflow blocks migrated (automated!)
- SQLAlchemy models + Alembic migrations
- Celery + Redis workers
- Socket.IO real-time service
- LangGraph workflow executor
- Docker infrastructure

### ⚠️ Partially Complete (Frontend)
- React + Vite setup ✅
- UI components (shadcn/ui) ✅
- Basic routing ✅
- Pages structure ✅
- Zustand stores ✅
- API integration layer ✅
- **Missing**: Complex workflow editor components
- **Missing**: Copilot integration
- **Missing**: Block palette & canvas

---

## Migration Roadmap

### Phase 1: Core Infrastructure ✅ DONE
- [x] Backend API setup
- [x] Database models
- [x] Frontend scaffolding
- [x] Docker Compose
- [x] CI/CD basics

### Phase 2: Essential Features (IN PROGRESS)
Priority order for migration:

#### 2.1 Workflow Editor Canvas 🎯 HIGH PRIORITY
**Source**: `apps/sim/app/workspace/[workspaceId]/w/[workflowId]/`

**Components to Migrate**:
```
workflow.tsx                    → services/frontend/src/components/workflow/WorkflowCanvas.tsx
components/workflow-edge/       → services/frontend/src/components/workflow/Edge/
components/panel-new/           → services/frontend/src/components/workflow/BlockPanel/
components/note-block/          → services/frontend/src/components/workflow/NoteBlock.tsx
components/subflows/            → services/frontend/src/components/workflow/Subflows/
```

**Hooks to Migrate**:
```
hooks/use-node-utilities.ts           → services/frontend/src/hooks/workflow/
hooks/use-block-connections.ts        → services/frontend/src/hooks/workflow/
hooks/use-block-dimensions.ts         → services/frontend/src/hooks/workflow/
hooks/use-current-workflow.ts         → services/frontend/src/hooks/workflow/
hooks/use-workflow-execution.ts       → services/frontend/src/hooks/workflow/
hooks/use-auto-layout.ts              → services/frontend/src/hooks/workflow/
```

**Action Items**:
1. Create `services/frontend/src/components/workflow/` directory
2. Migrate ReactFlow workflow canvas component
3. Migrate block node components
4. Migrate edge components
5. Update imports to use new API layer
6. Test drag & drop functionality
7. Test block connections
8. Test auto-layout

**Estimated Time**: 12-15 hours

---

#### 2.2 Block Palette & Library 🎯 HIGH PRIORITY
**Source**: `apps/sim/blocks/blocks/` (UI configs)

**Components to Create**:
```
services/frontend/src/components/blocks/
├── BlockPalette.tsx           # Searchable block library sidebar
├── BlockCard.tsx              # Individual block preview
├── BlockSearch.tsx            # Search/filter functionality
├── BlockCategories.tsx        # Category navigation
└── BlockDragPreview.tsx       # Drag preview component
```

**Backend Integration**:
- Use `/api/v1/blocks` endpoint for block metadata
- Use `/api/v1/blocks/{block_type}` for block details
- Use `/api/v1/blocks/category/{category}` for filtering

**Action Items**:
1. Create BlockPalette component
2. Integrate with backend blocks API
3. Implement search/filter
4. Implement drag-and-drop to canvas
5. Add block categorization
6. Add block documentation tooltips

**Estimated Time**: 8-10 hours

---

#### 2.3 Copilot Integration 🎯 HIGH PRIORITY
**Source**: `apps/sim/lib/copilot/` and `apps/sim/app/workspace/[workspaceId]/w/[workflowId]/components/panel-new/components/copilot/`

**Components to Migrate**:
```
apps/sim/lib/copilot/                              → services/frontend/src/lib/copilot/
apps/sim/.../copilot/components/                   → services/frontend/src/components/copilot/
apps/sim/.../copilot/hooks/                        → services/frontend/src/hooks/copilot/
```

**Key Files**:
- `prompts.ts` - System prompts
- `api.ts` - Copilot API integration
- `tools.ts` - Tool definitions
- `CopilotChat.tsx` - Chat interface
- `CopilotMessage.tsx` - Message component
- `UserInput.tsx` - Input component

**Backend Integration**:
- Create `/api/v1/copilot/chat` endpoint
- Create `/api/v1/copilot/generate-block` endpoint
- Create `/api/v1/copilot/suggest-workflow` endpoint
- Use LangGraph for agent orchestration

**Action Items**:
1. Copy copilot lib to new frontend
2. Create CopilotPanel component
3. Integrate with new backend API
4. Add to workspace layout
5. Connect to workflow context
6. Test block generation
7. Test workflow suggestions

**Estimated Time**: 10-12 hours

---

#### 2.4 Block Generation AI 🤖 MEDIUM PRIORITY
**Source**: `apps/sim/lib/copilot/tools/blocks/`

**Backend Implementation**:
```python
# services/backend/app/api/v1/ai_blocks.py
POST /api/v1/ai/generate-block
  Request: { "description": "A block that sends emails", "context": {...} }
  Response: { "block_type": "email", "config": {...}, "code": "..." }
```

**Frontend Component**:
```typescript
// services/frontend/src/components/ai/BlockGenerationDialog.tsx
- Input: User description
- Processing: Show loading state
- Output: Block preview + "Add to Workflow" button
```

**Action Items**:
1. Implement backend AI block generation
2. Create frontend dialog component
3. Add "Generate Block" button to palette
4. Implement block preview
5. Add to workflow functionality
6. Add error handling

**Estimated Time**: 6-8 hours

---

### Phase 3: Enhanced Features (NEXT)

#### 3.1 Knowledge Base
**Source**: `apps/sim/app/workspace/[workspaceId]/knowledge/`

**Migration**:
- `KnowledgePage.tsx` (already exists, enhance)
- Add file upload functionality
- Add document parsing
- Add vector search
- Backend: `/api/v1/knowledge/*` endpoints

**Estimated Time**: 8-10 hours

---

#### 3.2 Templates
**Source**: `apps/sim/app/workspace/[workspaceId]/templates/`

**Migration**:
- `TemplatesPage.tsx` (already exists, enhance)
- Add template gallery
- Add template preview
- Add "Use Template" functionality
- Backend: `/api/v1/templates/*` endpoints

**Estimated Time**: 6-8 hours

---

#### 3.3 Execution Logs & Monitoring
**Source**: `apps/sim/app/workspace/[workspaceId]/logs/`

**Migration**:
- `LogsPage.tsx` (already exists, enhance)
- Add real-time log streaming
- Add log filtering
- Add execution timeline
- Connect to Socket.IO for live updates

**Estimated Time**: 8-10 hours

---

### Phase 4: Advanced Features (LATER)

#### 4.1 Chat Interface
**Source**: `apps/sim/app/chat/`

**Status**: `ChatPage.tsx` exists but isolated

**Migration**:
- Integrate chat into workspace context
- Add workflow execution from chat
- Add file uploads
- Add conversation history
- Backend: Chat endpoints already exist

**Estimated Time**: 10-12 hours

---

#### 4.2 Collaboration Features
**Source**: `apps/sim/app/workspace/[workspaceId]/w/[workflowId]/components/cursors/`

**Migration**:
- Real-time cursors
- User presence
- Collaborative editing
- Comments system
- Backend: Socket.IO already implemented

**Estimated Time**: 12-15 hours

---

## Component Migration Reference

### From apps/sim → services/frontend

| Original Path | New Path | Priority | Status |
|--------------|----------|----------|--------|
| `app/workspace/[workspaceId]/w/[workflowId]/workflow.tsx` | `components/workflow/WorkflowCanvas.tsx` | 🔴 HIGH | ⏳ TODO |
| `app/workspace/[workspaceId]/w/[workflowId]/components/panel-new/` | `components/workflow/BlockPanel/` | 🔴 HIGH | ⏳ TODO |
| `lib/copilot/` | `lib/copilot/` | 🔴 HIGH | ⏳ TODO |
| `app/workspace/[workspaceId]/w/[workflowId]/components/copilot/` | `components/copilot/` | 🔴 HIGH | ⏳ TODO |
| `blocks/blocks/` (UI) | `components/blocks/` | 🟡 MEDIUM | ⏳ TODO |
| `app/workspace/[workspaceId]/knowledge/` | `pages/KnowledgePage.tsx` | 🟡 MEDIUM | 🟡 PARTIAL |
| `app/workspace/[workspaceId]/templates/` | `pages/TemplatesPage.tsx` | 🟡 MEDIUM | 🟡 PARTIAL |
| `app/workspace/[workspaceId]/logs/` | `pages/LogsPage.tsx` | 🟡 MEDIUM | 🟡 PARTIAL |
| `app/chat/` | `pages/ChatPage.tsx` | 🟢 LOW | 🟡 PARTIAL |

---

## Store Migration

### Zustand Stores to Enhance

```typescript
// Already exist - need backend integration
services/frontend/src/stores/
├── workflowStore.ts        ✅ Complete - Already integrated with API
├── copilot/store.ts        ⏳ Needs backend integration
├── execution/store.ts      ⏳ Needs real-time updates
└── subscription/store.ts   ⏳ Needs backend integration
```

### New Stores Needed

```typescript
services/frontend/src/stores/
├── blockStore.ts           # Block palette & library state
├── canvasStore.ts          # Canvas state (zoom, pan, selection)
├── collaborationStore.ts   # Real-time collaboration state
└── knowledgeStore.ts       # Knowledge base state
```

---

## Backend API Coverage

### ✅ Implemented
- `/api/v1/workflows/*` - Full CRUD
- `/api/v1/blocks` - Block metadata
- `/api/v1/executions/*` - Execution tracking
- `/api/v1/tasks/*` - Task monitoring
- `/api/v1/auth/*` - Basic auth
- `/api/v1/billing/*` - Billing stubs

### ⏳ Needs Implementation
- `/api/v1/copilot/*` - AI assistant
- `/api/v1/ai/generate-block` - Block generation
- `/api/v1/templates/*` - Template management
- `/api/v1/knowledge/*` - Knowledge base
- `/api/v1/collaboration/*` - Real-time collab

---

## Testing Strategy

### Unit Tests
- [ ] Backend API endpoints
- [ ] Frontend components
- [ ] Zustand stores
- [ ] Utility functions

### Integration Tests
- [ ] Workflow creation flow
- [ ] Workflow execution flow
- [ ] Block drag & drop
- [ ] Real-time updates

### E2E Tests
- [ ] Complete workflow building
- [ ] Copilot interaction
- [ ] Knowledge base usage
- [ ] Template usage

---

## Timeline Estimate

| Phase | Features | Time Estimate | Complexity |
|-------|----------|---------------|------------|
| Phase 2.1 | Workflow Canvas | 12-15 hours | 🔴 High |
| Phase 2.2 | Block Palette | 8-10 hours | 🟡 Medium |
| Phase 2.3 | Copilot | 10-12 hours | 🔴 High |
| Phase 2.4 | Block Gen AI | 6-8 hours | 🟡 Medium |
| Phase 3 | Enhanced Features | 20-25 hours | 🟡 Medium |
| Phase 4 | Advanced Features | 22-27 hours | 🔴 High |
| **Total** | **Complete Migration** | **78-97 hours** | - |

**Estimated Calendar Time**: 2-3 weeks with 1-2 developers

---

## Success Criteria

### Phase 2 Complete
- [ ] Can create workflows via UI
- [ ] Can drag blocks onto canvas
- [ ] Can connect blocks
- [ ] Can execute workflows
- [ ] Copilot accessible in workspace
- [ ] Can generate blocks with AI

### Phase 3 Complete
- [ ] Knowledge base functional
- [ ] Templates available
- [ ] Execution logs real-time
- [ ] All pages connected

### Phase 4 Complete
- [ ] Chat integrated with workflows
- [ ] Real-time collaboration working
- [ ] Feature parity with monolith
- [ ] Production ready

---

## Next Actions

### Immediate (This Week)
1. ✅ Create Docker Compose setup
2. ✅ Create backend .env file
3. ⏳ Start services and verify connectivity
4. ⏳ Begin workflow canvas migration
5. ⏳ Test workflow creation end-to-end

### Short Term (Next Week)
1. Complete workflow canvas
2. Implement block palette
3. Start Copilot integration
4. Test workflow execution

### Medium Term (Week 3)
1. Complete Copilot integration
2. Implement block generation
3. Enhance knowledge base
4. Enhance templates

---

## Dependencies

### Required for All Features
- Docker & Docker Compose
- PostgreSQL 17 with pgvector
- Redis 7
- Node.js 18+ (frontend)
- Python 3.11+ (backend)

### Optional (for enhanced features)
- OpenAI API key (for AI features)
- Anthropic API key (for Claude)
- Azure/AWS storage (for files)
- Resend API key (for emails)

---

## Risk Assessment

| Risk | Impact | Mitigation |
|------|--------|------------|
| ReactFlow breaking changes | High | Pin versions, test thoroughly |
| Real-time sync issues | Medium | Use Socket.IO rooms, test with multiple clients |
| AI API costs | Medium | Implement rate limiting, caching |
| Complex state management | Medium | Use Zustand devtools, comprehensive tests |
| Performance with large workflows | High | Implement virtualization, lazy loading |

---

## Resources

### Documentation References
- `services/docs/README.md` - Architecture comparison
- `services/docs/FINAL_REPORT.md` - Testing results
- `services/docs/MIGRATION_STATUS.md` - Current progress
- `services/docs/architecture.md` - Architecture decisions

### Code References
- `apps/sim/` - Original implementation
- `services/backend/` - New backend
- `services/frontend/` - New frontend

---

**Last Updated**: November 15, 2025
**Status**: Phase 2 In Progress
**Next Milestone**: Workflow Canvas Migration Complete
