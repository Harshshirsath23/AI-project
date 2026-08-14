import React, { useState, useEffect } from 'react';
import { 
  ShieldCheck, 
  Layers, 
  Cpu, 
  Bot, 
  Building2,
  TrendingUp,
  Sliders
} from 'lucide-react';

export const BrandHeader: React.FC = () => {
  const [agentStep, setAgentStep] = useState(0);

  // Live Agent Simulation Ticker
  useEffect(() => {
    const timer = setInterval(() => {
      setAgentStep((prev) => (prev + 1) % 3);
    }, 4000);
    return () => clearInterval(timer);
  }, []);

  const agentActivities = [
    {
      agent: 'Executive Sourcing Agent v4.2',
      action: 'Screened 142 VP candidates for Tech Lead role',
      metric: '98.4% Skill Alignment',
      status: 'Active Sourcing',
      time: 'Just now',
    },
    {
      agent: 'EEOC & Bias Sentinel Agent',
      action: 'Verified anonymized resume evaluation workflow',
      metric: '0 Compliance Flags',
      status: 'Audited & Shielded',
      time: '2 mins ago',
    },
    {
      agent: 'Compensation Benchmark AI',
      action: 'Generated market offer benchmarks for SF & NYC',
      metric: '+14% Acceptance Velocity',
      status: 'Real-time Analytics',
      time: '5 mins ago',
    },
  ];

  return (
    <div className="w-full flex flex-col justify-between space-y-8 pr-0 lg:pr-8 text-left select-none animate-fade-in">
      <div>
        {/* Institutional Compliance Badge */}
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full glass-panel text-xs text-zinc-600 dark:text-zinc-400 mb-6 shadow-sm">
          <span className="relative flex h-2 w-2">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
            <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
          </span>
          <span className="font-medium text-[11px] tracking-wide">
            SOC 2 Type II Certified
          </span>
          <span className="opacity-40">•</span>
          <span className="text-[11px] font-medium flex items-center gap-1">
            <ShieldCheck className="w-3.5 h-3.5" />
            ISO 27001 Verified
          </span>
        </div>

        {/* Corporate Logo Mark */}
        <div className="flex items-center gap-3.5 mb-6">
          <div className="w-12 h-12 rounded-xl glass-card flex items-center justify-center">
            <Layers className="w-6 h-6 dark:text-white light:text-zinc-900" />
          </div>
          <div>
            <div className="text-2xl sm:text-3xl font-medium tracking-tight dark:text-white light:text-zinc-900 flex items-center gap-2">
              TalentSphere
              <span className="text-[10px] font-mono font-medium px-2 py-0.5 rounded-md glass-panel uppercase tracking-widest">
                OS
              </span>
            </div>
            <p className="text-[11px] font-medium tracking-widest uppercase dark:text-zinc-400 light:text-zinc-600 mt-0.5">
              Autonomous Talent Operating System
            </p>
          </div>
        </div>

        {/* Headline */}
        <h1 className="text-3xl sm:text-4xl lg:text-5xl font-medium tracking-tight dark:text-white light:text-zinc-900 leading-[1.15] mb-4">
          Enterprise Hiring <br />
          <span className="dark:text-zinc-300 light:text-zinc-700">
            Driven by Autonomous AI
          </span>
        </h1>

        {/* Subtitle */}
        <p className="text-sm sm:text-base font-normal dark:text-zinc-400 light:text-zinc-600 leading-relaxed max-w-xl mb-8">
          The AI-native talent infrastructure engineered for recruiting leaders who require high-precision candidate matching, zero-bias EEOC audits, and SOC 2 Type II security.
        </p>
      </div>

      {/* Live AI Operating System Stream Widget */}
      <div className="rounded-2xl glass-card p-5 shadow-sm relative overflow-hidden">
        <div className="flex items-center justify-between mb-4 border-b border-zinc-200 dark:border-zinc-800 pb-3">
          <div className="flex items-center gap-2">
            <Cpu className="w-4 h-4 text-zinc-400" />
            <span className="text-xs font-medium dark:text-white light:text-zinc-900 tracking-wide uppercase font-mono">
              Live Agent Execution Stream
            </span>
          </div>

          <div className="flex items-center gap-1.5 text-[10px] font-mono text-emerald-600 dark:text-emerald-400 glass-panel px-2.5 py-0.5 rounded-full font-medium">
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse" />
            <span>SYSTEM NOMINAL</span>
          </div>
        </div>

        {/* Active Activity Highlight */}
        <div className="p-3.5 rounded-xl glass-panel space-y-2 mb-4">
          <div className="flex items-center justify-between text-xs">
            <div className="flex items-center gap-2 font-medium dark:text-white light:text-zinc-900">
              <Bot className="w-4 h-4 text-zinc-400" />
              <span>{agentActivities[agentStep].agent}</span>
            </div>
            <span className="text-[10px] dark:text-zinc-500 light:text-zinc-400 font-mono">
              {agentActivities[agentStep].time}
            </span>
          </div>

          <p className="text-xs dark:text-zinc-300 light:text-zinc-700 font-normal">
            {agentActivities[agentStep].action}
          </p>

          <div className="flex items-center justify-between pt-1 text-[11px]">
            <span className="font-mono font-medium text-emerald-600 dark:text-emerald-400">
              {agentActivities[agentStep].metric}
            </span>
            <span className="px-2 py-0.5 rounded glass-card text-[10px] font-mono dark:text-zinc-300 light:text-zinc-700">
              {agentActivities[agentStep].status}
            </span>
          </div>
        </div>

        {/* Metric Footers */}
        <div className="grid grid-cols-3 gap-2 text-center text-xs">
          <div className="p-2 rounded-lg glass-panel">
            <div className="dark:text-zinc-400 light:text-zinc-500 text-[10px] uppercase font-mono">Precision</div>
            <div className="text-sm font-medium dark:text-white light:text-zinc-900 mt-0.5 font-mono">98.4%</div>
          </div>
          <div className="p-2 rounded-lg glass-panel">
            <div className="dark:text-zinc-400 light:text-zinc-500 text-[10px] uppercase font-mono">EEOC Audit</div>
            <div className="text-sm font-medium text-emerald-600 dark:text-emerald-400 mt-0.5 font-mono">0 Flags</div>
          </div>
          <div className="p-2 rounded-lg glass-panel">
            <div className="dark:text-zinc-400 light:text-zinc-500 text-[10px] uppercase font-mono">SLA Uptime</div>
            <div className="text-sm font-medium dark:text-zinc-200 light:text-zinc-800 mt-0.5 font-mono">99.99%</div>
          </div>
        </div>
      </div>

      {/* Enterprise Social Proof */}
      <div className="pt-2">
        <p className="text-[11px] font-mono dark:text-zinc-500 light:text-zinc-400 uppercase tracking-widest mb-3">
          TRUSTED BY RECRUITMENT LEADERS AT
        </p>
        <div className="flex flex-wrap items-center gap-6 dark:text-zinc-400 light:text-zinc-600 text-xs font-medium tracking-wider">
          <span className="flex items-center gap-1.5 hover:text-zinc-900 dark:hover:text-white transition">
            <Building2 className="w-4 h-4 text-zinc-400" /> ACME GLOBAL
          </span>
          <span className="flex items-center gap-1.5 hover:text-zinc-900 dark:hover:text-white transition">
            <TrendingUp className="w-4 h-4 text-zinc-400" /> VANGUARD TALENT
          </span>
          <span className="flex items-center gap-1.5 hover:text-zinc-900 dark:hover:text-white transition">
            <ShieldCheck className="w-4 h-4 text-emerald-600 dark:text-emerald-400" /> TECHSPHERE
          </span>
          <span className="flex items-center gap-1.5 hover:text-zinc-900 dark:hover:text-white transition">
            <Sliders className="w-4 h-4 text-zinc-400" /> HYPERSCALE
          </span>
        </div>
      </div>
    </div>
  );
};
