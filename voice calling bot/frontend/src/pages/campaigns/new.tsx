import * as React from "react"
import { motion } from "framer-motion"
import { useNavigate } from "react-router-dom"
import { PageHeader } from "@/components/ui/page-header"
import { Card, CardContent } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Badge } from "@/components/ui/badge"
import { Bot, Users, Activity, Rocket, ArrowRight, ArrowLeft, Phone } from "lucide-react"
import { api } from "@/services/api"

const steps = [
  { id: 1, name: "Name & Settings" },
  { id: 2, name: "Choose Agent" },
  { id: 3, name: "Phone & Leads" },
  { id: 4, name: "Schedule" },
  { id: 5, name: "Concurrency" },
  { id: 6, name: "Launch" }
]

export function NewCampaignPage() {
  const navigate = useNavigate()
  const [currentStep, setCurrentStep] = React.useState(1)
  
  // Data from backend
  const [agents, setAgents] = React.useState<any[]>([])
  const [phoneNumbers, setPhoneNumbers] = React.useState<any[]>([])
  const [leads, setLeads] = React.useState<any[]>([])

  // Form state
  const [name, setName] = React.useState("")
  const [description, setDescription] = React.useState("")
  const [selectedAgentId, setSelectedAgentId] = React.useState<string>("")
  const [selectedFromNumber, setSelectedFromNumber] = React.useState<string>("")
  const [selectedLeadIds, setSelectedLeadIds] = React.useState<string[]>([])
  const [maxConcurrentCalls, setMaxConcurrentCalls] = React.useState<number>(5)
  const [isSubmitting, setIsSubmitting] = React.useState(false)

  React.useEffect(() => {
    api.getAgents().then(res => {
      setAgents(res)
      if (res.length > 0) setSelectedAgentId(res[0].id)
    }).catch(err => console.error(err))

    api.getPhoneNumbers().then(res => {
      setPhoneNumbers(res)
      if (res.length > 0) setSelectedFromNumber(res[0].number)
    }).catch(err => console.error(err))

    api.getLeads().then(res => {
      setLeads(res)
      setSelectedLeadIds(res.map((l: any) => l.id))
    }).catch(err => console.error(err))
  }, [])

  const handleLaunch = async () => {
    if (!name) {
      alert("Please provide a campaign name.")
      setCurrentStep(1)
      return
    }
    setIsSubmitting(true)
    try {
      await api.createCampaign({
        name,
        description,
        agent_id: selectedAgentId,
        from_number: selectedFromNumber,
        lead_ids: selectedLeadIds,
        max_concurrent_calls: maxConcurrentCalls
      })
      navigate('/campaigns')
    } catch (err) {
      console.error("Failed to launch campaign:", err)
      alert("Error launching campaign")
    } finally {
      setIsSubmitting(false)
    }
  }

  const selectedAgent = agents.find(a => a.id === selectedAgentId)

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-6 max-w-4xl mx-auto pb-12">
      <PageHeader
        title="Create Campaign"
        description="Launch a new outbound calling campaign in 6 simple steps."
      />

      {/* Progress Bar */}
      <div className="flex items-center justify-between mb-8 relative">
        <div className="absolute left-0 right-0 top-1/2 -translate-y-1/2 h-0.5 bg-muted z-0" />
        <div 
          className="absolute left-0 top-1/2 -translate-y-1/2 h-0.5 bg-primary z-0 transition-all duration-300" 
          style={{ width: `${((currentStep - 1) / (steps.length - 1)) * 100}%` }}
        />
        {steps.map((step) => (
          <div key={step.id} className="relative z-10 flex flex-col items-center gap-2">
            <div className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-semibold transition-colors duration-300 ${
              currentStep >= step.id 
                ? 'bg-primary text-primary-foreground border-2 border-background shadow-[0_0_0_2px_hsl(var(--primary))]' 
                : 'bg-muted text-muted-foreground border-2 border-background shadow-[0_0_0_2px_hsl(var(--muted))]'
            }`}>
              {step.id}
            </div>
            <span className={`text-xs font-medium absolute -bottom-6 w-max ${currentStep >= step.id ? 'text-foreground' : 'text-muted-foreground'}`}>
              {step.name}
            </span>
          </div>
        ))}
      </div>

      <Card className="mt-12">
        <CardContent className="p-8">
          <div className="min-h-[300px]">
            {currentStep === 1 && (
              <motion.div initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} className="space-y-4">
                <h2 className="text-xl font-semibold mb-6">Campaign Settings</h2>
                <div className="space-y-2">
                  <label className="text-sm font-medium">Campaign Name</label>
                  <Input 
                    placeholder="e.g. Q3 Enterprise Outreach" 
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                  />
                </div>
                <div className="space-y-2">
                  <label className="text-sm font-medium">Description (Optional)</label>
                  <Input 
                    placeholder="Internal notes about this campaign" 
                    value={description}
                    onChange={(e) => setDescription(e.target.value)}
                  />
                </div>
              </motion.div>
            )}

            {currentStep === 2 && (
              <motion.div initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} className="space-y-4">
                <h2 className="text-xl font-semibold mb-6">Choose AI Agent</h2>
                <div className="grid grid-cols-2 gap-4">
                  {agents.length === 0 ? (
                    <p className="text-muted-foreground col-span-2">No agents found. Using default SDR Agent.</p>
                  ) : (
                    agents.map((agent) => (
                      <div 
                        key={agent.id} 
                        onClick={() => setSelectedAgentId(agent.id)}
                        className={`p-4 border rounded-xl cursor-pointer transition-all ${
                          selectedAgentId === agent.id ? 'border-primary bg-primary/5' : 'hover:border-primary/50'
                        }`}
                      >
                        <div className="flex items-center gap-3 mb-2">
                          <div className="w-8 h-8 rounded-full bg-primary/10 text-primary flex items-center justify-center">
                            <Bot className="h-4 w-4" />
                          </div>
                          <span className="font-semibold">{agent.name}</span>
                        </div>
                        <p className="text-sm text-muted-foreground">{agent.description || "Voice SDR Agent"}</p>
                      </div>
                    ))
                  )}
                </div>
              </motion.div>
            )}

            {currentStep === 3 && (
              <motion.div initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} className="space-y-6">
                <div>
                  <h2 className="text-xl font-semibold mb-2">Select Outbound Phone Number</h2>
                  <div className="grid grid-cols-2 gap-3">
                    {phoneNumbers.length === 0 ? (
                      <div className="p-3 border rounded-lg bg-muted text-sm text-muted-foreground">
                        Default Twilio Outbound (+17372212163)
                      </div>
                    ) : (
                      phoneNumbers.map((p) => (
                        <div
                          key={p.id}
                          onClick={() => setSelectedFromNumber(p.number)}
                          className={`p-3 border rounded-lg cursor-pointer flex items-center gap-2 ${
                            selectedFromNumber === p.number ? 'border-primary bg-primary/5 font-medium' : ''
                          }`}
                        >
                          <Phone className="h-4 w-4 text-primary" />
                          <span>{p.number} ({p.provider})</span>
                        </div>
                      ))
                    )}
                  </div>
                </div>

                <div>
                  <h2 className="text-xl font-semibold mb-2">Target Lead List</h2>
                  <div className="p-4 border rounded-xl border-primary bg-primary/5 flex items-center justify-between">
                    <div className="flex items-center gap-3">
                      <div className="w-8 h-8 rounded-full bg-primary/10 text-primary flex items-center justify-center">
                        <Users className="h-4 w-4" />
                      </div>
                      <div>
                        <p className="font-semibold">All Inbound & Import Leads</p>
                        <p className="text-sm text-muted-foreground">{leads.length} total leads targeted</p>
                      </div>
                    </div>
                    <Badge>Selected</Badge>
                  </div>
                </div>
              </motion.div>
            )}

            {currentStep === 4 && (
              <motion.div initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} className="space-y-4">
                <h2 className="text-xl font-semibold mb-6">Calling Schedule</h2>
                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <label className="text-sm font-medium">Timezone</label>
                    <Input defaultValue="America/New_York (EST)" readOnly className="bg-muted" />
                  </div>
                  <div className="space-y-2">
                    <label className="text-sm font-medium">Calling Hours Window</label>
                    <Input defaultValue="09:00 AM - 05:00 PM" readOnly className="bg-muted" />
                  </div>
                </div>
              </motion.div>
            )}

            {currentStep === 5 && (
              <motion.div initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} className="space-y-4">
                <h2 className="text-xl font-semibold mb-6">Concurrency Settings</h2>
                <div className="space-y-2">
                  <label className="text-sm font-medium flex items-center gap-2">
                    <Activity className="h-4 w-4" /> Max Concurrent Calls
                  </label>
                  <Input 
                    type="number" 
                    value={maxConcurrentCalls} 
                    onChange={(e) => setMaxConcurrentCalls(Number(e.target.value))}
                  />
                  <p className="text-xs text-muted-foreground mt-1">Number of active calls being placed simultaneously.</p>
                </div>
              </motion.div>
            )}

            {currentStep === 6 && (
              <motion.div initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} className="flex flex-col items-center justify-center min-h-[300px] text-center space-y-4">
                <div className="w-20 h-20 rounded-full bg-green-500/10 text-green-500 flex items-center justify-center mb-4">
                  <Rocket className="h-10 w-10" />
                </div>
                <h2 className="text-2xl font-bold">Ready to Launch!</h2>
                <p className="text-muted-foreground max-w-[400px]">
                  You are about to launch <span className="font-semibold text-foreground">{name || "New Campaign"}</span> targeting <span className="font-semibold text-foreground">{leads.length} leads</span> using <span className="font-semibold text-foreground">{selectedAgent?.name || "Voice SDR Agent"}</span>.
                </p>
              </motion.div>
            )}
          </div>
        </CardContent>
        <div className="p-6 border-t bg-muted/20 flex justify-between rounded-b-xl">
          <Button 
            variant="outline" 
            onClick={() => setCurrentStep(prev => Math.max(1, prev - 1))}
            disabled={currentStep === 1 || isSubmitting}
          >
            <ArrowLeft className="mr-2 h-4 w-4" /> Back
          </Button>
          
          {currentStep < 6 ? (
            <Button onClick={() => setCurrentStep(prev => Math.min(6, prev + 1))}>
              Next Step <ArrowRight className="ml-2 h-4 w-4" />
            </Button>
          ) : (
            <Button className="bg-green-600 hover:bg-green-700 text-white" onClick={handleLaunch} disabled={isSubmitting}>
              <Rocket className="mr-2 h-4 w-4" /> {isSubmitting ? "Launching..." : "Launch Campaign"}
            </Button>
          )}
        </div>
      </Card>
    </motion.div>
  )
}
