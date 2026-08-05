import { motion } from "framer-motion"
import { PageHeader } from "@/components/ui/page-header"
import { StatCard } from "@/components/ui/stat-card"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { StatusIndicator } from "@/components/ui/status-indicator"
import {
  Phone,
  Bot,
  Megaphone,
  Users,
  TrendingUp,
  ArrowRight,
  Plus,
  Zap,
  Clock,
} from "lucide-react"
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts"



const container = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    transition: { staggerChildren: 0.06 },
  },
}

const item = {
  hidden: { opacity: 0, y: 20 },
  show: { opacity: 1, y: 0, transition: { type: "spring", damping: 25, stiffness: 300 } },
}

import * as React from "react"
import { api } from "@/services/api"

export function DashboardPage() {
  const [data, setData] = React.useState<any>(null)

  React.useEffect(() => {
    api.getAnalytics()
      .then(res => setData(res))
      .catch(err => console.error("Error loading dashboard metrics:", err))
  }, [])

  const metrics = data?.metrics || {
    total_calls: 0,
    success_rate: 0.0,
    active_campaigns: 0,
    total_agents: 1,
    total_leads: 1
  }


  const chartData = data?.chart_data || [
    { name: "Mon", calls: 12, success: 10 },
    { name: "Tue", calls: 24, success: 21 },
    { name: "Wed", calls: 18, success: 16 },
    { name: "Thu", calls: 32, success: 29 },
    { name: "Fri", calls: 42, success: 38 },
    { name: "Sat", calls: 15, success: 14 },
    { name: "Sun", calls: 10, success: 9 },
  ]

  const recentActivity = data?.recent_activity || [
    { id: "act_1", message: "Live call completed to +917039015196 via Twilio", time: "Just now", status: "success" },
    { id: "act_2", message: "Campaign 'Q3 Outreach' running with 5 concurrent channels", time: "5 mins ago", status: "info" },
    { id: "act_3", message: "Agent 'Sarah SDR' prompt updated with gTTS engine", time: "12 mins ago", status: "success" },
  ]


  return (
    <motion.div variants={container} initial="hidden" animate="show" className="space-y-8">
      {/* Header */}
      <motion.div variants={item}>
        <PageHeader
          title="Dashboard"
          description="Welcome back, Harsh. Here's what's happening today."
          actions={
            <Button>
              <Plus className="h-4 w-4 mr-2" />
              New Campaign
            </Button>
          }
        />
      </motion.div>

      {/* KPI Cards */}
      <motion.div variants={item} className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <StatCard
          title="Total Calls Today"
          value={metrics.total_calls?.toLocaleString() || "42"}
          change={12.5}
          changeLabel="vs last week"
          icon={Phone}
        />
        <StatCard
          title="Active Agents"
          value={metrics.total_agents?.toString() || "2"}
          change={4}
          changeLabel="vs yesterday"
          icon={Bot}
        />
        <StatCard
          title="Active Campaigns"
          value={metrics.active_campaigns?.toString() || "1"}
          change={-2}
          changeLabel="vs last week"
          icon={Megaphone}
        />
        <StatCard
          title="Success Rate"
          value={`${metrics.success_rate || 88.5}%`}
          change={6.8}
          changeLabel="vs last month"
          icon={TrendingUp}
        />
      </motion.div>


      {/* Charts + Activity */}
      <div className="grid gap-6 lg:grid-cols-7">
        {/* Call Volume Chart */}
        <motion.div variants={item} className="lg:col-span-4">
          <Card>
            <CardHeader className="flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-base font-semibold">Call Volume</CardTitle>
              <div className="flex items-center gap-4 text-xs text-muted-foreground">
                <div className="flex items-center gap-1.5">
                  <div className="h-2.5 w-2.5 rounded-full bg-primary" />
                  Total Calls
                </div>
                <div className="flex items-center gap-1.5">
                  <div className="h-2.5 w-2.5 rounded-full bg-green-500" />
                  Successful
                </div>
              </div>
            </CardHeader>
            <CardContent>
              <div className="h-[280px]">
                <ResponsiveContainer width="100%" height="100%">
                  <AreaChart data={chartData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                    <defs>
                      <linearGradient id="colorCalls" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="hsl(262, 83%, 58%)" stopOpacity={0.15} />
                        <stop offset="95%" stopColor="hsl(262, 83%, 58%)" stopOpacity={0} />
                      </linearGradient>
                      <linearGradient id="colorSuccess" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="hsl(142, 71%, 45%)" stopOpacity={0.15} />
                        <stop offset="95%" stopColor="hsl(142, 71%, 45%)" stopOpacity={0} />
                      </linearGradient>
                    </defs>
                    <CartesianGrid strokeDasharray="3 3" className="stroke-muted/50" />
                    <XAxis dataKey="name" className="text-xs" tick={{ fill: "hsl(var(--muted-foreground))" }} />
                    <YAxis className="text-xs" tick={{ fill: "hsl(var(--muted-foreground))" }} />
                    <Tooltip
                      contentStyle={{
                        backgroundColor: "hsl(var(--card))",
                        border: "1px solid hsl(var(--border))",
                        borderRadius: "0.75rem",
                        boxShadow: "0 4px 12px rgba(0,0,0,0.1)",
                      }}
                    />
                    <Area
                      type="monotone"
                      dataKey="calls"
                      stroke="hsl(262, 83%, 58%)"
                      fillOpacity={1}
                      fill="url(#colorCalls)"
                      strokeWidth={2}
                    />
                    <Area
                      type="monotone"
                      dataKey="success"
                      stroke="hsl(142, 71%, 45%)"
                      fillOpacity={1}
                      fill="url(#colorSuccess)"
                      strokeWidth={2}
                    />
                  </AreaChart>
                </ResponsiveContainer>
              </div>
            </CardContent>
          </Card>
        </motion.div>

        {/* Activity Feed */}
        <motion.div variants={item} className="lg:col-span-3">
          <Card className="h-full">
            <CardHeader className="flex-row items-center justify-between space-y-0 pb-4">
              <CardTitle className="text-base font-semibold">Recent Activity</CardTitle>
              <Button variant="ghost" size="sm" className="text-xs">
                View all <ArrowRight className="h-3 w-3 ml-1" />
              </Button>
            </CardHeader>
            <CardContent className="space-y-4">
              {recentActivity.map((activity: any, index: number) => (

                <motion.div
                  key={activity.id}
                  initial={{ opacity: 0, x: -10 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: 0.4 + index * 0.08 }}
                  className="flex items-start gap-3"
                >
                  <StatusIndicator
                    status={activity.status === "success" ? "active" : activity.status === "warning" ? "warning" : "pending"}
                    pulse={activity.status === "warning"}
                    className="mt-1.5"
                  />
                  <div className="flex-1 min-w-0">
                    <p className="text-sm leading-snug">{activity.message}</p>
                    <p className="text-xs text-muted-foreground mt-0.5 flex items-center gap-1">
                      <Clock className="h-3 w-3" />
                      {activity.time}
                    </p>
                  </div>
                </motion.div>
              ))}
            </CardContent>
          </Card>
        </motion.div>
      </div>

      {/* Quick Actions */}
      <motion.div variants={item}>
        <Card>
          <CardHeader>
            <CardTitle className="text-base font-semibold">Quick Actions</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
              {[
                { label: "Create AI Agent", icon: Bot, badge: "AI" },
                { label: "Launch Campaign", icon: Megaphone, badge: null },
                { label: "Import Leads", icon: Users, badge: null },
                { label: "AI Playground", icon: Zap, badge: "New" },
              ].map((action) => (
                <Button
                  key={action.label}
                  variant="outline"
                  className="h-auto py-4 justify-start gap-3 hover:border-primary/30 hover:bg-primary/5 transition-all"
                >
                  <div className="p-2 rounded-lg bg-primary/10">
                    <action.icon className="h-4 w-4 text-primary" />
                  </div>
                  <span className="font-medium">{action.label}</span>
                  {action.badge && (
                    <Badge variant="secondary" className="ml-auto text-[10px]">
                      {action.badge}
                    </Badge>
                  )}
                </Button>
              ))}
            </div>
          </CardContent>
        </Card>
      </motion.div>
    </motion.div>
  )
}
