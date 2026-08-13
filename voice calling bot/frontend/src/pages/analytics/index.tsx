import { motion } from "framer-motion"
import { PageHeader } from "@/components/ui/page-header"
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { StatCard } from "@/components/ui/stat-card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Activity, Users, Phone, DollarSign, Smile, Frown, Meh, Sparkles } from "lucide-react"
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar, Legend, PieChart, Pie, Cell } from 'recharts'
import * as React from "react"
import { api } from "@/services/api"
import { Progress } from "@/components/ui/progress"

import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle } from "@/components/ui/dialog"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Bot, User, PhoneCall, FileText } from "lucide-react"

export function AnalyticsPage() {
  const [data, setData] = React.useState<any>(null)
  const [calls, setCalls] = React.useState<any[]>([])
  const [selectedCall, setSelectedCall] = React.useState<any | null>(null)
  const [isDialogOpen, setIsDialogOpen] = React.useState(false)
  const [loading, setLoading] = React.useState<boolean>(true)

  React.useEffect(() => {
    Promise.all([api.getAnalytics(), api.getCalls()])
      .then(([res, callList]) => {
        setData(res)
        setCalls(callList || [])
      })
      .catch(err => console.error("Error loading analytics:", err))
      .finally(() => setLoading(false))
  }, [])

  const m = data?.metrics || {
    total_calls: 0,
    success_rate: 0.0,
    active_campaigns: 0,
    avg_duration_seconds: 0
  }

  const sentiment = data?.sentiment_breakdown || {
    positive: 0,
    neutral: 0,
    negative: 0
  }

  const chartData = data?.chart_data || []

  const providerData = [
    { name: 'gTTS (Google)', calls: m.total_calls || 0, cost: 0.00 },
    { name: 'Gemini 2.5 Flash', calls: m.total_calls || 0, cost: 0.00 },
  ]

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-6 pb-12">
      <PageHeader
        title="Analytics & Reporting"
        description="Comprehensive insights into your AI calling operations, customer sentiment, and transcripts."
      />

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <StatCard title="Total Calls" value={loading ? "..." : m.total_calls.toLocaleString()} icon={Phone} />
        <StatCard title="Overall Success Rate" value={loading ? "..." : `${m.success_rate}%`} icon={Activity} />
        <StatCard title="Interested / Positive" value={loading ? "..." : `${sentiment.positive}%`} icon={Smile} />
        <StatCard title="Avg Duration" value={loading ? "..." : `${m.avg_duration_seconds}s`} icon={DollarSign} />
      </div>

      <Tabs defaultValue="overview" className="space-y-6">
        <TabsList className="bg-card border h-12 p-1">
          <TabsTrigger value="overview" className="data-[state=active]:bg-primary/10 data-[state=active]:text-primary">Overview</TabsTrigger>
          <TabsTrigger value="sentiment" className="data-[state=active]:bg-primary/10 data-[state=active]:text-primary">AI Sentiment & Intent</TabsTrigger>
          <TabsTrigger value="providers" className="data-[state=active]:bg-primary/10 data-[state=active]:text-primary">Provider Usage & Cost</TabsTrigger>
        </TabsList>

        <TabsContent value="overview" className="space-y-6">
          <Card className="border-2 shadow-sm">
            <CardHeader>
              <CardTitle>Call Volume vs. Success</CardTitle>
              <CardDescription>Daily breakdown of total outbound calls compared to successful conversions.</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="h-[400px] w-full">
                {chartData.length === 0 ? (
                  <div className="h-full flex items-center justify-center text-xs text-muted-foreground">
                    No analytics call volume recorded yet.
                  </div>
                ) : (
                  <ResponsiveContainer width="100%" height="100%">
                    <AreaChart data={chartData} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
                      <defs>
                        <linearGradient id="colorCalls" x1="0" y1="0" x2="0" y2="1">
                          <stop offset="5%" stopColor="#8b5cf6" stopOpacity={0.3}/>
                          <stop offset="95%" stopColor="#8b5cf6" stopOpacity={0}/>
                        </linearGradient>
                        <linearGradient id="colorSuccess" x1="0" y1="0" x2="0" y2="1">
                          <stop offset="5%" stopColor="#10b981" stopOpacity={0.3}/>
                          <stop offset="95%" stopColor="#10b981" stopOpacity={0}/>
                        </linearGradient>
                      </defs>
                      <XAxis dataKey="name" stroke="#888888" fontSize={12} tickLine={false} axisLine={false} />
                      <YAxis stroke="#888888" fontSize={12} tickLine={false} axisLine={false} />
                      <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e5e7eb" />
                      <Tooltip
                        contentStyle={{ borderRadius: '8px', border: '1px solid #e2e8f0', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}
                      />
                      <Legend />
                      <Area type="monotone" dataKey="calls" stroke="#8b5cf6" strokeWidth={3} fillOpacity={1} fill="url(#colorCalls)" name="Total Calls" />
                      <Area type="monotone" dataKey="success" stroke="#10b981" strokeWidth={3} fillOpacity={1} fill="url(#colorSuccess)" name="Successful" />
                    </AreaChart>
                  </ResponsiveContainer>
                )}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="sentiment" className="space-y-6">
          <div className="grid gap-6 md:grid-cols-3">
            <Card className="border-2 shadow-sm">
              <CardHeader className="pb-3">
                <CardTitle className="text-sm font-medium flex items-center gap-2 text-emerald-600">
                  <Smile className="h-4 w-4" /> Interested / Positive
                </CardTitle>
                <CardDescription>Leads expressing interest, asking for details or booking demos.</CardDescription>
              </CardHeader>
              <CardContent className="space-y-2">
                <div className="text-3xl font-bold text-emerald-600">{sentiment.positive}%</div>
                <Progress value={sentiment.positive} className="h-2 bg-emerald-100" />
              </CardContent>
            </Card>

            <Card className="border-2 shadow-sm">
              <CardHeader className="pb-3">
                <CardTitle className="text-sm font-medium flex items-center gap-2 text-muted-foreground">
                  <Meh className="h-4 w-4" /> Neutral / Information
                </CardTitle>
                <CardDescription>Conversations with standard inquiry without strong intent.</CardDescription>
              </CardHeader>
              <CardContent className="space-y-2">
                <div className="text-3xl font-bold text-foreground">{sentiment.neutral}%</div>
                <Progress value={sentiment.neutral} className="h-2" />
              </CardContent>
            </Card>

            <Card className="border-2 shadow-sm">
              <CardHeader className="pb-3">
                <CardTitle className="text-sm font-medium flex items-center gap-2 text-rose-600">
                  <Frown className="h-4 w-4" /> Not Interested / Busy
                </CardTitle>
                <CardDescription>Leads indicating bad timing, wrong number, or no interest.</CardDescription>
              </CardHeader>
              <CardContent className="space-y-2">
                <div className="text-3xl font-bold text-rose-600">{sentiment.negative}%</div>
                <Progress value={sentiment.negative} className="h-2 bg-rose-100" />
              </CardContent>
            </Card>
          </div>

          <Card className="border-2 shadow-sm">
            <CardHeader className="pb-3">
              <CardTitle className="flex items-center gap-2 text-base">
                <Sparkles className="h-5 w-5 text-primary" /> Per-Lead Call Sentiment & Executive Summaries
              </CardTitle>
              <CardDescription>
                Detailed breakdown of sentiment classifications and AI summaries generated for every individual lead conversation.
              </CardDescription>
            </CardHeader>
            <CardContent>
              {calls.length === 0 ? (
                <div className="py-12 text-center text-xs text-muted-foreground italic">
                  No call sessions recorded yet. Start a call or campaign to see real-time per-lead sentiment analysis.
                </div>
              ) : (
                <div className="rounded-lg border overflow-hidden">
                  <table className="w-full text-xs text-left">
                    <thead className="bg-muted/50 text-muted-foreground uppercase font-semibold text-[10px] tracking-wider border-b">
                      <tr>
                        <th className="p-3">Lead / Target</th>
                        <th className="p-3">AI Sentiment</th>
                        <th className="p-3">AI Executive Summary</th>
                        <th className="p-3">Duration</th>
                        <th className="p-3 text-right">Action</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y">
                      {calls.map((call: any) => {
                        const s = (call.sentiment || "neutral").toLowerCase()
                        return (
                          <tr key={call.id} className="hover:bg-muted/20 transition-colors">
                            <td className="p-3">
                              <div className="font-semibold text-foreground">{call.contactName || call.to_number}</div>
                              <div className="text-[11px] text-muted-foreground font-mono">{call.to_number}</div>
                            </td>
                            <td className="p-3">
                              {s === "interested" || s === "positive" ? (
                                <Badge variant="secondary" className="bg-emerald-100 text-emerald-700 dark:bg-emerald-950 dark:text-emerald-300 font-semibold capitalize">
                                  Interested
                                </Badge>
                              ) : s === "not-interested" || s === "negative" ? (
                                <Badge variant="secondary" className="bg-rose-100 text-rose-700 dark:bg-rose-950 dark:text-rose-300 font-semibold capitalize">
                                  Not Interested
                                </Badge>
                              ) : (
                                <Badge variant="outline" className="capitalize text-muted-foreground">
                                  {s}
                                </Badge>
                              )}
                            </td>
                            <td className="p-3 max-w-[320px]">
                              <p className="line-clamp-2 text-foreground/80 leading-relaxed">
                                {call.summary || "Conversation completed. Standard inquiry."}
                              </p>
                            </td>
                            <td className="p-3 font-mono text-muted-foreground">
                              {Math.floor((call.duration_seconds || 0) / 60)}:{(call.duration_seconds || 0) % 60 < 10 ? '0' : ''}{(call.duration_seconds || 0) % 60}
                            </td>
                            <td className="p-3 text-right">
                              <Button
                                variant="outline"
                                size="sm"
                                className="h-7 text-xs"
                                onClick={() => {
                                  setSelectedCall(call)
                                  setIsDialogOpen(true)
                                }}
                              >
                                <FileText className="h-3 w-3 mr-1" /> View Transcript
                              </Button>
                            </td>
                          </tr>
                        )
                      })}
                    </tbody>
                  </table>
                </div>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="providers" className="space-y-6">
          <Card className="border-2 shadow-sm">
            <CardHeader>
              <CardTitle>Voice & LLM Provider Costs</CardTitle>
              <CardDescription>Usage metrics breakdown by AI engine.</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="h-[400px] w-full">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={providerData} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
                    <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e5e7eb" />
                    <XAxis dataKey="name" stroke="#888888" fontSize={12} tickLine={false} axisLine={false} />
                    <YAxis stroke="#888888" fontSize={12} tickLine={false} axisLine={false} />
                    <Tooltip cursor={{fill: 'transparent'}} contentStyle={{ borderRadius: '8px' }} />
                    <Legend />
                    <Bar dataKey="calls" fill="#8b5cf6" radius={[4, 4, 0, 0]} name="Processed Calls" maxBarSize={60} />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>

      {/* Transcript & AI Summary Modal Dialog */}
      <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
        <DialogContent className="sm:max-w-[550px]">
          <DialogHeader>
            <DialogTitle className="flex items-center gap-2">
              <PhoneCall className="h-5 w-5 text-primary" /> Call Analysis & Transcript Log
            </DialogTitle>
            <DialogDescription>
              Lead Target: <span className="font-mono text-foreground font-semibold">{selectedCall?.contactName || selectedCall?.to_number}</span> ({selectedCall?.to_number})
            </DialogDescription>
          </DialogHeader>

          {/* AI Executive Summary Card */}
          <div className="p-3.5 bg-primary/5 border border-primary/20 rounded-xl space-y-1">
            <div className="flex items-center justify-between">
              <span className="text-[11px] font-bold uppercase tracking-wider text-primary flex items-center gap-1">
                🤖 AI Executive Summary
              </span>
              <span className="text-[10px] font-semibold uppercase px-2 py-0.5 rounded-full bg-primary/10 text-primary">
                {selectedCall?.sentiment || "Neutral"}
              </span>
            </div>
            <p className="text-xs text-foreground/90 leading-relaxed pt-0.5">
              {selectedCall?.summary || "No automated summary available for this call session yet."}
            </p>
          </div>

          <ScrollArea className="max-h-[300px] p-4 bg-muted/20 rounded-md border">
            {(() => {
              if (!selectedCall?.transcript) {
                return (
                  <div className="p-8 text-center text-xs text-muted-foreground italic">
                    No speech transcript turns recorded for this call session.
                  </div>
                )
              }
              let turns = []
              try {
                if (typeof selectedCall.transcript === "string") turns = JSON.parse(selectedCall.transcript)
                else if (Array.isArray(selectedCall.transcript)) turns = selectedCall.transcript
                else turns = [{ role: "assistant", content: String(selectedCall.transcript) }]
              } catch (e) {
                turns = [{ role: "assistant", content: String(selectedCall.transcript) }]
              }

              if (turns.length === 0) {
                return (
                  <div className="p-8 text-center text-xs text-muted-foreground italic">
                    No speech transcript turns recorded for this call session.
                  </div>
                )
              }

              return (
                <div className="space-y-4">
                  {turns.map((msg: any, idx: number) => (
                    <div key={idx} className={`flex items-start gap-3 ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                      {msg.role !== 'user' && (
                        <div className="w-7 h-7 rounded-full bg-primary text-primary-foreground flex items-center justify-center text-xs shrink-0 mt-0.5">
                          <Bot className="h-3.5 w-3.5" />
                        </div>
                      )}
                      <div className={`p-3 rounded-xl text-xs leading-relaxed max-w-[80%] ${
                        msg.role === 'user'
                          ? 'bg-foreground text-background rounded-tr-none font-mono'
                          : 'bg-card border shadow-sm rounded-tl-none'
                      }`}>
                        <p className="font-semibold text-[10px] uppercase opacity-75 mb-1">
                          {msg.role === 'user' ? 'Lead' : 'AI Agent'}
                        </p>
                        <p>{msg.content}</p>
                      </div>
                      {msg.role === 'user' && (
                        <div className="w-7 h-7 rounded-full bg-muted flex items-center justify-center text-xs shrink-0 mt-0.5 border">
                          <User className="h-3.5 w-3.5" />
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              )
            })()}
          </ScrollArea>

          <div className="flex justify-end pt-2">
            <Button variant="secondary" onClick={() => setIsDialogOpen(false)}>Close</Button>
          </div>
        </DialogContent>
      </Dialog>
    </motion.div>
  )
}
