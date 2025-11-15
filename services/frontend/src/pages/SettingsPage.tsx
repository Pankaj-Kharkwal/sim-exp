import { useState } from 'react'
import { useParams } from 'react-router-dom'
import { Settings, Users, Key, Sparkles, Link as LinkIcon, CreditCard, Trash2, Plus, Loader2 } from 'lucide-react'

interface SettingsTab {
  id: string
  label: string
  description: string
  icon: any
}

const SETTINGS_TABS: SettingsTab[] = [
  {
    id: 'general',
    label: 'General',
    description: 'Workspace name, timezone, and general settings',
    icon: Settings,
  },
  {
    id: 'members',
    label: 'Members',
    description: 'Manage workspace members and permissions',
    icon: Users,
  },
  {
    id: 'api-keys',
    label: 'API Keys',
    description: 'Manage API keys for your workspace',
    icon: Key,
  },
  {
    id: 'copilot',
    label: 'Copilot',
    description: 'Configure your AI Copilot settings',
    icon: Sparkles,
  },
  {
    id: 'integrations',
    label: 'Integrations',
    description: 'Connect external services and tools',
    icon: LinkIcon,
  },
  {
    id: 'billing',
    label: 'Billing',
    description: 'Manage your subscription and billing',
    icon: CreditCard,
  },
]

