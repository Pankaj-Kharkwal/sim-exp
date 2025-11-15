import { useState, useEffect } from 'react'
import { useNavigate, Link, useSearchParams } from 'react-router-dom'
import { Eye, EyeOff } from 'lucide-react'
import { useUserStore } from '@/stores/userStore'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
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
    <div className="flex min-h-screen items-center justify-center bg-gray-50 px-4 py-12 sm:px-6 lg:px-8">
      <div className="w-full max-w-md space-y-8">
        <div className="text-center">
          <h1 className="font-medium text-3xl text-gray-900 tracking-tight">
            Create an account
          </h1>
          <p className="mt-2 text-gray-600 text-sm">
            Create an account or log in
          </p>
        </div>

        <form onSubmit={onSubmit} className="mt-8 space-y-6">
          {generalError && (
            <div className="rounded-md bg-red-50 p-4">
              <p className="text-red-800 text-sm">{generalError}</p>
            </div>
          )}

          <div className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="name">Full name</Label>
              <Input
                id="name"
                name="name"
                type="text"
                autoCapitalize="words"
                autoComplete="name"
                placeholder="Enter your name"
                value={name}
                onChange={handleNameChange}
                className={cn(
                  'rounded-lg shadow-sm transition-colors',
                  showNameError &&
                    nameErrors.length > 0 &&
                    'border-red-500 focus:border-red-500 focus:ring-red-100'
                )}
              />
              {showNameError && nameErrors.length > 0 && (
                <div className="mt-1 space-y-1 text-red-500 text-xs">
                  {nameErrors.map((error, index) => (
                    <p key={index}>{error}</p>
                  ))}
                </div>
              )}
            </div>

            <div className="space-y-2">
              <Label htmlFor="email">Email</Label>
              <Input
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
                  'rounded-lg shadow-sm transition-colors',
                  showEmailError &&
                    emailErrors.length > 0 &&
                    'border-red-500 focus:border-red-500 focus:ring-red-100'
                )}
              />
              {showEmailError && emailErrors.length > 0 && (
                <div className="mt-1 space-y-1 text-red-500 text-xs">
                  {emailErrors.map((error, index) => (
                    <p key={index}>{error}</p>
                  ))}
                </div>
              )}
            </div>

            <div className="space-y-2">
              <Label htmlFor="password">Password</Label>
              <div className="relative">
                <Input
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
                    'rounded-lg pr-10 shadow-sm transition-colors',
                    showPasswordError &&
                      passwordErrors.length > 0 &&
                      'border-red-500 focus:border-red-500 focus:ring-red-100'
                  )}
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="-translate-y-1/2 absolute top-1/2 right-3 text-gray-500 transition hover:text-gray-700"
                  aria-label={showPassword ? 'Hide password' : 'Show password'}
                >
                  {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
                </button>
              </div>
              {showPasswordError && passwordErrors.length > 0 && (
                <div className="mt-1 space-y-1 text-red-500 text-xs">
                  {passwordErrors.map((error, index) => (
                    <p key={index}>{error}</p>
                  ))}
                </div>
              )}
            </div>
          </div>

          <Button
            type="submit"
            className="flex w-full items-center justify-center gap-2 rounded-lg bg-gradient-to-r from-purple-600 to-blue-600 font-medium text-white transition-all duration-200 hover:from-purple-700 hover:to-blue-700"
            disabled={isLoading}
          >
            {isLoading ? 'Creating account...' : 'Create account'}
          </Button>
        </form>

        <div className="pt-4 text-center text-sm">
          <span className="text-gray-600">Already have an account? </span>
          <Link
            to="/login"
            className="font-medium text-purple-600 underline-offset-4 transition hover:text-purple-700 hover:underline"
          >
            Sign in
          </Link>
        </div>

        <div className="text-center text-gray-500 text-xs">
          By creating an account, you agree to our{' '}
          <Link
            to="/terms"
            className="underline-offset-4 transition hover:underline"
          >
            Terms of Service
          </Link>{' '}
          and{' '}
          <Link
            to="/privacy"
            className="underline-offset-4 transition hover:underline"
          >
            Privacy Policy
          </Link>
        </div>
      </div>
    </div>
  )
}
