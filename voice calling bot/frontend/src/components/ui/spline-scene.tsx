'use client'

import { Suspense, lazy, useState, useEffect, useRef } from 'react'
import { Sparkles, Cpu, Radio } from 'lucide-react'

const Spline = lazy(() => import('@splinetool/react-spline'))

interface SplineSceneProps {
  scene: string
  className?: string
}

function InstantCyberBot({ className }: { className?: string }) {
  const containerRef = useRef<HTMLDivElement>(null);
  const [mousePos, setMousePos] = useState({ x: 0, y: 0 });

  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      if (!containerRef.current) return;
      const rect = containerRef.current.getBoundingClientRect();
      const x = (e.clientX - rect.left) / rect.width - 0.5;
      const y = (e.clientY - rect.top) / rect.height - 0.5;
      setMousePos({ x: x * 30, y: y * 30 });
    };
    window.addEventListener('mousemove', handleMouseMove);
    return () => window.removeEventListener('mousemove', handleMouseMove);
  }, []);

  return (
    <div
      ref={containerRef}
      className={`w-full h-full relative overflow-hidden bg-black flex flex-col items-center justify-center p-6 text-white select-none ${className || ''}`}
    >
      {/* Background Animated Particle Grid */}
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,rgba(59,130,246,0.12)_0%,transparent_70%)] pointer-events-none" />

      {/* Cyber Bot Core Container with 3D Tilt */}
      <div
        className="relative flex flex-col items-center justify-center transition-transform duration-100 ease-out"
        style={{
          transform: `perspective(1000px) rotateY(${mousePos.x * 0.8}deg) rotateX(${-mousePos.y * 0.8}deg) translateZ(10px)`
        }}
      >
        {/* Outer Glow Ring */}
        <div className="absolute -inset-8 rounded-full bg-gradient-to-tr from-cyan-500/20 via-blue-600/30 to-purple-600/20 blur-2xl animate-pulse" />

        {/* Orbiting Tech Ring */}
        <div className="w-48 h-48 sm:w-56 sm:h-56 rounded-full border border-cyan-500/30 border-t-cyan-400 border-r-purple-500 animate-spin flex items-center justify-center relative shadow-[0_0_50px_rgba(6,182,212,0.25)]">
          <div className="w-36 h-36 sm:w-44 sm:h-44 rounded-full border border-indigo-500/40 border-b-purple-400 border-l-blue-400 animate-[spin_6s_linear_infinite_reverse] flex items-center justify-center">
            
            {/* Robot Head Core */}
            <div className="w-28 h-28 sm:w-32 sm:h-32 rounded-3xl bg-gradient-to-b from-zinc-900 via-zinc-950 to-black border border-cyan-500/40 shadow-2xl flex flex-col items-center justify-center relative group overflow-hidden">
              {/* Visor Glow Bar */}
              <div className="w-20 h-5 sm:w-24 sm:h-6 rounded-full bg-cyan-950 border border-cyan-400/60 shadow-[0_0_20px_rgba(34,211,238,0.8)] flex items-center justify-around px-3 relative mb-1">
                <div className="w-2.5 h-2.5 rounded-full bg-cyan-400 animate-ping" />
                <div className="w-8 h-1 rounded-full bg-gradient-to-r from-cyan-400 to-indigo-400 animate-pulse" />
                <div className="w-2.5 h-2.5 rounded-full bg-cyan-400" />
              </div>

              {/* Status Badge */}
              <div className="flex items-center gap-1.5 text-[10px] font-mono text-cyan-300/90 tracking-wider font-semibold uppercase">
                <Cpu className="w-3 h-3 text-cyan-400 animate-spin" />
                <span>VOXERA CORE</span>
              </div>
            </div>

          </div>
        </div>

        {/* Holographic Signal Indicator */}
        <div className="mt-6 flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-zinc-900/90 border border-cyan-500/30 text-cyan-300 text-xs font-mono backdrop-blur-md shadow-lg">
          <Radio className="w-3.5 h-3.5 text-cyan-400 animate-pulse" />
          <span>Voice AI Agent Active</span>
          <Sparkles className="w-3.5 h-3.5 text-amber-400 ml-1 animate-bounce" />
        </div>
      </div>
    </div>
  );
}

export function SplineScene({ scene, className }: SplineSceneProps) {
  const [hasLoaded, setHasLoaded] = useState(false);
  const [hasError, setHasError] = useState(false);

  useEffect(() => {
    const timer = setTimeout(() => {
      if (!hasLoaded) {
        setHasError(true);
      }
    }, 2500);
    return () => clearTimeout(timer);
  }, [hasLoaded]);

  if (hasError) {
    return <InstantCyberBot className={className} />;
  }

  return (
    <div className={`relative w-full h-full ${className || ''}`}>
      {!hasLoaded && (
        <div className="absolute inset-0 z-10">
          <InstantCyberBot className={className} />
        </div>
      )}

      <Suspense fallback={<InstantCyberBot className={className} />}>
        <Spline
          scene={scene}
          className={className}
          onLoad={() => setHasLoaded(true)}
          onError={() => setHasError(true)}
        />
      </Suspense>
    </div>
  )
}
