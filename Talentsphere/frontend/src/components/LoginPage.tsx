import React, { useEffect, useRef, useState, Suspense, lazy } from 'react';
import { motion, useSpring, useTransform } from 'framer-motion';
import { createNoise3D } from 'simplex-noise';
import {
  ChevronDown,
  Sparkles,
  Sliders,
  Terminal,
  Lock,
  Mail,
  Eye,
  EyeOff,
  ArrowRight,
  ShieldCheck,
  Loader2,
  Building2,
  Fingerprint,
  Info,
  KeyRound,
  X,
  CheckCircle2,
  ShieldAlert,
} from 'lucide-react';

// Lazy Spline component (kept same as original)
const Spline = lazy(() => import('@splinetool/react-spline'));

type LoginMode = 'password' | 'sso' | 'passkey';

type UserPreset = { id: string; name: string };
type RegionOption = { id: string; name: string; flag?: string };

const DEMO_PRESETS: UserPreset[] = [
  { id: 'andrew', name: 'Andrew UI' },
  { id: 'jane', name: 'Jane Doe' },
];

const REGION_OPTIONS: RegionOption[] = [
  { id: 'en', name: 'United Kingdom', flag: '🇬🇧' },
  { id: 'us', name: 'United States', flag: '🇺🇸' },
];

/* --------------------------- Spline Scene --------------------------- */
function SplineScene({ scene, className }: { scene: string; className?: string }) {
  return (
    <Suspense
      fallback={
        <div className="w-full h-full flex items-center justify-center">
          <div className="w-8 h-8 border-2 border-slate-400 border-t-white rounded-full animate-spin" />
        </div>
      }
    >
      {/* @ts-ignore dynamic import */}
      <Spline scene={scene} className={className} />
    </Suspense>
  );
}

/* --------------------------- Spotlight --------------------------- */
function Spotlight({ className, size = 200 }: { className?: string; size?: number }) {
  const containerRef = useRef<HTMLDivElement | null>(null);
  const [parentElement, setParentElement] = useState<HTMLElement | null>(null);
  const mouseX = useSpring(0, { bounce: 0 });
  const mouseY = useSpring(0, { bounce: 0 });

  const spotlightLeft = useTransform(mouseX, (x) => `${x - size / 2}px`);
  const spotlightTop = useTransform(mouseY, (y) => `${y - size / 2}px`);

  useEffect(() => {
    if (containerRef.current) {
      const parent = containerRef.current.parentElement;
      if (parent) {
        parent.style.position = 'relative';
        parent.style.overflow = 'hidden';
        setParentElement(parent);
      }
    }
  }, []);

  useEffect(() => {
    if (!parentElement) return;
    const handleMouseMove = (event: MouseEvent) => {
      const { left, top } = parentElement.getBoundingClientRect();
      mouseX.set(event.clientX - left);
      mouseY.set(event.clientY - top);
    };
    parentElement.addEventListener('mousemove', handleMouseMove);
    parentElement.addEventListener('mouseenter', () => {});
    parentElement.addEventListener('mouseleave', () => {});
    return () => {
      parentElement.removeEventListener('mousemove', handleMouseMove);
    };
  }, [parentElement, mouseX, mouseY]);

  return (
    <motion.div
      ref={containerRef}
      className={
        'pointer-events-none absolute rounded-full bg-[radial-gradient(circle_at_center,var(--tw-gradient-stops),transparent_80%)] blur-xl transition-opacity duration-200 from-zinc-50 via-zinc-100 to-zinc-200 opacity-100 ' +
        (className || '')
      }
      style={{ width: size, height: size, left: (spotlightLeft as any), top: (spotlightTop as any) }}
    />
  );
}

/* ------------------------ AsciiNumberCanvas ------------------------ */
export type AsciiPalette = 'mono' | 'gold' | 'cyan' | 'emerald';
export type AsciiMode = 'waves' | 'spotlight' | 'matrix';

