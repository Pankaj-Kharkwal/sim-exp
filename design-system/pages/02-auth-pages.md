# Authentication Pages Design

> **Routes**: `/login`, `/signup`
> **Type**: Public authentication
> **Goal**: Frictionless, secure user authentication

---

## 🎯 Login Page (`/login`)

### Layout Overview

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│                     ┌─────────────────┐                     │
│                     │                 │                     │
│                     │                 │                     │
│      [BRAND]        │  LOGIN FORM     │      [IMAGE/       │
│                     │                 │       VISUAL]      │
│                     │  - Email        │                     │
│                     │  - Password     │                     │
│                     │  - OAuth        │                     │
│                     │  - Submit       │                     │
│                     │                 │                     │
│                     └─────────────────┘                     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Full Implementation

```tsx
// app/(auth)/login/page.tsx
export default function LoginPage() {
  return (
    <div className="min-h-screen flex">
      {/* Left Side - Form */}
      <div className="flex-1 flex items-center justify-center p-8 bg-bg">
        <div className="w-full max-w-md space-y-8">
          {/* Logo */}
          <div className="text-center">
            <Logo className="mx-auto h-12 w-auto" />
            <h1 className="mt-6 text-3xl font-bold text-text-primary">
              Welcome back
            </h1>
            <p className="mt-2 text-sm text-text-secondary">
              Sign in to your account to continue
            </p>
          </div>

          {/* OAuth Buttons */}
          <div className="space-y-3">
            <Button
              variant="outline"
              className="w-full"
              onClick={() => signIn('github')}
            >
              <Github className="w-5 h-5 mr-2" />
              Continue with GitHub
            </Button>
            <Button
              variant="outline"
              className="w-full"
              onClick={() => signIn('google')}
            >
              <svg className="w-5 h-5 mr-2" viewBox="0 0 24 24">{/* Google icon */}</svg>
              Continue with Google
            </Button>
          </div>

          {/* Divider */}
          <div className="relative">
            <div className="absolute inset-0 flex items-center">
              <div className="w-full border-t border-border" />
            </div>
            <div className="relative flex justify-center text-sm">
              <span className="px-2 bg-bg text-text-muted">Or continue with email</span>
            </div>
          </div>

          {/* Email/Password Form */}
          <form className="space-y-4" onSubmit={handleSubmit}>
            <Input
              label="Email address"
              type="email"
              placeholder="you@company.com"
              required
              autoComplete="email"
            />
            <div className="space-y-1">
              <Input
                label="Password"
                type="password"
                placeholder="••••••••"
                required
                autoComplete="current-password"
              />
              <div className="flex justify-end">
                <Link
                  href="/forgot-password"
                  className="text-sm text-primary hover:text-primary-hover"
                >
                  Forgot password?
                </Link>
              </div>
            </div>

            <Button type="submit" variant="primary" className="w-full" size="lg">
              Sign In
            </Button>
          </form>

          {/* Footer */}
          <p className="text-center text-sm text-text-secondary">
            Don't have an account?{' '}
            <Link href="/signup" className="text-primary hover:text-primary-hover font-medium">
              Sign up
            </Link>
          </p>
        </div>
      </div>

      {/* Right Side - Visual */}
      <div className="hidden lg:flex lg:flex-1 bg-gradient-to-br from-primary/10 via-bg to-secondary/10 items-center justify-center p-12">
        <div className="max-w-md space-y-8">
          <div className="space-y-4">
            <h2 className="text-3xl font-bold text-text-primary">
              Automate anything with AI
            </h2>
            <p className="text-lg text-text-secondary">
              Build powerful workflows in minutes with our visual editor and AI agents.
            </p>
          </div>

          {/* Feature List */}
          <ul className="space-y-4">
            <Feature
              icon={<Zap className="w-5 h-5" />}
              text="Visual workflow builder"
            />
            <Feature
              icon={<Brain className="w-5 h-5" />}
              text="AI agent integration"
            />
            <Feature
              icon={<Boxes className="w-5 h-5" />}
              text="81+ pre-built integrations"
            />
          </ul>

          {/* Testimonial */}
          <blockquote className="border-l-4 border-primary pl-4 italic text-text-secondary">
            "Pankh AI reduced our automation time by 80%. The platform is incredibly powerful."
            <footer className="text-sm mt-2 not-italic text-text-muted">
              — Sarah Chen, Engineering Lead at TechCorp
            </footer>
          </blockquote>
        </div>
      </div>
    </div>
  )
}
```

### Component Styles

