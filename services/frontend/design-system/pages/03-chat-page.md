# Chat Page Design

> **Routes**: `/chat`, `/chat/:identifier`
> **Type**: Standalone chat interface
> **Goal**: Clean, distraction-free AI conversation experience

---

## 🎯 Layout Overview

```
┌──────────────────────────────────────────────────────────────────┐
│  HEADER (Sticky)                                    [User Menu]  │
├──────────┬──────────────────────────────────────────┬────────────┤
│          │                                          │            │
│          │                                          │  CONTEXT   │
│  CONV    │         CHAT MESSAGES                    │  PANEL     │
│  LIST    │                                          │            │
│          │  ┌───────────────────────────┐           │  - Sources │
│  [+New]  │  │ User: Hello               │           │  - Tools   │
│          │  └───────────────────────────┘           │  - Files   │
│  • Conv1 │                                          │  - Vars    │
│  • Conv2 │  ┌───────────────────────────┐           │  - Settings│
│  • Conv3 │  │ AI: Hi! How can I help?   │           │            │
│          │  └───────────────────────────┘           │            │
│          │                                          │            │
│          │                                          │            │
│          │                                          │            │
├──────────┴──────────────────────────────────────────┴────────────┤
│  MESSAGE COMPOSER                                                │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │ Type a message... [Attach] [Tools] [Mode]        [Send]    │  │
│  └────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────┘
```

**Dimensions**:
- Left sidebar: 280px (collapsible)
- Main chat: flex-1 (fluid)
- Right panel: 320px (toggleable)
- Header: 64px
- Composer: auto-height (min 60px, max 200px)

---

## 🧩 Component Breakdown

### 1. Header

```tsx
<header className="sticky top-0 z-50 h-16 border-b border-border bg-bg/95 backdrop-blur">
  <div className="h-full px-4 flex items-center justify-between">
    {/* Left: Logo + Sidebar Toggle */}
    <div className="flex items-center gap-3">
      <Button
        variant="ghost"
        size="sm"
        onClick={() => toggleSidebar()}
        className="lg:hidden"
      >
        <Menu className="w-5 h-5" />
      </Button>
      <Logo />
    </div>

    {/* Center: Conversation Title */}
    <div className="flex-1 text-center">
      <h1 className="text-sm font-medium text-text-primary truncate max-w-md mx-auto">
        {conversationTitle || 'New Conversation'}
      </h1>
    </div>

    {/* Right: Actions */}
    <div className="flex items-center gap-2">
      <Button
        variant="ghost"
        size="sm"
        onClick={() => toggleContextPanel()}
      >
        <SidebarRight className="w-5 h-5" />
      </Button>
      <UserMenu />
    </div>
  </div>
</header>
```

**Styles**:
```css
.chat-header {
  @apply sticky top-0 z-50 h-16;
  @apply border-b border-border;
  @apply bg-bg/95 backdrop-blur;
}
```

---

### 2. Conversation List Sidebar

```tsx
<aside className={cn(
  'w-[280px] border-r border-border bg-surface-1 flex flex-col',
  'transition-transform duration-200',
  isCollapsed && '-translate-x-full lg:translate-x-0'
)}>
  {/* Header */}
  <div className="p-4 border-b border-border">
    <Button
      variant="primary"
      className="w-full"
      onClick={createNewConversation}
    >
      <Plus className="w-4 h-4 mr-2" />
      New Chat
    </Button>
  </div>

  {/* Search */}
  <div className="p-3 border-b border-border">
    <Input
      type="search"
      placeholder="Search conversations..."
      className="h-9"
      value={searchQuery}
      onChange={(e) => setSearchQuery(e.target.value)}
    />
  </div>

  {/* Conversation List */}
  <div className="flex-1 overflow-y-auto p-2">
    <div className="space-y-1">
      {conversations.map((conv) => (
        <ConversationItem
          key={conv.id}
          conversation={conv}
          isActive={conv.id === currentConversation}
          onClick={() => selectConversation(conv.id)}
        />
      ))}
    </div>
  </div>

  {/* Footer */}
  <div className="p-4 border-t border-border">
    <Button
      variant="ghost"
      className="w-full justify-start"
      onClick={() => navigate('/workspace/default')}
    >
      <ArrowLeft className="w-4 h-4 mr-2" />
      Back to Workspace
    </Button>
  </div>
</aside>
```