const AsciiNumberCanvas: React.FC<{
  palette?: AsciiPalette;
  mode?: AsciiMode;
  cellSize?: number;
  fontSize?: number;
  speed?: number;
  interactive?: boolean;
  opacity?: number;
  className?: string;
}> = ({
  palette = 'mono',
  mode = 'waves',
  cellSize = 19,
  fontSize = 12,
  speed = 1.0,
  interactive = true,
  opacity = 0.9,
  className = '',
}) => {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const mousePosRef = useRef<{ x: number; y: number } | null>(null);
  const isHoveredRef = useRef(false);
  const noise3DRef = useRef(createNoise3D());

  useEffect(() => {
    if (!interactive) return;
    const handleMouseMove = (e: MouseEvent) => {
      const canvas = canvasRef.current;
      if (!canvas) return;
      const rect = canvas.getBoundingClientRect();
      mousePosRef.current = { x: e.clientX - rect.left, y: e.clientY - rect.top };
      isHoveredRef.current = e.clientX >= rect.left && e.clientX <= rect.right && e.clientY >= rect.top && e.clientY <= rect.bottom;
    };
    const handleMouseLeave = () => {
      isHoveredRef.current = false;
    };
    window.addEventListener('mousemove', handleMouseMove);
    window.addEventListener('mouseleave', handleMouseLeave);
    return () => {
      window.removeEventListener('mousemove', handleMouseMove);
      window.removeEventListener('mouseleave', handleMouseLeave);
    };
  }, [interactive]);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    let animationFrameId = 0;
    let startTime = performance.now();
    const CHARS = ['0','0','0','0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F'];

    const handleResize = () => {
      if (!canvas) return;
      const dpr = window.devicePixelRatio || 1;
      const width = canvas.parentElement?.clientWidth || window.innerWidth;
      const height = canvas.parentElement?.clientHeight || window.innerHeight;
      canvas.width = width * dpr;
      canvas.height = height * dpr;
      canvas.style.width = `${width}px`;
      canvas.style.height = `${height}px`;
      ctx.scale(dpr, dpr);
    };

    handleResize();
    window.addEventListener('resize', handleResize);

    const getColor = (density: number) => {
      if (palette === 'mono') {
        if (density < 0.18) return 'rgba(51,65,85,0.4)';
        if (density < 0.35) return 'rgba(100,116,139,0.65)';
        if (density < 0.52) return 'rgba(148,163,184,0.88)';
        if (density < 0.7) return 'rgba(203,213,225,0.95)';
        if (density < 0.85) return 'rgba(241,245,249,1.0)';
        return '#ffffff';
      } else if (palette === 'gold') {
        if (density < 0.18) return 'rgba(30,41,59,0.45)';
        if (density < 0.35) return 'rgba(71,85,105,0.7)';
        if (density < 0.52) return 'rgba(148,163,184,0.9)';
        if (density < 0.7) return 'rgba(234,179,8,0.95)';
        if (density < 0.86) return '#fde047';
        return '#ffffff';
      } else if (palette === 'cyan') {
        if (density < 0.18) return 'rgba(15,23,42,0.45)';
        if (density < 0.35) return 'rgba(30,58,138,0.7)';
        if (density < 0.52) return 'rgba(56,189,248,0.85)';
        if (density < 0.75) return '#38bdf8';
        if (density < 0.88) return '#7dd3fc';
        return '#ffffff';
      }
      if (density < 0.18) return 'rgba(6,78,59,0.35)';
      if (density < 0.35) return 'rgba(16,185,129,0.6)';
      if (density < 0.52) return 'rgba(52,211,153,0.85)';
      if (density < 0.75) return '#34d399';
      if (density < 0.88) return '#a7f3d0';
      return '#ffffff';
    };

    const render = (now: number) => {
      const elapsed = (now - startTime) * 0.001 * speed;
      const displayWidth = canvas.clientWidth;
      const displayHeight = canvas.clientHeight;
      ctx.clearRect(0, 0, displayWidth, displayHeight);
      ctx.font = `bold ${fontSize}px "JetBrains Mono", "Fira Code", monospace`;
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';

      const cols = Math.ceil(displayWidth / cellSize);
      const rows = Math.ceil(displayHeight / cellSize);
      const noise3D = noise3DRef.current;
      const mouse = mousePosRef.current;

      for (let r = 0; r < rows; r++) {
        const y = r * cellSize + cellSize / 2;
        for (let c = 0; c < cols; c++) {
          const x = c * cellSize + cellSize / 2;
          let rawDensity = 0;
          if (mode === 'matrix') {
            const fallSpeed = elapsed * 1.5 + c * 0.3;
            const yOffset = (r - fallSpeed) % rows;
            const normY = (yOffset < 0 ? yOffset + rows : yOffset) / rows;
            const n = noise3D(c * 0.1, normY * 2, elapsed * 0.2);
            rawDensity = Math.sin(normY * Math.PI) * (n * 0.5 + 0.5);
          } else {
            const nx = c * 0.045;
            const ny = r * 0.045;
            const nt = elapsed * 0.35;
            const n1 = noise3D(nx, ny, nt);
            const n2 = noise3D(nx * 2 + 10, ny * 2 + 10, nt * 1.2) * 0.5;
            const wave = Math.sin((c * 0.08 + r * 0.05) - elapsed * 0.9);
            const combined = (n1 + n2 + wave * 0.6) / 2.1;
            rawDensity = Math.max(0, Math.min(1, (combined + 1) / 2));
          }

          let density = Math.pow(rawDensity, 2.4);
          if (interactive && mouse && isHoveredRef.current) {
            const dx = x - mouse.x;
            const dy = y - mouse.y;
            const dist = Math.hypot(dx, dy);
            const spotlightRadius = 240;
            if (dist < spotlightRadius) {
              const spotFactor = Math.pow(1 - dist / spotlightRadius, 2.0);
              density = Math.min(1, density + spotFactor * 0.9);
            }
          }

          const glitch = Math.random() < 0.015;
          if (glitch && density > 0.1) density = Math.min(1, density + (Math.random() * 0.3 - 0.1));

          const charIndex = Math.min(CHARS.length - 1, Math.floor(density * CHARS.length));
          const char = CHARS[charIndex];
          const color = getColor(density);
          ctx.fillStyle = color;
          if (density > 0.82) {
            ctx.shadowColor = palette === 'gold' ? 'rgba(253,224,71,0.6)' : 'rgba(255,255,255,0.7)';
            ctx.shadowBlur = 8;
          } else ctx.shadowBlur = 0;
          ctx.fillText(char, x, y);
        }
      }

      animationFrameId = requestAnimationFrame(render);
    };

    animationFrameId = requestAnimationFrame(render);
    return () => {
      window.removeEventListener('resize', handleResize);
      cancelAnimationFrame(animationFrameId);
    };
  }, [palette, mode, cellSize, fontSize, speed, interactive]);

  return (
    <div className={`absolute inset-0 pointer-events-auto select-none overflow-hidden ${className}`} style={{ opacity }}>
      <canvas ref={canvasRef} className="block w-full h-full" />
    </div>
  );
};

