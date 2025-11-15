import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { Activity, Zap, Users, TrendingUp, ArrowRight, Play, Clock, CheckCircle } from 'lucide-react'

export default function DashboardPage() {
  const [stats, setStats] = useState({
    totalWorkflows: 12,
    activeWorkflows: 8,
    totalExecutions: 1247,
    successRate: 94.5,
  })

  const [recentWorkflows, setRecentWorkflows] = useState([
    {
      id: '1',
      name: 'Daily Data Sync',
      status: 'active',
      lastRun: '2 minutes ago',
      executions: 156,
      icon: '🔄',
    },
    {
      id: '2',
      name: 'Slack Notifications',
      status: 'active',
      lastRun: '15 minutes ago',
      executions: 89,
      icon: '💬',
    },
    {
      id: '3',
      name: 'AI Content Generator',
      status: 'active',
      lastRun: '1 hour ago',
      executions: 234,
      icon: '✨',
    },
    {
      id: '4',
      name: 'Email Automation',
      status: 'paused',
      lastRun: '3 hours ago',
      executions: 432,
      icon: '📧',
    },
  ])

  const [recentExecutions, setRecentExecutions] = useState([
    {
      id: '1',
      workflowName: 'Daily Data Sync',
      status: 'success',
      duration: '2.3s',
      time: '2 min ago',
    },
    {
      id: '2',
      workflowName: 'Slack Notifications',
      status: 'success',
      duration: '1.8s',
      time: '15 min ago',
    },
    {
      id: '3',
      workflowName: 'AI Content Generator',
      status: 'success',
      duration: '5.1s',
      time: '1 hour ago',
    },
    {
      id: '4',
      workflowName: 'Email Automation',
      status: 'failed',
      duration: '0.5s',
      time: '3 hours ago',
    },
  ])

  return (
    <div className="page-container">
      {/* Aurora Background */}
      <div className="aurora-background" />

      {/* Page Header */}
      <div className="page-header fade-in">
        <h1 className="page-title">Dashboard</h1>
        <p className="page-subtitle">Welcome back! Here's what's happening with your workflows.</p>
      </div>

      {/* Stats Grid */}
      <div className="grid-4 fade-in" style={{ animationDelay: '0.1s' }}>
        {/* Total Workflows */}
        <div className="glass-card stat-card shimmer">
          <div className="stat-value">{stats.totalWorkflows}</div>
          <div className="stat-label">Total Workflows</div>
          <div className="stat-change positive">
            <TrendingUp className="inline w-4 h-4 mr-1" />
            +2 this week
          </div>
        </div>

        {/* Active Workflows */}
        <div className="glass-card stat-card shimmer">
          <div className="stat-value">{stats.activeWorkflows}</div>
          <div className="stat-label">Active Workflows</div>
          <div className="stat-change positive">
            <Activity className="inline w-4 h-4 mr-1" />
            Running now
          </div>
        </div>

        {/* Total Executions */}
        <div className="glass-card stat-card shimmer">
          <div className="stat-value">{stats.totalExecutions.toLocaleString()}</div>
          <div className="stat-label">Total Executions</div>
          <div className="stat-change positive">
            <Zap className="inline w-4 h-4 mr-1" />
            +127 today
          </div>
        </div>

        {/* Success Rate */}
        <div className="glass-card stat-card shimmer">
          <div className="stat-value">{stats.successRate}%</div>
          <div className="stat-label">Success Rate</div>
          <div className="stat-change positive">
            <CheckCircle className="inline w-4 h-4 mr-1" />
            +1.2% this month
          </div>
        </div>
      </div>

      {/* Recent Workflows and Executions */}
      <div className="grid-2 mt-8 fade-in" style={{ animationDelay: '0.2s' }}>
        {/* Recent Workflows */}
        <div className="glass-panel">
          <div className="card-header">
            <h3 className="card-title">Recent Workflows</h3>
            <p className="card-description">Your most active automation workflows</p>
          </div>
          <div className="card-body">
            <div className="space-y-4">
              {recentWorkflows.map((workflow, index) => (
                <Link
                  key={workflow.id}
                  to={`/workflows/${workflow.id}`}
                  className="block slide-in"
                  style={{ animationDelay: `${index * 0.1}s` }}
                >
                  <div className="glass-card-subtle p-4 hover:bg-white/20 transition-all duration-200 cursor-pointer">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-3">
                        <div className="text-3xl">{workflow.icon}</div>
                        <div>
                          <h4 className="text-white font-semibold">{workflow.name}</h4>
                          <p className="text-white/60 text-sm mt-1">
                            Last run: {workflow.lastRun}
                          </p>
                        </div>
                      </div>
                      <div className="text-right">
                        <div className={`glass-badge ${workflow.status === 'active' ? 'success' : 'warning'} mb-2`}>
                          {workflow.status}
                        </div>
                        <p className="text-white/60 text-sm">{workflow.executions} executions</p>
                      </div>
                    </div>
                  </div>
                </Link>
              ))}
            </div>
          </div>
          <div className="card-footer">
            <Link to="/workflows" className="glass-button flex items-center space-x-2">
              <span>View All Workflows</span>
              <ArrowRight className="w-4 h-4" />
            </Link>
          </div>
        </div>

        {/* Recent Executions */}
        <div className="glass-panel">
          <div className="card-header">
            <h3 className="card-title">Recent Executions</h3>
            <p className="card-description">Latest workflow execution history</p>
          </div>
          <div className="card-body">
            <div className="space-y-4">
              {recentExecutions.map((execution, index) => (
                <div
                  key={execution.id}
                  className="glass-card-subtle p-4 slide-in"
                  style={{ animationDelay: `${index * 0.1}s` }}
                >
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-3">
                      {execution.status === 'success' ? (
                        <CheckCircle className="w-6 h-6 text-green-400" />
                      ) : (
                        <div className="w-6 h-6 rounded-full bg-red-500/20 border border-red-500/40 flex items-center justify-center">
                          <span className="text-red-400 text-xs">✕</span>
                        </div>
                      )}
                      <div>
                        <h4 className="text-white font-medium">{execution.workflowName}</h4>
                        <p className="text-white/60 text-sm mt-1">
                          <Clock className="inline w-3 h-3 mr-1" />
                          {execution.time}
                        </p>
                      </div>
                    </div>
                    <div className="text-right">
                      <div className={`glass-badge ${execution.status === 'success' ? 'success' : 'error'} mb-1`}>
                        {execution.status}
                      </div>
                      <p className="text-white/60 text-sm">{execution.duration}</p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
          <div className="card-footer">
            <Link to="/logs" className="glass-button flex items-center space-x-2">
              <span>View All Executions</span>
              <ArrowRight className="w-4 h-4" />
            </Link>
          </div>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="mt-8 fade-in" style={{ animationDelay: '0.3s' }}>
        <h3 className="text-2xl font-bold text-white mb-6">Quick Actions</h3>
        <div className="grid-3">
          <Link to="/workflows/new" className="glass-card p-6 hover:scale-105 transition-transform cursor-pointer glow">
            <div className="workflow-card-icon bg-purple-500/30">
              <Zap className="w-6 h-6 text-purple-200" />
            </div>
            <h4 className="text-xl font-semibold text-white mb-2">Create Workflow</h4>
            <p className="text-white/70 text-sm">Build a new automation workflow from scratch</p>
          </Link>

          <Link to="/templates" className="glass-card p-6 hover:scale-105 transition-transform cursor-pointer glow">
            <div className="workflow-card-icon bg-blue-500/30">
              <Activity className="w-6 h-6 text-blue-200" />
            </div>
            <h4 className="text-xl font-semibold text-white mb-2">Use Template</h4>
            <p className="text-white/70 text-sm">Start with a pre-built template</p>
          </Link>

          <Link to="/chat" className="glass-card p-6 hover:scale-105 transition-transform cursor-pointer glow">
            <div className="workflow-card-icon bg-pink-500/30">
              <Users className="w-6 h-6 text-pink-200" />
            </div>
            <h4 className="text-xl font-semibold text-white mb-2">AI Assistant</h4>
            <p className="text-white/70 text-sm">Get help building workflows with AI</p>
          </Link>
        </div>
      </div>
    </div>
  )
}
