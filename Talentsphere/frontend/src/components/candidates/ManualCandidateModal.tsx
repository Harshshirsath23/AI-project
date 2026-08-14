import React, { useState } from 'react';
import { useOrganization } from '../../context/OrganizationContext';
import { useNotification } from '../../context/NotificationContext';
import { UserPlus, X, UserCheck, Briefcase, Mail, Phone, MapPin, Award, FileText, Upload, Sparkles } from 'lucide-react';

interface ManualCandidateModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export const ManualCandidateModal: React.FC<ManualCandidateModalProps> = ({ isOpen, onClose }) => {
  const { addCandidate } = useOrganization();
  const { showSuccess, showError } = useNotification();

  const [formData, setFormData] = useState({
    firstName: '',
    lastName: '',
    email: '',
    phone: '',
    location: '',
    currentRole: '',
    currentCompany: '',
    summary: '',
    skills: '',
    matchScore: 85,
  });

  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  if (!isOpen) return null;

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setSelectedFile(file);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!formData.firstName.trim() || !formData.email.trim()) {
      showError('Validation Error', 'First Name and Email Address are required.');
      return;
    }

    setIsSubmitting(true);
    try {
      const fullName = `${formData.firstName.trim()} ${formData.lastName.trim()}`.trim();
      const parsedSkills = formData.skills
        ? formData.skills.split(',').map((s) => s.trim()).filter(Boolean)
        : [];

      const experiences = (formData.currentRole || formData.currentCompany) ? [
        {
          id: `exp-${Date.now()}`,
          company: formData.currentCompany || 'N/A',
          role: formData.currentRole || 'N/A',
          startDate: 'Recent',
          endDate: 'Present',
          isCurrent: true,
          description: formData.summary || `Role as ${formData.currentRole || 'Team Member'} at ${formData.currentCompany || 'Company'}`,
        }
      ] : [];

      await addCandidate({
        name: fullName,
        email: formData.email.trim(),
        phone: formData.phone.trim() || 'N/A',
        location: formData.location.trim() || 'Not Specified',
        currentRole: formData.currentRole.trim() || 'Candidate',
        currentCompany: formData.currentCompany.trim() || 'Organization',
        avatar: `https://ui-avatars.com/api/?name=${encodeURIComponent(fullName)}&background=random`,
        status: 'New',
        matchScore: formData.matchScore || 85,
        skills: parsedSkills,
        summary: formData.summary.trim() || `Manually created candidate profile for ${fullName}.`,
        experiences: experiences,
        education: [],
        documents: selectedFile ? [
          {
            id: `doc-${Date.now()}`,
            name: selectedFile.name,
            type: 'Resume',
            uploadDate: new Date().toISOString().split('T')[0],
            size: `${Math.round(selectedFile.size / 1024)} KB`,
          }
        ] : [],
        timeline: [
          {
            id: `tl-${Date.now()}`,
            title: 'Candidate Profile Created',
            description: 'Created manually via Candidate Command Center.',
            timestamp: new Date().toLocaleString(),
            actor: 'HR Recruiter',
            type: 'candidate_created',
          },
        ],
      });

      showSuccess('Candidate Profile Created!', `${fullName} has been saved to the backend database.`);
      setFormData({
        firstName: '',
        lastName: '',
        email: '',
        phone: '',
        location: '',
        currentRole: '',
        currentCompany: '',
        summary: '',
        skills: '',
        matchScore: 85,
      });
      setSelectedFile(null);
      onClose();
    } catch (err) {
      console.error('[ManualCandidateModal] Error saving candidate:', err);
      showError('Error Creating Candidate', 'Failed to save candidate to backend database.');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 sm:p-6 bg-slate-950/70 backdrop-blur-md animate-in fade-in duration-200">
      <div className="w-full max-w-3xl rounded-3xl bg-white dark:bg-slate-900 border border-slate-200/80 dark:border-slate-800/80 p-7 text-left relative space-y-6 shadow-2xl max-h-[90vh] overflow-y-auto">
        <button
          onClick={onClose}
          className="absolute top-6 right-6 p-2 rounded-xl bg-slate-100 dark:bg-slate-800 text-slate-400 hover:text-slate-900 dark:hover:text-white transition"
        >
          <X className="w-4 h-4" />
        </button>

        {/* Modal Header */}
        <div className="space-y-1.5 pr-8">
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 text-xs font-mono font-medium">
            <UserPlus className="w-3.5 h-3.5 text-slate-500 dark:text-slate-400" /> Manual Candidate Entry
          </div>
          <h3 className="text-xl font-semibold text-slate-900 dark:text-white tracking-tight">Add New Candidate Profile</h3>
          <p className="text-xs text-slate-500 dark:text-slate-400 font-normal leading-relaxed">
            Directly insert structured candidate credentials into TalentSphere DB without running resume OCR.
          </p>
        </div>

        {/* Form Body */}
        <form onSubmit={handleSubmit} className="space-y-6 text-xs">
          {/* Personal Information Section */}
          <div className="space-y-3">
            <h4 className="text-[11px] font-mono uppercase tracking-wider text-slate-500 dark:text-slate-400 font-semibold flex items-center gap-2 pb-1.5 border-b border-slate-100 dark:border-slate-800/80">
              <Mail className="w-3.5 h-3.5 text-slate-400" /> 1. Personal &amp; Contact Details
            </h4>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="text-xs font-medium text-slate-700 dark:text-slate-300 block mb-1.5">
                  First Name <span className="text-rose-500 font-bold">*</span>
                </label>
                <input
                  type="text"
                  required
                  placeholder="e.g. Rahul"
                  value={formData.firstName}
                  onChange={(e) => setFormData({ ...formData, firstName: e.target.value })}
                  className="w-full px-3.5 py-2.5 rounded-xl bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 text-xs text-slate-900 dark:text-white font-normal placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-slate-900/20 dark:focus:ring-white/20 focus:border-slate-400 dark:focus:border-slate-600 transition-all"
                />
              </div>

              <div>
                <label className="text-xs font-medium text-slate-700 dark:text-slate-300 block mb-1.5">Last Name</label>
                <input
                  type="text"
                  placeholder="e.g. Pote"
                  value={formData.lastName}
                  onChange={(e) => setFormData({ ...formData, lastName: e.target.value })}
                  className="w-full px-3.5 py-2.5 rounded-xl bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 text-xs text-slate-900 dark:text-white font-normal placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-slate-900/20 dark:focus:ring-white/20 focus:border-slate-400 dark:focus:border-slate-600 transition-all"
                />
              </div>

              <div>
                <label className="text-xs font-medium text-slate-700 dark:text-slate-300 block mb-1.5">
                  Email Address <span className="text-rose-500 font-bold">*</span>
                </label>
                <input
                  type="email"
                  required
                  placeholder="rahul.pote@example.com"
                  value={formData.email}
                  onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                  className="w-full px-3.5 py-2.5 rounded-xl bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 text-xs text-slate-900 dark:text-white font-normal placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-slate-900/20 dark:focus:ring-white/20 focus:border-slate-400 dark:focus:border-slate-600 transition-all"
                />
              </div>

              <div>
                <label className="text-xs font-medium text-slate-700 dark:text-slate-300 block mb-1.5">Phone Number</label>
                <input
                  type="text"
                  placeholder="+91 98765 43210"
                  value={formData.phone}
                  onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
                  className="w-full px-3.5 py-2.5 rounded-xl bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 text-xs text-slate-900 dark:text-white font-normal placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-slate-900/20 dark:focus:ring-white/20 focus:border-slate-400 dark:focus:border-slate-600 transition-all"
                />
              </div>

              <div className="md:col-span-2">
                <label className="text-xs font-medium text-slate-700 dark:text-slate-300 block mb-1.5">Current Location</label>
                <input
                  type="text"
                  placeholder="Mumbai, Maharashtra, India"
                  value={formData.location}
                  onChange={(e) => setFormData({ ...formData, location: e.target.value })}
                  className="w-full px-3.5 py-2.5 rounded-xl bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 text-xs text-slate-900 dark:text-white font-normal placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-slate-900/20 dark:focus:ring-white/20 focus:border-slate-400 dark:focus:border-slate-600 transition-all"
                />
              </div>
            </div>
          </div>

          {/* Professional Experience Section */}
          <div className="space-y-3 pt-2">
            <h4 className="text-[11px] font-mono uppercase tracking-wider text-slate-500 dark:text-slate-400 font-semibold flex items-center gap-2 pb-1.5 border-b border-slate-100 dark:border-slate-800/80">
              <Briefcase className="w-3.5 h-3.5 text-slate-400" /> 2. Professional Background
            </h4>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="text-xs font-medium text-slate-700 dark:text-slate-300 block mb-1.5">Current Role / Designation</label>
                <input
                  type="text"
                  placeholder="Senior Software Developer"
                  value={formData.currentRole}
                  onChange={(e) => setFormData({ ...formData, currentRole: e.target.value })}
                  className="w-full px-3.5 py-2.5 rounded-xl bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 text-xs text-slate-900 dark:text-white font-normal placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-slate-900/20 dark:focus:ring-white/20 focus:border-slate-400 dark:focus:border-slate-600 transition-all"
                />
              </div>

              <div>
                <label className="text-xs font-medium text-slate-700 dark:text-slate-300 block mb-1.5">Current Company / Employer</label>
                <input
                  type="text"
                  placeholder="Zenith Cloud Technologies"
                  value={formData.currentCompany}
                  onChange={(e) => setFormData({ ...formData, currentCompany: e.target.value })}
                  className="w-full px-3.5 py-2.5 rounded-xl bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 text-xs text-slate-900 dark:text-white font-normal placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-slate-900/20 dark:focus:ring-white/20 focus:border-slate-400 dark:focus:border-slate-600 transition-all"
                />
              </div>

              <div className="md:col-span-2">
                <label className="text-xs font-medium text-slate-700 dark:text-slate-300 block mb-1.5">Executive Summary</label>
                <textarea
                  rows={3}
                  placeholder="Results-driven Senior Software Developer with 9+ years experience building distributed systems..."
                  value={formData.summary}
                  onChange={(e) => setFormData({ ...formData, summary: e.target.value })}
                  className="w-full px-3.5 py-2.5 rounded-xl bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 text-xs text-slate-900 dark:text-white font-normal placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-slate-900/20 dark:focus:ring-white/20 focus:border-slate-400 dark:focus:border-slate-600 transition-all leading-relaxed"
                />
              </div>
            </div>
          </div>

          {/* Technical Skills Section */}
          <div className="space-y-3 pt-2">
            <h4 className="text-[11px] font-mono uppercase tracking-wider text-slate-500 dark:text-slate-400 font-semibold flex items-center gap-2 pb-1.5 border-b border-slate-100 dark:border-slate-800/80">
              <Award className="w-3.5 h-3.5 text-slate-400" /> 3. Core Skills &amp; Competencies
            </h4>
            <div>
              <label className="text-xs font-medium text-slate-700 dark:text-slate-300 block mb-1.5">Core Technical Skills (comma-separated)</label>
              <input
                type="text"
                placeholder="Python, Java, React, FastAPI, Docker, PostgreSQL"
                value={formData.skills}
                onChange={(e) => setFormData({ ...formData, skills: e.target.value })}
                className="w-full px-3.5 py-2.5 rounded-xl bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 text-xs text-slate-900 dark:text-white font-normal placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-slate-900/20 dark:focus:ring-white/20 focus:border-slate-400 dark:focus:border-slate-600 transition-all"
              />
            </div>
          </div>

          {/* Resume Attachment Section */}
          <div className="space-y-3 pt-2">
            <h4 className="text-[11px] font-mono uppercase tracking-wider text-slate-500 dark:text-slate-400 font-semibold flex items-center gap-2 pb-1.5 border-b border-slate-100 dark:border-slate-800/80">
              <FileText className="w-3.5 h-3.5 text-slate-400" /> 4. Resume File Attachment (Optional)
            </h4>
            <div className="flex items-center gap-3 p-3.5 rounded-2xl bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800">
              <input
                type="file"
                id="manual-resume-file"
                className="hidden"
                accept=".pdf,.doc,.docx"
                onChange={handleFileChange}
              />
              <label
                htmlFor="manual-resume-file"
                className="px-4 py-2 rounded-xl bg-slate-200 dark:bg-slate-800 text-slate-700 dark:text-slate-300 hover:bg-slate-300 dark:hover:bg-slate-700 transition cursor-pointer text-xs font-medium flex items-center gap-2"
              >
                <Upload className="w-3.5 h-3.5" /> {selectedFile ? 'Change File' : 'Select Resume File'}
              </label>
              <span className="text-xs text-slate-500 dark:text-slate-400 truncate max-w-xs font-mono">
                {selectedFile ? selectedFile.name : 'No file attached'}
              </span>
            </div>
          </div>

          {/* Form Actions Footer */}
          <div className="flex items-center justify-end gap-3 pt-5 border-t border-slate-200 dark:border-slate-800">
            <button
              type="button"
              onClick={onClose}
              className="px-5 py-2.5 rounded-xl bg-slate-100 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-slate-700 dark:text-slate-300 text-xs font-medium hover:bg-slate-200 dark:hover:bg-slate-700 transition"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={isSubmitting}
              className="px-6 py-2.5 rounded-xl bg-slate-900 dark:bg-white text-white dark:text-slate-900 text-xs font-semibold flex items-center gap-2 shadow-md hover:bg-slate-800 dark:hover:bg-slate-100 transition disabled:opacity-50"
            >
              <UserCheck className="w-4 h-4" /> {isSubmitting ? 'Saving...' : 'Save Candidate Profile'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};
