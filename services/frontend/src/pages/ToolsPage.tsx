import { useState } from 'react'
import {
  Plus,
  Search,
  Server,
  Wrench,
  Trash2,
  Edit,
  Play,
  CheckCircle,
  XCircle,
  AlertCircle,
  X
} from 'lucide-react'

export default function ToolsPage() {
  const [searchQuery, setSearchQuery] = useState('')

  // Placeholder data - will be replaced with real MCP store
  const [servers] = useState([
    {
      id: '1',
      name: 'GitHub MCP Server',
      url: 'https://api.github.com/mcp',
      status: 'connected',
      toolCount: 12,
      description: 'Access GitHub repositories, issues, and pull requests',
    },
    {
      id: '2',
      name: 'Slack MCP Server',
      url: 'https://slack.com/api/mcp',
      status: 'connected',
      toolCount: 8,
      description: 'Send messages and manage Slack channels',
    },
    {
      id: '3',
      name: 'Database Tools',
      url: 'http://localhost:3000/mcp',
      status: 'disconnected',
      toolCount: 5,
      description: 'Query and manage databases',
    },
  ])

  const [showAddModal, setShowAddModal] = useState(false)

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'connected':
        return <CheckCircle className="h-4 w-4 text-green-300" />
      case 'disconnected':
        return <XCircle className="h-4 w-4 text-red-300" />
      default:
        return <AlertCircle className="h-4 w-4 text-yellow-300" />
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'connected':
        return 'bg-green-500/20 text-green-300'
      case 'disconnected':
        return 'bg-red-500/20 text-red-300'
      default:
        return 'bg-yellow-500/20 text-yellow-300'
    }
  }

  return (
    <div className="flex-1 overflow-auto">
      <div className="mx-auto max-w-7xl">
        {/* Header */}
        <div className="mb-6 fade-in">
          <div className="mb-4 flex items-center justify-between">
            <div>
              <h1 className="font-bold text-3xl text-white">Tools & MCP Servers</h1>
              <p className="mt-2 text-white/70">
                Manage MCP (Model Context Protocol) servers and custom tools
              </p>
            </div>
            <button onClick={() => setShowAddModal(true)} className="glass-button px-4 py-2">
              <Plus className="mr-2 h-4 w-4" />
              Add Server
            </button>
          </div>

          {/* Search */}
          <div className="relative fade-in" style={{ animationDelay: '0.1s' }}>
            <Search className="-translate-y-1/2 absolute top-1/2 left-3 h-4 w-4 text-white/40" />
            <input
              placeholder="Search servers and tools..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="glass-input w-full pl-10"
            />
          </div>
        </div>

        {/* Stats Cards */}
        <div className="mb-8 grid grid-cols-1 gap-4 md:grid-cols-3">
          <div className="glass-card p-6 fade-in" style={{ animationDelay: '0.2s' }}>
            <div className="mb-4 flex items-center gap-2">
              <Server className="h-5 w-5 text-blue-300" />
              <div className="stat-label">Total Servers</div>
            </div>
            <div className="stat-value mb-2">{servers.length}</div>
            <p className="text-white/60 text-xs">
              {servers.filter((s) => s.status === 'connected').length} connected
            </p>
          </div>

          <div className="glass-card p-6 fade-in" style={{ animationDelay: '0.25s' }}>
            <div className="mb-4 flex items-center gap-2">
              <Wrench className="h-5 w-5 text-purple-300" />
              <div className="stat-label">Available Tools</div>
            </div>
            <div className="stat-value mb-2">
              {servers.reduce((acc, s) => acc + s.toolCount, 0)}
            </div>
            <p className="text-white/60 text-xs">Across all servers</p>
          </div>

          <div className="glass-card p-6 fade-in" style={{ animationDelay: '0.3s' }}>
            <div className="mb-4 flex items-center gap-2">
              <CheckCircle className="h-5 w-5 text-green-300" />
              <div className="stat-label">Status</div>
            </div>
            <div className="stat-value mb-2">
              {Math.round(
                (servers.filter((s) => s.status === 'connected').length / servers.length) * 100
              )}
              %
            </div>
            <p className="text-white/60 text-xs">Servers online</p>
          </div>
        </div>

        {/* Server List */}
        <div className="mb-8">
          <h2 className="mb-4 font-semibold text-xl text-white fade-in" style={{ animationDelay: '0.35s' }}>
            MCP Servers
          </h2>

          {servers.length === 0 ? (
            <div className="glass-card flex flex-col items-center justify-center p-12 fade-in" style={{ animationDelay: '0.4s' }}>
              <div className="mb-4 rounded-full bg-white/10 p-4">
                <Server className="h-8 w-8 text-white/40" />
              </div>
              <h3 className="font-semibold text-white">No MCP servers configured</h3>
              <p className="mt-2 text-center text-sm text-white/70">
                Add your first MCP server to start using external tools in your workflows
              </p>
              <button onClick={() => setShowAddModal(true)} className="glass-button mt-4 px-6 py-3">
                <Plus className="mr-2 h-4 w-4" />
                Add MCP Server
              </button>
            </div>
          ) : (
            <div className="grid grid-cols-1 gap-4">
              {servers.map((server, index) => (
                <div
                  key={server.id}
                  className="glass-card p-6 fade-in"
                  style={{ animationDelay: `${0.4 + index * 0.1}s` }}
                >
                  <div className="flex items-start justify-between">
                    <div className="flex items-start gap-4 flex-1">
                      <div className="rounded-lg bg-blue-500/20 p-3">
                        <Server className="h-6 w-6 text-blue-300" />
                      </div>
                      <div className="flex-1">
                        <h3 className="mb-1 font-semibold text-white">{server.name}</h3>
                        <p className="mb-3 text-sm text-white/70">{server.description}</p>
                        <div className="flex flex-wrap items-center gap-2">
                          <code className="rounded-lg bg-white/10 px-3 py-1 text-xs text-white/80">
                            {server.url}
                          </code>
                          <span
                            className={cn(
                              'flex items-center gap-1 rounded-full px-3 py-1 text-xs font-medium',
                              getStatusColor(server.status)
                            )}
                          >
                            {getStatusIcon(server.status)}
                            {server.status}
                          </span>
                        </div>
                        <div className="mt-4 flex items-center gap-4">
                          <div className="flex items-center gap-2 text-sm text-white/60">
                            <Wrench className="h-4 w-4" />
                            <span>{server.toolCount} tools available</span>
                          </div>
                          <button className="glass-button px-3 py-1.5 text-xs">
                            View Tools
                          </button>
                        </div>
                      </div>
                    </div>
                    <div className="flex items-center gap-1">
                      <button className="glass-button p-2">
                        <Play className="h-4 w-4" />
                      </button>
                      <button className="glass-button p-2">
                        <Edit className="h-4 w-4" />
                      </button>
                      <button className="glass-button p-2 hover:bg-red-500/20">
                        <Trash2 className="h-4 w-4 text-red-300" />
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Custom Tools Section */}
        <div className="fade-in" style={{ animationDelay: '0.7s' }}>
          <h2 className="mb-4 font-semibold text-xl text-white">Custom Tools</h2>
          <div className="glass-card border-2 border-dashed border-white/20 p-8 text-center">
            <p className="text-sm text-white/60">Custom JavaScript tools - Coming soon</p>
          </div>
        </div>
      </div>

      {/* Add Server Modal */}
      {showAddModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm fade-in">
          <div className="glass-card w-full max-w-md p-8">
            <div className="mb-6 flex items-center justify-between">
              <div>
                <h2 className="font-bold text-xl text-white">Add MCP Server</h2>
                <p className="mt-1 text-sm text-white/70">
                  Connect to a Model Context Protocol server
                </p>
              </div>
              <button
                onClick={() => setShowAddModal(false)}
                className="glass-button p-2"
              >
                <X className="h-4 w-4" />
              </button>
            </div>

            <div className="space-y-4">
              <div>
                <label className="mb-2 block text-sm font-medium text-white/80">
                  Server Name
                </label>
                <input
                  placeholder="GitHub MCP Server"
                  className="glass-input w-full"
                />
              </div>
              <div>
                <label className="mb-2 block text-sm font-medium text-white/80">
                  Server URL
                </label>
                <input
                  placeholder="https://api.example.com/mcp"
                  className="glass-input w-full"
                />
              </div>
              <div>
                <label className="mb-2 block text-sm font-medium text-white/80">
                  Description (optional)
                </label>
                <input
                  placeholder="Access GitHub repositories and issues"
                  className="glass-input w-full"
                />
              </div>
              <div className="flex gap-3 pt-2">
                <button
                  className="glass-button flex-1 py-3"
                  onClick={() => setShowAddModal(false)}
                >
                  Cancel
                </button>
                <button className="glass-button flex-1 bg-gradient-to-r from-purple-500/30 to-blue-500/30 py-3 font-semibold">
                  Add Server
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

function cn(...classes: any[]) {
  return classes.filter(Boolean).join(' ')
}
