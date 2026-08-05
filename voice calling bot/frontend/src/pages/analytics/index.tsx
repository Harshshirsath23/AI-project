import { motion } from "framer-motion"
import { PageHeader } from "@/components/ui/page-header"
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { StatCard } from "@/components/ui/stat-card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Activity, Users, Phone, DollarSign } from "lucide-react"

// Import Recharts
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar, Legend } from 'recharts'

const dailyData = [
  { name: 'Mon', calls: 4000, success: 2400 },
  { name: 'Tue', calls: 3000, success: 1398 },
  { name: 'Wed', calls: 2000, success: 9800 },
  { name: 'Thu', calls: 2780, success: 3908 },
  { name: 'Fri', calls: 1890, success: 4800 },
  { name: 'Sat', calls: 2390, success: 3800 },
  { name: 'Sun', calls: 3490, success: 4300 },
];

const providerData = [
  { name: 'ElevenLabs', cost: 400, latency: 240 },
  { name: 'PlayHT', cost: 300, latency: 139 },
  { name: 'OpenAI TTS', cost: 200, latency: 980 },
];

import * as React from "react"
import { api } from "@/services/api"

export function AnalyticsPage() {
  const [data, setData] = React.useState<any>(null)

  React.useEffect(() => {
    api.getAnalytics()
      .then(res => setData(res))
      .catch(err => console.error("Error loading analytics:", err))
  }, [])

  const m = data?.metrics || {
    total_calls: 42,
    success_rate: 88.5,
    active_campaigns: 1,
    avg_duration_seconds: 142
  }

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-6 pb-12">
      <PageHeader
        title="Analytics & Reporting"
        description="Comprehensive insights into your AI calling operations."
      />

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <StatCard title="Total Calls" value={m.total_calls?.toLocaleString() || "42"} change={12.5} icon={Phone} />
        <StatCard title="Overall Success Rate" value={`${m.success_rate || 88.5}%`} change={4.1} icon={Activity} />
        <StatCard title="Active Campaigns" value={m.active_campaigns?.toString() || "1"} change={-2.4} icon={Users} />
        <StatCard title="Avg Duration" value={`${m.avg_duration_seconds || 142}s`} change={8.2} icon={DollarSign} />
      </div>


      <Tabs defaultValue="overview" className="space-y-6">
        <TabsList className="bg-card border h-12 p-1">
          <TabsTrigger value="overview" className="data-[state=active]:bg-primary/10 data-[state=active]:text-primary">Overview</TabsTrigger>
          <TabsTrigger value="campaigns" className="data-[state=active]:bg-primary/10 data-[state=active]:text-primary">Campaign Performance</TabsTrigger>
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
                <ResponsiveContainer width="100%" height="100%">
                  <AreaChart data={dailyData} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
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
                    <YAxis stroke="#888888" fontSize={12} tickLine={false} axisLine={false} tickFormatter={(value) => `${value}`} />
                    <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e5e7eb" />
                    <Tooltip 
                      contentStyle={{ borderRadius: '8px', border: '1px solid #e2e8f0', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}
                    />
                    <Legend />
                    <Area type="monotone" dataKey="calls" stroke="#8b5cf6" strokeWidth={3} fillOpacity={1} fill="url(#colorCalls)" name="Total Calls" />
                    <Area type="monotone" dataKey="success" stroke="#10b981" strokeWidth={3} fillOpacity={1} fill="url(#colorSuccess)" name="Successful" />
                  </AreaChart>
                </ResponsiveContainer>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="providers" className="space-y-6">
          <Card className="border-2 shadow-sm">
            <CardHeader>
              <CardTitle>Voice Provider Costs</CardTitle>
              <CardDescription>Monthly spend breakdown by TTS provider.</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="h-[400px] w-full">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={providerData} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
                    <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e5e7eb" />
                    <XAxis dataKey="name" stroke="#888888" fontSize={12} tickLine={false} axisLine={false} />
                    <YAxis stroke="#888888" fontSize={12} tickLine={false} axisLine={false} tickFormatter={(value) => `$${value}`} />
                    <Tooltip cursor={{fill: 'transparent'}} contentStyle={{ borderRadius: '8px' }} />
                    <Legend />
                    <Bar dataKey="cost" fill="#8b5cf6" radius={[4, 4, 0, 0]} name="Cost ($)" maxBarSize={60} />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </motion.div>
  )
}
