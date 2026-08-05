import { useEffect, useState } from "react"
import { useParams, useNavigate } from "react-router-dom"
import { motion } from "framer-motion"
import { PageHeader } from "@/components/ui/page-header"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { StatusIndicator } from "@/components/ui/status-indicator"
import { Progress } from "@/components/ui/progress"
import { ArrowLeft, Pause, Play, Phone, CheckCircle2, XCircle, StopCircle } from "lucide-react"


export function CampaignDetailPage() {
  const { id } = useParams()
  const navigate = useNavigate()
  
  const [data, setData] = useState({
    status: "loading",
    total_leads: 0,
    completed: 0,
    failed: 0,
    success_rate: 0,
    active_calls: 0
  })

  // MVP Mock Name
  const campaignName = "Enterprise AI Outreach"

  useEffect(() => {
    // Initial fetch
    fetch(`http://localhost:8000/api/v1/campaigns/${id}/progress`)
      .then(res => res.json())
      .then(d => setData(prev => ({ ...prev, ...d })))
      .catch(console.error)

    // WebSocket for live updates
    const ws = new WebSocket(`ws://localhost:8000/api/v1/campaigns/ws/${id}`)
    ws.onmessage = (event) => {
      const payload = JSON.parse(event.data)
      setData(prev => ({ ...prev, ...payload }))
    }
    return () => ws.close()
  }, [id])

  const handleAction = async (action: "start" | "pause" | "stop") => {
    try {
      await fetch(`http://localhost:8000/api/v1/campaigns/${id}/${action}`, {
        method: "POST"
      })
      // Optimistic update
      setData(prev => ({ 
        ...prev, 
        status: action === "start" ? "running" : action === "pause" ? "paused" : "completed" 
      }))
    } catch (e) {
      console.error(e)
    }
  }

  const progressValue = data.total_leads > 0 
    ? ((data.completed + data.failed) / data.total_leads) * 100 
    : 0

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="space-y-6"
    >
      <PageHeader
        title={campaignName}
        breadcrumbs={[
          { label: "Campaigns", href: "/campaigns" },
          { label: campaignName },
        ]}
        actions={
          <>
            <Button variant="outline" onClick={() => navigate("/campaigns")}>
              <ArrowLeft className="mr-2 h-4 w-4" /> Back
            </Button>
            
            {data.status === "paused" || data.status === "draft" ? (
              <Button onClick={() => handleAction("start")}>
                <Play className="mr-2 h-4 w-4" /> Start Campaign
              </Button>
            ) : data.status === "running" ? (
              <Button variant="secondary" onClick={() => handleAction("pause")} className="text-amber-600 bg-amber-50 hover:bg-amber-100 border-amber-200">
                <Pause className="mr-2 h-4 w-4" /> Pause Campaign
              </Button>
            ) : null}

            <Button variant="destructive" onClick={() => handleAction("stop")}>
              <StopCircle className="mr-2 h-4 w-4" /> Stop
            </Button>
          </>
        }
      />

      <div className="grid gap-6 md:grid-cols-3">
        {/* Main Status Card */}
        <Card className="md:col-span-2 border-primary/20 shadow-md">
          <CardContent className="p-6">
            <div className="flex items-center justify-between mb-8">
              <div className="space-y-1">
                <p className="text-sm font-medium text-muted-foreground">Current Status</p>
                <div className="flex items-center gap-2">
                  <StatusIndicator status={data.status === "running" ? "active" : "pending"} pulse={data.status === "running"} />
                  <span className="text-2xl font-bold capitalize">{data.status}</span>
                </div>
              </div>
              <div className="text-right space-y-1">
                <p className="text-sm font-medium text-muted-foreground">Completion Estimate</p>
                <p className="text-lg font-semibold">{data.status === "running" ? "~2 hours remaining" : "-"}</p>
              </div>
            </div>

            <div className="space-y-2">
              <div className="flex items-center justify-between text-sm">
                <span className="font-medium">{progressValue.toFixed(1)}% Completed</span>
                <span className="text-muted-foreground">{(data.completed + data.failed)} / {data.total_leads} leads called</span>
              </div>
              <Progress value={progressValue} className="h-3" />
            </div>

            <div className="grid grid-cols-3 gap-4 mt-8 pt-6 border-t">
              <div>
                <p className="text-sm text-muted-foreground mb-1">Assigned Agent</p>
                <div className="flex items-center gap-2 font-medium">
                  <div className="w-6 h-6 rounded-full bg-primary/10 text-primary flex items-center justify-center text-xs">A</div>
                  Auto Assigned
                </div>
              </div>
              <div>
                <p className="text-sm text-muted-foreground mb-1">Concurrency</p>
                <p className="font-medium">Up to 20 simultaneous</p>
              </div>
              <div>
                <p className="text-sm text-muted-foreground mb-1">Success Rate</p>
                <p className="font-medium text-primary">{data.success_rate}%</p>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Live Call Stats */}
        <div className="space-y-4">
          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium">Live Call Status</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <Phone className="h-4 w-4 text-blue-500" />
                  <span className="text-sm">Currently Active</span>
                </div>
                <span className="font-bold">{data.active_calls}</span>
              </div>
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <CheckCircle2 className="h-4 w-4 text-green-500" />
                  <span className="text-sm">Successful</span>
                </div>
                <span className="font-bold text-green-600">{data.completed}</span>
              </div>
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <XCircle className="h-4 w-4 text-red-500" />
                  <span className="text-sm">Failed / Busy</span>
                </div>
                <span className="font-bold">{data.failed}</span>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </motion.div>
  )
}
