"use client";

import { memo, useCallback, useEffect, useRef } from "react";
import { cn } from "@/lib/utils";

interface GlowingEffectProps {
  blur?: number;
  spread?: number;
  variant?: "default" | "white";
  glow?: boolean;
  className?: string;
  disabled?: boolean;
  borderWidth?: number;
}
const GlowingEffect = memo(
  ({
    blur = 0,
    spread = 250, // Larger spread for the smooth spotlight effect
    variant = "default",
    glow = false,
    className,
    borderWidth = 1,
    disabled = false,
  }: GlowingEffectProps) => {
    const containerRef = useRef<HTMLDivElement>(null);
    const animationFrameRef = useRef<number>(0);

    const handleMove = useCallback((e: MouseEvent | PointerEvent) => {
      if (!containerRef.current) return;
      if (animationFrameRef.current) {
        cancelAnimationFrame(animationFrameRef.current);
      }
      animationFrameRef.current = requestAnimationFrame(() => {
        const element = containerRef.current;
        if (!element) return;
        const rect = element.getBoundingClientRect();
        
        // Calculate relative mouse position
        const mouseX = e.clientX - rect.left;
        const mouseY = e.clientY - rect.top;

        element.style.setProperty("--mouse-x", `${mouseX}px`);
        element.style.setProperty("--mouse-y", `${mouseY}px`);
      });
    }, []);

    useEffect(() => {
      if (disabled) return;
      
      const handlePointerMove = (e: PointerEvent) => handleMove(e);
      document.body.addEventListener("pointermove", handlePointerMove, {
        passive: true,
      });

      return () => {
        if (animationFrameRef.current) {
          cancelAnimationFrame(animationFrameRef.current);
        }
        document.body.removeEventListener("pointermove", handlePointerMove);
      };
    }, [handleMove, disabled]);

    // Bright blue neon spotlight
    const gradientColors = variant === "white" 
      ? "rgba(255,255,255,0.8), transparent" 
      : "rgba(0, 162, 255, 1), rgba(0, 102, 255, 0.3), transparent";

    return (
      <div
        ref={containerRef}
        style={{
          "--blur": `${blur}px`,
          "--spread": spread,
          "--mouse-x": "-1000px",
          "--mouse-y": "-1000px",
          "--border-width": `${borderWidth}px`,
        } as React.CSSProperties}
        className={cn(
          "pointer-events-none absolute inset-0 rounded-[inherit] transition-opacity duration-300",
          glow ? "opacity-100" : "opacity-0 group-hover:opacity-100",
          className,
          disabled && "!hidden"
        )}
      >
        {/* The actual border mask */}
        <div
          className="absolute inset-0 rounded-[inherit] mix-blend-screen"
          style={{
            padding: "var(--border-width)",
            background: `radial-gradient(calc(var(--spread) * 1px) circle at var(--mouse-x) var(--mouse-y), ${gradientColors})`,
            WebkitMask: "linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0)",
            WebkitMaskComposite: "xor",
            maskComposite: "exclude",
            filter: blur > 0 ? `blur(var(--blur))` : undefined,
          }}
        />
        {/* Subtle inner card glow */}
        <div
          className="absolute inset-0 rounded-[inherit] mix-blend-screen opacity-10"
          style={{
            background: `radial-gradient(calc(var(--spread) * 1.5px) circle at var(--mouse-x) var(--mouse-y), ${gradientColors})`,
          }}
        />
      </div>
    );
  }
);

GlowingEffect.displayName = "GlowingEffect";

export { GlowingEffect };
