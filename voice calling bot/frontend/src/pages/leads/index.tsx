import * as React from "react"
import { useNavigate } from "react-router-dom"
import { motion } from "framer-motion"
import { PageHeader } from "@/components/ui/page-header"
import { DataTable, type Column } from "@/components/ui/data-table"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog"
import { Search, Upload, PhoneCall, Bot, Play, Loader2, CheckCircle2, UserPlus, Sparkles, Edit3, Trash2 } from "lucide-react"
import { api } from "@/services/api"

interface Lead {
  id: string
  name: string
  phone_number?: string
  phone?: string
  email?: string
  company?: string
  status?: string
}

export function LeadsListPage() {
  const navigate = useNavigate()
  const [leads, setLeads] = React.useState<Lead[]>([])
  const [agents, setAgents] = React.useState<any[]>([])
  const [selectedAgentId, setSelectedAgentId] = React.useState<string>("")
  const [callingLeadId, setCallingLeadId] = React.useState<string | null>(null)
  const [callNotice, setCallNotice] = React.useState<string | null>(null)
  const [isBatchCalling, setIsBatchCalling] = React.useState(false)

  // Manual Lead Creation State
  const [isAddLeadOpen, setIsAddLeadOpen] = React.useState(false)
  const [newLeadName, setNewLeadName] = React.useState("")
  const [newLeadPhone, setNewLeadPhone] = React.useState("")
  const [newLeadEmail, setNewLeadEmail] = React.useState("")
  const [newLeadCompany, setNewLeadCompany] = React.useState("")
  const [isSavingLead, setIsSavingLead] = React.useState(false)

  // Lead Editing State
  const [editingLead, setEditingLead] = React.useState<Lead | null>(null)
  const [editName, setEditName] = React.useState("")
  const [editPhone, setEditPhone] = React.useState("")
  const [editEmail, setEditEmail] = React.useState("")
  const [editCompany, setEditCompany] = React.useState("")
  const [editStatus, setEditStatus] = React.useState("")
  const [isUpdatingLead, setIsUpdatingLead] = React.useState(false)

  const fetchLeads = () => {
    api.getLeads()
      .then(data => setLeads(data))
      .catch(err => console.error("Error loading leads:", err))
  }

  React.useEffect(() => {
    fetchLeads()

    api.getAgents()
      .then(data => {
        setAgents(data)
        if (data && data.length > 0) setSelectedAgentId(data[0].id)
      })
      .catch(err => console.error("Error loading agents:", err))
  }, [])

  // Create Manual Lead in DB
  const handleSaveManualLead = async () => {
    if (!newLeadName.trim() || !newLeadPhone.trim()) return
    setIsSavingLead(true)

    try {
      await api.createLead({
        name: newLeadName,
        phone_number: newLeadPhone,
        email: newLeadEmail,
        company: newLeadCompany,
      })

      setNewLeadName("")
      setNewLeadPhone("")
      setNewLeadEmail("")
      setNewLeadCompany("")
      setIsAddLeadOpen(false)
      fetchLeads()
    } catch (e) {
      console.error("Error saving lead:", e)
    } finally {
      setIsSavingLead(false)
    }
  }

  // Open Edit Modal
  const openEditLeadModal = (lead: Lead) => {
    setEditingLead(lead)
    setEditName(lead.name || "")
    setEditPhone(lead.phone_number || lead.phone || "")
    setEditEmail(lead.email || "")
    setEditCompany(lead.company || "")
    setEditStatus(lead.status || "pending")
  }

  // Save Edit Lead
  const handleSaveEditLead = async () => {
    if (!editingLead) return
    setIsUpdatingLead(true)
    try {
      await api.updateLead(editingLead.id, {
        name: editName,
        phone_number: editPhone,
        email: editEmail,
        company: editCompany,
        status: editStatus,
      })
      setEditingLead(null)
      fetchLeads()
    } catch (e) {
      console.error("Error updating lead:", e)
    } finally {
      setIsUpdatingLead(false)
    }
  }

  // Delete Lead
  const handleDeleteLead = async (leadId: string) => {
    if (!window.confirm("Are you sure you want to delete this lead?")) return
    try {
      await api.deleteLead(leadId)
      fetchLeads()
    } catch (e) {
      console.error("Error deleting lead:", e)
    }
  }

  // Start call to single lead
  const handleCallSingleLead = async (lead: Lead) => {
    const phoneNumber = lead.phone_number || lead.phone || "+917039015196"
    setCallingLeadId(lead.id)
    setCallNotice(`Dialing ${lead.name} (${phoneNumber})...`)

    try {
      const res = await api.startCall({
        agent_id: selectedAgentId || "00000000-0000-0000-0000-000000000000",
        from_number: "+17372212163",
        to_number: phoneNumber,
        lead_id: lead.id,
      })

      setCallNotice(`✅ Call Started to ${lead.name}! SID: ${res.provider_call_id || res.call_id}`)
    } catch (err: any) {
      setCallNotice(`⚠️ ${err.message || "Failed to trigger call"}`)
    } finally {
      setCallingLeadId(null)
    }
  }

  // Trigger sequential bulk campaign dialing for all leads
  const handleStartBulkCampaign = async () => {
    if (leads.length === 0) return
    setIsBatchCalling(true)
    setCallNotice("Initiating Bulk Campaign Dialing for leads...")

    for (let i = 0; i < leads.length; i++) {
      const lead = leads[i]
      const phoneNumber = lead.phone_number || lead.phone || "+917039015196"
      setCallNotice(`[${i + 1}/${leads.length}] Dialing ${lead.name} (${phoneNumber})...`)
      try {
        await api.startCall({
          agent_id: selectedAgentId || "00000000-0000-0000-0000-000000000000",
          from_number: "+17372212163",
          to_number: phoneNumber,
        })
      } catch (e) {
        console.error("Batch dial error:", e)
      }
      await new Promise(r => setTimeout(r, 2000))
    }
    setCallNotice("✅ Bulk Campaign Execution Complete!")
    setIsBatchCalling(false)
  }

  const columns: Column<Lead>[] = [
    {
      key: "name",
      header: "Lead Name",
      cell: (row) => (
        <div>
          <div className="font-medium text-foreground">{row.name}</div>
          <div className="text-xs text-muted-foreground">{row.company || "Enterprise Lead"}</div>
        </div>
      ),
    },
    {
      key: "contact",
      header: "Phone / Contact",
      cell: (row) => (
        <div>
          <div className="text-sm font-mono">{row.phone_number || row.phone || "+917039015196"}</div>
          <div className="text-xs text-muted-foreground">{row.email || "lead@example.com"}</div>
        </div>
      ),
    },
    {
      key: "status",
      header: "Status",
      cell: (row) => {
        const s = (row.status || "new").toLowerCase()
        if (s === "new" || s === "pending") return <Badge variant="secondary" className="bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400">Pending</Badge>
        if (s === "contacted" || s === "completed") return <Badge variant="secondary" className="bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400">Completed</Badge>
        return <Badge variant="outline">{row.status || "New"}</Badge>
      },
    },
    {
      key: "actions",
      header: "Actions",
      className: "w-[240px]",
      cell: (row) => (
        <div className="flex items-center gap-1.5">
          <Button
            size="sm"
            variant="default"
            className="bg-primary hover:bg-primary/90 text-xs gap-1 h-8 px-2"
            onClick={() => handleCallSingleLead(row)}
            disabled={callingLeadId === row.id || isBatchCalling}
          >
            {callingLeadId === row.id ? (
              <Loader2 className="h-3.5 w-3.5 animate-spin" />
            ) : (
              <PhoneCall className="h-3.5 w-3.5" />
            )}
            Call
          </Button>

          <Button
            size="sm"
            variant="outline"
            className="h-8 px-2 text-xs gap-1"
            onClick={() => openEditLeadModal(row)}
          >
            <Edit3 className="h-3.5 w-3.5 text-blue-600" /> Edit
          </Button>

          <Button
            size="sm"
            variant="ghost"
            className="h-8 px-2 text-xs text-red-600 hover:text-red-700 hover:bg-red-50"
            onClick={() => handleDeleteLead(row.id)}
          >
            <Trash2 className="h-3.5 w-3.5" />
          </Button>
        </div>
      ),
    },
  ]

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-6">
      <PageHeader
        title="Leads Management"
        description="Manage your sales contacts, assign AI agents, and trigger direct AI calls."
        actions={
          <div className="flex gap-2 items-center">
            <div className="flex items-center gap-2 mr-2">
              <Bot className="h-4 w-4 text-primary" />
              <Select value={selectedAgentId} onValueChange={setSelectedAgentId}>
                <SelectTrigger className="w-[180px] h-9 text-xs">
                  <SelectValue placeholder="Assign AI Agent" />
                </SelectTrigger>
                <SelectContent>
                  {agents.map(ag => (
                    <SelectItem key={ag.id} value={ag.id}>{ag.name}</SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            {/* Manual Add Lead Dialog */}
            <Dialog open={isAddLeadOpen} onOpenChange={setIsAddLeadOpen}>
              <DialogTrigger asChild>
                <Button size="sm" variant="outline">
                  <UserPlus className="mr-1.5 h-3.5 w-3.5" /> Add Lead Manually
                </Button>
              </DialogTrigger>
              <DialogContent className="sm:max-w-[450px]">
                <DialogHeader>
                  <DialogTitle className="flex items-center gap-2">
                    <Sparkles className="h-5 w-5 text-primary" /> Add New Lead Manually
                  </DialogTitle>
                  <DialogDescription>
                    Enter lead details to save directly into PostgreSQL for AI call dialing.
                  </DialogDescription>
                </DialogHeader>

                <div className="grid gap-4 py-4 text-xs">
                  <div className="space-y-1.5">
                    <label className="font-semibold">Full Name *</label>
                    <Input
                      placeholder="e.g., Harsh Shirsath"
                      value={newLeadName}
                      onChange={(e) => setNewLeadName(e.target.value)}
                    />
                  </div>
                  <div className="space-y-1.5">
                    <label className="font-semibold">Phone Number (E.164 format) *</label>
                    <Input
                      placeholder="e.g., +917039015196"
                      value={newLeadPhone}
                      onChange={(e) => setNewLeadPhone(e.target.value)}
                    />
                  </div>
                  <div className="space-y-1.5">
                    <label className="font-semibold">Email Address</label>
                    <Input
                      placeholder="e.g., harsh@example.com"
                      value={newLeadEmail}
                      onChange={(e) => setNewLeadEmail(e.target.value)}
                    />
                  </div>
                  <div className="space-y-1.5">
                    <label className="font-semibold">Company / Organization</label>
                    <Input
                      placeholder="e.g., Voxera AI Client"
                      value={newLeadCompany}
                      onChange={(e) => setNewLeadCompany(e.target.value)}
                    />
                  </div>
                </div>

                <div className="flex justify-end gap-2">
                  <Button variant="outline" onClick={() => setIsAddLeadOpen(false)}>Cancel</Button>
                  <Button onClick={handleSaveManualLead} disabled={isSavingLead || !newLeadName.trim() || !newLeadPhone.trim()}>
                    {isSavingLead ? <Loader2 className="mr-2 h-4 w-4 animate-spin" /> : <UserPlus className="mr-2 h-4 w-4" />}
                    Save Lead
                  </Button>
                </div>
              </DialogContent>
            </Dialog>

            <Button variant="outline" size="sm" onClick={() => navigate("/leads/import")}>
              <Upload className="mr-1.5 h-3.5 w-3.5" /> Import CSV
            </Button>
            <Button size="sm" onClick={handleStartBulkCampaign} disabled={isBatchCalling || leads.length === 0}>
              {isBatchCalling ? <Loader2 className="mr-1.5 h-3.5 w-3.5 animate-spin" /> : <Play className="mr-1.5 h-3.5 w-3.5" />}
              Start Bulk Campaign ({leads.length})
            </Button>
          </div>
        }
      />

      {callNotice && (
        <div className="p-3 bg-muted border border-primary/20 rounded-md text-xs font-mono text-center flex items-center justify-center gap-2">
          <CheckCircle2 className="h-4 w-4 text-green-500" />
          {callNotice}
        </div>
      )}

      <div className="flex items-center justify-between w-full">
        <div className="relative w-[300px]">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
          <Input placeholder="Search leads by name or phone..." className="pl-9" />
        </div>
      </div>

      <DataTable columns={columns} data={leads} />

      {/* Edit Lead Dialog */}
      <Dialog open={!!editingLead} onOpenChange={(open) => !open && setEditingLead(null)}>
        <DialogContent className="sm:max-w-[450px]">
          <DialogHeader>
            <DialogTitle className="flex items-center gap-2">
              <Edit3 className="h-5 w-5 text-primary" /> Edit Lead Information
            </DialogTitle>
            <DialogDescription>
              Update contact information and status for this lead.
            </DialogDescription>
          </DialogHeader>

          <div className="grid gap-4 py-4 text-xs">
            <div className="space-y-1.5">
              <label className="font-semibold">Full Name *</label>
              <Input
                value={editName}
                onChange={(e) => setEditName(e.target.value)}
              />
            </div>
            <div className="space-y-1.5">
              <label className="font-semibold">Phone Number (E.164 format) *</label>
              <Input
                value={editPhone}
                onChange={(e) => setEditPhone(e.target.value)}
              />
            </div>
            <div className="space-y-1.5">
              <label className="font-semibold">Email Address</label>
              <Input
                value={editEmail}
                onChange={(e) => setEditEmail(e.target.value)}
              />
            </div>
            <div className="space-y-1.5">
              <label className="font-semibold">Company / Organization</label>
              <Input
                value={editCompany}
                onChange={(e) => setEditCompany(e.target.value)}
              />
            </div>
            <div className="space-y-1.5">
              <label className="font-semibold">Status</label>
              <select
                className="w-full h-9 px-3 border rounded-md bg-background text-xs"
                value={editStatus}
                onChange={(e) => setEditStatus(e.target.value)}
              >
                <option value="pending">Pending</option>
                <option value="completed">Completed</option>
                <option value="contacted">Contacted</option>
                <option value="failed">Failed</option>
              </select>
            </div>
          </div>

          <div className="flex justify-end gap-2">
            <Button variant="outline" onClick={() => setEditingLead(null)}>Cancel</Button>
            <Button onClick={handleSaveEditLead} disabled={isUpdatingLead || !editName.trim() || !editPhone.trim()}>
              {isUpdatingLead ? <Loader2 className="mr-2 h-4 w-4 animate-spin" /> : <Edit3 className="mr-2 h-4 w-4" />}
              Save Changes
            </Button>
          </div>
        </DialogContent>
      </Dialog>
    </motion.div>
  )
}
