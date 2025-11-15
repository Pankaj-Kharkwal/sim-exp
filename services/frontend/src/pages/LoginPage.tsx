import { useState, useEffect } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { useUserStore } from '@/stores/userStore'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Alert } from '@/components/ui/alert'

export default function LoginPage() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const navigate = useNavigate()

  const { login, isLoading, error, isAuthenticated, clearError } = useUserStore()

  // Redirect if already authenticated
  useEffect(() => {
    if (isAuthenticated) {
      navigate('/dashboard')
    }
  }, [isAuthenticated, navigate])

  // Clear errors when component unmounts
  useEffect(() => {
    return () => clearError()
  }, [clearError])

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault()

    try {
      await login(email, password)
      // Navigation will happen via the useEffect above
    } catch (err) {
      // Error is already set in store
      console.error('Login failed:', err)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center p-4 relative overflow-hidden">
      {/* Animated background orbs */}
      <div className="parallax-bg" />

      {/* Main login card */}
      <div className="glass-modal w-full max-w-md p-10 animate-scaleIn relative">
        {/* Logo and header */}
        <div className="text-center mb-10">
          <div className="inline-block mb-4">
            <div className="w-16 h-16 rounded-2xl gradient-animated flex items-center justify-center mx-auto shadow-lg">
              <svg className="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
            </div>
          </div>
          <h1 className="text-heading-1 text-gradient mb-3 animate-slideIn">Pankh.AI</h1>
          <p className="text-body animate-slideIn delay-100">Welcome back! Sign in to continue your journey</p>
        </div>

        <form onSubmit={handleLogin} className="space-y-5">
          {error && (
            <div className="glass-card-enhanced border-2 border-red-500/30 bg-red-500/10 p-4 rounded-xl animate-slideIn">
              <div className="flex items-center gap-3">
                <svg className="w-5 h-5 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <p className="text-sm font-medium text-red-600 dark:text-red-400">{error}</p>
              </div>
            </div>
          )}

          <div className="space-y-2 animate-slideIn delay-200">
            <label htmlFor="email" className="text-sm font-medium text-secondary block">Email Address</label>
            <input
              id="email"
              type="email"
              placeholder="admin@pankh.ai"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              disabled={isLoading}
              className="input transition-all focus:scale-[1.01]"
            />
          </div>

          <div className="space-y-2 animate-slideIn delay-300">
            <label htmlFor="password" className="text-sm font-medium text-secondary block">Password</label>
            <input
              id="password"
              type="password"
              placeholder="••••••••"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              disabled={isLoading}
              className="input transition-all focus:scale-[1.01]"
            />
          </div>

          <button
            type="submit"
            className="btn btn-primary btn-ripple w-full mt-6 h-12 font-semibold text-base shadow-xl hover:shadow-2xl transition-all hover:scale-[1.02] active:scale-[0.98] animate-slideIn delay-400"
            disabled={isLoading}
          >
            {isLoading ? (
              <div className="flex items-center justify-center gap-2">
                <svg className="animate-spin h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                <span>Signing in...</span>
              </div>
            ) : 'Sign In'}
          </button>
        </form>

        <div className="mt-8 text-center animate-slideIn delay-500">
          <div className="relative">
            <div className="absolute inset-0 flex items-center">
              <div className="w-full border-t border-subtle"></div>
            </div>
            <div className="relative flex justify-center text-xs uppercase">
              <span className="bg-white/50 dark:bg-black/50 px-4 text-tertiary backdrop-blur-sm rounded-full">
                or
              </span>
            </div>
          </div>
        </div>

        <div className="mt-6 text-center animate-slideIn delay-600">
          <span className="text-body">Don't have an account? </span>
          <Link
            to="/signup"
            className="font-semibold text-gradient underline-offset-4 transition hover:underline"
          >
            Create one now
          </Link>
        </div>

        <div className="mt-8 glass-card-enhanced p-5 rounded-xl animate-slideIn delay-700">
          <p className="text-small font-medium text-center mb-3 text-secondary">✨ Demo Accounts</p>
          <div className="space-y-2">
            <div className="glass-button p-3 rounded-lg text-center hover:scale-[1.02] transition-all cursor-pointer" onClick={() => { setEmail('admin@pankh.ai'); setPassword('admin123'); }}>
              <p className="text-xs font-mono text-primary">admin@pankh.ai / admin123</p>
            </div>
            <div className="glass-button p-3 rounded-lg text-center hover:scale-[1.02] transition-all cursor-pointer" onClick={() => { setEmail('demo@pankh.ai'); setPassword('admin123'); }}>
              <p className="text-xs font-mono text-primary">demo@pankh.ai / admin123</p>
            </div>
            <div className="glass-button p-3 rounded-lg text-center hover:scale-[1.02] transition-all cursor-pointer" onClick={() => { setEmail('user@pankh.ai'); setPassword('admin123'); }}>
              <p className="text-xs font-mono text-primary">user@pankh.ai / admin123</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
