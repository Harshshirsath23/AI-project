import React, { useState } from 'react';
import { Sparkles, Send, Bot, User, X, RefreshCw } from 'lucide-react';

interface QuickAIAssistantModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export const QuickAIAssistantModal: React.FC<QuickAIAssistantModalProps> = ({
  isOpen,
  onClose,
}) => {
  const [messages, setMessages] = useState<Array<{ sender: 'user' | 'ai'; text: string; time: string }>>([
    {
      sender: 'ai',
      text: 'Hello! I am your TalentSphere AI Copilot. How can I assist with candidate sourcing, pipeline analytics, or job descriptions today?',
      time: 'Just now',
    },
  ]);
  const [input, setInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);

  if (!isOpen) return null;

  const handleSend = (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userText = input;
    const now = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

    setMessages((prev) => [...prev, { sender: 'user', text: userText, time: now }]);
    setInput('');
    setIsTyping(true);

    setTimeout(() => {
      let reply = 'I have analyzed our active candidate repository. Dr. Sarah Lin has a 95% match index for Principal AI Researcher with validated CUDA and Transformer skills.';
      if (userText.toLowerCase().includes('job') || userText.toLowerCase().includes('draft')) {
        reply = 'I generated a draft job description for Senior AI Engineer. Shall I publish it to your Job Requisitions catalog?';
      } else if (userText.toLowerCase().includes('interview') || userText.toLowerCase().includes('score')) {
        reply = 'Technical scorecards for Alex Mercer show a calculated score of 8.8/10 with unanimous "Strong Hire" recommendations from engineering leads.';
      }

      setMessages((prev) => [...prev, { sender: 'ai', text: reply, time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) }]);
      setIsTyping(false);
    }, 1200);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-md animate-fade-in">
      <div className="w-full max-w-xl rounded-2xl glass-card p-6 text-left relative flex flex-col h-[520px] shadow-2xl">
        <button
          onClick={onClose}
          className="absolute top-5 right-5 p-2 rounded-xl glass-panel dark:text-zinc-400 light:text-zinc-600 hover:text-zinc-900 dark:hover:text-white transition"
        >
          <X className="w-4 h-4" />
        </button>

        {/* Modal Header */}
        <div className="flex items-center gap-2.5 pb-4 border-b border-zinc-200 dark:border-zinc-800">
          <div className="w-9 h-9 rounded-xl glass-panel flex items-center justify-center dark:text-white light:text-zinc-900">
            <Sparkles className="w-4 h-4" />
          </div>
          <div>
            <h3 className="text-base font-medium dark:text-white light:text-zinc-900">TalentSphere AI Copilot</h3>
            <p className="text-[11px] dark:text-zinc-400 light:text-zinc-600 font-normal">Multi-agent reasoning • Real-time database grounding</p>
          </div>
        </div>

        {/* Messages Body */}
        <div className="flex-1 overflow-y-auto p-3 space-y-3 custom-scrollbar my-2">
          {messages.map((m, idx) => (
            <div
              key={idx}
              className={`flex items-start gap-2.5 text-xs ${
                m.sender === 'user' ? 'flex-row-reverse' : ''
              }`}
            >
              <div
                className={`w-7 h-7 rounded-lg flex items-center justify-center shrink-0 ${
                  m.sender === 'user'
                    ? 'bg-zinc-900 text-white font-medium'
                    : 'glass-panel text-zinc-700 dark:text-zinc-300'
                }`}
              >
                {m.sender === 'user' ? <User className="w-3.5 h-3.5" /> : <Bot className="w-3.5 h-3.5" />}
              </div>
              <div
                className={`p-3 rounded-2xl max-w-[80%] ${
                  m.sender === 'user'
                    ? 'bg-zinc-900 text-white font-normal rounded-tr-none'
                    : 'glass-panel dark:text-zinc-200 light:text-zinc-800 rounded-tl-none font-normal'
                }`}
              >
                <p className="leading-relaxed">{m.text}</p>
                <span className="text-[9px] opacity-70 font-mono mt-1 block text-right">{m.time}</span>
              </div>
            </div>
          ))}

          {isTyping && (
            <div className="flex items-center gap-2 text-xs dark:text-zinc-400 light:text-zinc-600 font-mono">
              <RefreshCw className="w-3.5 h-3.5 animate-spin" /> TalentSphere Agent thinking...
            </div>
          )}
        </div>

        {/* Input Bar */}
        <form onSubmit={handleSend} className="pt-3 border-t border-zinc-200 dark:border-zinc-800 flex items-center gap-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask about candidates, pipelines, or draft communications..."
            className="flex-1 px-4 py-2.5 rounded-xl dark:bg-black/80 light:bg-white border border-zinc-300 dark:border-zinc-700 text-xs dark:text-white light:text-zinc-900 placeholder-zinc-500 focus:outline-none"
          />
          <button
            type="submit"
            className="p-2.5 rounded-xl bg-zinc-900 text-white transition hover:bg-zinc-800 shrink-0"
          >
            <Send className="w-4 h-4 text-white" />
          </button>
        </form>
      </div>
    </div>
  );
};
