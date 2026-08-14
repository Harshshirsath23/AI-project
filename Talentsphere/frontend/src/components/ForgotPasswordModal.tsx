import React, { useState } from 'react';
import { X, Mail, CheckCircle2, ShieldAlert, ArrowRight, Loader2 } from 'lucide-react';

interface ForgotPasswordModalProps {
  isOpen: boolean;
  onClose: () => void;
  initialEmail?: string;
}

export const ForgotPasswordModal: React.FC<ForgotPasswordModalProps> = ({
  isOpen,
  onClose,
  initialEmail = '',
}) => {
  const [email, setEmail] = useState(initialEmail);
  const [isLoading, setIsLoading] = useState(false);
  const [isSubmitted, setIsSubmitted] = useState(false);
  const [error, setError] = useState('');

  if (!isOpen) return null;

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!email || !email.includes('@')) {
      setError('Please enter a valid work email address');
      return;
    }

    setError('');
    setIsLoading(true);

    setTimeout(() => {
      setIsLoading(false);
      setIsSubmitted(true);
    }, 1000);
  };

  const handleReset = () => {
    setIsSubmitted(false);
    setEmail('');
    onClose();
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-md animate-in fade-in duration-150">
      <div className="relative w-full max-w-md rounded-2xl glass-card overflow-hidden p-6 md:p-8 text-left space-y-4">
        <button
          onClick={onClose}
          className="absolute top-5 right-5 p-2 rounded-xl glass-panel dark:text-zinc-400 light:text-zinc-600 hover:text-zinc-900 dark:hover:text-white transition"
          aria-label="Close modal"
        >
          <X className="w-4 h-4" />
        </button>

        {!isSubmitted ? (
          <div>
            <div className="w-11 h-11 rounded-2xl glass-panel flex items-center justify-center mb-4 dark:text-zinc-300 light:text-zinc-700">
              <Mail className="w-6 h-6" />
            </div>

            <h3 className="text-xl font-medium dark:text-white light:text-zinc-900 tracking-tight mb-1">Reset Work Password</h3>
            <p className="text-xs dark:text-zinc-400 light:text-zinc-600 mb-6 leading-relaxed font-normal">
              Enter your corporate email address. If an enterprise account exists, a secure password reset link will be dispatched via your identity provider.
            </p>

            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label htmlFor="reset-email" className="block text-xs font-medium dark:text-zinc-300 light:text-zinc-700 mb-1.5">
                  Work Email Address
                </label>
                <input
                  id="reset-email"
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="name@company.com"
                  className="w-full px-4 py-3 rounded-xl dark:bg-black/80 light:bg-white border border-zinc-300 dark:border-zinc-700 text-xs dark:text-white light:text-zinc-900 placeholder-zinc-500 focus:outline-none"
                  required
                />
                {error && (
                  <p className="mt-2 text-xs text-red-500 font-medium flex items-center gap-1">
                    <ShieldAlert className="w-3.5 h-3.5" /> {error}
                  </p>
                )}
              </div>

              <div className="pt-2 flex items-center justify-end gap-3">
                <button
                  type="button"
                  onClick={onClose}
                  className="px-4 py-2.5 rounded-xl text-xs font-medium glass-panel dark:text-zinc-300 light:text-zinc-700 hover:bg-zinc-100 dark:hover:bg-zinc-800"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={isLoading}
                  className="px-6 py-3 rounded-xl bg-zinc-900 text-white font-medium text-xs tracking-wide shadow-sm flex items-center gap-2 disabled:opacity-50 hover:bg-zinc-800"
                >
                  {isLoading ? (
                    <>
                      <Loader2 className="w-4 h-4 animate-spin" /> Dispatching Link...
                    </>
                  ) : (
                    <>
                      Send Reset Email <ArrowRight className="w-4 h-4" />
                    </>
                  )}
                </button>
              </div>
            </form>
          </div>
        ) : (
          <div className="text-center py-4">
            <div className="w-12 h-12 rounded-full glass-panel text-emerald-600 dark:text-emerald-400 flex items-center justify-center mx-auto mb-4">
              <CheckCircle2 className="w-6 h-6" />
            </div>
            <h3 className="text-lg font-medium dark:text-white light:text-zinc-900 mb-2">Reset Instructions Sent</h3>
            <p className="text-xs dark:text-zinc-400 light:text-zinc-600 mb-6 leading-relaxed font-normal">
              We dispatched reset instructions to <strong className="dark:text-white light:text-zinc-900 font-medium">{email}</strong>. Check your corporate inbox or SSO portal.
            </p>
            <button
              onClick={handleReset}
              className="w-full py-3 rounded-xl bg-zinc-900 text-white text-xs font-medium tracking-wider transition shadow-sm hover:bg-zinc-800"
            >
              Return to Login
            </button>
          </div>
        )}
      </div>
    </div>
  );
};
