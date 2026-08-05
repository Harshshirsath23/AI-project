import * as React from "react"
import { useNavigate } from "react-router-dom"
import { motion } from "framer-motion"
import { PageHeader } from "@/components/ui/page-header"
import { DataTable, type Column } from "@/components/ui/data-table"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { StatusIndicator } from "@/components/ui/status-indicator"
import { Progress } from "@/components/ui/progress"
import { Search, Plus, Filter, MoreHorizontal, Play, Pause, BarChart3, Bot } from "lucide-react"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"

interface Campaign {
  id: string
  name: string
  agentName?: string
  agent_name?: string
  status: string
  progress?: number
  totalLeads?: number
  total_leads?: number
  successfulCalls?: number
  completed_calls?: number
}


import { api } from "@/services/api"

export function CampaignsListPage() {
  const navigate = useNavigate()
  const [searchQuery, setSearchQuery] = React.useState("")
  const [campaigns, setCampaigns] = React.useState<any[]>([])

  React.useEffect(() => {
    api.getCampaigns()
      .then(data => setCampaigns(data))
      .catch(err => console.error("Error loading campaigns:", err))
  }, [])


  const columns: Column<Campaign>[] = [
    {
      key: "agent",
      header: "Agent",
      cell: (row) => (
        <div>
          <p className="font-medium text-foreground">{row.name}</p>
          <div className="flex items-center gap-1 mt-1 text-xs text-muted-foreground">
            <Bot className="h-3 w-3" /> {row.agentName || row.agent_name || "Sales Agent"}
          </div>
        </div>
      ),
    },
    {
      key: "status",
      header: "Status",
      cell: (row) => {
        let statusMap: any = {
          running: { label: "Running", status: "active", pulse: true },
          paused: { label: "Paused", status: "warning", pulse: false },
          completed: { label: "Completed", status: "inactive", pulse: false },
          draft: { label: "Draft", status: "inactive", pulse: false },
        }
        const s = statusMap[row.status?.toLowerCase()] || { label: row.status || "Active", status: "active", pulse: false }
        return <StatusIndicator status={s.status} label={s.label} pulse={s.pulse} />
      },
    },
    {
      key: "progress",
      header: "Progress",
      className: "w-[250px]",
      cell: (row) => {
        const total = row.totalLeads ?? row.total_leads ?? 0
        const prog = row.progress ?? 0
        const completed = Math.floor(total * (prog / 100))
        return (
          <div className="space-y-2">
            <div className="flex items-center justify-between text-xs">
              <span className="font-medium">{prog}%</span>
              <span className="text-muted-foreground">
                {completed.toLocaleString()} / {total.toLocaleString()} leads
              </span>
            </div>
            <Progress value={prog} className="h-1.5" />
          </div>
        )
      },
    },
    {
      key: "metrics",
      header: "Success",
      cell: (row) => {
        const successful = row.successfulCalls ?? row.completed_calls ?? 0
        return (
          <div>
            <p className="font-medium text-foreground">{successful.toLocaleString()}</p>
            <p className="text-xs text-muted-foreground">successful calls</p>
          </div>
        )
      },
    },
    {
      key: "actions",
      header: "",
      className: "w-[50px]",
      cell: (row) => (
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button variant="ghost" size="icon" className="h-8 w-8">
              <MoreHorizontal className="h-4 w-4" />
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="end">
            <DropdownMenuItem onClick={() => navigate(`/campaigns/${row.id}`)}>
              <BarChart3 className="mr-2 h-4 w-4" /> View Analytics
            </DropdownMenuItem>
            {row.status === "paused" || row.status === "draft" ? (
              <DropdownMenuItem>
                <Play className="mr-2 h-4 w-4" /> Start Campaign
              </DropdownMenuItem>
            ) : row.status === "running" ? (
              <DropdownMenuItem>
                <Pause className="mr-2 h-4 w-4" /> Pause Campaign
              </DropdownMenuItem>
            ) : null}
          </DropdownMenuContent>
        </DropdownMenu>
      ),
    },
  ]

  const filteredData = campaigns.filter(
    (c: any) => (c.name || "").toLowerCase().includes(searchQuery.toLowerCase())
  )


  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="space-y-6"
    >
      <PageHeader
        title="Campaigns"
        description="Manage your outbound calling campaigns."
        actions={
          <Button onClick={() => navigate("/campaigns/new")}>
            <Plus className="mr-2 h-4 w-4" /> New Campaign
          </Button>
        }
      />

      <div className="flex items-center gap-2">
        <div className="relative w-[300px]">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground pointer-events-none" />
          <Input
            placeholder="Search campaigns..."
            className="pl-9 bg-card"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
        </div>
        <Button variant="outline" size="icon">
          <Filter className="h-4 w-4" />
        </Button>
      </div>

      <DataTable
        columns={columns}
        data={filteredData}
        getRowId={(row) => row.id}
        emptyTitle="No campaigns found"
        emptyDescription="Create a new campaign to start calling leads."
      />
    </motion.div>
  )
}
