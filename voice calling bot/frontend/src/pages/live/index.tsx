import * as React from "react"
import { motion } from "framer-motion"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Search, Phone, PhoneOff, PauseCircle, Mic, MicOff, BrainCircuit, Activity, Clock, PhoneCall } from "lucide-react"
import { api } from "@/services/api"

type CallState = "listening" | "thinking" | "speaking" | "tool_execution" | "ended" | "waiting"


export function LiveMonitorPage() {
  const [liveCalls, setLiveCalls] = React.useState<any[]>([])
  const [activeCallId, setActiveCallId] = React.useState<string | null>(null)
  const [isListening, setIsListening] = React.useState(false)
  const [liveTranscriptTurns, setLiveTranscriptTurns] = React.useState<any[]>([])
  const [liveState, setLiveState] = React.useState<CallState>("listening")
  const wsRef = React.useRef<WebSocket | null>(null)

  // Establish real-time WebSocket connection to backend for activeCallId
  React.useEffect(() => {
    if (!activeCallId) {
      setLiveTranscriptTurns([])
      return
    }

    const protocol = window.location.protocol === "https:" ? "wss:" : "ws:"
    const host = (window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1")
      ? `${window.location.hostname}:8000`
      : window.location.host
    const wsUrl = `${protocol}//${host}/ws/calls/${activeCallId}`

    const ws = new WebSocket(wsUrl)
    wsRef.current = ws

    ws.onopen = () => {
      console.log(`[WS Live Monitor] Connected to call ${activeCallId}`)
    }

    ws.onmessage = (event) => {
      try {
        const msg = JSON.parse(event.data)
        if (msg.event === "connected") {
          if (msg.transcript && Array.isArray(msg.transcript) && msg.transcript.length > 0) {
            setLiveTranscriptTurns(msg.transcript)
          }
          if (msg.state) setLiveState(msg.state)
        } else if (msg.event === "transcript_turn") {
          setLiveTranscriptTurns(prev => [...prev, { role: msg.role, content: msg.content }])
          if (msg.state) setLiveState(msg.state)
        } else if (msg.event === "state_change") {
          if (msg.state) setLiveState(msg.state)
        } else if (msg.event === "call_ended") {
          setLiveState("ended")
        }
      } catch (e) {
        console.warn("[WS Live Monitor] Parsing error:", e)
      }
    }

    ws.onclose = () => {
      console.log(`[WS Live Monitor] Disconnected from call ${activeCallId}`)
    }

    return () => {
      ws.close()
      wsRef.current = null
    }
  }, [activeCallId])

  React.useEffect(() => {
    const fetchLive = () => {
      api.getLiveCalls()
        .then(data => {
          if (data && data.length > 0) {
            const mapped = data.map((c: any) => ({
              id: c.id,
              customerName: c.contactName || c.to_number || "Target Lead",
              phoneNumber: c.to_number || "N/A",
              campaign: c.campaign_name || "Outbound AI Campaign",
              agent: c.agent_name || "AI Voice Agent",
              duration: `${Math.floor((c.duration_seconds || 0) / 60)}:${((c.duration_seconds || 0) % 60).toString().padStart(2, '0')}`,
              state: c.status === "in-progress" ? "speaking" : "listening",
              sentiment: c.sentiment || "neutral",
              confidence: 98,
              networkQuality: "excellent",
              transcript: c.transcript || null,
            }))
            setLiveCalls(mapped)

            if (!activeCallId && mapped.length > 0) {
              setActiveCallId(mapped[0].id)
            }
          } else {
            setLiveCalls([])
            setActiveCallId(null)
          }
        })
        .catch(err => console.error("Error loading live calls:", err))
    }
    fetchLive()
    const interval = setInterval(fetchLive, 4000)
    return () => clearInterval(interval)
  }, [])

  const activeCall = liveCalls.find(c => c.id === activeCallId) || liveCalls[0] || null

  const handleTerminateCall = async (callId: string) => {
    try {
      if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
        wsRef.current.send(JSON.stringify({ action: "end_call" }))
      }
      await api.terminateCall(callId)
      setLiveCalls(prev => prev.filter(c => c.id !== callId))
      setLiveState("ended")
    } catch (err) {
      console.error("Error terminating call:", err)
    }
  }

  // Parse live call transcript from DB as initial fallback
  const parsedLiveTranscript = React.useMemo(() => {
    if (liveTranscriptTurns.length > 0) {
      return liveTranscriptTurns
    }
    if (!activeCall?.transcript) {
      return [
        { role: "assistant", content: "Connected to live WebSocket call stream session..." }
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
  }, [activeCall, liveTranscriptTurns])

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
    const { color, label, icon: Icon } = config[state] || config.waiting
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
              <Input placeholder="Filter active calls..." className="pl-9" />
            </div>
          </div>
          <ScrollArea className="flex-1">
            <div className="p-4 space-y-3">
              {liveCalls.length === 0 ? (
                <div className="py-12 text-center text-xs text-muted-foreground space-y-2">
                  <PhoneCall className="h-8 w-8 mx-auto opacity-40 mb-2" />
                  <p className="font-medium">No Live Calls Active</p>
                  <p className="text-[11px] max-w-[200px] mx-auto opacity-70">
                    Active call channels will appear here automatically when triggered from Playground or Campaigns.
                  </p>
                </div>
              ) : (
                liveCalls.map((call: any) => (
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
                  </div>
                ))
              )}
            </div>
          </ScrollArea>
        </div>

        {/* Right Panel - Active Call Details */}
        <div className="flex-1 flex flex-col bg-background overflow-hidden">
          {!activeCall ? (
            <div className="flex-1 flex flex-col items-center justify-center p-8 text-center text-muted-foreground">
              <Activity className="h-12 w-12 text-muted-foreground/30 mb-3" />
              <h3 className="text-lg font-semibold text-foreground">Select an Active Call</h3>
              <p className="text-xs max-w-md mt-1">
                Trigger a live call from the Playground or Leads page to monitor real-time AI conversation audio streams and transcripts.
              </p>
            </div>
          ) : (
            <>
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
                    <div className="flex items-center gap-2">
                      <h3 className="font-semibold text-sm">Live WebSocket Transcript</h3>
                      <span className="flex h-2 w-2 relative">
                        <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                        <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
                      </span>
                    </div>
                    <StateBadge state={liveState} />
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
                    </div>
                  </ScrollArea>
                </div>

                {/* AI State Panel */}
                <div className="w-[350px] bg-card flex flex-col">
                  <Tabs defaultValue="variables" className="flex-1 flex flex-col">
                    <div className="px-4 pt-4 border-b">
                      <TabsList className="w-full grid grid-cols-1">
                        <TabsTrigger value="variables">Context & Providers</TabsTrigger>
                      </TabsList>
                    </div>

                    <ScrollArea className="flex-1">
                      <TabsContent value="variables" className="p-4 space-y-6 mt-0">
                        <div>
                          <h4 className="text-xs font-semibold text-muted-foreground uppercase tracking-wider mb-3">Active Session Info</h4>
                          <div className="space-y-2">
                            <div className="flex flex-col p-2 bg-muted rounded-md text-xs font-mono">
                              <span className="text-muted-foreground">Call ID</span>
                              <span className="text-foreground font-semibold mt-1">{activeCall.id}</span>
                            </div>
                            <div className="flex flex-col p-2 bg-muted rounded-md text-xs font-mono">
                              <span className="text-muted-foreground">Target Phone</span>
                              <span className="text-foreground font-semibold mt-1">{activeCall.phoneNumber}</span>
                            </div>
                          </div>
                        </div>

                        <div>
                          <h4 className="text-xs font-semibold text-muted-foreground uppercase tracking-wider mb-3">Configured Engine</h4>
                          <div className="space-y-3">
                            <div className="flex justify-between items-center text-sm">
                              <span className="text-muted-foreground">Voice Engine</span>
                              <span className="font-medium">gTTS (Google)</span>
                            </div>
                            <div className="flex justify-between items-center text-sm">
                              <span className="text-muted-foreground">LLM Engine</span>
                              <span className="font-medium">Gemini 2.5 Flash</span>
                            </div>
                          </div>
                        </div>
                      </TabsContent>
                    </ScrollArea>
                  </Tabs>
                </div>
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  )
}
