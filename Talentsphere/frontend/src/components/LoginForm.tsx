import React, { useState } from 'react';
import { 
  Lock, 
  Mail, 
  Eye, 
  EyeOff, 
  ArrowRight, 
  ShieldCheck, 
  Loader2, 
  Building2, 
  Fingerprint,
  Info
} from 'lucide-react';
import { LoginMode, UserPreset, RegionOption } from '../types';
import { DEMO_PRESETS } from '../data/presets';

interface LoginFormProps {
  onLoginSubmit: (email: string, pass: string, mode: LoginMode, preset?: UserPreset) => void;
  onOpenForgotPassword: (email: string) => void;
  onOpenComplianceModal: () => void;
  selectedRegion: RegionOption;
  onSelectRegion: (region: RegionOption) => void;
}

export const LoginForm: React.FC<LoginFormProps> = ({
  onLoginSubmit,
  onOpenForgotPassword,
  onOpenComplianceModal,
}) => {
  const [mode, setMode] = useState<LoginMode>('password');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [ssoDomain, setSsoDomain] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [rememberDevice, setRememberDevice] = useState(true);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [selectedPreset, setSelectedPreset] = useState<UserPreset | null>(null);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    if (mode === 'password') {
      if (!email || !email.includes('@')) {
        setError('Please enter a valid enterprise work email');
        return;
      }
      if (!password || password.length < 6) {
        setError('Password must be at least 6 characters');
        return;
      }
    } else if (mode === 'sso') {
      if (!ssoDomain && !email) {
        setError('Please enter your enterprise domain or identity email');
        return;
      }
    }

    setIsLoading(true);

    setTimeout(() => {
      setIsLoading(false);
      onLoginSubmit(email || ssoDomain, password, mode, selectedPreset || DEMO_PRESETS[0]);
    }, 900);
  };

  return (
    <div className="w-full max-w-lg mx-auto">
      {/* Main Authentication Card */}
      <div className="relative rounded-2xl glass-card p-6 sm:p-8 shadow-2xl text-left transition-all">
        
        {/* Card Header */}
        <div className="mb-6">
          <h2 className="text-2xl font-medium dark:text-white light:text-zinc-900 tracking-tight">Sign In to TalentSphere</h2>
          <p className="text-xs dark:text-zinc-400 light:text-zinc-600 mt-1 font-normal">Enter your corporate credentials to access your autonomous hiring pipeline.</p>
        </div>

        {/* Auth Mode Tabs (Segmented Control) */}
        <div className="grid grid-cols-3 gap-1 p-1 rounded-xl glass-panel mb-6 text-xs font-medium">
          <button
            type="button"
            onClick={() => {
              setMode('password');
              setError('');
            }}
            className={`py-2 px-3 rounded-lg transition-all flex items-center justify-center gap-1.5 ${
              mode === 'password'
                ? 'bg-zinc-900 text-white font-medium shadow-sm'
                : 'text-zinc-500 hover:text-zinc-900 dark:hover:text-white'
            }`}
          >
            <Mail className="w-3.5 h-3.5" />
            <span>Password</span>
          </button>

          <button
            type="button"
            onClick={() => {
              setMode('sso');
              setError('');
            }}
            className={`py-2 px-3 rounded-lg transition-all flex items-center justify-center gap-1.5 ${
              mode === 'sso'
                ? 'bg-zinc-900 text-white font-medium shadow-sm'
                : 'text-zinc-500 hover:text-zinc-900 dark:hover:text-white'
            }`}
          >
            <Building2 className="w-3.5 h-3.5" />
            <span>SSO / SAML</span>
          </button>

          <button
            type="button"
            onClick={() => {
              setMode('passkey');
              setError('');
            }}
            className={`py-2 px-3 rounded-lg transition-all flex items-center justify-center gap-1.5 ${
              mode === 'passkey'
                ? 'bg-zinc-900 text-white font-medium shadow-sm'
                : 'text-zinc-500 hover:text-zinc-900 dark:hover:text-white'
            }`}
          >
            <Fingerprint className="w-3.5 h-3.5" />
            <span>Passkey</span>
          </button>
        </div>

        {/* Form Controls */}
        <form onSubmit={handleSubmit} className="space-y-4">
          {mode === 'password' && (
            <>
              {/* Work Email */}
              <div>
                <label
                  htmlFor="work-email"
                  className="block text-xs font-medium dark:text-zinc-300 light:text-zinc-700 mb-1.5"
                >
                  Work Email Address
                </label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-zinc-400">
                    <Mail className="w-4 h-4" />
                  </div>
                  <input
                    id="work-email"
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="name@company.com"
                    required
                    className="w-full pl-10 pr-4 py-3 rounded-xl dark:bg-black/80 light:bg-white border border-zinc-300 dark:border-zinc-700 text-zinc-900 dark:text-white placeholder-zinc-400 text-sm font-normal focus:outline-none transition"
                  />
                </div>
              </div>

              {/* Password */}
              <div>
                <div className="flex items-center justify-between mb-1.5">
                  <label
                    htmlFor="work-password"
                    className="block text-xs font-medium dark:text-zinc-300 light:text-zinc-700"
                  >
                    Password
                  </label>
                  <button
                    type="button"
                    onClick={() => onOpenForgotPassword(email)}
                    className="text-xs text-zinc-600 dark:text-zinc-400 hover:underline font-medium transition"
                  >
                    Forgot password?
                  </button>
                </div>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-zinc-400">
                    <Lock className="w-4 h-4" />
                  </div>
                  <input
                    id="work-password"
                    type={showPassword ? 'text' : 'password'}
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="••••••••••••"
                    required
                    className="w-full pl-10 pr-10 py-3 rounded-xl dark:bg-black/80 light:bg-white border border-zinc-300 dark:border-zinc-700 text-zinc-900 dark:text-white placeholder-zinc-400 text-sm font-normal focus:outline-none transition"
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute inset-y-0 right-0 pr-3.5 flex items-center text-zinc-400 hover:text-zinc-700 transition"
                    aria-label={showPassword ? 'Hide password' : 'Show password'}
                  >
                    {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                  </button>
                </div>
              </div>

              {/* Trust Workstation */}
              <div className="flex items-center justify-between pt-1">
                <label className="flex items-center gap-2 cursor-pointer select-none">
                  <input
                    type="checkbox"
                    checked={rememberDevice}
                    onChange={(e) => setRememberDevice(e.target.checked)}
                    className="w-4 h-4 rounded bg-zinc-100 dark:bg-zinc-800 border-zinc-300 dark:border-zinc-700 text-zinc-900 focus:ring-0"
                  />
                  <span className="text-xs dark:text-zinc-400 light:text-zinc-600 font-normal">
                    Trust this workstation for 30 days
                  </span>
                </label>
              </div>
            </>
          )}

          {mode === 'sso' && (
            <div className="space-y-3">
              <div>
                <label
                  htmlFor="sso-domain"
                  className="block text-xs font-medium dark:text-zinc-300 light:text-zinc-700 mb-1.5"
                >
                  Enterprise Identity Domain / SAML Endpoint
                </label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-zinc-400">
                    <Building2 className="w-4 h-4" />
                  </div>
                  <input
                    id="sso-domain"
                    type="text"
                    value={ssoDomain || email}
                    onChange={(e) => {
                      setSsoDomain(e.target.value);
                      setEmail(e.target.value);
                    }}
                    placeholder="acme.okta.com or name@acme.com"
                    required
                    className="w-full pl-10 pr-4 py-3 rounded-xl dark:bg-black/80 light:bg-white border border-zinc-300 dark:border-zinc-700 text-zinc-900 dark:text-white placeholder-zinc-400 text-sm font-normal focus:outline-none transition"
                  />
                </div>
              </div>

              <div className="p-3 rounded-xl glass-panel text-xs dark:text-zinc-400 light:text-zinc-600 font-normal">
                <p className="font-medium dark:text-white light:text-zinc-900 flex items-center gap-1.5 mb-1">
                  <ShieldCheck className="w-3.5 h-3.5 text-emerald-600 dark:text-emerald-400" /> Automated SAML 2.0 / OIDC Handshake
                </p>
                <p className="text-[11px] leading-relaxed">
                  Redirects to your corporate Identity Provider (Okta, Azure AD, Ping, Google) with SCIM provisioning.
                </p>
              </div>
            </div>
          )}

          {mode === 'passkey' && (
            <div className="p-6 rounded-2xl glass-panel text-center space-y-2">
              <div className="w-11 h-11 rounded-2xl glass-card flex items-center justify-center dark:text-white light:text-zinc-900 mx-auto">
                <Fingerprint className="w-6 h-6 text-zinc-400" />
              </div>
              <h4 className="text-xs font-medium dark:text-white light:text-zinc-900">Hardware Key / WebAuthn Biometrics</h4>
              <p className="text-xs dark:text-zinc-400 light:text-zinc-600 max-w-xs mx-auto font-normal">
                Authenticate using YubiKey or biometric verification (Touch ID / Windows Hello).
              </p>
            </div>
          )}

          {/* Error Message */}
          {error && (
            <div className="p-3 rounded-xl glass-panel text-xs text-red-600 dark:text-red-400 font-medium flex items-center gap-2">
              <Info className="w-4 h-4 text-red-500 shrink-0" />
              <span>{error}</span>
            </div>
          )}

          {/* Primary Action Button */}
          <button
            type="submit"
            disabled={isLoading}
            className="w-full mt-2 py-3.5 px-5 rounded-full bg-zinc-900 text-white font-medium text-sm tracking-wide shadow-sm flex items-center justify-center gap-2 transition duration-150 disabled:opacity-50 hover:bg-zinc-800"
          >
            {isLoading ? (
              <>
                <Loader2 className="w-4 h-4 animate-spin text-white" />
                <span>Authenticating Identity Token...</span>
              </>
            ) : (
              <>
                <span>Sign In to TalentSphere</span>
                <ArrowRight className="w-4 h-4" />
              </>
            )}
          </button>
        </form>

        {/* Footer info inside card */}
        <div className="mt-6 pt-4 border-t border-zinc-200 dark:border-zinc-800 flex items-center justify-between text-xs dark:text-zinc-400 light:text-zinc-600 font-normal">
          <span className="flex items-center gap-1.5 text-[11px]">
            <Lock className="w-3.5 h-3.5 text-zinc-400" />
            256-bit Encrypted Session
          </span>

          <button
            type="button"
            onClick={onOpenComplianceModal}
            className="dark:text-zinc-300 light:text-zinc-700 hover:text-zinc-900 dark:hover:text-white font-medium text-[11px] underline underline-offset-2 transition"
          >
            Security Brief
          </button>
        </div>
      </div>
    </div>
  );
};
