import * as React from "react"
import { useNavigate } from "react-router-dom"
import { motion } from "framer-motion"
import { PageHeader } from "@/components/ui/page-header"
import { DataTable, type Column } from "@/components/ui/data-table"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { StatusIndicator } from "@/components/ui/status-indicator"
import { Search, Plus, Filter, MoreHorizontal } from "lucide-react"

import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import { Badge } from "@/components/ui/badge"

import { api } from "@/services/api"

export function AgentsListPage() {
  const navigate = useNavigate()
  const [searchQuery, setSearchQuery] = React.useState("")
  const [agents, setAgents] = React.useState<any[]>([])
  const [selectedRows, setSelectedRows] = React.useState<Set<string>>(new Set())

  React.useEffect(() => {
    api.getAgents()
      .then((data) => setAgents(data))
      .catch((err) => console.error("Error loading agents:", err))
  }, [])


  const columns: Column<any>[] = [
    {
      key: "name",
      header: "Agent",
      cell: (row) => (
        <div className="flex items-center gap-3">
          <div className="flex items-center justify-center h-10 w-10 rounded-full bg-primary/10 text-primary font-bold">
            {row.name.charAt(0)}
          </div>
          <div>
            <p className="font-medium text-foreground hover:underline cursor-pointer" onClick={() => navigate(`/agents/${row.id}`)}>
              {row.name}
            </p>
            <p className="text-xs text-muted-foreground">{row.voice || "Piper Voice"}</p>
          </div>
        </div>
      ),
    },
    {
      key: "status",
      header: "Status",
      cell: (row) => (
        <StatusIndicator
          status={row.status === "active" ? "active" : "inactive"}
          pulse={row.status === "active"}
        />
      ),
    },
    {
      key: "metrics",
      header: "Performance",
      cell: (row) => (
        <div>
          <p className="font-medium text-foreground">{row.successRate || 88.5}% Success</p>
          <p className="text-xs text-muted-foreground">{(row.totalCalls || 42).toLocaleString()} total calls</p>
        </div>
      ),
    },
    {
      key: "language",
      header: "Language",
      cell: (row) => <Badge variant="secondary">{row.default_language || "en-US"}</Badge>,
    },
    {
      key: "lastActive",
      header: "Last Active",
      cell: (row) => <span className="text-muted-foreground text-sm">{row.lastActive || "Just now"}</span>,
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
            <DropdownMenuItem onClick={() => navigate(`/agents/${row.id}`)}>Edit Config</DropdownMenuItem>
            <DropdownMenuItem onClick={() => navigate(`/playground`)}>Test in Playground</DropdownMenuItem>
            <DropdownMenuSeparator />
            <DropdownMenuItem className="text-destructive">Delete Agent</DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      ),
    },
  ]

  const filteredData = agents.filter(
    (agent: any) =>
      (agent.name || "").toLowerCase().includes(searchQuery.toLowerCase()) || 
      (agent.voice || "").toLowerCase().includes(searchQuery.toLowerCase())
  )

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="space-y-6"
    >
      <PageHeader
        title="AI Agents"
        description="Manage and configure your voice AI assistants."
        actions={
          <Button onClick={() => navigate("/agents/new")}>
            <Plus className="h-4 w-4 mr-2" />
            New Agent
          </Button>
        }
      />

      <div className="flex items-center justify-between gap-4">
        <div className="flex items-center gap-3 flex-1 max-w-md">
          <div className="relative flex-1">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
            <Input
              placeholder="Search agents..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="pl-9 bg-card"
            />
          </div>
          <Button variant="outline" size="icon">
            <Filter className="h-4 w-4" />
          </Button>
        </div>
        
        {selectedRows.size > 0 && (
          <div className="flex items-center gap-2 text-sm">
            <span className="text-muted-foreground">{selectedRows.size} selected</span>
            <Button variant="secondary" size="sm">Bulk Delete</Button>
          </div>
        )}
      </div>

      <DataTable
        columns={columns}
        data={filteredData}
        selectable
        selectedRows={selectedRows}
        onSelectionChange={setSelectedRows}
        getRowId={(row) => row.id}
        emptyTitle="No agents found"
        emptyDescription={searchQuery ? "Try adjusting your search query." : "Get started by creating your first AI voice agent."}
      />
    </motion.div>
  )
}