/* ------------------------- BackgroundCanvas ------------------------ */
function BackgroundCanvas({ reducedMotion, palette = 'mono', mode = 'waves' }: { reducedMotion?: boolean; palette?: AsciiPalette; mode?: AsciiMode }) {
  return (
    <div className="fixed inset-0 z-0 overflow-hidden select-none transition-colors duration-300 bg-[#040508]" aria-hidden>
      <AsciiNumberCanvas palette={palette} mode={mode} speed={reducedMotion ? 0.2 : 0.8} opacity={0.9} interactive />
      <div className="absolute -top-40 -left-40 w-[600px] h-[600px] rounded-full blur-[140px] opacity-20 pointer-events-none" style={{ background: 'radial-gradient(circle, rgba(255,255,255,0.2) 0%, rgba(9,9,11,0) 70%)' }} />
      <div className="absolute -bottom-40 -right-40 w-[700px] h-[700px] rounded-full blur-[160px] opacity-20 pointer-events-none" style={{ background: 'radial-gradient(circle, rgba(148,163,184,0.25) 0%, rgba(0,0,0,0) 70%)' }} />
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,transparent_20%,rgba(4,5,8,0.75)_100%)] pointer-events-none" />
      <div className="absolute inset-0 bg-gradient-to-b from-black/60 via-transparent to-black/70 pointer-events-none" />
    </div>
  );
}