export default function SettingsPage() {
  const { workspaceId } = useParams<{ workspaceId: string }>()
  const [activeTab, setActiveTab] = useState('general')
  const [workspaceName, setWorkspaceName] = useState('My Workspace')
  const [timezone, setTimezone] = useState('UTC')
  const [copilotEnabled, setCopilotEnabled] = useState(true)
  const [apiKeyInput, setApiKeyInput] = useState('')
  const [apiKeys, setApiKeys] = useState<Array<{ id: string; name: string; createdAt: string }>>([])
  const [isSaving, setIsSaving] = useState(false)

  const handleSaveSettings = async () => {
    setIsSaving(true)
    try {
      // TODO: Call backend API to save settings
      console.log('Saving settings...', {
        workspaceName,
        timezone,
        copilotEnabled,
      })
      // Simulate API delay
      await new Promise((resolve) => setTimeout(resolve, 500))
      alert('Settings saved successfully!')
    } catch (error) {
      console.error('Failed to save settings:', error)
      alert('Failed to save settings')
    } finally {
      setIsSaving(false)
    }
  }

  const handleAddApiKey = async () => {
    if (!apiKeyInput.trim()) {
      alert('Please enter an API key name')
      return
    }
    try {
      // TODO: Call backend API to create API key
      const newKey = {
        id: Math.random().toString(36).substr(2, 9),
        name: apiKeyInput,
        createdAt: new Date().toISOString(),
      }
      setApiKeys([...apiKeys, newKey])
      setApiKeyInput('')
      alert('API key created successfully!')
    } catch (error) {
      console.error('Failed to create API key:', error)
      alert('Failed to create API key')
    }
  }

  const handleDeleteApiKey = async (keyId: string) => {
    if (!confirm('Are you sure you want to delete this API key?')) {
      return
    }
    try {
      // TODO: Call backend API to delete API key
      setApiKeys(apiKeys.filter((key) => key.id !== keyId))
      alert('API key deleted successfully!')
    } catch (error) {
      console.error('Failed to delete API key:', error)
      alert('Failed to delete API key')
    }
  }

  const renderTabContent = () => {
    switch (activeTab) {
      case 'general':
        return (
          <div className="space-y-6">
            <div>
              <label className="mb-2 block text-sm font-medium text-white/80">Workspace Name</label>
              <input
                type="text"
                value={workspaceName}
                onChange={(e) => setWorkspaceName(e.target.value)}
                className="glass-input w-full"
                placeholder="Enter workspace name"
              />
            </div>
            <div>
              <label className="mb-2 block text-sm font-medium text-white/80">Timezone</label>
              <select
                value={timezone}
                onChange={(e) => setTimezone(e.target.value)}
                className="glass-input w-full"
              >
                <option value="UTC">UTC</option>
                <option value="EST">Eastern Standard Time</option>
                <option value="CST">Central Standard Time</option>
                <option value="MST">Mountain Standard Time</option>
                <option value="PST">Pacific Standard Time</option>
              </select>
            </div>
            <button
              onClick={handleSaveSettings}
              disabled={isSaving}
              className="glass-button bg-gradient-to-r from-purple-500/30 to-blue-500/30 px-6 py-3 font-semibold"
            >
              {isSaving ? (
                <div className="flex items-center gap-2">
                  <Loader2 className="h-4 w-4 animate-spin" />
                  Saving...
                </div>
              ) : (
                'Save Settings'
              )}
            </button>
          </div>
        )

      case 'members':
        return (
          <div className="space-y-6">
            <p className="text-white/70">Manage workspace members and their permissions.</p>
            <div className="glass-card border-2 border-dashed border-white/20 p-8 text-center">
              <Users className="mx-auto mb-2 h-8 w-8 text-white/40" />
              <p className="text-white/60">No members configured yet</p>
            </div>
          </div>
        )

      case 'api-keys':
        return (
          <div className="space-y-6">
            <div>
              <label className="mb-2 block text-sm font-medium text-white/80">Create New API Key</label>
              <div className="flex gap-2">
                <input
                  type="text"
                  value={apiKeyInput}
                  onChange={(e) => setApiKeyInput(e.target.value)}
                  className="glass-input flex-1"
                  placeholder="API Key Name"
                />
                <button
                  onClick={handleAddApiKey}
                  className="glass-button bg-gradient-to-r from-purple-500/30 to-blue-500/30 px-6 py-3 font-semibold"
                >
                  <Plus className="mr-2 h-4 w-4" />
                  Add
                </button>
              </div>
            </div>

            {apiKeys.length > 0 ? (
              <div>
                <h3 className="mb-4 text-sm font-medium text-white">Your API Keys</h3>
                <div className="space-y-2">
                  {apiKeys.map((key, index) => (
                    <div
                      key={key.id}
                      className="glass-card flex items-center justify-between p-4 fade-in"
                      style={{ animationDelay: `${index * 0.05}s` }}
                    >
                      <div>
                        <p className="font-medium text-white">{key.name}</p>
                        <p className="text-xs text-white/60">
                          Created {new Date(key.createdAt).toLocaleDateString()}
                        </p>
                      </div>
                      <button
                        onClick={() => handleDeleteApiKey(key.id)}
                        className="glass-button p-2 hover:bg-red-500/20"
                      >
                        <Trash2 className="h-4 w-4 text-red-300" />
                      </button>
                    </div>
                  ))}
                </div>
              </div>
            ) : (
              <div className="glass-card border-2 border-dashed border-white/20 p-8 text-center">
                <Key className="mx-auto mb-2 h-8 w-8 text-white/40" />
                <p className="text-white/60">No API keys created yet</p>
              </div>
            )}
          </div>
        )

      case 'copilot':
        return (
          <div className="space-y-6">
            <div className="glass-card flex items-center justify-between p-6">
              <div>
                <h3 className="font-medium text-white">Enable Copilot</h3>
                <p className="text-sm text-white/70">Allow AI-powered assistance in workflows</p>
              </div>
              <label className="relative inline-flex cursor-pointer items-center">
                <input
                  type="checkbox"
                  checked={copilotEnabled}
                  onChange={(e) => setCopilotEnabled(e.target.checked)}
                  className="peer sr-only"
                />
                <div className="peer h-6 w-11 rounded-full bg-white/20 after:absolute after:left-[2px] after:top-[2px] after:h-5 after:w-5 after:rounded-full after:bg-white after:transition-all after:content-[''] peer-checked:bg-purple-500/50 peer-checked:after:translate-x-full peer-focus:outline-none"></div>
              </label>
            </div>
            {copilotEnabled && (
              <div className="glass-card border-l-4 border-purple-500/50 bg-purple-500/10 p-4 fade-in">
                <p className="text-sm text-purple-200">
                  Copilot is enabled. You can now use AI-powered assistance when building workflows.
                </p>
              </div>
            )}
            <button
              onClick={handleSaveSettings}
              disabled={isSaving}
              className="glass-button bg-gradient-to-r from-purple-500/30 to-blue-500/30 px-6 py-3 font-semibold"
            >
              {isSaving ? (
                <div className="flex items-center gap-2">
                  <Loader2 className="h-4 w-4 animate-spin" />
                  Saving...
                </div>
              ) : (
                'Save Settings'
              )}
            </button>
          </div>
        )

      case 'integrations':
        return (
          <div className="space-y-6">
            <p className="text-white/70">Configure external service integrations.</p>
            <div className="glass-card border-2 border-dashed border-white/20 p-8 text-center">
              <LinkIcon className="mx-auto mb-2 h-8 w-8 text-white/40" />
              <p className="text-white/60">No integrations configured yet</p>
            </div>
          </div>
        )

      case 'billing':
        return (
          <div className="space-y-6">
            <p className="text-white/70">Manage your subscription and billing information.</p>
            <div className="glass-card border-2 border-dashed border-white/20 p-8 text-center">
              <CreditCard className="mx-auto mb-2 h-8 w-8 text-white/40" />
              <p className="text-white/60">No billing information available</p>
            </div>
          </div>
        )

      default:
        return null
    }
  }

  return (
    <div className="flex-1 overflow-auto">
      <div className="mx-auto max-w-6xl">
        {/* Header */}
        <div className="mb-8 fade-in">
          <h1 className="font-bold text-3xl text-white">Workspace Settings</h1>
          <p className="mt-2 text-white/60">ID · {workspaceId}</p>
        </div>

        <div className="grid grid-cols-1 gap-8 lg:grid-cols-4">
          {/* Sidebar Navigation */}
          <div className="lg:col-span-1">
            <nav className="glass-card space-y-1 p-2 fade-in" style={{ animationDelay: '0.1s' }}>
              {SETTINGS_TABS.map((tab, index) => {
                const Icon = tab.icon
                return (
                  <button
                    key={tab.id}
                    onClick={() => setActiveTab(tab.id)}
                    className={cn(
                      'flex w-full items-start gap-3 rounded-lg px-4 py-3 text-left transition-all',
                      activeTab === tab.id
                        ? 'bg-gradient-to-r from-purple-500/30 to-blue-500/30 text-white'
                        : 'text-white/70 hover:bg-white/10 hover:text-white'
                    )}
                  >
                    <Icon className="mt-0.5 h-4 w-4 flex-shrink-0" />
                    <div className="flex-1">
                      <div className="text-sm font-medium">{tab.label}</div>
                      <div
                        className={cn(
                          'mt-0.5 text-xs',
                          activeTab === tab.id ? 'text-white/80' : 'text-white/50'
                        )}
                      >
                        {tab.description}
                      </div>
                    </div>
                  </button>
                )
              })}
            </nav>
          </div>

          {/* Main Content */}
          <div className="lg:col-span-3">
            <div className="glass-card p-8 fade-in" style={{ animationDelay: '0.2s' }}>
              <h2 className="mb-6 font-bold text-2xl text-white">
                {SETTINGS_TABS.find((tab) => tab.id === activeTab)?.label}
              </h2>
              {renderTabContent()}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

function cn(...classes: any[]) {
  return classes.filter(Boolean).join(' ')
}
