import React, { useState, useRef, useEffect } from 'react';
import { ArrowRight, Loader2, KeyRound } from 'lucide-react';

interface MfaModalProps {
  isOpen: boolean;
  onVerifySuccess: () => void;
  onCancel: () => void;
  userEmail: string;
}

export const MfaModal: React.FC<MfaModalProps> = ({
  isOpen,
  onVerifySuccess,
  onCancel,
  userEmail,
}) => {
  const [code, setCode] = useState(['', '', '', '', '', '']);
  const [isVerifying, setIsVerifying] = useState(false);
  const [error, setError] = useState('');
  const inputRefs = useRef<(HTMLInputElement | null)[]>([]);

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

    if (value && index < 5) {
      inputRefs.current[index + 1]?.focus();
    }
  };

  const handleKeyDown = (index: number, e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Backspace' && !code[index] && index > 0) {
      inputRefs.current[index - 1]?.focus();
    }
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

    setTimeout(() => {
      setIsVerifying(false);
      onVerifySuccess();
    }, 900);
  };

  const fillDemoCode = () => {
    setCode(['8', '4', '2', '9', '1', '0']);
    setError('');
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-md animate-in fade-in duration-150">
      <div className="relative w-full max-w-md rounded-2xl glass-card p-6 md:p-8 text-left space-y-5">
        <div className="w-11 h-11 rounded-2xl glass-panel flex items-center justify-center dark:text-zinc-300 light:text-zinc-700">
          <KeyRound className="w-6 h-6" />
        </div>

        <div className="flex items-center justify-between">
          <h3 className="text-xl font-medium dark:text-white light:text-zinc-900 tracking-tight">Security Verification</h3>
          <span className="text-[10px] font-mono font-medium uppercase tracking-wider px-2.5 py-0.5 rounded-full glass-panel dark:text-zinc-300 light:text-zinc-700">
            MFA Mandatory
          </span>
        </div>

        <p className="text-xs dark:text-zinc-400 light:text-zinc-600 leading-relaxed font-normal">
          Enter the 6-digit TOTP code from Okta Verify / Duo / Authenticator for <strong className="dark:text-white light:text-zinc-900 font-medium">{userEmail || 'your account'}</strong>.
        </p>

        <form onSubmit={handleVerify} className="space-y-5">
          <div>
            <div className="flex items-center justify-between gap-2 mb-2">
              {code.map((digit, idx) => (
                <input
                  key={idx}
                  ref={(el) => { inputRefs.current[idx] = el; }}
                  type="text"
                  inputMode="numeric"
                  maxLength={1}
                  value={digit}
                  onChange={(e) => handleChange(idx, e.target.value)}
                  onKeyDown={(e) => handleKeyDown(idx, e)}
                  className="w-12 h-12 text-center text-xl font-medium rounded-xl dark:bg-black/80 light:bg-white border border-zinc-300 dark:border-zinc-700 dark:text-white light:text-zinc-900 focus:outline-none"
                />
              ))}
            </div>
            {error && (
              <p className="mt-2 text-xs text-red-500 font-medium">
                {error}
              </p>
            )}
          </div>

          <div className="p-3.5 rounded-xl glass-panel flex items-center justify-between">
            <span className="text-xs dark:text-zinc-400 light:text-zinc-600 font-normal">Demo Testing?</span>
            <button
              type="button"
              onClick={fillDemoCode}
              className="text-xs dark:text-zinc-200 light:text-zinc-800 hover:underline font-medium"
            >
              Autofill MFA Code (842910)
            </button>
          </div>

          <div className="flex items-center justify-end gap-3 pt-2">
            <button
              type="button"
              onClick={onCancel}
              className="px-4 py-2.5 rounded-xl text-xs font-medium glass-panel dark:text-zinc-300 light:text-zinc-700 hover:bg-zinc-100 dark:hover:bg-zinc-800"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={isVerifying}
              className="px-6 py-3 rounded-xl bg-zinc-900 text-white font-medium text-xs tracking-wide shadow-sm flex items-center gap-2 disabled:opacity-50 hover:bg-zinc-800"
            >
              {isVerifying ? (
                <>
                  <Loader2 className="w-4 h-4 animate-spin" /> Verifying Code...
                </>
              ) : (
                <>
                  Verify &amp; Access <ArrowRight className="w-4 h-4" />
                </>
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};
