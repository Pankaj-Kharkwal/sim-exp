import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import {
  Plus,
  Search,
  Server,
  Wrench,
  Trash2,
  Edit,
  Play,
  Loader2,
  CheckCircle,
  XCircle,
  AlertCircle
} from 'lucide-react'
import { cn } from '@/lib/utils'

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
        return <CheckCircle className="h-4 w-4 text-green-600" />
      case 'disconnected':
        return <XCircle className="h-4 w-4 text-red-600" />
      default:
        return <AlertCircle className="h-4 w-4 text-yellow-600" />
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'connected':
        return 'bg-green-50 text-green-700'
      case 'disconnected':
        return 'bg-red-50 text-red-700'
      default:
        return 'bg-yellow-50 text-yellow-700'
    }
  }

  return (
    <div className="flex h-full flex-col">
      {/* Header */}
      <div className="border-b bg-white px-6 py-4">
        <div className="mb-4 flex items-center justify-between">
          <div>
            <h1 className="font-bold text-2xl">Tools & MCP Servers</h1>
            <p className="text-gray-600 text-sm">
              Manage MCP (Model Context Protocol) servers and custom tools
            </p>
          </div>
          <Button onClick={() => setShowAddModal(true)}>
            <Plus className="mr-2 h-4 w-4" />
            Add Server
          </Button>
        </div>

        {/* Search */}
        <div className="relative">
          <Search className="-translate-y-1/2 absolute top-1/2 left-3 h-4 w-4 text-gray-400" />
          <Input
            placeholder="Search servers and tools..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="pl-10"
          />
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 overflow-y-auto bg-gray-50 p-6">
        {/* Stats Cards */}
        <div className="mb-6 grid grid-cols-1 gap-4 md:grid-cols-3">
          <Card>
            <CardHeader className="pb-3">
              <CardTitle className="flex items-center gap-2 text-sm font-medium">
                <Server className="h-4 w-4 text-blue-600" />
                Total Servers
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="font-bold text-2xl">{servers.length}</div>
              <p className="text-gray-600 text-xs">
                {servers.filter((s) => s.status === 'connected').length} connected
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="pb-3">
              <CardTitle className="flex items-center gap-2 text-sm font-medium">
                <Wrench className="h-4 w-4 text-purple-600" />
                Available Tools
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="font-bold text-2xl">
                {servers.reduce((acc, s) => acc + s.toolCount, 0)}
              </div>
              <p className="text-gray-600 text-xs">Across all servers</p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="pb-3">
              <CardTitle className="flex items-center gap-2 text-sm font-medium">
                <CheckCircle className="h-4 w-4 text-green-600" />
                Status
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="font-bold text-2xl">
                {Math.round(
                  (servers.filter((s) => s.status === 'connected').length / servers.length) *
                    100
                )}
                %
              </div>
              <p className="text-gray-600 text-xs">Servers online</p>
            </CardContent>
          </Card>
        </div>

        {/* Server List */}
        <div className="space-y-4">
          <h2 className="font-semibold text-lg">MCP Servers</h2>

          {servers.length === 0 ? (
            <div className="flex flex-col items-center justify-center rounded-lg border-2 border-dashed border-gray-300 bg-white p-12">
              <div className="rounded-full bg-gray-100 p-4">
                <Server className="h-8 w-8 text-gray-400" />
              </div>
              <h3 className="mt-4 font-semibold text-gray-900">No MCP servers configured</h3>
              <p className="mt-2 text-center text-gray-600 text-sm">
                Add your first MCP server to start using external tools in your workflows
              </p>
              <Button onClick={() => setShowAddModal(true)} className="mt-4">
                <Plus className="mr-2 h-4 w-4" />
                Add MCP Server
              </Button>
            </div>
          ) : (
            <div className="grid grid-cols-1 gap-4">
              {servers.map((server) => (
                <Card key={server.id} className="transition-shadow hover:shadow-md">
                  <CardHeader>
                    <div className="flex items-start justify-between">
                      <div className="flex items-start gap-3">
                        <div className="rounded-lg bg-blue-50 p-2">
                          <Server className="h-5 w-5 text-blue-600" />
                        </div>
                        <div>
                          <CardTitle className="mb-1 text-base">{server.name}</CardTitle>
                          <CardDescription className="text-xs">
                            {server.description}
                          </CardDescription>
                          <div className="mt-2 flex items-center gap-2">
                            <code className="rounded bg-gray-100 px-2 py-0.5 text-gray-700 text-xs">
                              {server.url}
                            </code>
                            <span
                              className={cn(
                                'flex items-center gap-1 rounded-full px-2 py-0.5 text-xs',
                                getStatusColor(server.status)
                              )}
                            >
                              {getStatusIcon(server.status)}
                              {server.status}
                            </span>
                          </div>
                        </div>
                      </div>
                      <div className="flex items-center gap-1">
                        <Button variant="ghost" size="sm">
                          <Play className="h-4 w-4" />
                        </Button>
                        <Button variant="ghost" size="sm">
                          <Edit className="h-4 w-4" />
                        </Button>
                        <Button variant="ghost" size="sm">
                          <Trash2 className="h-4 w-4 text-red-600" />
                        </Button>
                      </div>
                    </div>
                  </CardHeader>
                  <CardContent>
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-2 text-gray-600 text-sm">
                        <Wrench className="h-4 w-4" />
                        <span>{server.toolCount} tools available</span>
                      </div>
                      <Button variant="outline" size="sm">
                        View Tools
                      </Button>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          )}
        </div>

        {/* Placeholder for future: Custom Tools section */}
        <div className="mt-8">
          <h2 className="mb-4 font-semibold text-lg">Custom Tools</h2>
          <div className="rounded-lg border-2 border-dashed border-gray-300 bg-white p-8 text-center">
            <p className="text-gray-600 text-sm">Custom JavaScript tools - Coming soon</p>
          </div>
        </div>
      </div>

      {/* Add Server Modal - Placeholder */}
      {showAddModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
          <Card className="w-full max-w-md">
            <CardHeader>
              <CardTitle>Add MCP Server</CardTitle>
              <CardDescription>Connect to a Model Context Protocol server</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <label className="mb-1 block text-sm font-medium">Server Name</label>
                <Input placeholder="GitHub MCP Server" />
              </div>
              <div>
                <label className="mb-1 block text-sm font-medium">Server URL</label>
                <Input placeholder="https://api.example.com/mcp" />
              </div>
              <div>
                <label className="mb-1 block text-sm font-medium">Description (optional)</label>
                <Input placeholder="Access GitHub repositories and issues" />
              </div>
              <div className="flex gap-2">
                <Button variant="outline" className="flex-1" onClick={() => setShowAddModal(false)}>
                  Cancel
                </Button>
                <Button className="flex-1">Add Server</Button>
              </div>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  )
}
