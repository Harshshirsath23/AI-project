import * as React from "react"
import { useNavigate } from "react-router-dom"
import { motion, AnimatePresence } from "framer-motion"
import { PageHeader } from "@/components/ui/page-header"
import { Card, CardContent } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { ArrowLeft, ArrowRight, Bot, Mic, Sparkles, Loader2, Check } from "lucide-react"

import { api } from "@/services/api"

const steps = [
  { id: "basics", title: "Basic Info", icon: Bot },
  { id: "voice", title: "Voice Setup", icon: Mic },
  { id: "prompt", title: "Behavior", icon: Sparkles },
]

export function NewAgentPage() {
  const navigate = useNavigate()
  const [currentStep, setCurrentStep] = React.useState(0)
  const [name, setName] = React.useState("")
  const [description, setDescription] = React.useState("Outbound Sales SDR Agent")
  const [selectedVoice, setSelectedVoice] = React.useState<any>(null)
  const [systemPrompt, setSystemPrompt] = React.useState("You are a helpful AI voice sales agent for Voxera. Assist the customer professionally.")
  const [greetingMessage, setGreetingMessage] = React.useState("Hello! Thank you for taking my call. How can I help you today?")
  const [voices, setVoices] = React.useState<any[]>([])
  const [knowledgeBases, setKnowledgeBases] = React.useState<any[]>([])
  const [selectedKbId, setSelectedKbId] = React.useState<string>("")
  const [isSubmitting, setIsSubmitting] = React.useState(false)
  const [kbDocs, setKbDocs] = React.useState<any[]>([])


  React.useEffect(() => {
    api.getVoices()
      .then((data) => {
        setVoices(data)
        if (data.length > 0) setSelectedVoice(data[0])
      })
      .catch((err) => console.error("Error loading voices:", err))

    api.getKnowledgeBases()
      .then((kbs) => {
        setKnowledgeBases(kbs)
        if (kbs.length > 0) setSelectedKbId(kbs[0].id)
      })
      .catch((err) => console.error("Error loading KB:", err))

    api.getAllKnowledgeDocuments()
      .then((docs) => setKbDocs(docs))
      .catch((err) => console.error("Error loading KB docs:", err))
  }, [])


  const handleNext = async () => {
    if (currentStep < steps.length - 1) {
      setCurrentStep(c => c + 1)
    } else {
      setIsSubmitting(true)
      try {
        await api.createAgent({
          name: name || "New Voice Agent",
          description,
          default_language: selectedVoice?.language || "en-US",
          llm_provider: "gemini",
          stt_provider: "faster-whisper",
          tts_provider: selectedVoice?.engine || "gtts",
          system_prompt: systemPrompt,
          greeting_message: greetingMessage,
          knowledge_base_id: selectedKbId,
          voice_profile: {
            voice_id: selectedVoice?.id || "gtts-en",
            voice_name: selectedVoice?.name || "Google gTTS Voice",
            voice_gender: selectedVoice?.gender || "female",
            voice_accent: "US",
            pitch: 1.0,
            speed: 1.0,
          }
        })
        navigate("/agents")
      } catch (err) {
        console.error("Error creating agent:", err)
        navigate("/agents")
      } finally {
        setIsSubmitting(false)
      }
    }
  }


  const handleBack = () => {
    if (currentStep > 0) {
      setCurrentStep(c => c - 1)
    } else {
      navigate("/agents")
    }
  }

  return (
    <div className="max-w-3xl mx-auto space-y-8 pb-12">
      <PageHeader
        title="Create AI Agent"
        description="Configure a new voice assistant for your campaigns."
        breadcrumbs={[
          { label: "Agents", href: "/agents" },
          { label: "New Agent" },
        ]}
      />

      {/* Stepper */}
      <div className="flex items-center justify-between relative mb-8">
        <div className="absolute left-0 right-0 top-1/2 h-0.5 bg-border -z-10 -translate-y-1/2" />
        {steps.map((step, index) => {
          const isActive = index === currentStep
          const isPassed = index < currentStep
          return (
            <div key={step.id} className="flex flex-col items-center gap-2 bg-background px-2">
              <motion.div
                className={`w-10 h-10 rounded-full flex items-center justify-center border-2 transition-colors duration-300 ${
                  isActive ? "border-primary bg-primary text-primary-foreground" :
                  isPassed ? "border-primary bg-primary text-primary-foreground" :
                  "border-muted bg-card text-muted-foreground"
                }`}
                animate={{ scale: isActive ? 1.1 : 1 }}
              >
                {isPassed ? <Check className="h-5 w-5" /> : <step.icon className="h-5 w-5" />}
              </motion.div>
              <span className={`text-xs font-medium ${isActive ? "text-primary" : "text-muted-foreground"}`}>
                {step.title}
              </span>
            </div>
          )
        })}
      </div>

      {/* Form Content */}
      <Card className="overflow-hidden border-2">
        <CardContent className="p-0">
          <AnimatePresence mode="wait">
            <motion.div
              key={currentStep}
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
              transition={{ duration: 0.2 }}
              className="p-8 space-y-6 min-h-[400px]"
            >
              {currentStep === 0 && (
                <div className="space-y-4">
                  <div>
                    <h3 className="text-lg font-semibold">Basic Information</h3>
                    <p className="text-sm text-muted-foreground">Give your agent a name and primary role.</p>
                  </div>
                  <div className="space-y-4 max-w-md">
                    <div className="space-y-2">
                      <Label htmlFor="name">Agent Name</Label>
                      <Input 
                        id="name" 
                        placeholder="e.g. Sarah - Sales SDR" 
                        value={name} 
                        onChange={(e) => setName(e.target.value)} 
                        autoFocus 
                      />
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="desc">Description</Label>
                      <Input 
                        id="desc" 
                        placeholder="Purpose of this agent" 
                        value={description} 
                        onChange={(e) => setDescription(e.target.value)} 
                      />
                    </div>
                  </div>
                </div>
              )}

              {currentStep === 1 && (
                <div className="space-y-4">
                  <div>
                    <h3 className="text-lg font-semibold">Voice Setup</h3>
                    <p className="text-sm text-muted-foreground">Select how your AI agent sounds (TTS Provider Engine).</p>
                  </div>
                  <div className="grid sm:grid-cols-2 gap-4">
                    {voices.map((v) => (
                      <div
                        key={v.id}
                        onClick={() => setSelectedVoice(v)}
                        className={`p-4 rounded-xl border-2 cursor-pointer transition-all ${
                          selectedVoice?.id === v.id ? "border-primary bg-primary/5 shadow-sm" : "border-muted hover:border-primary/50"
                        }`}
                      >
                        <div className="flex items-center justify-between mb-2">
                          <span className="font-semibold text-sm">{v.name}</span>
                        </div>
                        <div className="flex gap-2 text-xs text-muted-foreground">
                          <span className="bg-muted px-2 py-1 rounded capitalize">{v.engine}</span>
                          <span className="bg-muted px-2 py-1 rounded capitalize">{v.gender}</span>
                          <span className="bg-muted px-2 py-1 rounded">{v.language}</span>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {currentStep === 2 && (
                <div className="space-y-4">
                  <div>
                    <h3 className="text-lg font-semibold">Behavior & Prompt</h3>
                    <p className="text-sm text-muted-foreground">Instruct your agent on how to handle conversations.</p>
                  </div>
                  <div className="space-y-4">
                    <div className="space-y-2">
                      <Label>Initial Greeting Message</Label>
                      <Input 
                        value={greetingMessage} 
                        onChange={(e) => setGreetingMessage(e.target.value)} 
                      />
                    </div>
                    <div className="space-y-2">
                      <Label>Assign Knowledge Base / Script Document</Label>
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
                          <SelectValue placeholder="Select Knowledge Base Script Document" />
                        </SelectTrigger>
                        <SelectContent>
                          {kbDocs.length > 0 ? (
                            kbDocs.map((doc: any) => (
                              <SelectItem key={doc.id} value={doc.id}>📄 {doc.title}</SelectItem>
                            ))
                          ) : (
                            knowledgeBases.map((kb: any) => (
                              <SelectItem key={kb.id} value={kb.id}>{kb.name} ({kb.document_count || 1} scripts)</SelectItem>
                            ))
                          )}

                        </SelectContent>
                      </Select>

                    </div>
                    <div className="space-y-2">
                      <Label>System Prompt (LLM Instructions)</Label>
                      <Textarea 
                        value={systemPrompt}
                        onChange={(e) => setSystemPrompt(e.target.value)}
                        className="min-h-[160px] font-mono text-sm"
                      />
                    </div>
                  </div>
                </div>
              )}

            </motion.div>
          </AnimatePresence>
        </CardContent>
        <div className="p-6 bg-muted/30 border-t flex items-center justify-between">
          <Button variant="ghost" onClick={handleBack}>
            {currentStep === 0 ? "Cancel" : <><ArrowLeft className="mr-2 h-4 w-4" /> Back</>}
          </Button>
          <Button onClick={handleNext} disabled={isSubmitting} className={currentStep === steps.length - 1 ? "gradient-primary text-white" : ""}>
            {isSubmitting ? <Loader2 className="h-4 w-4 animate-spin mr-2" /> : null}
            {currentStep === steps.length - 1 ? "Create Agent" : <>Next Step <ArrowRight className="ml-2 h-4 w-4" /></>}
          </Button>
        </div>
      </Card>
    </div>
  )
}

