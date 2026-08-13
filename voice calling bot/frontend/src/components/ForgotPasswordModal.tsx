import React, { useState } from 'react';
import { X, Mail, CheckCircle2, ShieldAlert, ArrowRight, Loader2 } from 'lucide-react';
import { api } from '../services/api';

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

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!email || !email.includes('@')) {
      setError('Please enter a valid work email address');
      return;
    }

    setError('');
    setIsLoading(true);

    try {
      await api.requestPasswordReset(email);
      setIsLoading(false);
      setIsSubmitted(true);
    } catch (err: any) {
      setIsLoading(false);
      setIsSubmitted(true); // Don't reveal if user exists
    }
  };

  const handleReset = () => {
    setIsSubmitted(false);
    setEmail('');
    onClose();
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-md animate-in fade-in duration-150">
      <div className="relative w-full max-w-md rounded-2xl bg-card border overflow-hidden p-6 md:p-8 text-left space-y-4">
        <button
          onClick={onClose}
          className="absolute top-5 right-5 p-2 rounded-xl border hover:bg-muted text-muted-foreground transition"
          aria-label="Close modal"
        >
          <X className="w-4 h-4" />
        </button>

        {!isSubmitted ? (
          <div>
            <div className="w-11 h-11 rounded-2xl bg-primary/10 text-primary flex items-center justify-center mb-4">
              <Mail className="w-6 h-6" />
            </div>

            <h3 className="text-xl font-bold tracking-tight mb-1">Reset Work Password</h3>
            <p className="text-xs text-muted-foreground mb-6 leading-relaxed font-normal">
              Enter your corporate email address. A secure password reset token will be dispatched via your identity provider.
            </p>

            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label htmlFor="reset-email" className="block text-xs font-medium mb-1.5">
                  Work Email Address
                </label>
                <input
                  id="reset-email"
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="name@company.com"
                  className="w-full px-4 py-3 rounded-xl bg-background border text-xs focus:outline-none focus:ring-2 focus:ring-primary"
                  required
                />
                {error && (
                  <p className="mt-2 text-xs text-destructive font-medium flex items-center gap-1">
                    <ShieldAlert className="w-3.5 h-3.5" /> {error}
                  </p>
                )}
              </div>

              <div className="pt-2 flex items-center justify-end gap-3">
                <button
                  type="button"
                  onClick={onClose}
                  className="px-4 py-2.5 rounded-xl text-xs font-medium border hover:bg-muted"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={isLoading}
                  className="px-6 py-3 rounded-xl bg-primary text-primary-foreground font-medium text-xs tracking-wide shadow-sm flex items-center gap-2 disabled:opacity-50 hover:bg-primary/90"
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
            <div className="w-12 h-12 rounded-full bg-green-100 text-green-600 flex items-center justify-center mx-auto mb-4">
              <CheckCircle2 className="w-6 h-6" />
            </div>
            <h3 className="text-lg font-bold mb-2">Reset Instructions Sent</h3>
            <p className="text-xs text-muted-foreground mb-6 leading-relaxed font-normal">
              If an account exists for <strong className="text-foreground font-semibold">{email}</strong>, reset instructions have been dispatched.
            </p>
            <button
              onClick={handleReset}
              className="w-full py-3 rounded-xl bg-primary text-primary-foreground text-xs font-medium tracking-wider transition shadow-sm hover:bg-primary/90"
            >
              Return to Login
            </button>
          </div>
        )}
      </div>
    </div>
  );
};
