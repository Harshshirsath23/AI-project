import React, { useState, useEffect } from 'react';
import {
  FileCheck,
  Plus,
  Search,
  Eye,
  CheckCircle,
  Clock,
  UserCheck,
  ShieldCheck,
  ArrowUpRight,
  Sparkles
} from 'lucide-react';
import { Offer, BackgroundVerification, OnboardingPlan } from '../../types';
import { offersApi } from '../../api';

export const OffersDashboardView: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'offers' | 'negotiation' | 'bgv' | 'onboarding'>('offers');
  const [offers, setOffers] = useState<Offer[]>([]);
  const [bgvList, setBgvList] = useState<BackgroundVerification[]>([]);
  const [onboardingPlans, setOnboardingPlans] = useState<OnboardingPlan[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedOffer, setSelectedOffer] = useState<Offer | null>(null);
  const [showCreateModal, setShowCreateModal] = useState(false);

  // New Offer Form state
  const [newOffer, setNewOffer] = useState({
    candidateName: '',
    jobTitle: '',
    department: 'Engineering',
    baseSalary: 180000,
    bonus: 25000,
    equity: '10,000 ISO Options',
    location: 'San Francisco, CA (Hybrid)',
    joiningDate: '2026-09-01'
  });

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    setLoading(true);
    try {
      const [offData, bgvData, onbData] = await Promise.all([
        offersApi.getOffers(),
        offersApi.getBackgroundChecks(),
        offersApi.getOnboardingPlans()
      ]);
      setOffers(offData);
      setBgvList(bgvData);
      setOnboardingPlans(onbData);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateOffer = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newOffer.candidateName || !newOffer.jobTitle) return;
    const created = await offersApi.createOffer(newOffer);
    setOffers([created, ...offers]);
    setShowCreateModal(false);
    setNewOffer({
      candidateName: '',
      jobTitle: '',
      department: 'Engineering',
      baseSalary: 180000,
      bonus: 25000,
      equity: '10,000 ISO Options',
      location: 'San Francisco, CA (Hybrid)',
      joiningDate: '2026-09-01'
    });
  };

  const filteredOffers = offers.filter(
    (o) =>
      o.candidateName.toLowerCase().includes(searchQuery.toLowerCase()) ||
      o.jobTitle.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div className="space-y-6 text-left animate-fade-in">
      {/* Header Banner */}
      <div className="p-6 rounded-2xl glass-card flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full glass-panel dark:text-zinc-300 light:text-zinc-700 text-xs font-mono font-medium mb-2">
            <ShieldCheck className="w-3.5 h-3.5 text-zinc-400" /> Milestone 8: Hiring Lifecycle
          </div>
          <h1 className="text-xl font-medium dark:text-white light:text-zinc-900 tracking-tight">Offer, Negotiation &amp; Onboarding OS</h1>
          <p className="text-xs dark:text-zinc-400 light:text-zinc-600 mt-1 font-normal">
            Governance-first offer dispatch, multi-party approvals, background verification checks, and employee transition plans.
          </p>
        </div>

        <div className="flex items-center gap-3 shrink-0">
          <button
            onClick={() => setShowCreateModal(true)}
            className="px-4 py-2.5 rounded-xl bg-zinc-900 text-white text-xs font-medium transition flex items-center gap-2 shadow-sm hover:bg-zinc-800"
          >
            <Plus className="w-4 h-4" /> Create Offer Wizard
          </button>
        </div>
      </div>

      {/* KPI Stats Grid */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="p-4 rounded-xl glass-card space-y-1">
          <span className="text-[10px] font-mono dark:text-zinc-400 light:text-zinc-500 uppercase font-medium">Total Offers Issued</span>
          <p className="text-2xl font-medium dark:text-white light:text-zinc-900 font-mono">{offers.length}</p>
          <span className="text-[11px] text-emerald-600 dark:text-emerald-400 font-medium flex items-center gap-1">
            <ArrowUpRight className="w-3 h-3" /> 100% Tracked
          </span>
        </div>
        <div className="p-4 rounded-xl glass-card space-y-1">
          <span className="text-[10px] font-mono dark:text-zinc-400 light:text-zinc-500 uppercase font-medium">Pending Approvals</span>
          <p className="text-2xl font-medium dark:text-white light:text-zinc-900 font-mono">
            {offers.filter((o) => o.status === 'Pending Approval').length}
          </p>
          <span className="text-[11px] dark:text-zinc-400 light:text-zinc-600 font-normal">Action Needed</span>
        </div>
        <div className="p-4 rounded-xl glass-card space-y-1">
          <span className="text-[10px] font-mono dark:text-zinc-400 light:text-zinc-500 uppercase font-medium">Under Negotiation</span>
          <p className="text-2xl font-medium dark:text-white light:text-zinc-900 font-mono">
            {offers.filter((o) => o.status === 'Negotiating').length}
          </p>
          <span className="text-[11px] dark:text-zinc-400 light:text-zinc-600 font-normal">Active Terms Delta</span>
        </div>
        <div className="p-4 rounded-xl glass-card space-y-1">
          <span className="text-[10px] font-mono dark:text-zinc-400 light:text-zinc-500 uppercase font-medium">BGV Cleared</span>
          <p className="text-2xl font-medium text-emerald-600 dark:text-emerald-400 font-mono">
            {bgvList.filter((b) => b.status === 'Passed').length}
          </p>
          <span className="text-[11px] text-emerald-600 dark:text-emerald-400 font-medium">100% Compliance</span>
        </div>
      </div>

      {/* View Navigation Tabs */}
      <div className="flex items-center gap-2 border-b border-zinc-200 dark:border-zinc-800 pb-2">
        <button
          onClick={() => setActiveTab('offers')}
          className={`px-4 py-2 rounded-xl text-xs font-medium transition flex items-center gap-2 ${activeTab === 'offers'
              ? 'bg-zinc-900 dark:bg-zinc-900 light:bg-zinc-100 text-white dark:text-white light:text-zinc-900 border border-zinc-800 dark:border-zinc-800 light:border-zinc-300'
              : 'text-zinc-400 hover:text-zinc-900 dark:hover:text-white'
            }`}
        >
          <FileCheck className="w-4 h-4 text-zinc-400" /> Offers Directory
        </button>
        <button
          onClick={() => setActiveTab('negotiation')}
          className={`px-4 py-2 rounded-xl text-xs font-medium transition flex items-center gap-2 ${activeTab === 'negotiation'
              ? 'bg-zinc-900 dark:bg-zinc-900 light:bg-zinc-100 text-white dark:text-white light:text-zinc-900 border border-zinc-800 dark:border-zinc-800 light:border-zinc-300'
              : 'text-zinc-400 hover:text-zinc-900 dark:hover:text-white'
            }`}
        >
          <Sparkles className="w-4 h-4 text-zinc-400" /> Negotiation Workspace
        </button>
        <button
          onClick={() => setActiveTab('bgv')}
          className={`px-4 py-2 rounded-xl text-xs font-medium transition flex items-center gap-2 ${activeTab === 'bgv'
              ? 'bg-zinc-900 dark:bg-zinc-900 light:bg-zinc-100 text-white dark:text-white light:text-zinc-900 border border-zinc-800 dark:border-zinc-800 light:border-zinc-300'
              : 'text-zinc-400 hover:text-zinc-900 dark:hover:text-white'
            }`}
        >
          <ShieldCheck className="w-4 h-4 text-zinc-400" /> Background Checks (BGV)
        </button>
        <button
          onClick={() => setActiveTab('onboarding')}
          className={`px-4 py-2 rounded-xl text-xs font-medium transition flex items-center gap-2 ${activeTab === 'onboarding'
              ? 'bg-zinc-900 dark:bg-zinc-900 light:bg-zinc-100 text-white dark:text-white light:text-zinc-900 border border-zinc-800 dark:border-zinc-800 light:border-zinc-300'
              : 'text-zinc-400 hover:text-zinc-900 dark:hover:text-white'
            }`}
        >
          <UserCheck className="w-4 h-4 text-zinc-400" /> Onboarding &amp; Conversion
        </button>
      </div>

      {/* Tab Content 1: OFFERS DIRECTORY */}
      {activeTab === 'offers' && (
        <div className="p-6 rounded-2xl glass-card space-y-4">
          <div className="flex flex-col sm:flex-row items-center justify-between gap-3">
            <div className="relative w-full sm:w-72">
              <Search className="w-4 h-4 text-zinc-400 absolute left-3 top-2.5" />
              <input
                type="text"
                placeholder="Filter by candidate or job..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full pl-9 pr-4 py-2 rounded-xl dark:bg-black/80 light:bg-white border border-zinc-300 dark:border-zinc-700 text-xs dark:text-white light:text-zinc-900 placeholder-zinc-500 focus:outline-none"
              />
            </div>
            <div className="text-xs dark:text-zinc-400 light:text-zinc-600 font-mono">
              Showing <span className="dark:text-white light:text-zinc-900 font-medium">{filteredOffers.length}</span> recorded offer packages
            </div>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs border-collapse">
              <thead>
                <tr className="border-b border-zinc-200 dark:border-zinc-800 dark:text-zinc-400 light:text-zinc-600 font-mono uppercase text-[10px]">
                  <th className="py-3 px-4 font-medium">Candidate</th>
                  <th className="py-3 px-4 font-medium">Job Title &amp; Dept</th>
                  <th className="py-3 px-4 font-medium">Compensation</th>
                  <th className="py-3 px-4 font-medium">Status</th>
                  <th className="py-3 px-4 font-medium">Approval</th>
                  <th className="py-3 px-4 font-medium">Owner</th>
                  <th className="py-3 px-4 text-right font-medium">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-zinc-200 dark:divide-zinc-800">
                {filteredOffers.map((off) => (
                  <tr key={off.id} className="hover:bg-zinc-50 dark:hover:bg-zinc-900/50 transition">
                    <td className="py-3 px-4">
                      <div className="flex items-center gap-2.5">
                        <img src={off.candidateAvatar} alt={off.candidateName} className="w-8 h-8 rounded-lg object-cover border border-zinc-300 dark:border-zinc-800" />
                        <div>
                          <span className="font-medium dark:text-white light:text-zinc-900 block">{off.candidateName}</span>
                          <span className="text-[10px] dark:text-zinc-400 light:text-zinc-500 font-mono">{off.location}</span>
                        </div>
                      </div>
                    </td>
                    <td className="py-3 px-4">
                      <span className="dark:text-zinc-200 light:text-zinc-800 font-medium block">{off.jobTitle}</span>
                      <span className="text-[10px] dark:text-zinc-400 light:text-zinc-500">{off.department}</span>
                    </td>
                    <td className="py-3 px-4 font-mono">
                      <span className="text-emerald-600 dark:text-emerald-400 font-medium block">${off.baseSalary.toLocaleString()} {off.currency}</span>
                      <span className="text-[10px] dark:text-zinc-400 light:text-zinc-500">+ ${off.bonus.toLocaleString()} Bonus</span>
                    </td>
                    <td className="py-3 px-4">
                      <span className={`px-2.5 py-1 rounded-lg text-[10px] font-mono font-medium border ${off.status === 'Accepted'
                          ? 'bg-emerald-500/10 border-emerald-500/30 text-emerald-600 dark:text-emerald-400'
                          : 'glass-panel text-zinc-700 dark:text-zinc-300'
                        }`}>
                        {off.status}
                      </span>
                    </td>
                    <td className="py-3 px-4 font-mono">
                      <span className={`text-[11px] font-medium ${off.approvalStatus === 'Approved' ? 'text-emerald-600 dark:text-emerald-400' : 'dark:text-zinc-300 light:text-zinc-700'
                        }`}>
                        {off.approvalStatus}
                      </span>
                    </td>
                    <td className="py-3 px-4 dark:text-zinc-300 light:text-zinc-700 font-normal">{off.owner}</td>
                    <td className="py-3 px-4 text-right">
                      <button
                        onClick={() => setSelectedOffer(off)}
                        className="px-3 py-1.5 rounded-lg glass-panel dark:text-zinc-200 light:text-zinc-800 font-medium transition inline-flex items-center gap-1 hover:bg-zinc-100 dark:hover:bg-zinc-800"
                      >
                        <Eye className="w-3.5 h-3.5 text-zinc-400" /> Inspect Package
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Tab Content 2: NEGOTIATION WORKSPACE */}
      {activeTab === 'negotiation' && (
        <div className="p-6 rounded-2xl glass-card space-y-6">
          <div className="flex items-center justify-between border-b border-zinc-200 dark:border-zinc-800 pb-4">
            <div>
              <h3 className="text-sm font-medium dark:text-white light:text-zinc-900 flex items-center gap-2">
                <Sparkles className="w-4 h-4 text-zinc-400" /> Active Compensation Negotiation Delta
              </h3>
              <p className="text-xs dark:text-zinc-400 light:text-zinc-600 mt-0.5 font-normal">
                AI-assisted compensation band benchmarking &amp; counter-offer decision workspace.
              </p>
            </div>
            <span className="px-3 py-1 rounded-full glass-panel dark:text-zinc-300 light:text-zinc-700 text-xs font-mono">
              AI Recommends — Human Decides
            </span>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <div className="p-5 rounded-xl glass-panel space-y-4">
              <div className="flex items-center gap-3">
                <img src={offers[0]?.candidateAvatar} alt="Cand" className="w-10 h-10 rounded-xl object-cover border border-zinc-300 dark:border-zinc-800" />
                <div>
                  <h4 className="text-xs font-medium dark:text-white light:text-zinc-900">{offers[0]?.candidateName}</h4>
                  <p className="text-[11px] dark:text-zinc-400 light:text-zinc-500">{offers[0]?.jobTitle}</p>
                </div>
              </div>

              <div className="p-3 rounded-lg glass-panel space-y-2">
                <div className="flex justify-between text-xs">
                  <span className="dark:text-zinc-400 light:text-zinc-600">Current Base Offer:</span>
                  <span className="font-mono text-emerald-600 dark:text-emerald-400 font-medium">${offers[0]?.baseSalary.toLocaleString()}</span>
                </div>
                <div className="flex justify-between text-xs">
                  <span className="dark:text-zinc-400 light:text-zinc-600">Candidate Counter Request:</span>
                  <span className="font-mono dark:text-zinc-200 light:text-zinc-800 font-medium">$225,000</span>
                </div>
                <div className="flex justify-between text-xs pt-2 border-t border-zinc-200 dark:border-zinc-800">
                  <span className="dark:text-zinc-300 light:text-zinc-700 font-medium">Compensation Delta:</span>
                  <span className="font-mono text-red-600 dark:text-red-400 font-medium">+$10,000 (+4.6%)</span>
                </div>
              </div>

              <div className="p-3 rounded-lg glass-panel text-xs space-y-1">
                <span className="font-medium dark:text-zinc-200 light:text-zinc-800 block flex items-center gap-1">
                  <Sparkles className="w-3.5 h-3.5 text-zinc-400" /> AI Compensation Insight
                </span>
                <p className="text-[11px] leading-relaxed dark:text-zinc-300 light:text-zinc-700">
                  $225,000 sits within 75th percentile of Level 7 AI Engineers in SF. Granting counter request has a predicted 92% offer acceptance conversion rate.
                </p>
              </div>
            </div>

            <div className="lg:col-span-2 p-5 rounded-xl glass-panel space-y-4">
              <h4 className="text-xs font-medium dark:text-white light:text-zinc-900 uppercase tracking-wider font-mono">Negotiation Event Log</h4>
              <div className="space-y-3">
                <div className="p-3.5 rounded-xl glass-card flex items-start justify-between gap-4">
                  <div>
                    <span className="text-[10px] font-mono dark:text-zinc-300 light:text-zinc-700 font-medium uppercase">Candidate Request</span>
                    <p className="text-xs dark:text-zinc-300 light:text-zinc-700 mt-1 font-normal">
                      "Requested $10,000 increase in base salary or additional relocation stipend to cover SF housing adjustment."
                    </p>
                    <span className="text-[10px] dark:text-zinc-500 light:text-zinc-400 font-mono block mt-1">2026-08-09 10:00 PST</span>
                  </div>
                  <span className="px-2 py-1 rounded glass-panel text-[10px] font-mono dark:text-zinc-300 light:text-zinc-700">
                    Under Review
                  </span>
                </div>

                <div className="p-3.5 rounded-xl glass-card flex items-start justify-between gap-4">
                  <div>
                    <span className="text-[10px] font-mono dark:text-zinc-300 light:text-zinc-700 font-medium uppercase">Original Offer Dispatched</span>
                    <p className="text-xs dark:text-zinc-300 light:text-zinc-700 mt-1 font-normal">
                      $215,000 Base + $35,000 Sign-on Bonus + 15,000 ISO Options.
                    </p>
                    <span className="text-[10px] dark:text-zinc-500 light:text-zinc-400 font-mono block mt-1">2026-08-08 14:20 PST</span>
                  </div>
                  <span className="px-2 py-1 rounded glass-panel text-[10px] font-mono dark:text-zinc-300 light:text-zinc-700">
                    Initial Dispatch
                  </span>
                </div>
              </div>

              <div className="flex items-center gap-3 pt-3">
                <button className="px-4 py-2 rounded-xl bg-zinc-900 text-white text-xs font-medium transition hover:bg-zinc-800">
                  Approve Counter Terms ($225k)
                </button>
                <button className="px-4 py-2 rounded-xl glass-panel text-zinc-700 dark:text-zinc-300 text-xs font-medium transition hover:bg-zinc-100 dark:hover:bg-zinc-800">
                  Maintain Baseline ($215k)
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Tab Content 3: BACKGROUND VERIFICATION (BGV) */}
      {activeTab === 'bgv' && (
        <div className="p-6 rounded-2xl glass-card space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-sm font-medium dark:text-white light:text-zinc-900 flex items-center gap-2">
              <ShieldCheck className="w-4 h-4 text-emerald-600 dark:text-emerald-400" /> Background Verification &amp; Security Audits
            </h3>
            <span className="text-xs dark:text-zinc-400 light:text-zinc-600 font-mono">SOC 2 Type II Integrated Verification</span>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs border-collapse">
              <thead>
                <tr className="border-b border-zinc-200 dark:border-zinc-800 dark:text-zinc-400 light:text-zinc-600 font-mono uppercase text-[10px]">
                  <th className="py-3 px-4 font-medium">Candidate &amp; Role</th>
                  <th className="py-3 px-4 font-medium">Identity Check</th>
                  <th className="py-3 px-4 font-medium">Education Check</th>
                  <th className="py-3 px-4 font-medium">Employment Check</th>
                  <th className="py-3 px-4 font-medium">Criminal Check</th>
                  <th className="py-3 px-4 font-medium">Reference Check</th>
                  <th className="py-3 px-4 font-medium">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-zinc-200 dark:divide-zinc-800">
                {bgvList.map((bgv) => (
                  <tr key={bgv.id} className="hover:bg-zinc-50 dark:hover:bg-zinc-900/50 transition">
                    <td className="py-3 px-4">
                      <span className="font-medium dark:text-white light:text-zinc-900 block">{bgv.candidateName}</span>
                      <span className="text-[10px] dark:text-zinc-400 light:text-zinc-500">{bgv.jobTitle}</span>
                    </td>
                    <td className="py-3 px-4">
                      <span className="text-emerald-600 dark:text-emerald-400 font-medium inline-flex items-center gap-1">
                        <CheckCircle className="w-3.5 h-3.5" /> {bgv.identityCheck}
                      </span>
                    </td>
                    <td className="py-3 px-4">
                      <span className="text-emerald-600 dark:text-emerald-400 font-medium inline-flex items-center gap-1">
                        <CheckCircle className="w-3.5 h-3.5" /> {bgv.educationCheck}
                      </span>
                    </td>
                    <td className="py-3 px-4">
                      <span className={`font-medium inline-flex items-center gap-1 ${bgv.employmentCheck === 'Verified' ? 'text-emerald-600 dark:text-emerald-400' : 'dark:text-zinc-300 light:text-zinc-700'}`}>
                        {bgv.employmentCheck === 'Verified' ? <CheckCircle className="w-3.5 h-3.5" /> : <Clock className="w-3.5 h-3.5" />} {bgv.employmentCheck}
                      </span>
                    </td>
                    <td className="py-3 px-4">
                      <span className="text-emerald-600 dark:text-emerald-400 font-medium inline-flex items-center gap-1">
                        <CheckCircle className="w-3.5 h-3.5" /> {bgv.criminalCheck}
                      </span>
                    </td>
                    <td className="py-3 px-4">
                      <span className={`font-medium inline-flex items-center gap-1 ${bgv.referenceCheck === 'Verified' ? 'text-emerald-600 dark:text-emerald-400' : 'dark:text-zinc-300 light:text-zinc-700'}`}>
                        {bgv.referenceCheck === 'Verified' ? <CheckCircle className="w-3.5 h-3.5" /> : <Clock className="w-3.5 h-3.5" />} {bgv.referenceCheck}
                      </span>
                    </td>
                    <td className="py-3 px-4">
                      <span className={`px-2.5 py-1 rounded-lg text-[10px] font-mono font-medium border ${bgv.status === 'Passed' ? 'bg-emerald-500/10 border-emerald-500/30 text-emerald-600 dark:text-emerald-400' : 'glass-panel text-zinc-700 dark:text-zinc-300'
                        }`}>
                        {bgv.status}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Tab Content 4: ONBOARDING & CONVERSION */}
      {activeTab === 'onboarding' && (
        <div className="p-6 rounded-2xl glass-card space-y-6">
          <div className="flex items-center justify-between border-b border-zinc-200 dark:border-zinc-800 pb-4">
            <div>
              <h3 className="text-sm font-medium dark:text-white light:text-zinc-900 flex items-center gap-2">
                <UserCheck className="w-4 h-4 text-zinc-400" /> Active Employee Onboarding Plan
              </h3>
              <p className="text-xs dark:text-zinc-400 light:text-zinc-600 mt-0.5 font-normal">
                Automated HR document provisioning, hardware setup, compliance verification, and 30-day onboarding milestones.
              </p>
            </div>
            <span className="text-xs font-mono dark:text-zinc-300 light:text-zinc-700 font-medium">
              Conversion Status: Employee Transition Active
            </span>
          </div>

          {onboardingPlans.map((plan) => (
            <div key={plan.id} className="p-5 rounded-xl glass-panel space-y-4">
              <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div>
                  <h4 className="text-sm font-medium dark:text-white light:text-zinc-900">{plan.candidateName}</h4>
                  <p className="text-xs dark:text-zinc-400 light:text-zinc-500">{plan.jobTitle} • {plan.department} (Joining: {plan.joiningDate})</p>
                </div>
                <div className="flex items-center gap-3">
                  <div className="w-48 bg-zinc-200 dark:bg-zinc-800 rounded-full h-2.5 overflow-hidden">
                    <div className="bg-zinc-900 dark:bg-zinc-100 h-full rounded-full" style={{ width: `${plan.progressPercent}%` }} />
                  </div>
                  <span className="text-xs font-mono font-medium dark:text-zinc-200 light:text-zinc-800">{plan.progressPercent}% Complete</span>
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-3 pt-2">
                {plan.tasks.map((task) => (
                  <div key={task.id} className="p-3.5 rounded-xl glass-card flex items-center justify-between">
                    <div className="flex items-center gap-3">
                      <input
                        type="checkbox"
                        checked={task.completed}
                        readOnly
                        className="w-4 h-4 rounded bg-zinc-100 dark:bg-zinc-800 border-zinc-300 dark:border-zinc-700 text-zinc-900 focus:ring-0"
                      />
                      <div>
                        <span className={`text-xs block font-medium ${task.completed ? 'dark:text-zinc-500 light:text-zinc-400 line-through' : 'dark:text-white light:text-zinc-900'}`}>
                          {task.title}
                        </span>
                        <span className="text-[10px] dark:text-zinc-500 light:text-zinc-400 font-mono">{task.category} • Owner: {task.owner}</span>
                      </div>
                    </div>
                    <span className="text-[10px] dark:text-zinc-400 light:text-zinc-500 font-mono">{task.dueDate}</span>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      )}

      {/* INSPECT OFFER PACKAGE MODAL DRAWER */}
      {selectedOffer && (
        <div className="fixed inset-0 bg-black/70 backdrop-blur-md z-50 flex items-center justify-center p-4">
          <div className="glass-card rounded-2xl w-full max-w-2xl overflow-hidden shadow-2xl">
            <div className="p-5 border-b border-zinc-200 dark:border-zinc-800 flex items-center justify-between glass-panel">
              <div className="flex items-center gap-3">
                <img src={selectedOffer.candidateAvatar} alt="Cand" className="w-10 h-10 rounded-xl object-cover border border-zinc-300 dark:border-zinc-800" />
                <div>
                  <h3 className="text-sm font-medium dark:text-white light:text-zinc-900">{selectedOffer.candidateName}</h3>
                  <p className="text-xs dark:text-zinc-400 light:text-zinc-600">{selectedOffer.jobTitle}</p>
                </div>
              </div>
              <button onClick={() => setSelectedOffer(null)} className="dark:text-zinc-400 light:text-zinc-600 hover:text-zinc-900 dark:hover:text-white text-xs font-medium">
                Close
              </button>
            </div>

            <div className="p-6 space-y-5 max-h-[75vh] overflow-y-auto custom-scrollbar">
              <div className="grid grid-cols-2 gap-4">
                <div className="p-3.5 rounded-xl glass-panel">
                  <span className="text-[10px] font-mono dark:text-zinc-400 light:text-zinc-500 uppercase block">Base Salary</span>
                  <span className="text-lg font-mono font-medium text-emerald-600 dark:text-emerald-400">${selectedOffer.baseSalary.toLocaleString()} {selectedOffer.currency}</span>
                </div>
                <div className="p-3.5 rounded-xl glass-panel">
                  <span className="text-[10px] font-mono dark:text-zinc-400 light:text-zinc-500 uppercase block">Sign-On Bonus</span>
                  <span className="text-lg font-mono font-medium dark:text-zinc-200 light:text-zinc-800">${selectedOffer.bonus.toLocaleString()} {selectedOffer.currency}</span>
                </div>
              </div>

              <div className="p-4 rounded-xl glass-panel space-y-2">
                <span className="text-xs font-medium dark:text-white light:text-zinc-900 uppercase tracking-wider font-mono block">Equity Grant</span>
                <p className="text-xs font-mono dark:text-zinc-200 light:text-zinc-800">{selectedOffer.equity}</p>
              </div>

              <div className="space-y-2">
                <span className="text-xs font-medium dark:text-white light:text-zinc-900 uppercase tracking-wider font-mono block">Perks &amp; Benefits Included</span>
                <div className="flex flex-wrap gap-2">
                  {selectedOffer.benefits.map((b, idx) => (
                    <span key={idx} className="px-3 py-1 rounded-lg glass-panel dark:text-zinc-300 light:text-zinc-700 text-xs font-normal">
                      ✓ {b}
                    </span>
                  ))}
                </div>
              </div>

              <div className="space-y-2">
                <span className="text-xs font-medium dark:text-white light:text-zinc-900 uppercase tracking-wider font-mono block">Approval Timeline</span>
                <div className="space-y-2">
                  {selectedOffer.approvalHistory.map((app, idx) => (
                    <div key={idx} className="p-3 rounded-lg glass-panel flex items-center justify-between text-xs">
                      <div>
                        <span className="dark:text-white light:text-zinc-900 font-medium block">{app.approver} ({app.role})</span>
                        <span className="text-[10px] dark:text-zinc-400 light:text-zinc-500">{app.comments}</span>
                      </div>
                      <span className="font-mono text-emerald-600 dark:text-emerald-400 font-medium">{app.decision}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* CREATE OFFER WIZARD MODAL */}
      {showCreateModal && (
        <div className="fixed inset-0 bg-black/70 backdrop-blur-md z-50 flex items-center justify-center p-4">
          <div className="glass-card rounded-2xl w-full max-w-xl overflow-hidden shadow-2xl">
            <div className="p-5 border-b border-zinc-200 dark:border-zinc-800 flex items-center justify-between glass-panel">
              <h3 className="text-sm font-medium dark:text-white light:text-zinc-900 flex items-center gap-2">
                <Plus className="w-4 h-4 text-zinc-400" /> Offer Creation Wizard
              </h3>
              <button onClick={() => setShowCreateModal(false)} className="dark:text-zinc-400 light:text-zinc-600 hover:text-zinc-900 dark:hover:text-white text-xs font-medium">
                Cancel
              </button>
            </div>

            <form onSubmit={handleCreateOffer} className="p-6 space-y-4">
              <div>
                <label className="text-xs font-medium dark:text-zinc-300 light:text-zinc-700 block mb-1">Candidate Name</label>
                <input
                  type="text"
                  required
                  placeholder="e.g. Alex Mercer"
                  value={newOffer.candidateName}
                  onChange={(e) => setNewOffer({ ...newOffer, candidateName: e.target.value })}
                  className="w-full px-3 py-2 rounded-xl dark:bg-black/80 light:bg-white border border-zinc-300 dark:border-zinc-700 text-xs dark:text-white light:text-zinc-900 focus:outline-none"
                />
              </div>

              <div>
                <label className="text-xs font-medium dark:text-zinc-300 light:text-zinc-700 block mb-1">Target Job Title</label>
                <input
                  type="text"
                  required
                  placeholder="e.g. Principal AI Engineer"
                  value={newOffer.jobTitle}
                  onChange={(e) => setNewOffer({ ...newOffer, jobTitle: e.target.value })}
                  className="w-full px-3 py-2 rounded-xl dark:bg-black/80 light:bg-white border border-zinc-300 dark:border-zinc-700 text-xs dark:text-white light:text-zinc-900 focus:outline-none"
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="text-xs font-medium dark:text-zinc-300 light:text-zinc-700 block mb-1">Base Salary (USD)</label>
                  <input
                    type="number"
                    value={newOffer.baseSalary}
                    onChange={(e) => setNewOffer({ ...newOffer, baseSalary: Number(e.target.value) })}
                    className="w-full px-3 py-2 rounded-xl dark:bg-black/80 light:bg-white border border-zinc-300 dark:border-zinc-700 text-xs font-mono dark:text-white light:text-zinc-900 focus:outline-none"
                  />
                </div>
                <div>
                  <label className="text-xs font-medium dark:text-zinc-300 light:text-zinc-700 block mb-1">Sign-On Bonus (USD)</label>
                  <input
                    type="number"
                    value={newOffer.bonus}
                    onChange={(e) => setNewOffer({ ...newOffer, bonus: Number(e.target.value) })}
                    className="w-full px-3 py-2 rounded-xl dark:bg-black/80 light:bg-white border border-zinc-300 dark:border-zinc-700 text-xs font-mono dark:text-white light:text-zinc-900 focus:outline-none"
                  />
                </div>
              </div>

              <div>
                <label className="text-xs font-medium dark:text-zinc-300 light:text-zinc-700 block mb-1">Target Joining Date</label>
                <input
                  type="date"
                  value={newOffer.joiningDate}
                  onChange={(e) => setNewOffer({ ...newOffer, joiningDate: e.target.value })}
                  className="w-full px-3 py-2 rounded-xl dark:bg-black/80 light:bg-white border border-zinc-300 dark:border-zinc-700 text-xs dark:text-white light:text-zinc-900 focus:outline-none"
                />
              </div>

              <button
                type="submit"
                className="w-full py-2.5 rounded-xl bg-zinc-900 text-white text-xs font-medium transition mt-2 shadow-sm hover:bg-zinc-800"
              >
                Dispatch Offer for Executive Approval
              </button>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};
