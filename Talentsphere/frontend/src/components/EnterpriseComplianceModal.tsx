import React from 'react';
import { X, ShieldCheck, Lock, FileCheck, Cpu, Globe, Check } from 'lucide-react';

interface EnterpriseComplianceModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export const EnterpriseComplianceModal: React.FC<EnterpriseComplianceModalProps> = ({
  isOpen,
  onClose,
}) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-md animate-in fade-in duration-150">
      <div className="relative w-full max-w-2xl max-h-[85vh] rounded-2xl glass-card overflow-y-auto p-6 md:p-8 text-left space-y-4">
        <button
          onClick={onClose}
          className="absolute top-5 right-5 p-2 rounded-xl glass-panel dark:text-zinc-400 light:text-zinc-600 hover:text-zinc-900 dark:hover:text-white transition"
          aria-label="Close modal"
        >
          <X className="w-4 h-4" />
        </button>

        <div className="flex items-center gap-3.5 mb-6">
          <div className="w-11 h-11 rounded-2xl glass-panel flex items-center justify-center dark:text-zinc-300 light:text-zinc-700">
            <ShieldCheck className="w-6 h-6" />
          </div>
          <div>
            <h3 className="text-xl font-medium dark:text-white light:text-zinc-900 tracking-tight">Enterprise Security &amp; Compliance</h3>
            <p className="text-xs dark:text-zinc-400 light:text-zinc-600 font-normal">TalentSphere OS Security Portal</p>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
          <div className="p-4.5 rounded-xl glass-panel">
            <div className="flex items-center gap-2 mb-1.5 text-emerald-600 dark:text-emerald-400 font-medium text-xs">
              <FileCheck className="w-4 h-4" /> SOC 2 Type II Certified
            </div>
            <p className="text-xs dark:text-zinc-300 light:text-zinc-700 leading-relaxed font-normal">
              Audited annually. Covers Security, Availability, Processing Integrity, Confidentiality, and Privacy controls.
            </p>
          </div>

          <div className="p-4.5 rounded-xl glass-panel">
            <div className="flex items-center gap-2 mb-1.5 dark:text-zinc-200 light:text-zinc-800 font-medium text-xs">
              <Lock className="w-4 h-4" /> AES-256 &amp; TLS 1.3
            </div>
            <p className="text-xs dark:text-zinc-300 light:text-zinc-700 leading-relaxed font-normal">
              End-to-end data encryption at rest and in transit. Customer-Managed Encryption Keys (CMEK / AWS KMS) supported.
            </p>
          </div>

          <div className="p-4.5 rounded-xl glass-panel">
            <div className="flex items-center gap-2 mb-1.5 dark:text-zinc-200 light:text-zinc-800 font-medium text-xs">
              <Globe className="w-4 h-4" /> Data Residency &amp; GDPR
            </div>
            <p className="text-xs dark:text-zinc-300 light:text-zinc-700 leading-relaxed font-normal">
              Granular region isolation (US-East, EU Frankfurt, APAC, FedRAMP). Candidate data never leaves tenant boundaries.
            </p>
          </div>

          <div className="p-4.5 rounded-xl glass-panel">
            <div className="flex items-center gap-2 mb-1.5 dark:text-zinc-200 light:text-zinc-800 font-medium text-xs">
              <Cpu className="w-4 h-4" /> Non-Training AI Safeguard
            </div>
            <p className="text-xs dark:text-zinc-300 light:text-zinc-700 leading-relaxed font-normal">
              Strict zero-retention AI policy. Your recruitment data and candidate resumes are never used to train public LLMs.
            </p>
          </div>
        </div>

        <div className="p-4.5 rounded-xl glass-panel mb-6">
          <h4 className="text-xs font-medium dark:text-zinc-200 light:text-zinc-800 uppercase tracking-wider mb-2 font-mono">
            Identity &amp; SSO Compatibility
          </h4>
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 text-xs font-normal dark:text-zinc-300 light:text-zinc-700">
            <span className="flex items-center gap-1.5"><Check className="w-3.5 h-3.5 text-emerald-600 dark:text-emerald-400" /> Okta SAML 2.0</span>
            <span className="flex items-center gap-1.5"><Check className="w-3.5 h-3.5 text-emerald-600 dark:text-emerald-400" /> Azure AD / Entra</span>
            <span className="flex items-center gap-1.5"><Check className="w-3.5 h-3.5 text-emerald-600 dark:text-emerald-400" /> Google Workspace</span>
            <span className="flex items-center gap-1.5"><Check className="w-3.5 h-3.5 text-emerald-600 dark:text-emerald-400" /> Ping Identity</span>
          </div>
        </div>

        <div className="flex justify-end pt-2">
          <button
            onClick={onClose}
            className="px-5 py-2.5 rounded-xl bg-zinc-900 text-white font-medium text-xs tracking-wide transition shadow-sm hover:bg-zinc-800"
          >
            Close Security Brief
          </button>
        </div>
      </div>
    </div>
  );
};
