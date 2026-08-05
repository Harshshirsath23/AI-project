import * as React from "react"
import { useParams, useNavigate } from "react-router-dom"
import { PageHeader } from "@/components/ui/page-header"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Badge } from "@/components/ui/badge"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Save, Mic, BookOpen, BrainCircuit, Activity, Settings, ArrowLeft, Loader2, CheckCircle2 } from "lucide-react"

import { api } from "@/services/api"

export function AgentDetailPage() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const [knowledgeBases, setKnowledgeBases] = React.useState<any[]>([])
  const [kbDocs, setKbDocs] = React.useState<any[]>([])
  const [selectedKbId, setSelectedKbId] = React.useState<string>("")
  const [name, setName] = React.useState("")
  const [description, setDescription] = React.useState("")
  const [systemPrompt, setSystemPrompt] = React.useState("")
  const [greetingMessage, setGreetingMessage] = React.useState("")
  const [isSaving, setIsSaving] = React.useState(false)
  const [saveNotice, setSaveNotice] = React.useState<string | null>(null)

  React.useEffect(() => {
    // Load Knowledge Bases
    api.getKnowledgeBases()
      .then(kbs => setKnowledgeBases(kbs))
      .catch((e: any) => console.error("Error loading KBs:", e))

    api.getAllKnowledgeDocuments()
      .then((docs) => setKbDocs(docs))
      .catch((e: any) => console.error("Error loading KB docs:", e))

    // Load Agent Details
    if (id) {
      api.getAgentDetail(id)
        .then((ag: any) => {
          setName(ag.name || "Sales SDR (Outbound)")
          setDescription(ag.description || "")
          setSystemPrompt(ag.system_prompt || "")
          setGreetingMessage(ag.greeting_message || "")
          setSelectedKbId(ag.knowledge_base_id || "")
        })
        .catch((e: any) => console.error("Error loading agent:", e))
    }
  }, [id])


  const handleSave = async () => {
    if (!id) return
    setIsSaving(true)
    try {
      await api.updateAgent(id, {
        name,
        description,
        system_prompt: systemPrompt,
        greeting_message: greetingMessage,
        knowledge_base_id: selectedKbId,
      })
      setSaveNotice("✅ Agent configuration saved successfully to PostgreSQL!")
      setTimeout(() => setSaveNotice(null), 3000)
    } catch (e: any) {
      setSaveNotice(`⚠️ Save error: ${e.message || "Failed to update agent"}`)
    } finally {
      setIsSaving(false)
    }
  }

  return (
    <div className="flex flex-col h-[calc(100vh-4rem)] -m-6 bg-muted/10">
      <div className="border-b bg-card p-6 flex-shrink-0 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <Button variant="ghost" size="icon" onClick={() => navigate("/agents")}>
            <ArrowLeft className="h-5 w-5" />
          </Button>
          <PageHeader
            title={name || "Configure Agent"}
            description="Manage AI personality, voice, phone numbers, scripts, and assigned Knowledge Base."
          />
        </div>
        <div className="flex gap-3">
          <Button onClick={handleSave} disabled={isSaving}>
            {isSaving ? <Loader2 className="mr-2 h-4 w-4 animate-spin" /> : <Save className="mr-2 h-4 w-4" />}
            Save Configuration
          </Button>
        </div>
      </div>

      {saveNotice && (
        <div className="p-3 bg-muted border-b border-primary/20 text-xs font-mono text-center flex items-center justify-center gap-2">
          <CheckCircle2 className="h-4 w-4 text-green-500" />
          {saveNotice}
        </div>
      )}

      <div className="flex-1 overflow-y-auto p-8">
        <Tabs defaultValue="basic" className="max-w-5xl mx-auto flex flex-col h-full">
          <TabsList className="grid w-full grid-cols-5 mb-8">
            <TabsTrigger value="basic">General</TabsTrigger>
            <TabsTrigger value="script">Scripts & Prompt</TabsTrigger>
            <TabsTrigger value="knowledge">Assigned Script KB</TabsTrigger>
            <TabsTrigger value="voice">Voice & AI</TabsTrigger>
            <TabsTrigger value="rules">Calling Rules</TabsTrigger>
          </TabsList>

          <TabsContent value="basic" className="space-y-6 m-0">
            <Card>
              <CardHeader>
                <CardTitle>Basic Information</CardTitle>
                <CardDescription>The core identity of your AI agent.</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <label className="text-sm font-medium">Agent Name</label>
                    <Input value={name} onChange={(e) => setName(e.target.value)} />
                  </div>
                  <div className="space-y-2">
                    <label className="text-sm font-medium">Status</label>
                    <div className="flex items-center h-10 px-3 border rounded-md bg-muted/50">
                      <Badge variant="secondary" className="bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400">Active</Badge>
                    </div>
                  </div>
                </div>
                <div className="space-y-2">
                  <label className="text-sm font-medium">Description</label>
                  <Textarea value={description} onChange={(e) => setDescription(e.target.value)} className="h-20" />
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="script" className="space-y-6 m-0">
            <Card className="h-full flex flex-col">
              <CardHeader>
                <CardTitle className="flex items-center gap-2"><Activity className="h-5 w-5 text-primary" /> System Prompt & Script</CardTitle>
                <CardDescription>Define how the agent speaks and handles objections.</CardDescription>
              </CardHeader>
              <CardContent className="flex-1 space-y-6">
                <div className="space-y-2">
                  <label className="text-sm font-medium">System Prompt (LLM Persona & Persona Rules)</label>
                  <Textarea className="h-32 font-mono text-sm" value={systemPrompt} onChange={(e) => setSystemPrompt(e.target.value)} />
                </div>
                <div className="space-y-2">
                  <label className="text-sm font-medium">Greeting Message</label>
                  <Textarea className="h-20 font-mono text-sm" value={greetingMessage} onChange={(e) => setGreetingMessage(e.target.value)} />
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="knowledge" className="space-y-6 m-0">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2"><BookOpen className="h-5 w-5 text-primary" /> Assigned Knowledge Base Script Document</CardTitle>
                <CardDescription>Select which Knowledge Base script document belongs to this specific Agent.</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="space-y-2">
                  <label className="text-sm font-semibold">Select Knowledge Base Script</label>
                  <Select value={selectedKbId} onValueChange={(val) => {
                    setSelectedKbId(val)
                    const doc = kbDocs.find(d => d.kb_id === val || d.id === val)
                    if (doc) {
                      if (doc.title.toLowerCase().includes("recruitment") || doc.title.toLowerCase().includes("ai/ml") || doc.title.toLowerCase().includes("screening")) {
                        setGreetingMessage("Hello, am I speaking with {Candidate Name}?")
                        setSystemPrompt("You are Sarah, a professional AI Talent Acquisition Specialist calling candidate {Candidate Name} regarding the AI/ML Engineer position at Innovate AI Labs.")
                      }
                    }
                  }}>
                    <SelectTrigger className="w-full text-xs">
                      <SelectValue placeholder="Select Knowledge Base Script" />
                    </SelectTrigger>
                    <SelectContent>
                      {kbDocs.length > 0 ? (
                        kbDocs.map((doc: any) => (
                          <SelectItem key={doc.id} value={doc.id}>📄 {doc.title}</SelectItem>
                        ))
                      ) : (
                        knowledgeBases.map((kb: any) => (
                          <SelectItem key={kb.id} value={kb.id}>{kb.name} ({kb.description || "Knowledge Script"})</SelectItem>
                        ))
                      )}

                    </SelectContent>
                  </Select>

                </div>
                <p className="text-xs text-muted-foreground font-mono">
                  Assigned KB ID: <span className="text-primary font-bold">{selectedKbId || "None (Uses Default)"}</span>
                </p>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="voice" className="space-y-6 m-0">
            <div className="grid grid-cols-2 gap-6">
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2"><Mic className="h-5 w-5 text-primary" /> Voice Engine</CardTitle>
                  <CardDescription>Google gTTS + 8kHz mono mu-law conversion.</CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="space-y-2">
                    <label className="text-sm font-medium">Provider Engine</label>
                    <Input defaultValue="gTTS (Google TTS) + MiniAudio" readOnly className="bg-muted text-xs font-mono" />
                  </div>
                  <div className="space-y-2">
                    <label className="text-sm font-medium">Voice Codec</label>
                    <Input defaultValue="8000 Hz 8-bit mu-law (audio/x-mulaw)" readOnly className="bg-muted text-xs font-mono" />
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2"><BrainCircuit className="h-5 w-5 text-primary" /> AI Model (LLM)</CardTitle>
                  <CardDescription>Real-time speech reasoning.</CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="space-y-2">
                    <label className="text-sm font-medium">Model</label>
                    <Input defaultValue="Gemini 2.5 Flash (Google DeepMind)" readOnly className="bg-muted text-xs font-mono" />
                  </div>
                </CardContent>
              </Card>
            </div>
          </TabsContent>

          <TabsContent value="rules" className="space-y-6 m-0">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2"><Settings className="h-5 w-5 text-primary" /> Calling Rules</CardTitle>
                <CardDescription>Configuring dialing parameters and limits.</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <label className="text-sm font-medium">Max Call Duration (minutes)</label>
                    <Input type="number" defaultValue={10} />
                  </div>
                  <div className="space-y-2">
                    <label className="text-sm font-medium">Rings Before Hangup</label>
                    <Input type="number" defaultValue={6} />
                  </div>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

        </Tabs>
      </div>
    </div>
  )
}