/* ------------------------ MfaModal / Forgot ------------------------ */
function MfaModal({ isOpen, onVerifySuccess, onCancel, userEmail }: { isOpen: boolean; onVerifySuccess: () => void; onCancel: () => void; userEmail: string; }) {
  const [code, setCode] = useState(['', '', '', '', '', '']);
  const [isVerifying, setIsVerifying] = useState(false);
  const [error, setError] = useState('');
  const inputRefs = useRef<Array<HTMLInputElement | null>>([]);

  useEffect(() => {
    if (isOpen) {
      setCode(['', '', '', '', '', '']);
      setError('');
      setTimeout(() => inputRefs.current[0]?.focus(), 100);
    }
  }, [isOpen]);

  if (!isOpen) return null;

  const handleChange = (index: number, value: string) => {
    if (!/^\d*$/.test(value)) return;
    const newCode = [...code];
    newCode[index] = value.slice(-1);
    setCode(newCode);
    if (value && index < 5) inputRefs.current[index + 1]?.focus();
  };

  const handleKeyDown = (index: number, e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Backspace' && !code[index] && index > 0) inputRefs.current[index - 1]?.focus();
  };

  const handleVerify = (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    const fullCode = code.join('');
    if (fullCode.length !== 6) {
      setError('Please enter all 6 digits from your Authenticator app');
      return;
    }
    setError('');
    setIsVerifying(true);
    setTimeout(() => { setIsVerifying(false); onVerifySuccess(); }, 900);
  };

  const fillDemoCode = () => { setCode(['8','4','2','9','1','0']); setError(''); };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-md">
      <div className="relative w-full max-w-md rounded-2xl glass-card p-6 md:p-8 text-left space-y-5">
        <div className="w-11 h-11 rounded-2xl glass-panel flex items-center justify-center dark:text-zinc-300 light:text-zinc-700"><KeyRound className="w-6 h-6" /></div>
        <div className="flex items-center justify-between">
          <h3 className="text-xl font-medium">Security Verification</h3>
          <span className="text-[10px] font-mono uppercase tracking-wider px-2.5 py-0.5 rounded-full glass-panel">MFA Mandatory</span>
        </div>
        <p className="text-xs">Enter the 6-digit TOTP code for <strong>{userEmail || 'your account'}</strong>.</p>

        <form onSubmit={handleVerify} className="space-y-5">
          <div>
            <div className="flex items-center justify-between gap-2 mb-2">
              {code.map((digit, idx) => (
                <input key={idx} ref={(el) => (inputRefs.current[idx] = el)} type="text" inputMode="numeric" maxLength={1} value={digit} onChange={(e) => handleChange(idx, e.target.value)} onKeyDown={(e) => handleKeyDown(idx, e)} className="w-12 h-12 text-center text-xl font-medium rounded-xl dark:bg-black/80 light:bg-white border" />
              ))}
            </div>
            {error && <p className="mt-2 text-xs text-red-500">{error}</p>}
          </div>

          <div className="p-3.5 rounded-xl glass-panel flex items-center justify-between">
            <span className="text-xs">Demo Testing?</span>
            <button type="button" onClick={fillDemoCode} className="text-xs">Autofill MFA Code (842910)</button>
          </div>

          <div className="flex items-center justify-end gap-3 pt-2">
            <button type="button" onClick={onCancel} className="px-4 py-2.5 rounded-xl text-xs">Cancel</button>
            <button type="submit" disabled={isVerifying} className="px-6 py-3 rounded-xl bg-zinc-900 text-white text-xs">
              {isVerifying ? <><Loader2 className="w-4 h-4 animate-spin"/> Verifying...</> : <>Verify & Access <ArrowRight className="w-4 h-4"/></>}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

function ForgotPasswordModal({ isOpen, onClose, initialEmail = '' }: { isOpen: boolean; onClose: () => void; initialEmail?: string }) {
  const [email, setEmail] = useState(initialEmail);
  const [isLoading, setIsLoading] = useState(false);
  const [isSubmitted, setIsSubmitted] = useState(false);
  const [error, setError] = useState('');

  if (!isOpen) return null;

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!email || !email.includes('@')) { setError('Please enter a valid work email address'); return; }
    setError(''); setIsLoading(true);
    setTimeout(() => { setIsLoading(false); setIsSubmitted(true); }, 1000);
  };

  const handleReset = () => { setIsSubmitted(false); setEmail(''); onClose(); };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-md">
      <div className="relative w-full max-w-md rounded-2xl glass-card overflow-hidden p-6 md:p-8 text-left space-y-4">
        <button onClick={onClose} className="absolute top-5 right-5 p-2 rounded-xl" aria-label="Close"><X className="w-4 h-4"/></button>
        {!isSubmitted ? (
          <div>
            <div className="w-11 h-11 rounded-2xl glass-panel flex items-center justify-center mb-4"><Mail className="w-6 h-6"/></div>
            <h3 className="text-xl font-medium mb-1">Reset Work Password</h3>
            <p className="text-xs mb-6">Enter your corporate email address. If an enterprise account exists, a secure password reset link will be dispatched.</p>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label htmlFor="reset-email" className="block text-xs font-medium mb-1.5">Work Email Address</label>
                <input id="reset-email" type="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="name@company.com" className="w-full px-4 py-3 rounded-xl" required />
                {error && <p className="mt-2 text-xs text-red-500">{error}</p>}
              </div>
              <div className="pt-2 flex items-center justify-end gap-3">
                <button type="button" onClick={onClose} className="px-4 py-2.5 rounded-xl text-xs">Cancel</button>
                <button type="submit" disabled={isLoading} className="px-6 py-3 rounded-xl bg-zinc-900 text-white text-xs">
                  {isLoading ? <> <Loader2 className="w-4 h-4 animate-spin"/> Dispatching Link...</> : <>Send Reset Email <ArrowRight className="w-4 h-4"/></>}
                </button>
              </div>
            </form>
          </div>
        ) : (
          <div className="text-center py-4">
            <div className="w-12 h-12 rounded-full glass-panel text-emerald-600 flex items-center justify-center mx-auto mb-4"><CheckCircle2 className="w-6 h-6"/></div>
            <h3 className="text-lg font-medium mb-2">Reset Instructions Sent</h3>
            <p className="text-xs mb-6">We dispatched reset instructions to <strong>{email}</strong>. Check your corporate inbox.</p>
            <button onClick={handleReset} className="w-full py-3 rounded-xl bg-zinc-900 text-white text-xs">Return to Login</button>
          </div>
        )}
      </div>
    </div>
  );
}

