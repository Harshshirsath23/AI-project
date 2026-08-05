import * as React from "react"
import { motion } from "framer-motion"
import { Card, CardContent } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Slider } from "@/components/ui/slider"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog"
import { Badge } from "@/components/ui/badge"
import { Send, Bot, User, PhoneCall, Settings2, Sparkles, AlertCircle, Loader2, Zap, DollarSign, Hash } from "lucide-react"
import { api } from "@/services/api"

interface Message {
  role: "user" | "assistant" | "system"
  content: string
}

interface Voice {
  id: string
  name: string
  engine: string
  language: string
  gender: string
}

interface Agent {
  id: string
  name: string
  system_prompt: string
  greeting_message: string
  llm_provider: string
  tts_provider: string
}

export function PlaygroundPage() {
  const [agentsList, setAgentsList] = React.useState<Agent[]>([])
  const [voicesList, setVoicesList] = React.useState<Voice[]>([])
  const [selectedAgentId, setSelectedAgentId] = React.useState<string>("")
  const [selectedAgent, setSelectedAgent] = React.useState<Agent | null>(null)
  const [selectedVoiceId, setSelectedVoiceId] = React.useState<string>("gtts-en-us")
  const [selectedLLM, setSelectedLLM] = React.useState<string>("gemini")
  const [temperature, setTemperature] = React.useState<number>(70)
  const [systemPrompt, setSystemPrompt] = React.useState<string>(
    "You are a helpful and friendly AI voice assistant. Keep responses under 2-3 short sentences."
  )

  const [messages, setMessages] = React.useState<Message[]>([
    { role: "system", content: "Agent ready. Select an agent or type a message to begin." },
  ])
  const [input, setInput] = React.useState("")
  const [isTyping, setIsTyping] = React.useState(false)

  // Stats from real API
  const [latencyMs, setLatencyMs] = React.useState<number | null>(null)
  const [tokens, setTokens] = React.useState<number | null>(null)
  const [cost, setCost] = React.useState<number | null>(null)

  // Call dialog
  const [targetPhone, setTargetPhone] = React.useState("+917039015196")
  const [isCalling, setIsCalling] = React.useState(false)
  const [callStatus, setCallStatus] = React.useState<string | null>(null)
  const [isDialogOpen, setIsDialogOpen] = React.useState(false)

  const messagesEndRef = React.useRef<HTMLDivElement>(null)

  // Load agents and voices on mount
  React.useEffect(() => {
    api.getAgents()
      .then(data => {
        setAgentsList(data)
        if (data && data.length > 0) {
          setSelectedAgentId(data[0].id)
          setSelectedAgent(data[0])
          if (data[0].system_prompt) setSystemPrompt(data[0].system_prompt)
          if (data[0].llm_provider) setSelectedLLM(data[0].llm_provider)
        }
      })
      .catch(err => console.error("Error loading agents:", err))

    api.getVoices()
      .then(data => {
        setVoicesList(data)
      })
      .catch(err => console.error("Error loading voices:", err))
  }, [])

  // Auto-scroll to bottom
  React.useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }, [messages, isTyping])

  // When agent changes, update system prompt
  const handleAgentChange = (agentId: string) => {
    setSelectedAgentId(agentId)
    const agent = agentsList.find(a => a.id === agentId)
    if (agent) {
      setSelectedAgent(agent)
      if (agent.system_prompt) setSystemPrompt(agent.system_prompt)
      if (agent.llm_provider) setSelectedLLM(agent.llm_provider)

      // Reset chat with agent greeting
      setMessages([
        { role: "system", content: `Agent '${agent.name}' loaded.` },
        ...(agent.greeting_message ? [{ role: "assistant" as const, content: agent.greeting_message }] : [])
      ])
      setLatencyMs(null)
      setTokens(null)
      setCost(null)
    }
  }

  // Apply configuration button
  const handleApplyConfig = () => {
    setMessages(prev => [
      ...prev,
      { role: "system", content: `Configuration updated: LLM=${selectedLLM}, Voice=${selectedVoiceId}, Temp=${(temperature / 100).toFixed(1)}` }
    ])
  }

  // Send message to real backend
  const handleSend = async () => {
    if (!input.trim() || isTyping) return
    const userMsg: Message = { role: "user", content: input }
    const updatedHistory = [...messages, userMsg]
    setMessages(updatedHistory)
    setInput("")
    setIsTyping(true)

    try {
      const history = updatedHistory
        .filter(m => m.role !== "system")
        .slice(-10) // send last 10 messages for context

      const res = await fetch("http://localhost:8000/api/v1/playground/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          agent_id: selectedAgentId || null,
          message: input,
          voice_id: selectedVoiceId,
          llm_provider: selectedLLM,
          temperature: temperature / 100,
          conversation_history: history,
        })
      })

      if (res.ok) {
        const data = await res.json()
        setMessages(prev => [...prev, { role: "assistant", content: data.response }])
        setLatencyMs(data.latency_ms)
        setTokens(data.tokens)
        setCost(data.cost)
      } else {
        setMessages(prev => [...prev, { role: "assistant", content: "Error: Could not connect to AI backend. Make sure `python run.py` is running." }])
      }
    } catch (err) {
      setMessages(prev => [...prev, { role: "assistant", content: "⚠️ Backend offline. Run `python run.py` in the backend directory." }])
    } finally {
      setIsTyping(false)
    }
  }

  const triggerLiveCall = async () => {
    setIsCalling(true)
    setCallStatus("Dialing via Twilio...")
    try {
      const response = await fetch("http://localhost:8000/api/v1/calls/start", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          agent_id: selectedAgentId || "00000000-0000-0000-0000-000000000000",
          from_number: "+17372212163",
          to_number: targetPhone
        })
      })
      const data = await response.json()
      if (response.ok) {
        setCallStatus(`✅ Call Initiated! SID: ${data.provider_call_id || data.call_id || "Pending"}`)
      } else {
        setCallStatus(`⚠️ ${data.detail || "Call queued in dev mode"}`)
      }
    } catch (err) {
      setCallStatus("⚠️ Backend offline. Run `python run.py` first.")
    } finally {
      setIsCalling(false)
    }
  }

  const gttsVoices = voicesList.filter(v => v.engine === "gtts")


  return (
    <div className="flex flex-col h-[calc(100vh-4rem)] -m-6">
      {/* Header */}
      <div className="border-b bg-card p-6 flex-shrink-0">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold tracking-tight">AI Playground</h1>
            <p className="text-muted-foreground text-sm">
              Test your AI Agent live — powered by <span className="text-primary font-semibold">Gemini LLM</span> + <span className="text-primary font-semibold">gTTS Voice</span>
            </p>
          </div>

          <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
            <DialogTrigger asChild>
              <Button variant="default" className="bg-primary hover:bg-primary/90">
                <PhoneCall className="mr-2 h-4 w-4" /> Start Voice Call Test
              </Button>
            </DialogTrigger>
            <DialogContent className="sm:max-w-[425px]">
              <DialogHeader>
                <DialogTitle>Start Outbound AI Call Test</DialogTitle>
                <DialogDescription>
                  Dial your real phone number via Twilio. The AI agent will speak using <strong>gTTS (Google TTS)</strong>.
                </DialogDescription>
              </DialogHeader>
              <div className="grid gap-4 py-4">
                <div className="space-y-2">
                  <Label>Target Phone Number</Label>
                  <Input
                    value={targetPhone}
                    onChange={(e) => setTargetPhone(e.target.value)}
                    placeholder="+91XXXXXXXXXX"
                  />
                </div>
                <div className="space-y-2">
                  <Label>Outbound Caller ID (Twilio)</Label>
                  <Input value="+17372212163" disabled className="font-mono text-sm" />
                </div>
                <div className="space-y-2">
                  <Label>Selected Agent</Label>
                  <Input value={selectedAgent?.name || "No agent selected"} disabled className="text-sm" />
                </div>
                {callStatus && (
                  <div className="p-3 bg-muted rounded-md text-xs font-mono text-center">
                    {callStatus}
                  </div>
                )}
              </div>
              <div className="flex justify-end gap-2">
                <Button variant="outline" onClick={() => setIsDialogOpen(false)}>Cancel</Button>
                <Button onClick={triggerLiveCall} disabled={isCalling}>
                  {isCalling ? <Loader2 className="mr-2 h-4 w-4 animate-spin" /> : <PhoneCall className="mr-2 h-4 w-4" />}
                  Dial Outbound Call
                </Button>
              </div>
            </DialogContent>
          </Dialog>
        </div>
      </div>

      <div className="flex flex-1 overflow-hidden">
        {/* Left Panel - Configuration */}
        <div className="w-[420px] border-r bg-card flex flex-col">
          <ScrollArea className="flex-1 p-6">
            <div className="space-y-6">

              {/* Load Agent */}
              <div className="space-y-3">
                <h3 className="font-semibold flex items-center gap-2 text-sm">
                  <Bot className="h-4 w-4 text-primary" /> Load Agent
                </h3>
                <Select value={selectedAgentId} onValueChange={handleAgentChange}>
                  <SelectTrigger><SelectValue placeholder="Select an AI Agent" /></SelectTrigger>
                  <SelectContent>
                    {agentsList.map((ag) => (
                      <SelectItem key={ag.id} value={ag.id}>
                        {ag.name}
                      </SelectItem>
                    ))}
                    {agentsList.length === 0 && (
                      <SelectItem value="none" disabled>No agents found — create one first</SelectItem>
                    )}
                  </SelectContent>
                </Select>
              </div>

              {/* Engine Settings */}
              <div className="space-y-4 pt-4 border-t">
                <h3 className="font-semibold flex items-center gap-2 text-sm">
                  <Settings2 className="h-4 w-4 text-primary" /> Engine Settings
                </h3>

                {/* LLM Provider */}
                <div className="space-y-2">
                  <Label className="text-xs text-muted-foreground">LLM Provider</Label>
                  <Select value={selectedLLM} onValueChange={setSelectedLLM}>
                    <SelectTrigger><SelectValue /></SelectTrigger>
                    <SelectContent>
                      <SelectItem value="gemini">
                        <div className="flex items-center gap-2">
                          <span>Gemini 2.5 Flash</span>
                          <Badge variant="secondary" className="text-xs px-1 py-0">✅ Active</Badge>
                        </div>
                      </SelectItem>
                      <SelectItem value="huggingface">
                        <div className="flex items-center gap-2">
                          <span>Nemotron (HuggingFace)</span>
                          <Badge variant="outline" className="text-xs px-1 py-0">NVIDIA</Badge>
                        </div>
                      </SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                {/* Voice (gTTS only — real voices we built) */}
                <div className="space-y-2">
                  <Label className="text-xs text-muted-foreground">Voice (TTS Engine)</Label>
                  <Select value={selectedVoiceId} onValueChange={setSelectedVoiceId}>
                    <SelectTrigger><SelectValue /></SelectTrigger>
                    <SelectContent>
                      {gttsVoices.length > 0 ? (
                        gttsVoices.map(v => (
                          <SelectItem key={v.id} value={v.id}>
                            <div className="flex items-center gap-2">
                              <span>{v.name}</span>
                              <Badge variant="secondary" className="text-xs px-1 py-0">Free</Badge>
                            </div>
                          </SelectItem>
                        ))
                      ) : (
                        <>
                          <SelectItem value="gtts-en-us">gTTS - English (Free) ✅</SelectItem>
                          <SelectItem value="gtts-hi-in">gTTS - Hindi / Hinglish (Free) ✅</SelectItem>
                        </>
                      )}
                    </SelectContent>
                  </Select>
                  <p className="text-xs text-muted-foreground">
                    Using <strong>Google TTS (gTTS)</strong> — free, no API key required.
                  </p>
                </div>

                {/* Temperature */}
                <div className="space-y-3 pt-1">
                  <div className="flex items-center justify-between">
                    <Label className="text-xs text-muted-foreground">Temperature</Label>
                    <span className="text-xs font-mono text-muted-foreground">{(temperature / 100).toFixed(1)}</span>
                  </div>
                  <Slider
                    value={[temperature]}
                    onValueChange={([v]) => setTemperature(v)}
                    max={100} min={0} step={1}
                  />
                </div>
              </div>

              {/* System Prompt */}
              <div className="space-y-3 pt-4 border-t">
                <h3 className="font-semibold flex items-center gap-2 text-sm">
                  <Sparkles className="h-4 w-4 text-primary" /> System Prompt
                </h3>
                <Textarea
                  className="min-h-[180px] font-mono text-xs resize-none"
                  value={systemPrompt}
                  onChange={(e) => setSystemPrompt(e.target.value)}
                  placeholder="Enter the agent's system prompt..."
                />
              </div>
            </div>
          </ScrollArea>

          <div className="p-4 border-t bg-muted/20">
            <Button className="w-full" onClick={handleApplyConfig}>Apply Configuration</Button>
          </div>
        </div>

        {/* Right Panel - Chat Interface */}
        <div className="flex-1 flex flex-col bg-muted/10 relative">

          {/* Stats Bar */}
          <div className="absolute top-4 right-4 z-10">
            <Card className="shadow-lg border-primary/20 bg-card/95 backdrop-blur">
              <CardContent className="p-3 py-2 flex items-center gap-4 text-xs font-mono">
                <div className="flex items-center gap-1.5">
                  <Zap className="h-3 w-3 text-green-500" />
                  <span className="text-muted-foreground">Latency:</span>
                  <span className={latencyMs !== null ? "text-green-500 font-semibold" : "text-muted-foreground"}>
                    {latencyMs !== null ? `${latencyMs}ms` : "—"}
                  </span>
                </div>
                <div className="flex items-center gap-1.5">
                  <Hash className="h-3 w-3 text-blue-500" />
                  <span className="text-muted-foreground">Tokens:</span>
                  <span>{tokens !== null ? tokens.toLocaleString() : "—"}</span>
                </div>
                <div className="flex items-center gap-1.5">
                  <DollarSign className="h-3 w-3 text-yellow-500" />
                  <span className="text-muted-foreground">Cost:</span>
                  <span>{cost !== null ? `$${cost.toFixed(5)}` : "—"}</span>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Messages */}
          <ScrollArea className="flex-1 p-6">
            <div className="max-w-3xl mx-auto space-y-6 pt-14">
              {messages.map((msg, i) => (
                <motion.div
                  initial={{ opacity: 0, y: 8 }}
                  animate={{ opacity: 1, y: 0 }}
                  key={i}
                  className={`flex ${msg.role === "user" ? "justify-end" : msg.role === "system" ? "justify-center" : "justify-start"}`}
                >
                  {msg.role === "system" ? (
                    <div className="bg-muted px-4 py-1.5 rounded-full text-xs text-muted-foreground font-mono flex items-center gap-2">
                      <Settings2 className="h-3 w-3" /> {msg.content}
                    </div>
                  ) : (
                    <div className="flex items-start gap-3 max-w-[80%]">
                      {msg.role === "assistant" && (
                        <div className="w-8 h-8 rounded-full bg-primary flex items-center justify-center text-primary-foreground shrink-0 shadow-sm mt-1">
                          <Bot className="h-4 w-4" />
                        </div>
                      )}
                      <div className={`p-4 rounded-2xl ${
                        msg.role === "user"
                          ? "bg-foreground text-background rounded-tr-sm"
                          : "bg-card border shadow-sm rounded-tl-sm"
                      }`}>
                        <p className="text-sm leading-relaxed">{msg.content}</p>
                      </div>
                      {msg.role === "user" && (
                        <div className="w-8 h-8 rounded-full bg-muted flex items-center justify-center shrink-0 mt-1">
                          <User className="h-4 w-4" />
                        </div>
                      )}
                    </div>
                  )}
                </motion.div>
              ))}

              {isTyping && (
                <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="flex items-start gap-3">
                  <div className="w-8 h-8 rounded-full bg-primary flex items-center justify-center text-primary-foreground shrink-0 shadow-sm">
                    <Bot className="h-4 w-4" />
                  </div>
                  <div className="p-4 rounded-2xl bg-card border shadow-sm rounded-tl-sm flex items-center gap-1">
                    <span className="w-2 h-2 bg-primary rounded-full animate-bounce" />
                    <span className="w-2 h-2 bg-primary rounded-full animate-bounce" style={{ animationDelay: "0.2s" }} />
                    <span className="w-2 h-2 bg-primary rounded-full animate-bounce" style={{ animationDelay: "0.4s" }} />
                  </div>
                </motion.div>
              )}
              <div ref={messagesEndRef} />
            </div>
          </ScrollArea>

          {/* Input */}
          <div className="p-6 bg-card border-t shrink-0">
            <div className="max-w-3xl mx-auto flex items-end gap-4">
              <div className="flex-1 relative">
                <Textarea
                  placeholder="Type a message to test the agent..."
                  className="min-h-[80px] resize-none pr-12 text-base"
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyDown={(e) => {
                    if (e.key === "Enter" && !e.shiftKey) {
                      e.preventDefault()
                      handleSend()
                    }
                  }}
                />
              </div>
              <Button
                size="icon"
                className="h-12 w-12 rounded-full shadow-md"
                onClick={handleSend}
                disabled={!input.trim() || isTyping}
              >
                {isTyping ? <Loader2 className="h-5 w-5 animate-spin" /> : <Send className="h-5 w-5 ml-1" />}
              </Button>
            </div>
            <div className="max-w-3xl mx-auto mt-2 text-center">
              <p className="text-xs text-muted-foreground flex items-center justify-center gap-1">
                <AlertCircle className="h-3 w-3" />
                Powered by <strong className="mx-1">Gemini 2.5 Flash</strong> LLM · Voice synthesis via <strong className="mx-1">gTTS (Google)</strong>
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
