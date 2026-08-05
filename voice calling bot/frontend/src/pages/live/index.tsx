import * as React from "react"
import { motion } from "framer-motion"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Search, Phone, PhoneOff, PauseCircle, Mic, MicOff, BrainCircuit, Activity, Clock, AlertTriangle } from "lucide-react"

// Types
type CallState = "listening" | "thinking" | "speaking" | "tool_execution" | "ended" | "waiting"
type Sentiment = "positive" | "neutral" | "negative"








const mockEvents = [
  { id: 1, type: "intent", title: "Objection Detected", detail: "Customer concerned about latency.", time: "00:26" },
  { id: 2, type: "tool", title: "Knowledge Base Search", detail: "Query: 'latency metrics and selling points'", time: "00:27" },
  { id: 3, type: "memory", title: "Variable Updated", detail: "is_exploring_ai = true", time: "00:30" },
]

import { api } from "@/services/api"

export function LiveMonitorPage() {
  const [liveCalls, setLiveCalls] = React.useState<any[]>([])
  const [activeCallId, setActiveCallId] = React.useState<string>("call_1")

  React.useEffect(() => {
    const fetchLive = () => {
      api.getLiveCalls()
        .then(data => {
          if (data && data.length > 0) {
            const mapped = data.map((c: any) => ({
              id: c.id,
              customerName: c.customerName || c.to_number || "PSTN Call Target",
              phoneNumber: c.to_number || "+917039015196",
              campaign: "Outbound SDR Outreach",
              agent: c.agent_name || "Sarah - Sales SDR",
              duration: `${Math.floor((c.duration_seconds || 12) / 60)}:${((c.duration_seconds || 12) % 60).toString().padStart(2, '0')}`,
              state: c.status === "in-progress" ? "speaking" : "listening",
              sentiment: "positive",
              confidence: 96,
              networkQuality: "excellent",
              transcript: c.transcript || null,
            }))
            setLiveCalls(mapped)

            if (!activeCallId) setActiveCallId(mapped[0].id)
          } else {
            setLiveCalls([])
          }
        })
        .catch(err => console.error("Error loading live calls:", err))
    }
    fetchLive()
    const interval = setInterval(fetchLive, 3000)
    return () => clearInterval(interval)
  }, [])

  const activeCall = liveCalls.find(c => c.id === activeCallId) || liveCalls[0] || {
    id: "call_live_demo",
    customerName: "+917039015196",
    phoneNumber: "+917039015196",
    campaign: "Live Outbound Outreach",
    agent: "Sarah - Sales SDR",
    duration: "00:45",
    state: "speaking" as CallState,
    sentiment: "positive" as Sentiment,
    confidence: 98,
    networkQuality: "excellent" as const
  }

  const [isListening, setIsListening] = React.useState(false)

  const handleTerminateCall = async (callId: string) => {
    try {
      await api.terminateCall(callId)
      setLiveCalls(prev => prev.filter(c => c.id !== callId))
    } catch (err) {
      console.error("Error terminating call:", err)
    }
  }


  // Parse live call transcript from DB (persisted in real-time by webhooks.py)
  const parsedLiveTranscript = React.useMemo(() => {
    if (!activeCall?.transcript) {
      return [
        { role: "assistant", content: "Waiting for call to connect..." }
      ]
    }
    try {
      if (typeof activeCall.transcript === "string") {
        return JSON.parse(activeCall.transcript)
      }
      if (Array.isArray(activeCall.transcript)) {
        return activeCall.transcript
      }
      return [{ role: "assistant", content: String(activeCall.transcript) }]
    } catch (e) {
      return [{ role: "assistant", content: String(activeCall.transcript) }]
    }
  }, [activeCall])




  // Waveform animation helper
  const Waveform = ({ state }: { state: CallState }) => {
    const bars = 5
    const isSpeaking = state === "speaking"
    return (
      <div className="flex items-center gap-1 h-6">
        {Array.from({ length: bars }).map((_, i) => (
          <motion.div
            key={i}
            className={`w-1 rounded-full ${isSpeaking ? 'bg-primary' : 'bg-muted-foreground/30'}`}
            animate={isSpeaking ? {
              height: ["20%", "80%", "40%", "100%", "30%"],
            } : { height: "20%" }}
            transition={{
              repeat: Infinity,
              duration: 0.8,
              ease: "easeInOut",
              delay: i * 0.1,
            }}
            style={{ height: "20%" }}
          />
        ))}
      </div>
    )
  }

  // AI State Badge mapping
  const StateBadge = ({ state }: { state: CallState }) => {
    const config = {
      listening: { color: "bg-blue-500", label: "Listening", icon: Mic },
      thinking: { color: "bg-purple-500", label: "Thinking", icon: BrainCircuit },
      speaking: { color: "bg-green-500", label: "Speaking", icon: Phone },
      tool_execution: { color: "bg-amber-500", label: "Executing Tool", icon: Activity },
      waiting: { color: "bg-gray-400", label: "Waiting", icon: Clock },
      ended: { color: "bg-red-500", label: "Ended", icon: PhoneOff },
    }
    const { color, label, icon: Icon } = config[state]
    return (
      <div className="flex items-center gap-2">
        <div className="relative flex h-3 w-3 items-center justify-center">
          <Icon className="h-3 w-3 absolute -left-4 text-muted-foreground" />
          {(state === "thinking" || state === "tool_execution") && (
            <span className={`animate-ping absolute inline-flex h-full w-full rounded-full opacity-75 ${color}`}></span>
          )}
          <span className={`relative inline-flex rounded-full h-3 w-3 ${color}`}></span>
        </div>
        <span className="text-sm font-medium">{label}</span>
      </div>
    )
  }

  return (
    <div className="flex flex-col h-[calc(100vh-4rem)] -m-6">
      {/* Header */}
      <div className="border-b bg-card p-6 flex-shrink-0">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold tracking-tight">Live Call Monitor</h1>
            <p className="text-muted-foreground">Monitor and intervene in active AI conversations in real-time.</p>
          </div>
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-2 bg-muted px-4 py-2 rounded-lg">
              <span className="relative flex h-3 w-3">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
                <span className="relative inline-flex rounded-full h-3 w-3 bg-green-500"></span>
              </span>
              <span className="font-semibold">{liveCalls.length} Active Calls</span>
            </div>
          </div>
        </div>
      </div>

      {/* Main Split View */}
      <div className="flex flex-1 overflow-hidden">
        {/* Left Column: Active Call Stream Cards */}
        <div className="w-[380px] border-r bg-card flex flex-col">
          <div className="p-4 border-b space-y-3">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
              <Input placeholder="Filter by phone or lead..." className="pl-9" />
            </div>
            <div className="flex gap-2">
              <Badge variant="secondary" className="cursor-pointer">All ({liveCalls.length})</Badge>
              <Badge variant="outline" className="cursor-pointer border-dashed">Sales</Badge>
              <Badge variant="outline" className="cursor-pointer border-dashed">Support</Badge>
            </div>
          </div>
          <ScrollArea className="flex-1">
            <div className="p-4 space-y-3">
              {liveCalls.map((call: any) => (
                <div
                  key={call.id}
                  onClick={() => setActiveCallId(call.id)}
                  className={`p-4 rounded-xl border-2 cursor-pointer transition-all ${
                    activeCallId === call.id 
                      ? "border-primary bg-primary/5 shadow-sm" 
                      : "border-border bg-card hover:border-primary/50"
                  }`}
                >
                  <div className="flex items-center justify-between mb-3">
                    <span className="font-semibold truncate pr-2">{call.customerName}</span>
                    <span className="text-xs font-mono text-muted-foreground">{call.duration}</span>
                  </div>
                  <div className="flex items-center justify-between">
                    <StateBadge state={call.state} />
                    <Waveform state={call.state} />
                  </div>
                  <div className="mt-4 pt-3 border-t flex items-center justify-between text-xs text-muted-foreground">
                    <span className="truncate max-w-[150px]">{call.campaign}</span>
                    <div className="flex items-center gap-1">
                      <div className={`w-2 h-2 rounded-full ${call.sentiment === 'positive' ? 'bg-green-500' : call.sentiment === 'negative' ? 'bg-red-500' : 'bg-gray-400'}`} />
                      {call.sentiment}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </ScrollArea>
        </div>

        {/* Right Panel - Active Call Details */}
        <div className="flex-1 flex flex-col bg-background overflow-hidden">
          {/* Active Call Header */}
          <div className="p-6 border-b flex items-center justify-between bg-card shrink-0">
            <div>
              <h2 className="text-xl font-bold flex items-center gap-3">
                {activeCall.customerName}
                <Badge variant={activeCall.sentiment === 'negative' ? 'destructive' : 'secondary'}>
                  {activeCall.confidence}% Confidence
                </Badge>
              </h2>
              <div className="flex items-center gap-4 mt-2 text-sm text-muted-foreground">
                <span className="flex items-center gap-1"><Phone className="h-3 w-3" /> {activeCall.phoneNumber}</span>
                <span className="flex items-center gap-1"><BrainCircuit className="h-3 w-3" /> {activeCall.agent}</span>
              </div>
            </div>
            
            <div className="flex items-center gap-3">
              <Button 
                variant={isListening ? "secondary" : "default"} 
                className={isListening ? "bg-primary/20 text-primary hover:bg-primary/30" : ""}
                onClick={() => setIsListening(!isListening)}
              >
                {isListening ? <MicOff className="mr-2 h-4 w-4" /> : <Mic className="mr-2 h-4 w-4" />}
                {isListening ? "Stop Listening" : "Listen Live"}
              </Button>
              <Button variant="outline" className="text-amber-600 border-amber-200 hover:bg-amber-50 dark:hover:bg-amber-900/20">
                <PauseCircle className="mr-2 h-4 w-4" /> Pause
              </Button>
              <Button variant="destructive" onClick={() => handleTerminateCall(activeCall.id)}>
                <PhoneOff className="mr-2 h-4 w-4" /> Terminate
              </Button>

            </div>
          </div>

          <div className="flex-1 flex overflow-hidden">
            {/* Transcript Area */}
            <div className="flex-1 flex flex-col border-r">
              <div className="p-4 bg-muted/20 border-b flex items-center justify-between">
                <h3 className="font-semibold text-sm">Live Transcript</h3>
                <StateBadge state={activeCall.state} />
              </div>
              <ScrollArea className="flex-1 p-6">
                <div className="space-y-6">
                  {parsedLiveTranscript.map((msg: any, idx: number) => (
                    <div key={idx} className={`flex flex-col ${msg.role === 'user' ? 'items-end' : 'items-start'}`}>
                      <div className="flex items-center gap-2 mb-1">
                        <span className="text-xs font-semibold">{msg.role === 'user' ? activeCall.customerName : activeCall.agent}</span>
                      </div>
                      <div className={`p-4 rounded-2xl max-w-[85%] text-sm ${
                        msg.role === 'user'
                          ? 'bg-primary text-primary-foreground rounded-tr-none font-mono'
                          : 'bg-card border shadow-sm rounded-tl-none'
                      }`}>
                        {msg.content}
                      </div>
                    </div>
                  ))}
                  
                  {activeCall.state === 'listening' && (
                    <div className="flex flex-col items-end">
                      <div className="p-4 rounded-2xl bg-primary/20 text-primary rounded-tr-sm max-w-[80%]">
                        <div className="flex gap-1">
                          <span className="w-1.5 h-1.5 bg-primary rounded-full animate-bounce" />
                          <span className="w-1.5 h-1.5 bg-primary rounded-full animate-bounce" style={{ animationDelay: '0.2s' }} />
                          <span className="w-1.5 h-1.5 bg-primary rounded-full animate-bounce" style={{ animationDelay: '0.4s' }} />
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              </ScrollArea>
            </div>

            {/* AI State Panel */}
            <div className="w-[350px] bg-card flex flex-col">
              <Tabs defaultValue="timeline" className="flex-1 flex flex-col">
                <div className="px-4 pt-4 border-b">
                  <TabsList className="w-full grid grid-cols-2">
                    <TabsTrigger value="timeline">AI Brain</TabsTrigger>
                    <TabsTrigger value="variables">Context</TabsTrigger>
                  </TabsList>
                </div>
                
                <ScrollArea className="flex-1">
                  <TabsContent value="timeline" className="p-4 space-y-4 mt-0">
                    <h4 className="text-xs font-semibold text-muted-foreground uppercase tracking-wider mb-4">Recent Events</h4>
                    <div className="space-y-4">
                      {mockEvents.map((event, i) => (
                        <div key={event.id} className="relative pl-6">
                          <div className={`absolute left-0 top-1.5 w-2 h-2 rounded-full ${
                            event.type === 'intent' ? 'bg-purple-500' :
                            event.type === 'tool' ? 'bg-amber-500' : 'bg-blue-500'
                          }`} />
                          {i !== mockEvents.length - 1 && (
                            <div className="absolute left-[3px] top-4 bottom-[-16px] w-[2px] bg-border" />
                          )}
                          <div className="flex items-center justify-between mb-1">
                            <span className="text-sm font-medium">{event.title}</span>
                            <span className="text-xs text-muted-foreground">{event.time}</span>
                          </div>
                          <p className="text-xs text-muted-foreground">{event.detail}</p>
                        </div>
                      ))}
                    </div>
                    
                    <div className="mt-8 p-4 rounded-lg bg-red-50 dark:bg-red-950/20 border border-red-100 dark:border-red-900/30">
                      <div className="flex items-start gap-3">
                        <AlertTriangle className="h-4 w-4 text-red-500 mt-0.5 shrink-0" />
                        <div>
                          <p className="text-sm font-medium text-red-700 dark:text-red-400">High Latency Detected</p>
                          <p className="text-xs text-red-600/80 dark:text-red-400/80 mt-1">LLM generation took 1.2s on last turn. Provider: OpenAI.</p>
                        </div>
                      </div>
                    </div>
                  </TabsContent>

                  <TabsContent value="variables" className="p-4 space-y-6 mt-0">
                    <div>
                      <h4 className="text-xs font-semibold text-muted-foreground uppercase tracking-wider mb-3">Session Variables</h4>
                      <div className="space-y-2">
                        {[
                          { key: "customer_name", value: "Acme Corp" },
                          { key: "is_exploring_ai", value: "true" },
                          { key: "pain_point", value: "latency" },
                          { key: "call_goal", value: "book_demo" },
                        ].map((v) => (
                          <div key={v.key} className="flex flex-col p-2 bg-muted rounded-md text-xs font-mono">
                            <span className="text-muted-foreground">{v.key}</span>
                            <span className="text-foreground font-semibold mt-1">{v.value}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                    
                    <div>
                      <h4 className="text-xs font-semibold text-muted-foreground uppercase tracking-wider mb-3">Providers</h4>
                      <div className="space-y-3">
                        <div className="flex justify-between items-center text-sm">
                          <span className="text-muted-foreground">Voice TTS</span>
                          <span className="font-medium">ElevenLabs (Turbo v2)</span>
                        </div>
                        <div className="flex justify-between items-center text-sm">
                          <span className="text-muted-foreground">LLM Engine</span>
                          <span className="font-medium">GPT-4o-mini</span>
                        </div>
                        <div className="flex justify-between items-center text-sm">
                          <span className="text-muted-foreground">Telephony</span>
                          <span className="font-medium">Twilio</span>
                        </div>
                      </div>
                    </div>
                  </TabsContent>
                </ScrollArea>
              </Tabs>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
