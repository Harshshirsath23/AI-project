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
  TrendingUp,
  ArrowRight,
  Plus,
  Zap,
  Clock,
  Users,
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
import * as React from "react"
import { useNavigate } from "react-router-dom"
import { api } from "@/services/api"

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

export function DashboardPage() {
  const navigate = useNavigate()
  const [data, setData] = React.useState<any>(null)
  const [loading, setLoading] = React.useState<boolean>(true)

  React.useEffect(() => {
    api.getAnalytics()
      .then((res) => setData(res))
      .catch((err) => console.error("Error loading dashboard metrics:", err))
      .finally(() => setLoading(false))
  }, [])

  const metrics = data?.metrics || {
    total_calls: 0,
    success_rate: 0.0,
    active_campaigns: 0,
    total_agents: 0,
    total_leads: 0,
  }

  const chartData = data?.chart_data || []
  const recentActivity = data?.recent_activity || []

  return (
    <motion.div variants={container} initial="hidden" animate="show" className="space-y-8">
      {/* Header */}
      <motion.div variants={item}>
        <PageHeader
          title="Dashboard"
          description="Welcome back. Here's what's happening across your AI calling platform."
          actions={
            <Button onClick={() => navigate("/campaigns/new")}>
              <Plus className="h-4 w-4 mr-2" />
              New Campaign
            </Button>
          }
        />
      </motion.div>

      {/* KPI Cards */}
      <motion.div variants={item} className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <StatCard
          title="Total Calls"
          value={loading ? "..." : metrics.total_calls.toLocaleString()}
          icon={Phone}
        />
        <StatCard
          title="Active Agents"
          value={loading ? "..." : metrics.total_agents.toString()}
          icon={Bot}
        />
        <StatCard
          title="Active Campaigns"
          value={loading ? "..." : metrics.active_campaigns.toString()}
          icon={Megaphone}
        />
        <StatCard
          title="Success Rate"
          value={loading ? "..." : `${metrics.success_rate}%`}
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
                {chartData.length === 0 ? (
                  <div className="h-full flex items-center justify-center text-xs text-muted-foreground">
                    No call volume data recorded yet.
                  </div>
                ) : (
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
                )}
              </div>
            </CardContent>
          </Card>
        </motion.div>

        {/* Activity Feed */}
        <motion.div variants={item} className="lg:col-span-3">
          <Card className="h-full">
            <CardHeader className="flex-row items-center justify-between space-y-0 pb-4">
              <CardTitle className="text-base font-semibold">Recent Activity</CardTitle>
              <Button variant="ghost" size="sm" className="text-xs" onClick={() => navigate("/calls")}>
                View calls <ArrowRight className="h-3 w-3 ml-1" />
              </Button>
            </CardHeader>
            <CardContent className="space-y-4">
              {recentActivity.length === 0 ? (
                <div className="py-8 text-center text-xs text-muted-foreground">
                  No activity recorded yet. Start a call or campaign to see events here.
                </div>
              ) : (
                recentActivity.map((activity: any, index: number) => (
                  <motion.div
                    key={activity.id || index}
                    initial={{ opacity: 0, x: -10 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: 0.1 + index * 0.05 }}
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
                ))
              )}
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
                { label: "Create AI Agent", icon: Bot, path: "/agents/new" },
                { label: "Launch Campaign", icon: Megaphone, path: "/campaigns/new" },
                { label: "Import Leads", icon: Users, path: "/leads" },
                { label: "AI Playground", icon: Zap, path: "/playground", badge: "Live" },
              ].map((action) => (
                <Button
                  key={action.label}
                  variant="outline"
                  className="h-auto py-4 justify-start gap-3 hover:border-primary/30 hover:bg-primary/5 transition-all"
                  onClick={() => navigate(action.path)}
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