```css
/* Form container */
.auth-form-container {
  @apply w-full max-w-md space-y-8;
}

/* OAuth button */
.oauth-button {
  @apply w-full h-11 px-4 rounded-lg;
  @apply border border-border bg-bg;
  @apply hover:bg-surface-2 hover:border-border-secondary;
  @apply transition-all duration-150;
  @apply flex items-center justify-center gap-2;
  @apply text-sm font-medium text-text-primary;
}

/* Divider */
.auth-divider {
  @apply relative py-4;
}

.auth-divider::before {
  @apply absolute inset-0 flex items-center;
  content: '';
  @apply border-t border-border;
}

.auth-divider-text {
  @apply relative flex justify-center text-sm;
  @apply px-2 bg-bg text-text-muted;
}
```

---

## 🎯 Signup Page (`/signup`)

### Layout (Similar to Login with variations)

```tsx
// app/(auth)/signup/page.tsx
export default function SignupPage() {
  return (
    <div className="min-h-screen flex">
      <div className="flex-1 flex items-center justify-center p-8 bg-bg">
        <div className="w-full max-w-md space-y-8">
          {/* Logo */}
          <div className="text-center">
            <Logo className="mx-auto h-12 w-auto" />
            <h1 className="mt-6 text-3xl font-bold text-text-primary">
              Create your account
            </h1>
            <p className="mt-2 text-sm text-text-secondary">
              Start automating your workflows in minutes
            </p>
          </div>

          {/* OAuth Buttons */}
          <div className="space-y-3">
            <Button variant="outline" className="w-full" onClick={() => signIn('github')}>
              <Github className="w-5 h-5 mr-2" />
              Sign up with GitHub
            </Button>
            <Button variant="outline" className="w-full" onClick={() => signIn('google')}>
              <svg className="w-5 h-5 mr-2" viewBox="0 0 24 24">{/* Google icon */}</svg>
              Sign up with Google
            </Button>
          </div>

          {/* Divider */}
          <div className="relative">
            <div className="absolute inset-0 flex items-center">
              <div className="w-full border-t border-border" />
            </div>
            <div className="relative flex justify-center text-sm">
              <span className="px-2 bg-bg text-text-muted">Or sign up with email</span>
            </div>
          </div>

          {/* Signup Form */}
          <form className="space-y-4" onSubmit={handleSubmit}>
            <Input
              label="Full name"
              type="text"
              placeholder="John Doe"
              required
              autoComplete="name"
            />
            <Input
              label="Email address"
              type="email"
              placeholder="you@company.com"
              required
              autoComplete="email"
            />
            <div className="space-y-2">
              <Input
                label="Password"
                type="password"
                placeholder="••••••••"
                required
                autoComplete="new-password"
              />
              {/* Password strength indicator */}
              <PasswordStrength password={password} />
              <p className="text-xs text-text-muted">
                Must be at least 8 characters with uppercase, lowercase, and numbers
              </p>
            </div>

            {/* Terms checkbox */}
            <div className="flex items-start gap-2">
              <Checkbox id="terms" required />
              <label htmlFor="terms" className="text-sm text-text-secondary leading-relaxed">
                I agree to the{' '}
                <Link href="/terms" className="text-primary hover:underline">
                  Terms of Service
                </Link>{' '}
                and{' '}
                <Link href="/privacy" className="text-primary hover:underline">
                  Privacy Policy
                </Link>
              </label>
            </div>

            <Button type="submit" variant="primary" className="w-full" size="lg">
              Create Account
            </Button>
          </form>

          {/* Footer */}
          <p className="text-center text-sm text-text-secondary">
            Already have an account?{' '}
            <Link href="/login" className="text-primary hover:text-primary-hover font-medium">
              Sign in
            </Link>
          </p>
        </div>
      </div>

      {/* Right Side - Same as Login */}
      <div className="hidden lg:flex lg:flex-1 bg-gradient-to-br from-primary/10 via-bg to-secondary/10 items-center justify-center p-12">
        {/* Same content as login page */}
      </div>
    </div>
  )
}
```

---

## 🔒 Password Strength Component

