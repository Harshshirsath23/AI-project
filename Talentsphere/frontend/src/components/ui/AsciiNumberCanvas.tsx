import React, { useEffect, useRef, useState } from 'react';
import { createNoise3D } from 'simplex-noise';

export type AsciiPalette = 'mono' | 'gold' | 'cyan' | 'emerald';
export type AsciiMode = 'waves' | 'spotlight' | 'matrix';

export interface AsciiNumberCanvasProps {
  palette?: AsciiPalette;
  mode?: AsciiMode;
  cellSize?: number;
  fontSize?: number;
  speed?: number;
  interactive?: boolean;
  opacity?: number;
  className?: string;
}

export const AsciiNumberCanvas: React.FC<AsciiNumberCanvasProps> = ({
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

  // Setup noise generator
  const noise3DRef = useRef(createNoise3D());

  // Track mouse position over canvas / window
  useEffect(() => {
    if (!interactive) return;

    const handleMouseMove = (e: MouseEvent) => {
      const canvas = canvasRef.current;
      if (!canvas) return;
      const rect = canvas.getBoundingClientRect();
      mousePosRef.current = {
        x: e.clientX - rect.left,
        y: e.clientY - rect.top,
      };
      isHoveredRef.current =
        e.clientX >= rect.left &&
        e.clientX <= rect.right &&
        e.clientY >= rect.top &&
        e.clientY <= rect.bottom;
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

    let animationFrameId: number;
    let startTime = performance.now();

    // Characters map based on density scale (0 = zero, higher = hex digits 1..9, A..F)
    const CHARS = ['0', '0', '0', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F'];

    // Resize canvas to parent / window size
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

    // Color mapper based on density [0, 1] and chosen palette
    const getColor = (density: number, valIndex: number) => {
      if (palette === 'mono') {
        // Pure White & Gray Palette (Crisp High-Contrast Monochrome)
        if (density < 0.18) return 'rgba(51, 65, 85, 0.4)';   // dim dark gray background zeros
        if (density < 0.35) return 'rgba(100, 116, 139, 0.65)';// steel gray
        if (density < 0.52) return 'rgba(148, 163, 184, 0.88)';// slate gray
        if (density < 0.70) return 'rgba(203, 213, 225, 0.95)';// light silver gray
        if (density < 0.85) return 'rgba(241, 245, 249, 1.0)'; // bright white-gray
        return '#ffffff';                                     // pure brilliant white peak
      } else if (palette === 'gold') {
        // Gold Accent Palette
        if (density < 0.18) return 'rgba(30, 41, 59, 0.45)';
        if (density < 0.35) return 'rgba(71, 85, 105, 0.7)';
        if (density < 0.52) return 'rgba(148, 163, 184, 0.9)';
        if (density < 0.70) return 'rgba(234, 179, 8, 0.95)';
        if (density < 0.86) return '#fde047';
        return '#ffffff';
      } else if (palette === 'cyan') {
        if (density < 0.18) return 'rgba(15, 23, 42, 0.45)';
        if (density < 0.35) return 'rgba(30, 58, 138, 0.7)';
        if (density < 0.52) return 'rgba(56, 189, 248, 0.85)';
        if (density < 0.75) return '#38bdf8';
        if (density < 0.88) return '#7dd3fc';
        return '#ffffff';
      } else {
        // Emerald
        if (density < 0.18) return 'rgba(6, 78, 59, 0.35)';
        if (density < 0.35) return 'rgba(16, 185, 129, 0.6)';
        if (density < 0.52) return 'rgba(52, 211, 153, 0.85)';
        if (density < 0.75) return '#34d399';
        if (density < 0.88) return '#a7f3d0';
        return '#ffffff';
      }
    };

    // Render loop
    const render = (now: number) => {
      const elapsed = (now - startTime) * 0.001 * speed;
      const displayWidth = canvas.clientWidth;
      const displayHeight = canvas.clientHeight;

      ctx.clearRect(0, 0, displayWidth, displayHeight);

      // Monospace Font styling
      ctx.font = `bold ${fontSize}px "JetBrains Mono", "Fira Code", "Courier New", monospace`;
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
            // Matrix Rain style vertical fall with noise
            const fallSpeed = elapsed * 1.5 + (c * 0.3);
            const yOffset = (r - fallSpeed) % rows;
            const normY = (yOffset < 0 ? yOffset + rows : yOffset) / rows;
            const n = noise3D(c * 0.1, normY * 2, elapsed * 0.2);
            rawDensity = Math.sin(normY * Math.PI) * (n * 0.5 + 0.5);
          } else {
            // Waves / Spotlight Density Field (Exact match for reference Image 2)
            const nx = c * 0.045;
            const ny = r * 0.045;
            const nt = elapsed * 0.35;

            // Multi-octave 3D noise for organic density topography
            const n1 = noise3D(nx, ny, nt);
            const n2 = noise3D(nx * 2 + 10, ny * 2 + 10, nt * 1.2) * 0.5;
            const wave = Math.sin((c * 0.08 + r * 0.05) - elapsed * 0.9);

            const combined = (n1 + n2 + wave * 0.6) / 2.1;
            rawDensity = Math.max(0, Math.min(1, (combined + 1) / 2));
          }

          // Apply power curve so zeros dominate ambient spaces (like Image 2)
          let density = Math.pow(rawDensity, 2.4);

          // Interactive Mouse Spotlight bump
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

          // Random glitch/flicker (1.5% chance) for high-tech telemetry effect
          const glitch = Math.random() < 0.015;
          if (glitch && density > 0.1) {
            density = Math.min(1, density + (Math.random() * 0.3 - 0.1));
          }

          // Map density to character index
          const charIndex = Math.min(
            CHARS.length - 1,
            Math.floor(density * CHARS.length)
          );
          const char = CHARS[charIndex];

          // Text color
          const color = getColor(density, charIndex);
          ctx.fillStyle = color;

          // Render character with text glow for peak hex values
          if (density > 0.82) {
            ctx.shadowColor = palette === 'gold' ? 'rgba(253, 224, 71, 0.6)' : 'rgba(255, 255, 255, 0.7)';
            ctx.shadowBlur = 8;
          } else {
            ctx.shadowBlur = 0;
          }

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
    <div
      className={`absolute inset-0 pointer-events-auto select-none overflow-hidden ${className}`}
      style={{ opacity }}
    >
      <canvas ref={canvasRef} className="block w-full h-full" />
    </div>
  );
};