/* ------------------------- RedesignedLoginPortal ------------------------- */
function RedesignedLoginPortal({ onLoginSubmit, onOpenForgotPassword, onOpenComplianceModal, selectedRegion, onSelectRegion, asciiPalette = 'mono', onSelectPalette, asciiMode = 'waves', onSelectMode, }: {
  onLoginSubmit: (email: string, pass: string, mode: LoginMode, preset?: UserPreset) => void;
  onOpenForgotPassword: (email: string) => void;
  onOpenComplianceModal: () => void;
  selectedRegion: RegionOption;
  onSelectRegion: (region: RegionOption) => void;
  asciiPalette?: AsciiPalette;
  onSelectPalette?: (palette: AsciiPalette) => void;
  asciiMode?: AsciiMode;
  onSelectMode?: (mode: AsciiMode) => void;
}) {
  const [email, setEmail] = useState('andrew.ui@uisocial.com');
  const [password, setPassword] = useState('');
  const [selectedPreset, setSelectedPreset] = useState<UserPreset>(DEMO_PRESETS[0]);
  const [isRegionOpen, setIsRegionOpen] = useState(false);
  const [isAsciiControlOpen, setIsAsciiControlOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [authMode, setAuthMode] = useState<LoginMode>('password');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!email || !email.includes('@')) { setError('Please enter a valid email address'); return; }
    setError(''); setIsLoading(true);
    setTimeout(() => { setIsLoading(false); onLoginSubmit(email, password, authMode, selectedPreset); }, 700);
  };

  return (
    <div className="w-full max-w-5xl mx-auto p-2 sm:p-4 my-auto select-none">
      <svg className="absolute w-0 h-0 pointer-events-none" aria-hidden>
        <defs>
          <clipPath id="slantedInnerBox" clipPathUnits="objectBoundingBox">
            <path d="M 0.05 0 L 0.94 0 Q 1 0 0.99 0.04 L 0.88 0.95 Q 0.86 1 0.81 1 L 0.05 1 Q 0 1 0 0.95 L 0 0.05 Q 0 0 0.05 0 Z" />
          </clipPath>
        </defs>
      </svg>

      <div className="bg-white/95 backdrop-blur-xl rounded-[36px] sm:rounded-[42px] p-3 sm:p-4 shadow-2xl border border-zinc-200 overflow-hidden grid grid-cols-1 lg:grid-cols-12 gap-4 lg:gap-6 items-stretch relative z-10">
        <div className="robot-hero-card lg:col-span-6 relative overflow-hidden min-h-[480px] sm:min-h-[560px] lg:min-h-[620px] flex flex-col justify-between p-6 sm:p-8 text-white bg-black group shadow-2xl" style={{ clipPath: 'url(#slantedInnerBox)' }}>
          <Spotlight className="-top-40 left-0 md:left-60 md:-top-20" size={300} />
          <div className="absolute inset-0 z-0 overflow-hidden flex items-center justify-center">
            <div className="w-full h-full transform scale-[0.80] sm:scale-[0.83] md:scale-[0.85] origin-center">
              <SplineScene scene="https://prod.spline.design/kZDDjO5HuC9GJUM2/scene.splinecode" className="w-full h-full" />
            </div>
            <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-black/40 pointer-events-none" />
          </div>
          <div className="flex-1 my-auto pointer-events-none" />
        </div>

        <div className="lg:col-span-6 bg-white rounded-[28px] sm:rounded-[32px] p-6 sm:p-8 lg:p-10 flex flex-col justify-between text-zinc-900">
          <div className="flex items-center justify-between gap-2 mb-4">
            <div className="flex items-center gap-1.5"><span className="text-xl font-medium tracking-tight text-zinc-900 uppercase font-mono">TALENTSPHERE</span></div>
            <div className="flex items-center gap-2">
              <div className="relative">
                <button type="button" onClick={() => { setIsAsciiControlOpen(!isAsciiControlOpen); setIsRegionOpen(false); }} title="ASCII Matrix Controls" className="px-3 py-1.5 rounded-full border border-zinc-300 bg-zinc-100 text-xs font-mono font-medium flex items-center gap-1.5 shadow-sm"><Terminal className="w-3.5 h-3.5"/><Sliders className="w-3 h-3"/></button>
                {isAsciiControlOpen && (
                  <div className="absolute right-0 mt-2 w-60 rounded-2xl bg-zinc-900 border border-zinc-700 shadow-2xl p-3 z-40 text-left text-white space-y-3">
                    <div>
                      <div className="flex items-center gap-1.5 text-zinc-200 text-xs font-mono font-medium mb-1.5"><Sparkles className="w-3.5 h-3.5"/><span>ASCII Number Palette</span></div>
                      <div className="grid grid-cols-2 gap-1.5 text-xs font-mono">
                        {[
                          { id: 'mono', label: '⚪ White & Gray' },
                          { id: 'gold', label: '🟡 Amber Gold' },
                          { id: 'cyan', label: '🔵 Cyber Cyan' },
                          { id: 'emerald', label: '🟢 Matrix Green' },
                        ].map((item) => (
                          <button key={item.id} type="button" onClick={() => onSelectPalette && onSelectPalette(item.id as AsciiPalette)} className={`p-1.5 rounded-lg text-left text-[11px] transition ${asciiPalette === item.id ? 'bg-white/20 border border-white/40 text-white' : 'bg-zinc-800/60 text-zinc-400'}`}>{item.label}</button>
                        ))}
                      </div>
                    </div>
                    <div className="border-t border-zinc-800 pt-2">
                      <div className="text-[11px] text-zinc-400 font-mono mb-1.5">Matrix Pattern Mode</div>
                      <div className="grid grid-cols-3 gap-1 text-xs font-mono">
                        {[{ id: 'waves', label: 'Waves' }, { id: 'spotlight', label: 'Spotlight' }, { id: 'matrix', label: 'Rain' }].map((m) => (
                          <button key={m.id} type="button" onClick={() => onSelectMode && onSelectMode(m.id as AsciiMode)} className={`py-1 px-1.5 rounded-lg text-center text-[10px] transition ${asciiMode === m.id ? 'bg-amber-500 text-zinc-950' : 'bg-zinc-800 text-zinc-400'}`}>{m.label}</button>
                        ))}
                      </div>
                    </div>
                  </div>
                )}
              </div>

              <div className="relative">
                <button type="button" onClick={() => { setIsRegionOpen(!isRegionOpen); setIsAsciiControlOpen(false); }} className="px-3.5 py-1.5 rounded-full border border-zinc-200 bg-white text-xs font-medium text-zinc-700"><span>🇬🇧 EN</span><ChevronDown className="w-3.5 h-3.5 text-zinc-400"/></button>
                {isRegionOpen && (
                  <div className="absolute right-0 mt-2 w-52 rounded-2xl bg-white border border-zinc-200 shadow-xl p-2 z-30 text-left space-y-1">
                    <p className="text-[10px] uppercase font-medium text-zinc-400 px-2 py-1">Select Language &amp; Region</p>
                    {REGION_OPTIONS.map((reg) => (
                      <button key={reg.id} type="button" onClick={() => { onSelectRegion(reg); setIsRegionOpen(false); }} className={`w-full text-left p-2 rounded-xl text-xs font-medium ${selectedRegion.id === reg.id ? 'bg-zinc-100' : 'text-zinc-600'}`}><span>{reg.flag} {reg.name}</span></button>
                    ))}
                  </div>
                )}
              </div>
            </div>
          </div>

          <div className="my-auto py-2">
            <div className="text-center mb-6">
              <h2 className="text-3xl sm:text-4xl font-medium text-zinc-900 tracking-tight">Hi {selectedPreset.name.split(' ')[0]}</h2>
              <p className="text-xs sm:text-sm font-normal text-zinc-500 mt-1.5">Welcome to TalentSphere OS</p>
            </div>

            <form onSubmit={handleSubmit} className="space-y-4 text-left">
              <div>
                <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="Email" required className="w-full border border-zinc-200 rounded-xl px-4 py-3 text-zinc-900 text-sm placeholder-zinc-400" />
              </div>
              <div>
                <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="Password" required className="w-full border border-zinc-200 rounded-xl px-4 py-3 text-zinc-900 text-sm placeholder-zinc-400" />
              </div>
              <div className="flex justify-end">
                <button type="button" onClick={() => onOpenForgotPassword(email)} className="text-xs font-medium text-zinc-600">Forgot password ?</button>
              </div>

              <div className="relative my-3">
                <div className="absolute inset-0 flex items-center"><div className="w-full border-t border-zinc-200"/></div>
                <div className="relative flex justify-center text-xs text-zinc-400 font-normal"><span className="bg-white px-3">or</span></div>
              </div>

              <button type="button" onClick={() => { setAuthMode('sso'); handleSubmit(new Event('submit') as any); }} className="w-full border border-zinc-200 bg-white rounded-xl py-3 px-4 font-medium text-xs text-zinc-700 flex items-center justify-center gap-2">Login with Google <svg className="w-4 h-4 ml-0.5" viewBox="0 0 24 24"><path fill="#4285F4" d="M23.745 12.27c0-.7-.06-1.4-.19-2.07H12v4.51h6.6c-.29 1.52-1.14 2.82-2.4 3.68v3.05h3.88c2.27-2.09 3.665-5.17 3.665-9.17z"/><path fill="#34A853" d="M12 24c3.24 0 5.95-1.08 7.93-2.91l-3.88-3.05c-1.08.72-2.45 1.16-4.05 1.16-3.12 0-5.77-2.11-6.72-4.96H1.29v3.15C3.26 21.3 7.31 24 12 24z"/><path fill="#FBBC05" d="M5.28 14.24c-.25-.72-.38-1.49-.38-2.24s.13-1.52.38-2.24V6.61H1.29C.47 8.24 0 10.06 0 12s.47 3.76 1.29 5.39l3.99-3.15z"/><path fill="#EA4335" d="M12 4.75c1.77 0 3.35.61 4.6 1.8l3.42-3.42C17.95 1.19 15.24 0 12 0 7.31 0 3.26 2.7 1.29 6.61l3.99 3.15c.95-2.85 3.6-4.96 6.72-4.96z"/></svg></button>

              {error && <p className="text-xs text-red-500 font-medium pt-1 text-center">{error}</p>}

              <button type="submit" disabled={isLoading} className="w-full py-3.5 px-6 rounded-full bg-zinc-900 text-white font-medium text-sm tracking-wide shadow-sm mt-2">{isLoading ? 'Authenticating...' : 'Login'}</button>

              <p className="text-xs font-normal text-zinc-500 text-center mt-3">Don't have an account? <button type="button" onClick={() => onOpenComplianceModal()} className="font-medium text-zinc-900 underline">Sign up</button></p>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
}

