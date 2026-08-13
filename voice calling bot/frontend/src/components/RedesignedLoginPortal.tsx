import React, { useState } from 'react';
import { 
  ChevronDown,
  Sparkles,
  Sliders,
  Terminal,
  Bot
} from 'lucide-react';
import type { LoginMode, UserPreset, RegionOption, AsciiPalette, AsciiMode } from '../types/auth';

import { DEMO_PRESETS, REGION_OPTIONS } from '../data/presets';
import { SplineScene } from './ui/spline';
import { Spotlight } from './ui/spotlight';

interface RedesignedLoginPortalProps {
  onLoginSubmit: (email: string, pass: string, mode: LoginMode, preset?: UserPreset) => void;
  onOpenForgotPassword: (email: string) => void;
  onOpenComplianceModal: () => void;
  selectedRegion: RegionOption;
  onSelectRegion: (region: RegionOption) => void;
  asciiPalette?: AsciiPalette;
  onSelectPalette?: (palette: AsciiPalette) => void;
  asciiMode?: AsciiMode;
  onSelectMode?: (mode: AsciiMode) => void;
}

export const RedesignedLoginPortal: React.FC<RedesignedLoginPortalProps> = ({
  onLoginSubmit,
  onOpenForgotPassword,
  onOpenComplianceModal,
  selectedRegion,
  onSelectRegion,
  asciiPalette = 'mono',
  onSelectPalette,
  asciiMode = 'waves',
  onSelectMode,
}) => {
  const [email, setEmail] = useState('andrew.ui@uisocial.com');
  const [password, setPassword] = useState('Password123!');
  const [selectedPreset, setSelectedPreset] = useState<UserPreset>(DEMO_PRESETS[0]);
  const [isRegionOpen, setIsRegionOpen] = useState(false);
  const [isAsciiControlOpen, setIsAsciiControlOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [authMode, setAuthMode] = useState<LoginMode>('password');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!email || !email.includes('@')) {
      setError('Please enter a valid email address');
      return;
    }
    setError('');
    setIsLoading(true);

    setTimeout(() => {
      setIsLoading(false);
      onLoginSubmit(email, password, authMode, selectedPreset);
    }, 700);
  };

  return (
    <div className="w-full max-w-5xl mx-auto p-2 sm:p-4 my-auto select-none">
      {/* Hidden SVG for slanted cross section clipPath with rounded corners */}
      <svg className="absolute w-0 h-0 pointer-events-none" aria-hidden="true">
        <defs>
          <clipPath id="slantedInnerBox" clipPathUnits="objectBoundingBox">
            <path d="M 0.05 0 L 0.94 0 Q 1 0 0.99 0.04 L 0.88 0.95 Q 0.86 1 0.81 1 L 0.05 1 Q 0 1 0 0.95 L 0 0.05 Q 0 0 0.05 0 Z" />
          </clipPath>
        </defs>
      </svg>

      {/* Outer Floating White Card matching reference image exact geometry */}
      <div className="bg-white/95 backdrop-blur-xl rounded-[36px] sm:rounded-[42px] p-3 sm:p-4 shadow-2xl border border-zinc-200 overflow-hidden grid grid-cols-1 lg:grid-cols-12 gap-4 lg:gap-6 items-stretch relative z-10">
        
        {/* ================= LEFT SIDE: INTERACTIVE 3D ROBOT CARD WITH SLANTED CROSS SECTION (ALWAYS PITCH BLACK) ================= */}
        <div 
          className="robot-hero-card lg:col-span-6 relative overflow-hidden min-h-[480px] sm:min-h-[560px] lg:min-h-[620px] flex flex-col justify-between p-6 sm:p-8 text-white bg-black group shadow-2xl rounded-[28px]"
        >
          {/* Spotlight Effect */}
          <Spotlight className="-top-40 left-0 md:left-60 md:-top-20" size={300} />

          {/* Interactive 3D Robot Canvas */}
          <div className="absolute inset-0 z-0 overflow-hidden flex items-center justify-center">
            <div className="w-full h-full transform scale-[0.80] sm:scale-[0.83] md:scale-[0.85] origin-center">
              <SplineScene 
                scene="https://prod.spline.design/kZDDjO5HuC9GJUM2/scene.splinecode"
                className="w-full h-full"
              />
            </div>
            {/* Subtle gradient vignette at top and bottom to ensure text readability */}
            <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-black/40 pointer-events-none" />
          </div>

          {/* Center Space: Unobstructed View of the Interactive 3D Robot */}
          <div className="flex-1 my-auto pointer-events-none" />
        </div>

        {/* ================= RIGHT SIDE: CLEAN WHITE LOGIN FORM ================= */}
        <div className="lg:col-span-6 bg-white rounded-[28px] sm:rounded-[32px] p-6 sm:p-8 lg:p-10 flex flex-col justify-between text-zinc-900">
          
          {/* Top Row: Logo on Left | ASCII Theme & EN Flag Dropdown on Right */}
          <div className="flex items-center justify-between gap-2 mb-4">
            {/* Logo */}
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 rounded-lg bg-primary text-primary-foreground flex items-center justify-center font-bold">
                <Bot className="w-5 h-5" />
              </div>
              <span className="text-xl font-bold tracking-tight text-zinc-900 uppercase font-mono">
                VOXERA AI
              </span>
            </div>

            {/* Top Right Actions */}
            <div className="flex items-center gap-2">
              {/* ASCII Theme Dropdown */}
              <div className="relative">
                <button
                  type="button"
                  onClick={() => {
                    setIsAsciiControlOpen(!isAsciiControlOpen);
                    setIsRegionOpen(false);
                  }}
                  title="ASCII Matrix Controls"
                  className="px-3 py-1.5 rounded-full border border-zinc-300 bg-zinc-100 hover:bg-zinc-200 text-zinc-900 text-xs font-mono font-medium transition flex items-center gap-1.5 shadow-sm"
                >
                  <Terminal className="w-3.5 h-3.5 text-zinc-700" />
                  <span className="hidden sm:inline">ASCII Grid</span>
                  <Sliders className="w-3 h-3 text-zinc-500 ml-0.5" />
                </button>

                {isAsciiControlOpen && (
                  <div className="absolute right-0 mt-2 w-60 rounded-2xl bg-zinc-900 border border-zinc-700 shadow-2xl p-3 z-40 text-left text-white space-y-3 font-sans backdrop-blur-xl">
                    <div>
                      <div className="flex items-center gap-1.5 text-zinc-200 text-xs font-mono font-medium mb-1.5">
                        <Sparkles className="w-3.5 h-3.5 text-zinc-400" />
                        <span>ASCII Number Palette</span>
                      </div>
                      <div className="grid grid-cols-2 gap-1.5 text-xs font-mono">
                        {[
                          { id: 'mono', label: '⚪ White & Gray' },
                          { id: 'gold', label: '🟡 Amber Gold' },
                          { id: 'cyan', label: '🔵 Cyber Cyan' },
                          { id: 'emerald', label: '🟢 Matrix Green' },
                        ].map((item) => (
                          <button
                            key={item.id}
                            type="button"
                            onClick={() => onSelectPalette && onSelectPalette(item.id as AsciiPalette)}
                            className={`p-1.5 rounded-lg text-left text-[11px] transition ${
                              asciiPalette === item.id
                                ? 'bg-white/20 border border-white/40 text-white font-semibold'
                                : 'bg-zinc-800/60 hover:bg-zinc-800 text-zinc-400'
                            }`}
                          >
                            {item.label}
                          </button>
                        ))}
                      </div>
                    </div>

                    <div className="border-t border-zinc-800 pt-2">
                      <div className="text-[11px] text-zinc-400 font-mono mb-1.5">Matrix Pattern Mode</div>
                      <div className="grid grid-cols-3 gap-1 text-xs font-mono">
                        {[
                          { id: 'waves', label: 'Waves' },
                          { id: 'spotlight', label: 'Spotlight' },
                          { id: 'matrix', label: 'Rain' },
                        ].map((m) => (
                          <button
                            key={m.id}
                            type="button"
                            onClick={() => onSelectMode && onSelectMode(m.id as AsciiMode)}
                            className={`py-1 px-1.5 rounded-lg text-center text-[10px] transition ${
                              asciiMode === m.id
                                ? 'bg-amber-500 text-zinc-950 font-bold'
                                : 'bg-zinc-800 text-zinc-400 hover:bg-zinc-700'
                            }`}
                          >
                            {m.label}
                          </button>
                        ))}
                      </div>
                    </div>
                  </div>
                )}
              </div>

              {/* Language / Region Pill */}
              <div className="relative">
                <button
                  type="button"
                  onClick={() => {
                    setIsRegionOpen(!isRegionOpen);
                    setIsAsciiControlOpen(false);
                  }}
                  className="px-3.5 py-1.5 rounded-full border border-zinc-200 hover:border-zinc-300 bg-white text-xs font-medium text-zinc-700 transition flex items-center gap-1.5 shadow-sm"
                >
                  <span>{selectedRegion.flag} {selectedRegion.name.split(' ')[0]}</span>
                  <ChevronDown className="w-3.5 h-3.5 text-zinc-400" />
                </button>

                {isRegionOpen && (
                  <div className="absolute right-0 mt-2 w-52 rounded-2xl bg-white border border-zinc-200 shadow-xl p-2 z-30 text-left space-y-1">
                    <p className="text-[10px] uppercase font-medium text-zinc-400 px-2 py-1">
                      Select Language &amp; Region
                    </p>
                    {REGION_OPTIONS.map((reg) => (
                      <button
                        key={reg.id}
                        type="button"
                        onClick={() => {
                          onSelectRegion(reg);
                          setIsRegionOpen(false);
                        }}
                        className={`w-full text-left p-2 rounded-xl text-xs font-medium transition flex items-center justify-between ${
                          selectedRegion.id === reg.id
                            ? 'bg-zinc-100 font-medium text-zinc-900'
                            : 'text-zinc-600 hover:bg-zinc-50'
                        }`}
                      >
                        <span>{reg.flag} {reg.name}</span>
                      </button>
                    ))}
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* Middle Form Area */}
          <div className="my-auto py-2">
            
            {/* Title Greeting */}
            <div className="text-center mb-6">
              <h2 className="text-3xl sm:text-4xl font-bold text-zinc-900 tracking-tight">
                Hi {selectedPreset.name.split(' ')[0]}
              </h2>
              <p className="text-xs sm:text-sm font-normal text-zinc-500 mt-1.5">
                Welcome to Voxera Voice AI Platform
              </p>
            </div>

            {/* Form inputs */}
            <form onSubmit={handleSubmit} className="space-y-4 text-left">
              
              {/* Preset Selector */}
              <div className="flex gap-2 mb-2">
                {DEMO_PRESETS.map((preset) => (
                  <button
                    key={preset.id}
                    type="button"
                    onClick={() => {
                      setSelectedPreset(preset);
                      setEmail(preset.email);
                      setPassword('Password123!');
                    }}
                    className={`flex-1 py-1.5 px-2 rounded-xl text-[11px] font-medium border text-center transition ${
                      selectedPreset.id === preset.id
                        ? 'bg-zinc-900 text-white border-zinc-900'
                        : 'bg-zinc-50 text-zinc-600 border-zinc-200 hover:bg-zinc-100'
                    }`}
                  >
                    {preset.name.split(' ')[0]}
                  </button>
                ))}
              </div>

              {/* Email Input */}
              <div>
                <input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="Email"
                  required
                  className="w-full border border-zinc-200 focus:border-zinc-800 rounded-xl px-4 py-3 text-zinc-900 text-sm font-normal placeholder-zinc-400 focus:ring-1 focus:ring-zinc-800 outline-none transition"
                />
              </div>

              {/* Password Input */}
              <div>
                <input
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="Password"
                  required
                  className="w-full border border-zinc-200 focus:border-zinc-800 rounded-xl px-4 py-3 text-zinc-900 text-sm font-normal placeholder-zinc-400 focus:ring-1 focus:ring-zinc-800 outline-none transition"
                />
              </div>

              {/* Forgot Password Link */}
              <div className="flex justify-end">
                <button
                  type="button"
                  onClick={() => onOpenForgotPassword(email)}
                  className="text-xs font-medium text-zinc-600 hover:underline"
                >
                  Forgot password?
                </button>
              </div>

              {/* Divider */}
              <div className="relative my-3">
                <div className="absolute inset-0 flex items-center">
                  <div className="w-full border-t border-zinc-200" />
                </div>
                <div className="relative flex justify-center text-xs text-zinc-400 font-normal">
                  <span className="bg-white px-3">or</span>
                </div>
              </div>

              {/* Google SSO Button */}
              <button
                type="button"
                onClick={() => {
                  setAuthMode('sso');
                  handleSubmit(new Event('submit') as any);
                }}
                className="w-full border border-zinc-200 hover:border-zinc-300 bg-white hover:bg-zinc-50 rounded-xl py-3 px-4 font-medium text-xs text-zinc-700 flex items-center justify-center gap-2 transition duration-150 shadow-sm"
              >
                <span>Login with Google</span>
                <svg className="w-4 h-4 ml-0.5" viewBox="0 0 24 24">
                  <path
                    fill="#4285F4"
                    d="M23.745 12.27c0-.7-.06-1.4-.19-2.07H12v4.51h6.6c-.29 1.52-1.14 2.82-2.4 3.68v3.05h3.88c2.27-2.09 3.665-5.17 3.665-9.17z"
                  />
                  <path
                    fill="#34A853"
                    d="M12 24c3.24 0 5.95-1.08 7.93-2.91l-3.88-3.05c-1.08.72-2.45 1.16-4.05 1.16-3.12 0-5.77-2.11-6.72-4.96H1.29v3.15C3.26 21.3 7.31 24 12 24z"
                  />
                  <path
                    fill="#FBBC05"
                    d="M5.28 14.24c-.25-.72-.38-1.49-.38-2.24s.13-1.52.38-2.24V6.61H1.29C.47 8.24 0 10.06 0 12s.47 3.76 1.29 5.39l3.99-3.15z"
                  />
                  <path
                    fill="#EA4335"
                    d="M12 4.75c1.77 0 3.35.61 4.6 1.8l3.42-3.42C17.95 1.19 15.24 0 12 0 7.31 0 3.26 2.7 1.29 6.61l3.99 3.15c.95-2.85 3.6-4.96 6.72-4.96z"
                  />
                </svg>
              </button>

              {/* Error Message */}
              {error && (
                <p className="text-xs text-red-500 font-medium pt-1 text-center">
                  {error}
                </p>
              )}

              {/* Primary Submit CTA Button */}
              <button
                type="submit"
                disabled={isLoading}
                className="w-full py-3.5 px-6 rounded-full bg-zinc-900 hover:bg-zinc-800 text-white font-medium text-sm tracking-wide shadow-sm transition duration-150 disabled:opacity-50 mt-2"
              >
                {isLoading ? 'Authenticating...' : 'Login'}
              </button>

              {/* Bottom text */}
              <p className="text-xs font-normal text-zinc-500 text-center mt-3">
                Don't have an account?{' '}
                <button
                  type="button"
                  onClick={() => onOpenComplianceModal()}
                  className="font-medium text-zinc-900 underline"
                >
                  Sign up
                </button>
              </p>
            </form>
          </div>

        </div>
      </div>
    </div>
  );
};
