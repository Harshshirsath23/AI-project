import React, { useState } from 'react';
import { createPortal } from 'react-dom';
import { X, Building } from 'lucide-react';
import { useOrganization } from '../../context/OrganizationContext';

interface Props {
  isOpen: boolean;
  onClose: () => void;
}

export const CreateOrganizationModal: React.FC<Props> = ({ isOpen, onClose }) => {
  const { createOrganization } = useOrganization();
  const [formData, setFormData] = useState({
    organization_code: '',
    legal_name: '',
    display_name: '',
    subscription_plan: 'Enterprise Tier 1',
  });
  const [isSubmitting, setIsSubmitting] = useState(false);

  if (!isOpen) return null;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    
    // Auto-generate some required fields for backend validation testing
    const payload = {
      ...formData,
      industry_id: '00000000-0000-0000-0000-000000000000', // Mock UUID for testing
      subscription_status: 'Active',
    };

    await createOrganization(payload);
    setIsSubmitting(false);
    onClose();
  };

  const modalContent = (
    <div className="fixed inset-0 z-[100] flex items-center justify-center bg-black/60 backdrop-blur-sm animate-fade-in">
      <div className="bg-white dark:bg-[#0a0a0a] border border-zinc-200 dark:border-zinc-800 w-full max-w-lg rounded-2xl shadow-2xl overflow-hidden flex flex-col max-h-[90vh]">
        
        {/* Header */}
        <div className="flex items-center justify-between p-4 border-b border-zinc-200 dark:border-zinc-800 shrink-0">
          <div className="flex items-center gap-2">
            <Building className="w-5 h-5 dark:text-zinc-300 light:text-zinc-700" />
            <h3 className="text-sm font-medium dark:text-white light:text-zinc-900">Create New Organization</h3>
          </div>
          <button onClick={onClose} className="p-1 rounded-lg hover:bg-zinc-100 dark:hover:bg-zinc-800 text-zinc-500 transition">
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Body */}
        <div className="p-4 overflow-y-auto">
          <form id="create-org-form" onSubmit={handleSubmit} className="space-y-4">
            
            <div className="space-y-1">
              <label className="text-xs font-medium dark:text-zinc-300 light:text-zinc-700">Organization Code</label>
              <input
                type="text"
                required
                value={formData.organization_code}
                onChange={(e) => setFormData({ ...formData, organization_code: e.target.value })}
                placeholder="e.g. ACME"
                className="w-full px-3 py-2 text-xs rounded-lg border border-zinc-200 dark:border-zinc-800 dark:bg-black/50 focus:outline-none focus:ring-1 focus:ring-blue-500"
              />
            </div>

            <div className="space-y-1">
              <label className="text-xs font-medium dark:text-zinc-300 light:text-zinc-700">Legal Name</label>
              <input
                type="text"
                required
                value={formData.legal_name}
                onChange={(e) => setFormData({ ...formData, legal_name: e.target.value })}
                placeholder="e.g. Acme Corporation"
                className="w-full px-3 py-2 text-xs rounded-lg border border-zinc-200 dark:border-zinc-800 dark:bg-black/50 focus:outline-none focus:ring-1 focus:ring-blue-500"
              />
            </div>

            <div className="space-y-1">
              <label className="text-xs font-medium dark:text-zinc-300 light:text-zinc-700">Display Name</label>
              <input
                type="text"
                required
                value={formData.display_name}
                onChange={(e) => setFormData({ ...formData, display_name: e.target.value })}
                placeholder="e.g. Acme Corp"
                className="w-full px-3 py-2 text-xs rounded-lg border border-zinc-200 dark:border-zinc-800 dark:bg-black/50 focus:outline-none focus:ring-1 focus:ring-blue-500"
              />
            </div>

            <div className="space-y-1">
              <label className="text-xs font-medium dark:text-zinc-300 light:text-zinc-700">Subscription Plan</label>
              <select
                required
                value={formData.subscription_plan}
                onChange={(e) => setFormData({ ...formData, subscription_plan: e.target.value })}
                className="w-full px-3 py-2 text-xs rounded-lg border border-zinc-200 dark:border-zinc-800 dark:bg-black/50 focus:outline-none focus:ring-1 focus:ring-blue-500"
              >
                <option value="Enterprise Tier 1">Enterprise Tier 1</option>
                <option value="Scale">Scale</option>
                <option value="Government">Government</option>
              </select>
            </div>
            
          </form>
        </div>

        {/* Footer */}
        <div className="p-4 border-t border-zinc-200 dark:border-zinc-800 flex justify-end gap-2 shrink-0 bg-zinc-50 dark:bg-zinc-900/30">
          <button
            type="button"
            onClick={onClose}
            className="px-4 py-2 rounded-xl text-xs font-medium dark:text-zinc-300 light:text-zinc-700 hover:bg-zinc-200 dark:hover:bg-zinc-800 transition"
          >
            Cancel
          </button>
          <button
            type="submit"
            form="create-org-form"
            disabled={isSubmitting}
            className="px-4 py-2 rounded-xl bg-zinc-900 dark:bg-white text-white dark:text-zinc-900 text-xs font-medium transition disabled:opacity-50"
          >
            {isSubmitting ? 'Creating...' : 'Create Organization'}
          </button>
        </div>
      </div>
    </div>
  );

  // Use portal to mount modal directly to body to avoid flex/transform parent constraints
  return typeof document !== 'undefined' ? createPortal(modalContent, document.body) : null;
};
