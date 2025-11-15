# Quick Dev Reference - Sim Frontend Fixes

## 🚀 Current Status
- Settings page: ✅ FIXED
- Workflow creation: ❌ NEEDS FIX
- Workflow editor: ❌ NEEDS FIX
- Copilot integration: ❌ NEEDS FIX

---

## 🎯 Priority Fixes

### #1: Make "New Workflow" Button Work
**File**: `services/frontend/src/pages/WorkflowsListPage.tsx`

```typescript
// Look for: New Workflow button handler
// Add: Dialog state management
// Implement: Create dialog component

const [isCreateDialogOpen, setIsCreateDialogOpen] = useState(false)

const handleCreateWorkflow = () => {
  setIsCreateDialogOpen(true)
}

// Render dialog with form to:
// - Get workflow name
// - Set description (optional)
// - Select initial block (optional)
// - Call API to create workflow
```

### #2: Make Workflow Cards Clickable
**File**: `services/frontend/src/pages/WorkflowsListPage.tsx`

```typescript
// Add onClick to workflow cards:
const handleOpenWorkflow = (workflowId: string) => {
  navigate(`/workspace/${workspaceId}/w/${workflowId}`)
}

// Make cards clickable:
<div 
  onClick={() => handleOpenWorkflow(workflow.id)}
  className="cursor-pointer hover:shadow-lg ..."
>
  {/* workflow card content */}
</div>
```

### #3: Fix Credentials Error
**File**: `services/frontend/src/services/` (auth service)

```typescript
// Check that:
// 1. Auth token is in localStorage/cookies
// 2. Token is sent in API request headers
// 3. Backend validates token correctly

// Verify in API calls:
const headers = {
  'Authorization': `Bearer ${token}`,
  'Content-Type': 'application/json'
}
```

### #4: Add Chat to Workspace Navigation
**File**: `services/frontend/src/components/` (workspace layout)

```typescript
// Add Chat/Copilot link to sidebar:
const navItems = [
  { label: 'Home', path: '/workspace/default' },
  { label: 'Workflows', path: '/workspace/default/workflows' },
  { label: 'Chat', path: '/chat' },  // ADD THIS
  // ... other items
]
```

---

## 🧪 Testing Workflow

After each fix:
1. Restart dev server (npm run dev)
2. Test in browser
3. Check browser console for errors
4. Update checklist below

---

## 📋 Implementation Checklist

```
PRIORITY 1 (Must have for basic functionality):
[ ] New Workflow button opens dialog
[ ] Can create workflow via dialog
[ ] Workflow cards are clickable
[ ] Workflow editor loads when clicked
[ ] Credentials validation works
[ ] Chat accessible from workspace

PRIORITY 2 (Core features):
[ ] Block canvas renders
[ ] Block palette available
[ ] Can drag blocks to canvas
[ ] Can connect blocks
[ ] Can configure block properties

PRIORITY 3 (AI features):
[ ] Copilot chat in workflow editor
[ ] AI block generation
[ ] Tool suggestions from Copilot
[ ] Workflow execution

PRIORITY 4 (Polish):
[ ] Performance optimization
[ ] Error handling improvements
[ ] UI/UX refinements
[ ] Testing coverage
```

---

## 🔍 Key Components

### Pages
- `WorkflowsListPage.tsx` - Workflow list (needs: create dialog + clickable cards)
- `WorkflowEditorPage.tsx` - Workflow editor (needs: test if loads)
- `ChatPage.tsx` - Copilot chat (needs: integration with workspace)
- `SettingsPage.tsx` - Settings (✅ DONE)

### Services
- Auth service - Handle authentication
- API service - Make HTTP calls
- Storage service - Local data caching

### Components
- Dialog/Modal - For workflow creation
- Canvas - For workflow visualization
- BlockPalette - For available blocks
- BlockProperties - For configuration

---

## 🗂️ File Structure Reference

```
services/frontend/src/
├── pages/
│   ├── WorkflowsListPage.tsx      ← FIX: New Workflow dialog
│   ├── WorkflowEditorPage.tsx      ← TEST: Editor loads
│   ├── ChatPage.tsx                ← FIX: Integration
│   ├── SettingsPage.tsx            ✅ DONE
│   └── ...
├── components/
│   ├── WorkflowCanvas/             ← Needed
│   ├── BlockPalette/               ← Needed
│   ├── Dialog/                     ← Needed for workflow creation
│   └── ...
├── services/
│   ├── api.ts                      ← API calls
│   ├── auth.ts                     ← Authentication
│   └── ...
├── routes.tsx                      ✅ DONE (added settings)
└── ...
```

---

## 🐛 Known Issues to Fix

1. **Settings Page 404** → ✅ FIXED
2. **New Workflow Dialog** → TO DO
3. **Workflow Navigation** → TO DO
4. **Credentials Error** → TO DO
5. **Missing Copilot Integration** → TO DO
6. **No Block Generation** → TO DO

---

## 📞 Backend APIs Needed

For full functionality, backend must provide:

```
GET /api/workflows                    - List workflows
POST /api/workflows                   - Create workflow
GET /api/workflows/:id                - Get workflow details
PUT /api/workflows/:id                - Update workflow
DELETE /api/workflows/:id             - Delete workflow

GET /api/blocks                       - List available blocks
POST /api/blocks/generate            - Generate block from AI

POST /api/chat/messages              - Send chat message
GET /api/chat/history/:id            - Get conversation history

GET /api/workspace/settings          - Get settings
PUT /api/workspace/settings          - Update settings
GET/POST /api/workspace/api-keys     - Manage API keys
```

---

## 💡 Tips

1. **Check Console**: Always check browser dev console for actual errors
2. **Use Network Tab**: Monitor API calls to see what's being sent/received
3. **React DevTools**: Use React DevTools extension to inspect component state
4. **Restart Server**: Always restart dev server after code changes
5. **Clear Cache**: Clear browser cache if changes don't appear
6. **Check Routes**: Verify routes.tsx has all necessary routes

---

## 📚 Reference Docs

See `services/docs/` for detailed information:
- `COMPLETE_FEATURE_ANALYSIS.md` - Full feature breakdown
- `CRITICAL_FIXES_PLAN.md` - Detailed fix plan
- `MISSING_FEATURES_ANALYSIS.md` - Feature gaps
- `README.md` - Original documentation

---

**Last Updated**: November 15, 2025  
**Status**: Mid-development - Settings fixed, 5 more critical issues to address
