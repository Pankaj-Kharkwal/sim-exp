import { useState, useEffect } from 'react'
import { useNavigate, Link, useSearchParams } from 'react-router-dom'
import { Eye, EyeOff } from 'lucide-react'
import { useUserStore } from '@/stores/userStore'
import { cn } from '@/lib/utils'

const PASSWORD_VALIDATIONS = {
  minLength: { regex: /.{8,}/, message: 'Password must be at least 8 characters long.' },
  uppercase: {
    regex: /(?=.*?[A-Z])/,
    message: 'Password must include at least one uppercase letter.',
  },
  lowercase: {
    regex: /(?=.*?[a-z])/,
    message: 'Password must include at least one lowercase letter.',
  },
  number: { regex: /(?=.*?[0-9])/, message: 'Password must include at least one number.' },
  special: {
    regex: /(?=.*?[#?!@$%^&*-])/,
    message: 'Password must include at least one special character.',
  },
}

const NAME_VALIDATIONS = {
  required: {
    test: (value: string) => Boolean(value && typeof value === 'string'),
    message: 'Name is required.',
  },
  notEmpty: {
    test: (value: string) => value.trim().length > 0,
    message: 'Name cannot be empty.',
  },
  validCharacters: {
    regex: /^[\p{L}\s\-']+$/u,
    message: 'Name can only contain letters, spaces, hyphens, and apostrophes.',
  },
}

const validateEmail = (email: string): string[] => {
  const errors: string[] = []

  if (!email || !email.trim()) {
    errors.push('Email is required.')
    return errors
  }

  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  if (!emailRegex.test(email)) {
    errors.push('Please enter a valid email address.')
  }

  return errors
}

export default function SignupPage() {
  const navigate = useNavigate()
  const [searchParams] = useSearchParams()
  const [showPassword, setShowPassword] = useState(false)

  const [name, setName] = useState('')
  const [email, setEmail] = useState(searchParams.get('email') || '')
  const [password, setPassword] = useState('')

  const [nameErrors, setNameErrors] = useState<string[]>([])
  const [emailErrors, setEmailErrors] = useState<string[]>([])
  const [passwordErrors, setPasswordErrors] = useState<string[]>([])

  const [showNameError, setShowNameError] = useState(false)
  const [showEmailError, setShowEmailError] = useState(false)
  const [showPasswordError, setShowPasswordError] = useState(false)

  const { signup, isLoading, error, isAuthenticated, clearError } = useUserStore()
  const generalError = error || ''

  // Redirect if already authenticated
  useEffect(() => {
    if (isAuthenticated) {
      const redirect = searchParams.get('redirect') || '/dashboard'
      navigate(redirect)
    }
  }, [isAuthenticated, navigate, searchParams])

  // Clear errors when component unmounts
  useEffect(() => {
    return () => clearError()
  }, [clearError])

  const validatePassword = (passwordValue: string): string[] => {
    const errors: string[] = []

    if (!PASSWORD_VALIDATIONS.minLength.regex.test(passwordValue)) {
      errors.push(PASSWORD_VALIDATIONS.minLength.message)
    }
    if (!PASSWORD_VALIDATIONS.uppercase.regex.test(passwordValue)) {
      errors.push(PASSWORD_VALIDATIONS.uppercase.message)
    }
    if (!PASSWORD_VALIDATIONS.lowercase.regex.test(passwordValue)) {
      errors.push(PASSWORD_VALIDATIONS.lowercase.message)
    }
    if (!PASSWORD_VALIDATIONS.number.regex.test(passwordValue)) {
      errors.push(PASSWORD_VALIDATIONS.number.message)
    }
    if (!PASSWORD_VALIDATIONS.special.regex.test(passwordValue)) {
      errors.push(PASSWORD_VALIDATIONS.special.message)
    }

    return errors
  }

  const validateName = (nameValue: string): string[] => {
    const errors: string[] = []

    if (!NAME_VALIDATIONS.required.test(nameValue)) {
      errors.push(NAME_VALIDATIONS.required.message)
      return errors
    }
    if (!NAME_VALIDATIONS.notEmpty.test(nameValue)) {
      errors.push(NAME_VALIDATIONS.notEmpty.message)
      return errors
    }
    if (!NAME_VALIDATIONS.validCharacters.regex.test(nameValue.trim())) {
      errors.push(NAME_VALIDATIONS.validCharacters.message)
    }

    return errors
  }

  const handleNameChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value
    setName(value)
    const errors = validateName(value)
    setNameErrors(errors)
    setShowNameError(false)
  }

  const handleEmailChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value
    setEmail(value)
    const errors = validateEmail(value)
    setEmailErrors(errors)
    setShowEmailError(false)
    clearError()
  }

  const handlePasswordChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value
    setPassword(value)
    const errors = validatePassword(value)
    setPasswordErrors(errors)
    setShowPasswordError(false)
  }

  async function onSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault()
    clearError()

    const trimmedName = name.trim()
    const trimmedEmail = email.trim().toLowerCase()

    const nameValidationErrors = validateName(trimmedName)
    const emailValidationErrors = validateEmail(trimmedEmail)
    const passwordValidationErrors = validatePassword(password)

    setNameErrors(nameValidationErrors)
    setEmailErrors(emailValidationErrors)
    setPasswordErrors(passwordValidationErrors)

    setShowNameError(nameValidationErrors.length > 0)
    setShowEmailError(emailValidationErrors.length > 0)
    setShowPasswordError(passwordValidationErrors.length > 0)

    if (
      nameValidationErrors.length > 0 ||
      emailValidationErrors.length > 0 ||
      passwordValidationErrors.length > 0
    ) {
      return
    }

    try {
      await signup(trimmedEmail, password, trimmedName)
      // Navigation will happen via the useEffect above
    } catch (error: any) {
      console.error('Signup error:', error)

      // Check if it's a conflict error (email already exists)
      if (error.message?.includes('already registered') || error.message?.includes('409')) {
        setShowEmailError(true)
      }
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center p-4 relative overflow-hidden">
      {/* Aurora background */}
      <div className="aurora-background" />

      {/* Main signup card */}
      <div className="glass-card w-full max-w-md p-10 fade-in relative">
        {/* Logo and header */}
        <div className="text-center mb-10">
          <div className="inline-block mb-4">
            <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-purple-500/40 to-blue-500/40 flex items-center justify-center mx-auto shadow-lg shimmer">
              <svg className="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
            </div>
          </div>
          <h1 className="text-3xl font-bold text-white mb-3 slide-in">Create an Account</h1>
          <p className="text-white/70 slide-in" style={{ animationDelay: '0.1s' }}>Join Pankh.AI and start building workflows</p>
        </div>

        <form onSubmit={onSubmit} className="space-y-5">
          {generalError && (
            <div className="glass-card border-2 border-red-500/30 bg-red-500/10 p-4 rounded-xl fade-in">
              <div className="flex items-center gap-3">
                <svg className="w-5 h-5 text-red-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <p className="text-sm font-medium text-red-200">{generalError}</p>
              </div>
            </div>
          )}

          <div className="space-y-2 fade-in" style={{ animationDelay: '0.2s' }}>
            <label htmlFor="name" className="text-sm font-medium text-white/80 block">Full Name</label>
            <input
              id="name"
              name="name"
              type="text"
              autoCapitalize="words"
              autoComplete="name"
              placeholder="Enter your name"
              value={name}
              onChange={handleNameChange}
              className={cn(
                'glass-input w-full h-12',
                showNameError && nameErrors.length > 0 && 'border-red-500/50'
              )}
            />
            {showNameError && nameErrors.length > 0 && (
              <div className="mt-1 space-y-1">
                {nameErrors.map((error, index) => (
                  <p key={index} className="text-xs text-red-300">{error}</p>
                ))}
              </div>
            )}
          </div>

          <div className="space-y-2 fade-in" style={{ animationDelay: '0.3s' }}>
            <label htmlFor="email" className="text-sm font-medium text-white/80 block">Email</label>
            <input
              id="email"
              name="email"
              type="email"
              autoCapitalize="none"
              autoComplete="email"
              autoCorrect="off"
              placeholder="Enter your email"
              value={email}
              onChange={handleEmailChange}
              className={cn(
                'glass-input w-full h-12',
                showEmailError && emailErrors.length > 0 && 'border-red-500/50'
              )}
            />
            {showEmailError && emailErrors.length > 0 && (
              <div className="mt-1 space-y-1">
                {emailErrors.map((error, index) => (
                  <p key={index} className="text-xs text-red-300">{error}</p>
                ))}
              </div>
            )}
          </div>

          <div className="space-y-2 fade-in" style={{ animationDelay: '0.4s' }}>
            <label htmlFor="password" className="text-sm font-medium text-white/80 block">Password</label>
            <div className="relative">
              <input
                id="password"
                name="password"
                type={showPassword ? 'text' : 'password'}
                autoCapitalize="none"
                autoComplete="new-password"
                autoCorrect="off"
                placeholder="Enter your password"
                value={password}
                onChange={handlePasswordChange}
                className={cn(
                  'glass-input w-full h-12 pr-12',
                  showPasswordError && passwordErrors.length > 0 && 'border-red-500/50'
                )}
              />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="absolute top-1/2 -translate-y-1/2 right-3 text-white/60 transition hover:text-white"
                aria-label={showPassword ? 'Hide password' : 'Show password'}
              >
                {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
              </button>
            </div>
            {showPasswordError && passwordErrors.length > 0 && (
              <div className="mt-1 space-y-1">
                {passwordErrors.map((error, index) => (
                  <p key={index} className="text-xs text-red-300">{error}</p>
                ))}
              </div>
            )}
          </div>

          <button
            type="submit"
            className="glass-button w-full mt-6 h-12 font-semibold text-base bg-gradient-to-r from-purple-500/30 to-blue-500/30 disabled:opacity-50 fade-in"
            style={{ animationDelay: '0.5s' }}
            disabled={isLoading}
          >
            {isLoading ? (
              <div className="flex items-center justify-center gap-2">
                <svg className="animate-spin h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                <span>Creating account...</span>
              </div>
            ) : 'Create Account'}
          </button>
        </form>

        <div className="mt-8 text-center fade-in" style={{ animationDelay: '0.6s' }}>
          <div className="relative">
            <div className="absolute inset-0 flex items-center">
              <div className="w-full border-t border-white/20"></div>
            </div>
            <div className="relative flex justify-center text-xs uppercase">
              <span className="bg-white/10 px-4 text-white/60 backdrop-blur-sm rounded-full">
                or
              </span>
            </div>
          </div>
        </div>

        <div className="mt-6 text-center fade-in" style={{ animationDelay: '0.7s' }}>
          <span className="text-white/70">Already have an account? </span>
          <Link
            to="/login"
            className="font-semibold text-white underline-offset-4 transition hover:underline"
          >
            Sign in
          </Link>
        </div>

        <div className="mt-6 text-center text-xs text-white/60 fade-in" style={{ animationDelay: '0.8s' }}>
          By creating an account, you agree to our{' '}
          <Link
            to="/terms"
            className="underline-offset-4 transition hover:underline text-white/80"
          >
            Terms of Service
          </Link>{' '}
          and{' '}
          <Link
            to="/privacy"
            className="underline-offset-4 transition hover:underline text-white/80"
          >
            Privacy Policy
          </Link>
        </div>
      </div>
    </div>
  )
}
