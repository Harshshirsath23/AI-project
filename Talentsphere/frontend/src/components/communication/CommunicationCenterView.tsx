import React, { useState, useEffect } from 'react';
import {
  Mail,
  Send,
  Sparkles,
  FileText,
  Bell,
  Radio,
  Paperclip,
  Calendar,
  Search,
  Plus
} from 'lucide-react';
import { CommMessage, CommTemplate, NotificationItem, WebhookLog } from '../../types';
import { commsApi } from '../../api';

export const CommunicationCenterView: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'inbox' | 'templates' | 'notifications' | 'webhooks'>('inbox');
  const [messages, setMessages] = useState<CommMessage[]>([]);
  const [templates, setTemplates] = useState<CommTemplate[]>([]);
  const [notifications, setNotifications] = useState<NotificationItem[]>([]);
  const [webhookLogs, setWebhookLogs] = useState<WebhookLog[]>([]);
  const [loading, setLoading] = useState(true);

  // Conversation inbox state
  const [selectedCandidateId, setSelectedCandidateId] = useState<string>('cand-1');
  const [composerText, setComposerText] = useState('');
  const [selectedChannel, setSelectedChannel] = useState<'Email' | 'SMS' | 'WhatsApp'>('Email');

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    setLoading(true);
    try {
      const [msgData, tmplData, notifData, whData] = await Promise.all([
        commsApi.getMessages(),
        commsApi.getTemplates(),
        commsApi.getNotifications(),
        commsApi.getWebhookLogs()
      ]);
      setMessages(msgData);
      setTemplates(tmplData);
      setNotifications(notifData);
      setWebhookLogs(whData);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!composerText.trim()) return;
    const activeMsg = messages.find((m) => m.candidateId === selectedCandidateId) || messages[0];
    const created = await commsApi.sendMessage({
      candidateId: selectedCandidateId,
      candidateName: activeMsg?.candidateName || 'Alex Mercer',
      channel: selectedChannel,
      body: composerText,
      subject: selectedChannel === 'Email' ? 'Follow up regarding your recruitment pipeline' : undefined
    });
    setMessages([created, ...messages]);
    setComposerText('');
  };

  const activeThread = messages.filter((m) => m.candidateId === selectedCandidateId);
  const activeCandidate = messages.find((m) => m.candidateId === selectedCandidateId);

  return (
    <div className="space-y-6 text-left animate-fade-in">
      {/* Header Banner */}
      <div className="p-6 rounded-2xl glass-panel flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-zinc-800 dark:bg-zinc-800 light:bg-zinc-100 border border-zinc-700 dark:border-zinc-700 light:border-zinc-300 text-zinc-300 dark:text-zinc-300 light:text-zinc-700 text-xs font-mono font-medium mb-2">
            <Radio className="w-3.5 h-3.5" /> Milestone 9: Communication Engine
          </div>
          <h1 className="text-xl font-medium dark:text-white light:text-zinc-900 tracking-tight">Enterprise Communication &amp; Inbox</h1>
          <p className="text-xs dark:text-zinc-400 light:text-zinc-600 mt-1 font-normal">
            Omnichannel outreach via Email, SMS, &amp; WhatsApp with AI draft synthesis, template variables, and webhook delivery monitoring.
          </p>
        </div>

        <div className="flex items-center gap-3 shrink-0">
          <span className="px-3 py-1.5 rounded-xl glass-panel text-xs font-mono text-emerald-600 dark:text-emerald-400 font-medium flex items-center gap-1.5">
            <span className="w-2 h-2 rounded-full bg-emerald-400" /> Providers Operational
          </span>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="flex items-center gap-2 border-b border-zinc-200 dark:border-zinc-800 pb-2">
        <button
          onClick={() => setActiveTab('inbox')}
          className={`px-4 py-2 rounded-xl text-xs font-medium transition flex items-center gap-2 ${activeTab === 'inbox'
              ? 'bg-zinc-900 dark:bg-zinc-900 light:bg-zinc-100 text-white dark:text-white light:text-zinc-900 border border-zinc-800 dark:border-zinc-800 light:border-zinc-300'
              : 'text-zinc-400 hover:text-zinc-900 dark:hover:text-white'
            }`}
        >
          <Mail className="w-4 h-4" /> Conversation Inbox
        </button>
        <button
          onClick={() => setActiveTab('templates')}
          className={`px-4 py-2 rounded-xl text-xs font-medium transition flex items-center gap-2 ${activeTab === 'templates'
              ? 'bg-zinc-900 dark:bg-zinc-900 light:bg-zinc-100 text-white dark:text-white light:text-zinc-900 border border-zinc-800 dark:border-zinc-800 light:border-zinc-300'
              : 'text-zinc-400 hover:text-zinc-900 dark:hover:text-white'
            }`}
        >
          <FileText className="w-4 h-4" /> Templates Manager
        </button>
        <button
          onClick={() => setActiveTab('notifications')}
          className={`px-4 py-2 rounded-xl text-xs font-medium transition flex items-center gap-2 ${activeTab === 'notifications'
              ? 'bg-zinc-900 dark:bg-zinc-900 light:bg-zinc-100 text-white dark:text-white light:text-zinc-900 border border-zinc-800 dark:border-zinc-800 light:border-zinc-300'
              : 'text-zinc-400 hover:text-zinc-900 dark:hover:text-white'
            }`}
        >
          <Bell className="w-4 h-4" /> Notifications Center
        </button>
        <button
          onClick={() => setActiveTab('webhooks')}
          className={`px-4 py-2 rounded-xl text-xs font-medium transition flex items-center gap-2 ${activeTab === 'webhooks'
              ? 'bg-zinc-900 dark:bg-zinc-900 light:bg-zinc-100 text-white dark:text-white light:text-zinc-900 border border-zinc-800 dark:border-zinc-800 light:border-zinc-300'
              : 'text-zinc-400 hover:text-zinc-900 dark:hover:text-white'
            }`}
        >
          <Radio className="w-4 h-4" /> Webhook &amp; Provider Logs
        </button>
      </div>

      {/* TAB 1: CONVERSATION INBOX */}
      {activeTab === 'inbox' && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 glass-card rounded-2xl overflow-hidden min-h-[550px]">
          {/* Candidates List Pane */}
          <div className="border-r border-zinc-200 dark:border-zinc-800 p-4 space-y-3">
            <div className="relative">
              <Search className="w-3.5 h-3.5 text-zinc-500 absolute left-3 top-2.5" />
              <input
                type="text"
                placeholder="Search candidate threads..."
                className="w-full pl-8 pr-3 py-1.5 rounded-xl dark:bg-black/80 light:bg-zinc-50 border border-zinc-300 dark:border-zinc-700 text-xs dark:text-white light:text-zinc-900 placeholder-zinc-500 focus:outline-none"
              />
            </div>

            <div className="space-y-1">
              {Array.from(new Set(messages.map((m) => m.candidateId))).map((candId) => {
                const sampleMsg = messages.find((m) => m.candidateId === candId)!;
                const isSelected = selectedCandidateId === candId;

                return (
                  <button
                    key={candId}
                    onClick={() => setSelectedCandidateId(candId)}
                    className={`w-full p-3 rounded-xl text-left transition flex items-center gap-3 ${isSelected
                        ? 'bg-zinc-100 dark:bg-zinc-900 border border-zinc-300 dark:border-zinc-700 text-zinc-900 dark:text-white font-medium'
                        : 'hover:bg-zinc-50 dark:hover:bg-zinc-900/50 text-zinc-600 dark:text-zinc-400'
                      }`}
                  >
                    <img src={sampleMsg.candidateAvatar} alt={sampleMsg.candidateName} className="w-9 h-9 rounded-xl object-cover border border-zinc-300 dark:border-zinc-800" />
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center justify-between">
                        <span className="text-xs font-medium dark:text-white light:text-zinc-900 truncate">{sampleMsg.candidateName}</span>
                        <span className="text-[10px] font-mono dark:text-zinc-500 light:text-zinc-400">{sampleMsg.timestamp}</span>
                      </div>
                      <p className="text-[11px] dark:text-zinc-400 light:text-zinc-600 truncate mt-0.5">{sampleMsg.body}</p>
                    </div>
                  </button>
                );
              })}
            </div>
          </div>

          {/* Conversation Thread & Composer */}
          <div className="md:col-span-2 flex flex-col justify-between p-5 space-y-4">
            {/* Thread Header */}
            <div className="flex items-center justify-between border-b border-zinc-200 dark:border-zinc-800 pb-3">
              <div className="flex items-center gap-3">
                <img src={activeCandidate?.candidateAvatar} alt="Cand" className="w-9 h-9 rounded-xl object-cover border border-zinc-300 dark:border-zinc-800" />
                <div>
                  <h3 className="text-xs font-medium dark:text-white light:text-zinc-900">{activeCandidate?.candidateName}</h3>
                  <span className="text-[10px] dark:text-zinc-400 light:text-zinc-600 font-mono">Channel: {selectedChannel}</span>
                </div>
              </div>

              <div className="flex items-center gap-2">
                {(['Email', 'SMS', 'WhatsApp'] as const).map((ch) => (
                  <button
                    key={ch}
                    onClick={() => setSelectedChannel(ch)}
                    className={`px-2.5 py-1 rounded-lg text-[10px] font-mono font-medium border transition ${selectedChannel === ch ? 'bg-zinc-900 dark:bg-zinc-900 light:bg-zinc-900 text-white border-zinc-700' : 'glass-panel text-zinc-600 dark:text-zinc-400'
                      }`}
                  >
                    {ch}
                  </button>
                ))}
              </div>
            </div>

            {/* Messages Thread Window */}
            <div className="flex-1 space-y-3 overflow-y-auto max-h-[350px] p-2 custom-scrollbar">
              {activeThread.map((msg) => (
                <div
                  key={msg.id}
                  className={`flex flex-col ${msg.direction === 'outbound' ? 'items-end' : 'items-start'}`}
                >
                  <div
                    className={`p-3.5 rounded-2xl max-w-md text-xs space-y-1 ${msg.direction === 'outbound'
                        ? 'bg-zinc-900 dark:bg-zinc-900 light:bg-zinc-900 text-white border border-zinc-800 dark:border-zinc-800 light:border-zinc-700 rounded-br-none shadow-sm'
                        : 'glass-panel dark:text-zinc-200 light:text-zinc-800 rounded-bl-none'
                      }`}
                  >
                    {msg.subject && <span className="font-medium text-white light:text-white block mb-1 font-mono">{msg.subject}</span>}
                    <p className="leading-relaxed font-normal">{msg.body}</p>
                    <div className="flex items-center justify-between text-[9px] font-mono opacity-70 pt-1">
                      <span>{msg.timestamp}</span>
                      <span>{msg.status}</span>
                    </div>
                  </div>
                </div>
              ))}
            </div>

            {/* Composer */}
            <form onSubmit={handleSendMessage} className="space-y-2 pt-2 border-t border-zinc-200 dark:border-zinc-800">
              <div className="relative">
                <textarea
                  rows={3}
                  placeholder={`Write your ${selectedChannel} message...`}
                  value={composerText}
                  onChange={(e) => setComposerText(e.target.value)}
                  className="w-full p-3 rounded-xl dark:bg-black/80 light:bg-white border border-zinc-300 dark:border-zinc-700 text-xs dark:text-white light:text-zinc-900 placeholder-zinc-500 focus:outline-none"
                />
                <button
                  type="button"
                  onClick={() => setComposerText("Hi Alex, we'd like to confirm your final executive interview panel on Tuesday at 10 AM PST. Please confirm if this time works!")}
                  className="absolute right-3 bottom-3 px-2 py-1 rounded bg-zinc-800 dark:bg-zinc-800 light:bg-zinc-100 text-zinc-300 dark:text-zinc-300 light:text-zinc-700 text-[10px] font-mono font-medium flex items-center gap-1 border border-zinc-700 dark:border-zinc-700 light:border-zinc-300"
                >
                  <Sparkles className="w-3 h-3 text-zinc-400" /> AI Draft Assistant
                </button>
              </div>

              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2 dark:text-zinc-400 light:text-zinc-600">
                  <button type="button" className="p-1.5 rounded-lg hover:bg-zinc-100 dark:hover:bg-zinc-900"><Paperclip className="w-4 h-4" /></button>
                  <button type="button" className="p-1.5 rounded-lg hover:bg-zinc-100 dark:hover:bg-zinc-900"><Calendar className="w-4 h-4" /></button>
                </div>
                <button
                  type="submit"
                  className="px-4 py-2 rounded-xl bg-zinc-900 dark:bg-zinc-900 light:bg-zinc-900 text-white text-xs font-medium transition flex items-center gap-1.5 hover:bg-zinc-800"
                >
                  <Send className="w-3.5 h-3.5" /> Dispatch Message
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* TAB 2: TEMPLATES MANAGER */}
      {activeTab === 'templates' && (
        <div className="p-6 rounded-2xl glass-card space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-sm font-medium dark:text-white light:text-zinc-900 flex items-center gap-2">
              <FileText className="w-4 h-4" /> Communication Template Library
            </h3>
            <button className="px-3 py-1.5 rounded-xl bg-zinc-900 text-white text-xs font-medium flex items-center gap-1">
              <Plus className="w-3.5 h-3.5" /> New Template
            </button>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {templates.map((tmpl) => (
              <div key={tmpl.id} className="p-4 rounded-xl glass-panel space-y-3">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-medium dark:text-white light:text-zinc-900">{tmpl.name}</span>
                  <span className="px-2 py-0.5 rounded bg-zinc-100 dark:bg-zinc-900 text-zinc-700 dark:text-zinc-300 border border-zinc-200 dark:border-zinc-800 text-[10px] font-mono">
                    {tmpl.channel} • {tmpl.version}
                  </span>
                </div>

                {tmpl.subject && <p className="text-xs dark:text-zinc-300 light:text-zinc-700 font-mono">Subject: {tmpl.subject}</p>}
                <div className="p-3 rounded-lg glass-panel text-xs font-mono dark:text-zinc-400 light:text-zinc-600 whitespace-pre-wrap">
                  {tmpl.body}
                </div>

                <div className="flex flex-wrap items-center gap-1.5 pt-1">
                  <span className="text-[10px] font-mono dark:text-zinc-500 light:text-zinc-400 uppercase">Variables:</span>
                  {tmpl.variables.map((v, idx) => (
                    <span key={idx} className="px-2 py-0.5 rounded bg-zinc-100 dark:bg-zinc-800 text-zinc-700 dark:text-zinc-300 text-[10px] font-mono">
                      {`{{${v}}}`}
                    </span>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* TAB 3: NOTIFICATIONS CENTER */}
      {activeTab === 'notifications' && (
        <div className="p-6 rounded-2xl glass-card space-y-4">
          <h3 className="text-sm font-medium dark:text-white light:text-zinc-900 flex items-center gap-2">
            <Bell className="w-4 h-4" /> Enterprise Notification Center
          </h3>

          <div className="space-y-2">
            {notifications.map((notif) => (
              <div key={notif.id} className="p-3.5 rounded-xl glass-panel flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <span className={`w-2 h-2 rounded-full ${notif.read ? 'bg-zinc-400' : 'bg-emerald-400'}`} />
                  <div>
                    <span className="text-xs font-medium dark:text-white light:text-zinc-900 block">{notif.title}</span>
                    <p className="text-xs dark:text-zinc-400 light:text-zinc-600">{notif.message}</p>
                  </div>
                </div>
                <div className="text-right">
                  <span className="text-[10px] font-mono dark:text-zinc-500 light:text-zinc-400 block">{notif.timestamp}</span>
                  <span className="text-[10px] font-mono dark:text-zinc-300 light:text-zinc-700 font-medium">{notif.priority} Priority</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* TAB 4: WEBHOOK LOGS */}
      {activeTab === 'webhooks' && (
        <div className="p-6 rounded-2xl glass-card space-y-4">
          <h3 className="text-sm font-medium dark:text-white light:text-zinc-900 flex items-center gap-2">
            <Radio className="w-4 h-4" /> Webhook &amp; Provider Monitoring
          </h3>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs border-collapse">
              <thead>
                <tr className="border-b border-zinc-200 dark:border-zinc-800 dark:text-zinc-400 light:text-zinc-600 font-mono uppercase text-[10px]">
                  <th className="py-3 px-4 font-medium">Provider</th>
                  <th className="py-3 px-4 font-medium">Endpoint</th>
                  <th className="py-3 px-4 font-medium">Payload Summary</th>
                  <th className="py-3 px-4 font-medium">Message ID</th>
                  <th className="py-3 px-4 font-medium">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-zinc-200 dark:divide-zinc-800">
                {webhookLogs.map((wh) => (
                  <tr key={wh.id} className="hover:bg-zinc-50 dark:hover:bg-zinc-900/50 transition">
                    <td className="py-3 px-4 font-medium dark:text-white light:text-zinc-900">{wh.provider}</td>
                    <td className="py-3 px-4 font-mono dark:text-zinc-400 light:text-zinc-600 text-[11px]">{wh.endpoint}</td>
                    <td className="py-3 px-4 dark:text-zinc-300 light:text-zinc-700">{wh.payloadSummary}</td>
                    <td className="py-3 px-4 font-mono dark:text-zinc-400 light:text-zinc-600">{wh.messageId}</td>
                    <td className="py-3 px-4">
                      <span className={`px-2 py-0.5 rounded text-[10px] font-mono font-medium ${wh.status === 'Success' ? 'bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border border-emerald-500/30' : 'bg-amber-500/10 text-amber-600 dark:text-amber-400 border border-amber-500/30'
                        }`}>
                        {wh.status}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
};
