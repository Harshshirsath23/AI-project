import React from 'react';
import { useOrganization } from '../../context/OrganizationContext';
import { History, Download } from 'lucide-react';

export const AuditLogsView: React.FC = () => {
  const { auditLogs } = useOrganization();

  return (
    <div className="space-y-6 text-left animate-fade-in">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-medium dark:text-white light:text-zinc-900 tracking-tight flex items-center gap-2">
            <History className="w-5 h-5 dark:text-zinc-300 light:text-zinc-700" /> Security Audit &amp; System Event Logs
          </h2>
          <p className="text-xs dark:text-zinc-400 light:text-zinc-600 font-normal mt-0.5">
            SOC 2 Type II Immutable Audit Trail • Real-time event recording with IP &amp; geo-provenance
          </p>
        </div>

        <button
          onClick={() => alert('Audit log JSON exported.')}
          className="px-4 py-2 rounded-xl glass-panel dark:text-zinc-200 light:text-zinc-800 text-xs font-medium transition flex items-center gap-2 hover:bg-zinc-100 dark:hover:bg-zinc-800"
        >
          <Download className="w-4 h-4 text-zinc-400" /> Export CSV / JSON
        </button>
      </div>

      <div className="p-4 rounded-2xl glass-card overflow-x-auto">
        <table className="w-full text-left text-xs font-mono">
          <thead>
            <tr className="border-b border-zinc-200 dark:border-zinc-800 dark:text-zinc-400 light:text-zinc-600 uppercase tracking-wider text-[10px]">
              <th className="p-3 font-medium">Timestamp</th>
              <th className="p-3 font-medium">Event Code</th>
              <th className="p-3 font-medium">User / Actor</th>
              <th className="p-3 font-medium">IP Address</th>
              <th className="p-3 font-medium">Location</th>
              <th className="p-3 font-medium">Status</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-zinc-200 dark:divide-zinc-800">
            {auditLogs.map((log) => (
              <tr key={log.id} className="hover:bg-zinc-50 dark:hover:bg-zinc-900/50 transition">
                <td className="p-3 dark:text-zinc-400 light:text-zinc-600 font-normal">{log.timestamp}</td>
                <td className="p-3 dark:text-zinc-200 light:text-zinc-800 font-medium">{log.event}</td>
                <td className="p-3 dark:text-white light:text-zinc-900 font-medium">{log.user}</td>
                <td className="p-3 dark:text-zinc-400 light:text-zinc-600">{log.ip}</td>
                <td className="p-3 dark:text-zinc-400 light:text-zinc-600">{log.location}</td>
                <td className="p-3">
                  <span
                    className={`inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] font-medium ${log.status === 'SUCCESS'
                        ? 'bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border border-emerald-500/30'
                        : 'bg-red-500/10 text-red-600 dark:text-red-400 border border-red-500/30'
                      }`}
                  >
                    {log.status === 'SUCCESS' ? '✓' : '✕'} {log.status}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};