**ConversationItem Component**:
```tsx
function ConversationItem({ conversation, isActive, onClick }) {
  return (
    <button
      className={cn(
        'w-full text-left px-3 py-2.5 rounded-lg',
        'flex items-start gap-3',
        'hover:bg-surface-2 transition-colors',
        'group',
        isActive && 'bg-surface-3'
      )}
      onClick={onClick}
    >
      <MessageSquare className="w-4 h-4 mt-0.5 text-text-muted shrink-0" />
      <div className="flex-1 min-w-0">
        <p className="text-sm font-medium text-text-primary truncate">
          {conversation.title}
        </p>
        <p className="text-xs text-text-muted truncate">
          {conversation.lastMessage}
        </p>
      </div>
      <DropdownMenu>
        <DropdownMenuTrigger asChild>
          <Button
            variant="ghost"
            size="xs"
            className="opacity-0 group-hover:opacity-100"
          >
            <MoreVertical className="w-4 h-4" />
          </Button>
        </DropdownMenuTrigger>
        <DropdownMenuContent>
          <DropdownMenuItem>
            <Edit className="w-4 h-4 mr-2" />
            Rename
          </DropdownMenuItem>
          <DropdownMenuItem className="text-error">
            <Trash2 className="w-4 h-4 mr-2" />
            Delete
          </DropdownMenuItem>
        </DropdownMenuContent>
      </DropdownMenu>
    </button>
  )
}
```

---

### 3. Chat Messages Area

```tsx
<main className="flex-1 flex flex-col overflow-hidden bg-bg">
  {/* Messages Container */}
  <div
    ref={messagesContainerRef}
    className="flex-1 overflow-y-auto px-4 py-6 space-y-6"
  >
    {messages.map((message, index) => (
      <Message
        key={message.id}
        message={message}
        isLast={index === messages.length - 1}
      />
    ))}

    {/* Loading indicator */}
    {isLoading && (
      <div className="flex items-center gap-2 text-text-muted">
        <Loader2 className="w-4 h-4 animate-spin" />
        <span className="text-sm">AI is thinking...</span>
      </div>
    )}

    {/* Auto-scroll anchor */}
    <div ref={messagesEndRef} />
  </div>

  {/* Message Composer */}
  <MessageComposer />
</main>
```

**Message Component**:
```tsx
function Message({ message, isLast }) {
  const isUser = message.role === 'user'

  return (
    <div
      className={cn(
        'flex gap-4 max-w-4xl',
        isUser ? 'ml-auto' : 'mr-auto'
      )}
    >
      {/* Avatar */}
      {!isUser && (
        <div className="w-8 h-8 rounded-full bg-primary flex items-center justify-center shrink-0">
          <Bot className="w-5 h-5 text-white" />
        </div>
      )}

      {/* Message Content */}
      <div className="flex-1 space-y-2">
        <div
          className={cn(
            'rounded-lg px-4 py-3',
            isUser
              ? 'bg-primary text-white ml-auto max-w-2xl'
              : 'bg-surface-2 text-text-primary'
          )}
        >
          {/* Text content */}
          <div className="prose prose-sm dark:prose-invert max-w-none">
            <Markdown>{message.content}</Markdown>
          </div>

          {/* Tool calls */}
          {message.toolCalls && (
            <div className="mt-3 space-y-2">
              {message.toolCalls.map((tool) => (
                <ToolCallCard key={tool.id} tool={tool} />
              ))}
            </div>
          )}

          {/* Attachments */}
          {message.attachments && (
            <div className="mt-3 flex flex-wrap gap-2">
              {message.attachments.map((file) => (
                <FileChip key={file.id} file={file} />
              ))}
            </div>
          )}
        </div>

        {/* Message actions */}
        <div className="flex items-center gap-2 text-text-muted">
          <span className="text-xs">
            {formatTime(message.timestamp)}
          </span>
          {!isUser && (
            <>
              <Button variant="ghost" size="xs">
                <Copy className="w-3 h-3" />
              </Button>
              <Button variant="ghost" size="xs">
                <ThumbsUp className="w-3 h-3" />
              </Button>
              <Button variant="ghost" size="xs">
                <ThumbsDown className="w-3 h-3" />
              </Button>
            </>
          )}
        </div>
      </div>

      {/* User avatar */}
      {isUser && (
        <Avatar className="w-8 h-8 shrink-0">
          <AvatarImage src={user.avatar} />
          <AvatarFallback>{user.initials}</AvatarFallback>
        </Avatar>
      )}
    </div>
  )
}
```

