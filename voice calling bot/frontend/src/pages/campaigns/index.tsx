import * as React from "react"
import { useNavigate } from "react-router-dom"
import { motion } from "framer-motion"
import { PageHeader } from "@/components/ui/page-header"
import { DataTable, type Column } from "@/components/ui/data-table"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { StatusIndicator } from "@/components/ui/status-indicator"
import { Progress } from "@/components/ui/progress"
import { Search, Plus, Filter, MoreHorizontal, Pause, BarChart3, Bot, Phone, Edit3, Trash2 } from "lucide-react"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
} from "@/components/ui/dialog"
import { api } from "@/services/api"

interface Campaign {
  id: string
  name: string
  description?: string
  agentName?: string
  agent_name?: string
  agent_id?: string
  from_number?: string
  status: string
  progress?: number
  totalLeads?: number
  total_leads?: number
  successfulCalls?: number
  completed_calls?: number
  max_concurrent_calls?: number
}

export function CampaignsListPage() {
  const navigate = useNavigate()
  const [searchQuery, setSearchQuery] = React.useState("")
  const [campaigns, setCampaigns] = React.useState<any[]>([])
  
  // Edit Modal State
  const [editingCampaign, setEditingCampaign] = React.useState<any | null>(null)
  const [editName, setEditName] = React.useState("")
  const [editDescription, setEditDescription] = React.useState("")
  const [editAgentId, setEditAgentId] = React.useState("")
  const [editFromNumber, setEditFromNumber] = React.useState("")
  const [editMaxConcurrent, setEditMaxConcurrent] = React.useState(5)
  const [isSaving, setIsSaving] = React.useState(false)

  // Options
  const [agents, setAgents] = React.useState<any[]>([])
  const [phoneNumbers, setPhoneNumbers] = React.useState<any[]>([])

  const fetchCampaigns = () => {
    api.getCampaigns()
      .then(data => setCampaigns(data))
      .catch(err => console.error("Error loading campaigns:", err))
  }

  React.useEffect(() => {
    fetchCampaigns()
    api.getAgents().then(setAgents).catch(console.error)
    api.getPhoneNumbers().then(setPhoneNumbers).catch(console.error)
  }, [])

  const handleStartCampaign = async (id: string) => {
    try {
      await api.startCampaign(id)
      fetchCampaigns()
    } catch (e) {
      console.error("Error starting campaign:", e)
    }
  }

  const handlePauseCampaign = async (id: string) => {
    try {
      await api.pauseCampaign(id)
      fetchCampaigns()
    } catch (e) {
      console.error("Error pausing campaign:", e)
    }
  }

  const handleDeleteCampaign = async (id: string) => {
    if (!window.confirm("Are you sure you want to delete this campaign?")) return
    try {
      await api.deleteCampaign(id)
      fetchCampaigns()
    } catch (e) {
      console.error("Error deleting campaign:", e)
    }
  }

  const openEditModal = (campaign: any) => {
    setEditingCampaign(campaign)
    setEditName(campaign.name || "")
    setEditDescription(campaign.description || "")
    setEditAgentId(campaign.agent_id || (agents[0]?.id || ""))
    setEditFromNumber(campaign.from_number || (phoneNumbers[0]?.number || "+17372212163"))
    setEditMaxConcurrent(campaign.max_concurrent_calls || 5)
  }

  const handleSaveEdit = async () => {
    if (!editingCampaign) return
    setIsSaving(true)
    try {
      await api.updateCampaign(editingCampaign.id, {
        name: editName,
        description: editDescription,
        agent_id: editAgentId,
        from_number: editFromNumber,
        max_concurrent_calls: editMaxConcurrent
      })
      setEditingCampaign(null)
      fetchCampaigns()
    } catch (err) {
      console.error("Failed to update campaign:", err)
    } finally {
      setIsSaving(false)
    }
  }

  const columns: Column<Campaign>[] = [
    {
      key: "agent",
      header: "Campaign & Agent",
      cell: (row) => {
        const agent = agents.find(a => a.id === row.agent_id)
        return (
          <div>
            <p className="font-medium text-foreground">{row.name}</p>
            <div className="flex items-center gap-1 mt-1 text-xs text-muted-foreground">
              <Bot className="h-3 w-3" /> {agent?.name || row.agentName || row.agent_name || "Voice SDR Agent"}
            </div>
          </div>
        )
      },
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
        const completed = row.completed_calls ?? 0
        const prog = total > 0 ? Math.round((completed / total) * 100) : (row.progress ?? 0)
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
            <p className="text-xs text-muted-foreground">calls processed</p>
          </div>
        )
      },
    },
    {
      key: "actions",
      header: "",
      className: "w-[50px]",
      cell: (row) => (
        <div className="flex items-center gap-2">
          {row.status === "running" && (
            <Button size="sm" variant="default" className="bg-green-600 hover:bg-green-700 h-8 px-2 text-xs" onClick={() => handleStartCampaign(row.id)}>
              <Phone className="mr-1 h-3 w-3" /> Call Leads
            </Button>
          )}
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
              <DropdownMenuItem onClick={() => openEditModal(row)}>
                <Edit3 className="mr-2 h-4 w-4 text-blue-600" /> Edit Campaign
              </DropdownMenuItem>
              <DropdownMenuItem onClick={() => handleStartCampaign(row.id)}>
                <Phone className="mr-2 h-4 w-4 text-green-600" /> Start / Trigger Calling
              </DropdownMenuItem>
              {row.status === "running" ? (
                <DropdownMenuItem onClick={() => handlePauseCampaign(row.id)}>
                  <Pause className="mr-2 h-4 w-4" /> Pause Campaign
                </DropdownMenuItem>
              ) : null}
              <DropdownMenuItem className="text-red-600 focus:text-red-600" onClick={() => handleDeleteCampaign(row.id)}>
                <Trash2 className="mr-2 h-4 w-4" /> Delete Campaign
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </div>
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

      {/* Edit Campaign Dialog */}
      <Dialog open={!!editingCampaign} onOpenChange={(open) => !open && setEditingCampaign(null)}>
        <DialogContent className="sm:max-w-[500px]">
          <DialogHeader>
            <DialogTitle>Edit Campaign</DialogTitle>
          </DialogHeader>
          <div className="space-y-4 py-2">
            <div className="space-y-2">
              <Label>Campaign Name</Label>
              <Input value={editName} onChange={(e) => setEditName(e.target.value)} placeholder="Campaign Name" />
            </div>
            <div className="space-y-2">
              <Label>Description</Label>
              <Input value={editDescription} onChange={(e) => setEditDescription(e.target.value)} placeholder="Description" />
            </div>
            <div className="space-y-2">
              <Label>Assigned AI Agent</Label>
              <select 
                className="w-full h-10 px-3 border rounded-md bg-background text-sm"
                value={editAgentId}
                onChange={(e) => setEditAgentId(e.target.value)}
              >
                {agents.map((a: any) => (
                  <option key={a.id} value={a.id}>{a.name}</option>
                ))}
              </select>
            </div>
            <div className="space-y-2">
              <Label>Outbound Phone Number</Label>
              <select 
                className="w-full h-10 px-3 border rounded-md bg-background text-sm"
                value={editFromNumber}
                onChange={(e) => setEditFromNumber(e.target.value)}
              >
                {phoneNumbers.map((p: any) => (
                  <option key={p.id} value={p.number}>{p.number} ({p.provider})</option>
                ))}
              </select>
            </div>
            <div className="space-y-2">
              <Label>Max Concurrent Calls</Label>
              <Input 
                type="number" 
                value={editMaxConcurrent} 
                onChange={(e) => setEditMaxConcurrent(Number(e.target.value))} 
              />
            </div>
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setEditingCampaign(null)}>Cancel</Button>
            <Button onClick={handleSaveEdit} disabled={isSaving}>
              {isSaving ? "Saving..." : "Save Changes"}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </motion.div>
  )
}
