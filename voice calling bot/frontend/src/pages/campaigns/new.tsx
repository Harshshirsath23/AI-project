import * as React from "react"
import { motion } from "framer-motion"
import { useNavigate } from "react-router-dom"
import { PageHeader } from "@/components/ui/page-header"
import { Card, CardContent } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Badge } from "@/components/ui/badge"
import { Bot, Users, Calendar, Activity, Rocket, ArrowRight, ArrowLeft } from "lucide-react"

const steps = [
  { id: 1, name: "Name & Settings" },
  { id: 2, name: "Choose Agent" },
  { id: 3, name: "Lead List" },
  { id: 4, name: "Schedule" },
  { id: 5, name: "Concurrency" },
  { id: 6, name: "Launch" }
]

export function NewCampaignPage() {
  const navigate = useNavigate()
  const [currentStep, setCurrentStep] = React.useState(1)

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
                  <Input placeholder="e.g. Q3 Enterprise Outreach" />
                </div>
                <div className="space-y-2">
                  <label className="text-sm font-medium">Description (Optional)</label>
                  <Input placeholder="Internal notes about this campaign" />
                </div>
              </motion.div>
            )}

            {currentStep === 2 && (
              <motion.div initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} className="space-y-4">
                <h2 className="text-xl font-semibold mb-6">Choose AI Agent</h2>
                <div className="grid grid-cols-2 gap-4">
                  {[
                    { name: 'Sales SDR (Outbound)', desc: 'Qualifies inbound leads and books demos.' },
                    { name: 'Billing Support', desc: 'Handles failed payments.' }
                  ].map((agent, i) => (
                    <div key={i} className={`p-4 border rounded-xl cursor-pointer transition-all ${i===0 ? 'border-primary bg-primary/5' : 'hover:border-primary/50'}`}>
                      <div className="flex items-center gap-3 mb-2">
                        <div className="w-8 h-8 rounded-full bg-primary/10 text-primary flex items-center justify-center">
                          <Bot className="h-4 w-4" />
                        </div>
                        <span className="font-semibold">{agent.name}</span>
                      </div>
                      <p className="text-sm text-muted-foreground">{agent.desc}</p>
                    </div>
                  ))}
                </div>
              </motion.div>
            )}

            {currentStep === 3 && (
              <motion.div initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} className="space-y-4">
                <h2 className="text-xl font-semibold mb-6">Select Lead List</h2>
                <div className="p-4 border rounded-xl cursor-pointer border-primary bg-primary/5 flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <div className="w-8 h-8 rounded-full bg-primary/10 text-primary flex items-center justify-center">
                      <Users className="h-4 w-4" />
                    </div>
                    <div>
                      <p className="font-semibold">Q3 Webinar Signups</p>
                      <p className="text-sm text-muted-foreground">1,245 leads ready to call</p>
                    </div>
                  </div>
                  <Badge>Selected</Badge>
                </div>
                <Button variant="outline" className="w-full mt-4 border-dashed border-2 py-8">
                  Import New Leads (CSV)
                </Button>
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
                    <label className="text-sm font-medium">Start Date</label>
                    <div className="relative">
                      <Calendar className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                      <Input defaultValue="Oct 12, 2024" className="pl-9" />
                    </div>
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
                  <Input type="number" defaultValue={50} />
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
                  You are about to launch <span className="font-semibold text-foreground">Q3 Enterprise Outreach</span> with <span className="font-semibold text-foreground">1,245 leads</span> using <span className="font-semibold text-foreground">Sales SDR (Outbound)</span>.
                </p>
              </motion.div>
            )}
          </div>
        </CardContent>
        <div className="p-6 border-t bg-muted/20 flex justify-between rounded-b-xl">
          <Button 
            variant="outline" 
            onClick={() => setCurrentStep(prev => Math.max(1, prev - 1))}
            disabled={currentStep === 1}
          >
            <ArrowLeft className="mr-2 h-4 w-4" /> Back
          </Button>
          
          {currentStep < 6 ? (
            <Button onClick={() => setCurrentStep(prev => Math.min(6, prev + 1))}>
              Next Step <ArrowRight className="ml-2 h-4 w-4" />
            </Button>
          ) : (
            <Button className="bg-green-600 hover:bg-green-700 text-white" onClick={() => navigate('/campaigns')}>
              <Rocket className="mr-2 h-4 w-4" /> Launch Campaign
            </Button>
          )}
        </div>
      </Card>
    </motion.div>
  )
}