---

### 4. Message Composer

```tsx
function MessageComposer() {
  const [message, setMessage] = useState('')
  const [attachments, setAttachments] = useState([])
  const [selectedTools, setSelectedTools] = useState([])
  const textareaRef = useRef(null)

  const handleSubmit = async () => {
    if (!message.trim() && attachments.length === 0) return
    await sendMessage({ message, attachments, tools: selectedTools })
    setMessage('')
    setAttachments([])
  }

  return (
    <div className="border-t border-border bg-surface-1 p-4">
      {/* Attachments preview */}
      {attachments.length > 0 && (
        <div className="mb-3 flex flex-wrap gap-2">
          {attachments.map((file) => (
            <FileChip
              key={file.id}
              file={file}
              onRemove={() => removeAttachment(file.id)}
            />
          ))}
        </div>
      )}

      {/* Tools preview */}
      {selectedTools.length > 0 && (
        <div className="mb-3 flex flex-wrap gap-2">
          {selectedTools.map((tool) => (
            <Badge key={tool.id} variant="primary">
              {tool.name}
              <button
                onClick={() => removeTool(tool.id)}
                className="ml-1 hover:text-white/80"
              >
                <X className="w-3 h-3" />
              </button>
            </Badge>
          ))}
        </div>
      )}

      {/* Input area */}
      <div className="flex items-end gap-2">
        {/* Textarea */}
        <div className="flex-1 relative">
          <Textarea
            ref={textareaRef}
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault()
                handleSubmit()
              }
            }}
            placeholder="Type a message... (Shift+Enter for new line)"
            className="min-h-[60px] max-h-[200px] pr-24 resize-none"
            rows={1}
          />

          {/* Inline actions */}
          <div className="absolute bottom-2 right-2 flex items-center gap-1">
            <Popover>
              <PopoverTrigger asChild>
                <Button variant="ghost" size="xs">
                  <Paperclip className="w-4 h-4" />
                </Button>
              </PopoverTrigger>
              <PopoverContent>
                <AttachmentPicker onSelect={addAttachment} />
              </PopoverContent>
            </Popover>

            <Popover>
              <PopoverTrigger asChild>
                <Button variant="ghost" size="xs">
                  <Wrench className="w-4 h-4" />
                </Button>
              </PopoverTrigger>
              <PopoverContent>
                <ToolPicker
                  selected={selectedTools}
                  onSelect={setSelectedTools}
                />
              </PopoverContent>
            </Popover>

            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button variant="ghost" size="xs">
                  <Settings className="w-4 h-4" />
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent>
                <DropdownMenuItem>
                  <Zap className="w-4 h-4 mr-2" />
                  Quick Mode
                </DropdownMenuItem>
                <DropdownMenuItem>
                  <Brain className="w-4 h-4 mr-2" />
                  Agent Mode
                </DropdownMenuItem>
                <DropdownMenuItem>
                  <Code className="w-4 h-4 mr-2" />
                  Code Mode
                </DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>
          </div>
        </div>

        {/* Send button */}
        <Button
          variant="primary"
          size="lg"
          onClick={handleSubmit}
          disabled={!message.trim() && attachments.length === 0}
          className="shrink-0"
        >
          <Send className="w-5 h-5" />
        </Button>
      </div>

      {/* Footer hint */}
      <p className="text-xs text-text-muted mt-2">
        Press Shift+Enter for new line, Enter to send
      </p>
    </div>
  )
}
```

---

### 5. Context Panel (Right)