/* ----------------------------- LoginPage ----------------------------- */
export default function LoginPage() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [isMfaOpen, setIsMfaOpen] = useState(false);
  const [isForgotPasswordOpen, setIsForgotPasswordOpen] = useState(false);
  const [isComplianceOpen, setIsComplianceOpen] = useState(false);
  const [pendingEmail, setPendingEmail] = useState('');
  const [pendingPreset, setPendingPreset] = useState<UserPreset | undefined>();
  const [pendingMode, setPendingMode] = useState<LoginMode>('password');
  const [asciiPalette, setAsciiPalette] = useState<AsciiPalette>('mono');
  const [asciiMode, setAsciiMode] = useState<AsciiMode>('waves');
  const [selectedRegion, setSelectedRegion] = useState<RegionOption>(REGION_OPTIONS[0]);

  const handleLoginSubmit = (email: string, pass: string, mode: LoginMode, preset?: UserPreset) => {
    setPendingEmail(email); setPendingPreset(preset); setPendingMode(mode);
    // demo flow: require MFA for demo email containing 'mfa'
    if (email.includes('mfa')) {
      setIsMfaOpen(true);
    } else {
      setIsLoggedIn(true);
    }
  };

  const handleMfaVerifySuccess = () => { setIsMfaOpen(false); setIsLoggedIn(true); };

  return (
    <div className="min-h-screen bg-black text-slate-100 flex flex-col justify-between font-sans relative overflow-x-hidden">
      <BackgroundCanvas reducedMotion={false} palette={asciiPalette} mode={asciiMode} />

      <main className="relative z-10 flex-1 flex flex-col items-center justify-center px-4 py-8 md:py-12 w-full max-w-7xl mx-auto my-auto">
        <RedesignedLoginPortal
          onLoginSubmit={handleLoginSubmit}
          onOpenForgotPassword={(email) => { setPendingEmail(email); setIsForgotPasswordOpen(true); }}
          onOpenComplianceModal={() => setIsComplianceOpen(true)}
          selectedRegion={selectedRegion}
          onSelectRegion={setSelectedRegion}
          asciiPalette={asciiPalette}
          onSelectPalette={setAsciiPalette}
          asciiMode={asciiMode}
          onSelectMode={setAsciiMode}
        />
      </main>

      <MfaModal isOpen={isMfaOpen} userEmail={pendingEmail} onVerifySuccess={handleMfaVerifySuccess} onCancel={() => setIsMfaOpen(false)} />
      <ForgotPasswordModal isOpen={isForgotPasswordOpen} initialEmail={pendingEmail} onClose={() => setIsForgotPasswordOpen(false)} />
    </div>
  );
}
