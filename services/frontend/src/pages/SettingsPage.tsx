import { useState } from 'react'
import { useParams } from 'react-router-dom'

interface SettingsTab {
  id: string
  label: string
  description: string
}

const SETTINGS_TABS: SettingsTab[] = [
  {
    id: 'general',
    label: 'General',
    description: 'Workspace name, timezone, and general settings',
  },
  {
    id: 'members',
    label: 'Members',
    description: 'Manage workspace members and permissions',
  },
  {
    id: 'api-keys',
    label: 'API Keys',
    description: 'Manage API keys for your workspace',
  },
  {
    id: 'copilot',
    label: 'Copilot',
    description: 'Configure your AI Copilot settings',
  },
  {
    id: 'integrations',
    label: 'Integrations',
    description: 'Connect external services and tools',
  },
  {
    id: 'billing',
    label: 'Billing',
    description: 'Manage your subscription and billing',
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
              <label className="block text-sm font-medium mb-2">Workspace Name</label>
              <input
                type="text"
                value={workspaceName}
                onChange={(e) => setWorkspaceName(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Enter workspace name"
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-2">Timezone</label>
              <select
                value={timezone}
                onChange={(e) => setTimezone(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
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
              className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
            >
              {isSaving ? 'Saving...' : 'Save Settings'}
            </button>
          </div>
        )

      case 'members':
        return (
          <div className="space-y-6">
            <p className="text-gray-600">Manage workspace members and their permissions.</p>
            <div className="border border-gray-200 rounded-lg p-4">
              <p className="text-gray-500 text-center py-8">No members configured yet</p>
            </div>
          </div>
        )

      case 'api-keys':
        return (
          <div className="space-y-6">
            <div>
              <label className="block text-sm font-medium mb-2">Create New API Key</label>
              <div className="flex gap-2">
                <input
                  type="text"
                  value={apiKeyInput}
                  onChange={(e) => setApiKeyInput(e.target.value)}
                  className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="API Key Name"
                />
                <button
                  onClick={handleAddApiKey}
                  className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
                >
                  Add
                </button>
              </div>
            </div>

            {apiKeys.length > 0 ? (
              <div>
                <h3 className="text-sm font-medium mb-4">Your API Keys</h3>
                <div className="space-y-2">
                  {apiKeys.map((key) => (
                    <div
                      key={key.id}
                      className="flex justify-between items-center border border-gray-200 rounded-lg p-3"
                    >
                      <div>
                        <p className="font-medium">{key.name}</p>
                        <p className="text-xs text-gray-500">
                          Created {new Date(key.createdAt).toLocaleDateString()}
                        </p>
                      </div>
                      <button
                        onClick={() => handleDeleteApiKey(key.id)}
                        className="px-3 py-1 bg-red-500 text-white rounded hover:bg-red-600 text-sm"
                      >
                        Delete
                      </button>
                    </div>
                  ))}
                </div>
              </div>
            ) : (
              <div className="border border-gray-200 rounded-lg p-4">
                <p className="text-gray-500 text-center py-8">No API keys created yet</p>
              </div>
            )}
          </div>
        )

      case 'copilot':
        return (
          <div className="space-y-6">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="font-medium">Enable Copilot</h3>
                <p className="text-sm text-gray-600">Allow AI-powered assistance in workflows</p>
              </div>
              <label className="flex items-center cursor-pointer">
                <input
                  type="checkbox"
                  checked={copilotEnabled}
                  onChange={(e) => setCopilotEnabled(e.target.checked)}
                  className="w-4 h-4"
                />
              </label>
            </div>
            {copilotEnabled && (
              <div className="border-l-4 border-blue-500 bg-blue-50 p-4 rounded">
                <p className="text-sm text-blue-900">
                  Copilot is enabled. You can now use AI-powered assistance when building workflows.
                </p>
              </div>
            )}
            <button
              onClick={handleSaveSettings}
              disabled={isSaving}
              className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
            >
              {isSaving ? 'Saving...' : 'Save Settings'}
            </button>
          </div>
        )

      case 'integrations':
        return (
          <div className="space-y-6">
            <p className="text-gray-600">Configure external service integrations.</p>
            <div className="border border-gray-200 rounded-lg p-4">
              <p className="text-gray-500 text-center py-8">No integrations configured yet</p>
            </div>
          </div>
        )

      case 'billing':
        return (
          <div className="space-y-6">
            <p className="text-gray-600">Manage your subscription and billing information.</p>
            <div className="border border-gray-200 rounded-lg p-4">
              <p className="text-gray-500 text-center py-8">No billing information available</p>
            </div>
          </div>
        )

      default:
        return null
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-6xl mx-auto px-4 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Workspace Settings</h1>
          <p className="text-gray-600 mt-2">ID · {workspaceId}</p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
          {/* Sidebar Navigation */}
          <div className="lg:col-span-1">
            <nav className="space-y-1">
              {SETTINGS_TABS.map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`w-full text-left px-4 py-3 rounded-lg transition-colors ${
                    activeTab === tab.id
                      ? 'bg-blue-600 text-white'
                      : 'text-gray-700 hover:bg-gray-100'
                  }`}
                >
                  <div className="font-medium text-sm">{tab.label}</div>
                  <div
                    className={`text-xs mt-1 ${
                      activeTab === tab.id ? 'text-blue-100' : 'text-gray-500'
                    }`}
                  >
                    {tab.description}
                  </div>
                </button>
              ))}
            </nav>
          </div>

          {/* Main Content */}
          <div className="lg:col-span-3">
            <div className="bg-white rounded-lg shadow-sm p-8">
              <h2 className="text-2xl font-bold mb-6">
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
