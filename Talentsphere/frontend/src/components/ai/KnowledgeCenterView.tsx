import React, { useState, useEffect } from 'react';
import { Database, Upload, Eye } from 'lucide-react';
import { KnowledgeDoc } from '../../types';
import { aiIntelligenceApi } from '../../api';

export const KnowledgeCenterView: React.FC = () => {
  const [docs, setDocs] = useState<KnowledgeDoc[]>([]);
  const [selectedDoc, setSelectedDoc] = useState<KnowledgeDoc | null>(null);

  useEffect(() => {
    aiIntelligenceApi.getKnowledgeDocs().then(setDocs);
  }, []);

  return (
    <div className="space-y-6 text-left animate-fade-in">
      <div className="p-6 rounded-2xl glass-card flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-xl font-medium dark:text-white light:text-zinc-900 tracking-tight flex items-center gap-2">
            <Database className="w-5 h-5 dark:text-zinc-300 light:text-zinc-700" /> Enterprise Knowledge Base (RAG)
          </h1>
          <p className="text-xs dark:text-zinc-400 light:text-zinc-600 mt-1 font-normal">
            Indexed organizational policies, compensation benchmarks, and rubric vectors powering AI retrieval.
          </p>
        </div>

        <button className="px-4 py-2.5 rounded-xl bg-zinc-900 text-white text-xs font-medium transition flex items-center gap-2 shadow-sm shrink-0 hover:bg-zinc-800">
          <Upload className="w-4 h-4 text-zinc-300" /> Upload Knowledge Document
        </button>
      </div>

      <div className="p-6 rounded-2xl glass-card space-y-4">
        <div className="overflow-x-auto custom-scrollbar">
          <table className="w-full text-left text-xs border-collapse">
            <thead>
              <tr className="border-b border-zinc-200 dark:border-zinc-800 dark:text-zinc-400 light:text-zinc-600 font-mono uppercase text-[10px]">
                <th className="py-3 px-4 font-medium">Document Title</th>
                <th className="py-3 px-4 font-medium">Category</th>
                <th className="py-3 px-4 font-medium">Vector Chunks</th>
                <th className="py-3 px-4 font-medium">Embedding Model</th>
                <th className="py-3 px-4 font-medium">Status</th>
                <th className="py-3 px-4 text-right font-medium">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-zinc-200 dark:divide-zinc-800">
              {docs.map((doc) => (
                <tr key={doc.id} className="hover:bg-zinc-50 dark:hover:bg-zinc-900/50 transition">
                  <td className="py-3 px-4">
                    <span className="font-medium dark:text-white light:text-zinc-900 block">{doc.title}</span>
                    <span className="text-[10px] dark:text-zinc-500 light:text-zinc-400 font-mono">{doc.size} • Uploaded {doc.uploadDate}</span>
                  </td>
                  <td className="py-3 px-4 dark:text-zinc-300 light:text-zinc-700 font-normal">{doc.category}</td>
                  <td className="py-3 px-4 font-mono font-medium dark:text-zinc-200 light:text-zinc-800">{doc.chunksCount} Chunks</td>
                  <td className="py-3 px-4 font-mono dark:text-zinc-400 light:text-zinc-600">{doc.embeddingModel}</td>
                  <td className="py-3 px-4">
                    <span className="px-2.5 py-1 rounded-lg text-[10px] font-mono font-medium bg-emerald-500/10 border border-emerald-500/30 text-emerald-600 dark:text-emerald-400">
                      {doc.status}
                    </span>
                  </td>
                  <td className="py-3 px-4 text-right">
                    <button
                      onClick={() => setSelectedDoc(doc)}
                      className="px-3 py-1.5 rounded-lg glass-panel dark:text-zinc-200 light:text-zinc-800 font-medium transition inline-flex items-center gap-1 hover:bg-zinc-100 dark:hover:bg-zinc-800"
                    >
                      <Eye className="w-3.5 h-3.5 text-zinc-400" /> View Chunks
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {selectedDoc && (
        <div className="fixed inset-0 bg-black/70 backdrop-blur-md z-50 flex items-center justify-center p-4">
          <div className="glass-card rounded-2xl w-full max-w-xl overflow-hidden shadow-2xl">
            <div className="p-5 border-b border-zinc-200 dark:border-zinc-800 flex items-center justify-between glass-panel">
              <h3 className="text-sm font-medium dark:text-white light:text-zinc-900">{selectedDoc.title}</h3>
              <button onClick={() => setSelectedDoc(null)} className="dark:text-zinc-400 light:text-zinc-600 hover:text-zinc-900 dark:hover:text-white text-xs font-medium">
                Close
              </button>
            </div>
            <div className="p-6 space-y-3 font-mono text-xs text-zinc-300">
              <div className="p-3 rounded-xl glass-panel space-y-1">
                <span className="dark:text-zinc-400 light:text-zinc-600 text-[10px] uppercase font-medium block">Chunk #1 Vector ID: 88102-a</span>
                <p className="dark:text-zinc-200 light:text-zinc-800">"Level 7 Staff Engineers in US Region are benchmarked at $200k - $240k Base Salary range with 15k RSU options over 4-year vesting schedule."</p>
              </div>
              <div className="p-3 rounded-xl glass-panel space-y-1">
                <span className="dark:text-zinc-400 light:text-zinc-600 text-[10px] uppercase font-medium block">Chunk #2 Vector ID: 88102-b</span>
                <p className="dark:text-zinc-200 light:text-zinc-800">"Exceptions exceeding 15% of upper band threshold require dual sign-off from Head of People and VP of Engineering."</p>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