```tsx
<aside className={cn(
  'w-[320px] border-l border-border bg-surface-1 flex flex-col',
  'transition-transform duration-200',
  !isPanelOpen && 'translate-x-full'
)}>
  {/* Header */}
  <div className="p-4 border-b border-border flex items-center justify-between">
    <h3 className="font-semibold text-text-primary">Context</h3>
    <Button variant="ghost" size="xs" onClick={() => closePanel()}>
      <X className="w-4 h-4" />
    </Button>
  </div>

  {/* Tabs */}
  <Tabs defaultValue="sources" className="flex-1 flex flex-col">
    <TabsList className="px-4 py-2 border-b border-border">
      <TabsTrigger value="sources">Sources</TabsTrigger>
      <TabsTrigger value="tools">Tools</TabsTrigger>
      <TabsTrigger value="settings">Settings</TabsTrigger>
    </TabsList>

    <div className="flex-1 overflow-y-auto">
      {/* Sources Tab */}
      <TabsContent value="sources" className="p-4 space-y-4">
        <div>
          <h4 className="text-sm font-medium text-text-secondary mb-2">
            Knowledge Sources
          </h4>
          <div className="space-y-2">
            <SourceItem
              title="Product Documentation"
              type="document"
              status="active"
            />
            <SourceItem
              title="Customer Database"
              type="database"
              status="active"
            />
          </div>
        </div>

        <div>
          <h4 className="text-sm font-medium text-text-secondary mb-2">
            Uploaded Files
          </h4>
          <div className="space-y-2">
            <FileItem name="report.pdf" size="2.4 MB" />
            <FileItem name="data.csv" size="156 KB" />
          </div>
        </div>
      </TabsContent>

      {/* Tools Tab */}
      <TabsContent value="tools" className="p-4 space-y-2">
        <ToolToggle
          name="Web Search"
          description="Search the internet for information"
          enabled={true}
        />
        <ToolToggle
          name="Calculator"
          description="Perform mathematical calculations"
          enabled={false}
        />
        <ToolToggle
          name="Code Interpreter"
          description="Run Python code"
          enabled={true}
        />
      </TabsContent>

      {/* Settings Tab */}
      <TabsContent value="settings" className="p-4 space-y-4">
        <div>
          <label className="text-sm font-medium text-text-primary">
            AI Model
          </label>
          <Select value={model} onValueChange={setModel}>
            <SelectTrigger className="mt-1.5">
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="gpt-4">GPT-4</SelectItem>
              <SelectItem value="claude-3">Claude 3</SelectItem>
              <SelectItem value="gemini-pro">Gemini Pro</SelectItem>
            </SelectContent>
          </Select>
        </div>

        <div>
          <label className="text-sm font-medium text-text-primary mb-1.5 block">
            Temperature: {temperature}
          </label>
          <Slider
            value={[temperature]}
            onValueChange={([val]) => setTemperature(val)}
            min={0}
            max={2}
            step={0.1}
            className="mt-1.5"
          />
        </div>

        <div>
          <label className="text-sm font-medium text-text-primary mb-1.5 block">
            Max Tokens: {maxTokens}
          </label>
          <Slider
            value={[maxTokens]}
            onValueChange={([val]) => setMaxTokens(val)}
            min={100}
            max={4000}
            step={100}
            className="mt-1.5"
          />
        </div>
      </TabsContent>
    </div>
  </Tabs>
</aside>
```

---

## 🎨 Design Tokens Used

**Layout**:
- Sidebar: 280px fixed width
- Context panel: 320px fixed width
- Main chat: flex-1
- Message max-width: 4xl (896px)

**Colors**:
- User messages: bg-primary, text-white
- AI messages: bg-surface-2, text-text-primary
- Backgrounds: bg, surface-1, surface-2

**Typography**:
- Message text: prose prose-sm
- Timestamps: text-xs text-text-muted
- Composer: text-sm

**Spacing**:
- Message gap: space-y-6
- Composer padding: p-4
- Panel sections: p-4 space-y-4

---

## ♿ Accessibility

- [ ] Messages have proper ARIA roles
- [ ] Textarea has accessible label
- [ ] Keyboard shortcuts documented (Enter, Shift+Enter)
- [ ] Focus management when switching conversations
- [ ] Screen reader announcements for new messages

---

## ✨ Interactions

**Auto-scroll**: Scroll to bottom when new message arrives
**Typing indicator**: Show when AI is generating response
**Message actions**: Copy, like, dislike buttons on hover
**Composer auto-resize**: Grows with content up to max-height

---

**Implementation File**: `/apps/sim/app/chat/[identifier]/page.tsx`