```tsx
// components/auth/password-strength.tsx
export function PasswordStrength({ password }: { password: string }) {
  const strength = calculateStrength(password)

  return (
    <div className="space-y-1.5">
      <div className="flex gap-1.5">
        <div className={cn(
          'h-1 flex-1 rounded-full transition-colors',
          strength >= 1 ? 'bg-error' : 'bg-surface-3'
        )} />
        <div className={cn(
          'h-1 flex-1 rounded-full transition-colors',
          strength >= 2 ? 'bg-warning' : 'bg-surface-3'
        )} />
        <div className={cn(
          'h-1 flex-1 rounded-full transition-colors',
          strength >= 3 ? 'bg-success' : 'bg-surface-3'
        )} />
        <div className={cn(
          'h-1 flex-1 rounded-full transition-colors',
          strength >= 4 ? 'bg-success' : 'bg-surface-3'
        )} />
      </div>
      <p className="text-xs text-text-muted">
        {strength === 0 && 'Enter a password'}
        {strength === 1 && 'Weak password'}
        {strength === 2 && 'Fair password'}
        {strength === 3 && 'Good password'}
        {strength === 4 && 'Strong password'}
      </p>
    </div>
  )
}

function calculateStrength(password: string): number {
  let strength = 0
  if (password.length >= 8) strength++
  if (password.match(/[a-z]/) && password.match(/[A-Z]/)) strength++
  if (password.match(/\d/)) strength++
  if (password.match(/[^a-zA-Z\d]/)) strength++
  return strength
}
```

---

## 🎨 Design Tokens Used

**Layout**:
- Split layout: 50/50 on desktop, full-width form on mobile
- Form container: max-w-md (448px)
- Padding: p-8
- Spacing: space-y-8 (sections), space-y-4 (form fields)

**Colors**:
- Background: bg, surface-1
- Right panel: gradient-to-br from-primary/10 to-secondary/10
- Text: text-primary, text-secondary, text-muted
- Links: text-primary with hover:text-primary-hover

**Typography**:
- H1: text-3xl font-bold
- Body: text-sm, text-base
- Labels: text-sm font-medium
- Helper text: text-xs text-text-muted

**Components**:
- Inputs: h-11, rounded-lg
- Buttons: size-lg, w-full
- OAuth buttons: outline variant, w-full
- Divider: border-t with centered text

---

## 🔐 Security Features

1. **Password Requirements**:
   - Minimum 8 characters
   - Mix of uppercase, lowercase, numbers
   - Visual strength indicator

2. **OAuth Security**:
   - PKCE flow for authorization
   - Secure state parameter
   - Token storage in httpOnly cookies

3. **Form Validation**:
   - Client-side: Real-time validation with error messages
   - Server-side: Validation before account creation
   - Email verification required

4. **Error Handling**:
   ```tsx
   {error && (
     <div className="rounded-lg bg-error-bg border border-error-border p-4">
       <div className="flex items-center gap-2">
         <AlertCircle className="w-5 h-5 text-error" />
         <p className="text-sm text-error">{error}</p>
       </div>
     </div>
   )}
   ```

---

## ♿ Accessibility

- [ ] Form fields have associated labels
- [ ] Password field has show/hide toggle with ARIA label
- [ ] Error messages announced by screen readers
- [ ] Focus states on all interactive elements
- [ ] Tab order follows visual flow
- [ ] OAuth buttons have descriptive text (not just icons)
- [ ] Terms checkbox is keyboard accessible

---

## 📱 Responsive Design

**Mobile (< 1024px)**:
- Hide right visual panel
- Full-width form centered
- Stack OAuth buttons
- Adjust padding to p-6

**Desktop (>= 1024px)**:
- 50/50 split layout
- Fixed max-width form (448px)
- Show visual/testimonial panel

---

## ✨ Interactions

**Focus States**:
```css
input:focus {
  @apply outline-none ring-2 ring-primary ring-offset-2;
}
```

**Loading States**:
```tsx
<Button disabled={isLoading}>
  {isLoading ? (
    <>
      <Loader2 className="w-4 h-4 mr-2 animate-spin" />
      Signing in...
    </>
  ) : (
    'Sign In'
  )}
</Button>
```

**Success State** (after signup):
```tsx
{success && (
  <div className="rounded-lg bg-success-bg border border-success-border p-4">
    <div className="flex items-center gap-2">
      <CheckCircle className="w-5 h-5 text-success" />
      <p className="text-sm text-green-700">
        Account created! Check your email to verify.
      </p>
    </div>
  </div>
)}
```

---

## 🔄 Flow Diagram

```
LOGIN FLOW:
User enters credentials → Validate → Authenticate → Redirect to /workspace/default

SIGNUP FLOW:
User creates account → Send verification email → Verify email → Redirect to onboarding

OAUTH FLOW:
User clicks OAuth → Redirect to provider → Callback → Create/login user → Redirect to workspace
```

---

**Implementation Files**:
- `/apps/sim/app/(auth)/login/page.tsx`
- `/apps/sim/app/(auth)/signup/page.tsx`
- `/apps/sim/app/(auth)/login/login-form.tsx`
- `/apps/sim/app/(auth)/signup/signup-form.tsx`
