import React from 'react';
import { useTheme } from '../context/ThemeContext';
import { AsciiNumberCanvas, AsciiPalette, AsciiMode } from './ui/AsciiNumberCanvas';

interface BackgroundCanvasProps {
  reducedMotion?: boolean;
  palette?: AsciiPalette;
  mode?: AsciiMode;
}

export const BackgroundCanvas: React.FC<BackgroundCanvasProps> = ({
  reducedMotion,
  palette = 'mono',
  mode = 'waves',
}) => {
  const { theme } = useTheme();

  return (
    <div
      className="fixed inset-0 z-0 overflow-hidden select-none transition-colors duration-300 bg-[#040508]"
      aria-hidden="true"
    >
      {/* Dynamic ASCII Art Numeric Matrix Grid Background */}
      <AsciiNumberCanvas
        palette={palette}
        mode={mode}
        speed={reducedMotion ? 0.2 : 0.8}
        opacity={0.9}
        interactive={true}
      />

      {/* Executive Monochrome Ambient Glow Radial Orbs */}
      <div 
        className="absolute -top-40 -left-40 w-[600px] h-[600px] rounded-full blur-[140px] opacity-20 pointer-events-none"
        style={{
          background: 'radial-gradient(circle, rgba(255, 255, 255, 0.2) 0%, rgba(9, 9, 11, 0) 70%)',
        }}
      />
      <div 
        className="absolute -bottom-40 -right-40 w-[700px] h-[700px] rounded-full blur-[160px] opacity-20 pointer-events-none"
        style={{
          background: 'radial-gradient(circle, rgba(148, 163, 184, 0.25) 0%, rgba(0, 0, 0, 0) 70%)',
        }}
      />

      {/* Subtle Vignette Overlay to frame the central floating card */}
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,transparent_20%,rgba(4,5,8,0.75)_100%)] pointer-events-none" />
      <div className="absolute inset-0 bg-gradient-to-b from-black/60 via-transparent to-black/70 pointer-events-none" />
    </div>
  );
};

