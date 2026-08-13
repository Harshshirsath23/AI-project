import * as React from "react"
import { motion } from "framer-motion"
import { PageHeader } from "@/components/ui/page-header"
import { DataTable, type Column } from "@/components/ui/data-table"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle } from "@/components/ui/dialog"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Search, Filter, FileText, Download, Bot, User, PhoneCall } from "lucide-react"
import { api } from "@/services/api"

export function CallHistoryPage() {
  const [calls, setCalls] = React.useState<any[]>([])
  const [selectedCall, setSelectedCall] = React.useState<any | null>(null)
  const [isDialogOpen, setIsDialogOpen] = React.useState(false)
  const [searchQuery, setSearchQuery] = React.useState("")

  React.useEffect(() => {
    api.getCalls()
      .then(data => setCalls(data))
      .catch(err => console.error("Error loading call history:", err))
  }, [])

  const handleOpenTranscript = (row: any) => {
    setSelectedCall(row)
    setIsDialogOpen(true)
  }

  // Parse transcript JSON from DB
  const parsedTranscript = React.useMemo(() => {
    if (!selectedCall?.transcript) {
      return []
    }
    try {
      if (typeof selectedCall.transcript === "string") {
        return JSON.parse(selectedCall.transcript)
      }
      if (Array.isArray(selectedCall.transcript)) {
        return selectedCall.transcript
      }
      return [{ role: "assistant", content: String(selectedCall.transcript) }]
    } catch (e) {
      return [{ role: "assistant", content: String(selectedCall.transcript) }]
    }
  }, [selectedCall])

  const columns: Column<any>[] = [
    {
      key: "contact",
      header: "Contact / Target",
      cell: (row) => (
        <div>
          <div className="font-medium text-foreground">{row.contactName || row.to_number || "Target Phone"}</div>
          <div className="text-xs text-muted-foreground font-mono">{row.to_number || "N/A"}</div>
        </div>
      ),
    },
    {
      key: "outcome",
      header: "Status / Outcome",
      cell: (row) => {
        const s = (row.status || "completed").toLowerCase()
        if (s === "completed") return <Badge variant="secondary" className="bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400">Completed</Badge>
        if (s === "in-progress" || s === "ringing") return <Badge variant="secondary" className="bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400">In Progress</Badge>
        if (s === "queued") return <Badge variant="outline">Queued</Badge>
        return <Badge variant="secondary" className="bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400">Failed / No Answer</Badge>
      },
    },
    {
      key: "sentiment",
      header: "AI Sentiment",
      cell: (row) => {
        const s = (row.sentiment || "neutral").toLowerCase()
        if (s === "interested" || s === "positive") {
          return <Badge variant="secondary" className="bg-emerald-100 text-emerald-700 dark:bg-emerald-950 dark:text-emerald-300 font-semibold capitalize">Interested</Badge>
        }
        if (s === "not-interested" || s === "negative") {
          return <Badge variant="secondary" className="bg-rose-100 text-rose-700 dark:bg-rose-950 dark:text-rose-300 font-semibold capitalize">Not Interested</Badge>
        }
        return <Badge variant="outline" className="capitalize text-muted-foreground">{s}</Badge>
      },
    },
    {
      key: "details",
      header: "Caller ID / Agent",
      cell: (row) => (
        <div>
          <div className="text-sm font-medium">{row.agent_name || "Voice AI Agent"}</div>
          <div className="text-xs text-muted-foreground font-mono">{row.from_number || "System Number"}</div>
        </div>
      ),
    },
    {
      key: "duration",
      header: "Duration",
      cell: (row) => {
        const secs = row.duration_seconds || 0
        const mins = Math.floor(secs / 60)
        const rem = secs % 60
        return <span className="text-sm font-mono">{`${mins}:${rem.toString().padStart(2, '0')}`}</span>
      },
    },
    {
      key: "actions",
      header: "Action",
      cell: (row) => (
        <div className="flex gap-2 justify-end">
          <Button variant="outline" size="sm" onClick={() => handleOpenTranscript(row)}>
            <FileText className="mr-1.5 h-3.5 w-3.5" /> View Analysis & Transcript
          </Button>
        </div>
      ),
    },
  ]

  const filteredCalls = calls.filter((c: any) =>
    (c.to_number || "").toLowerCase().includes(searchQuery.toLowerCase()) ||
    (c.contactName || "").toLowerCase().includes(searchQuery.toLowerCase())
  )

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-6">
      <PageHeader
        title="Call History & Transcripts"
        description="Review past AI calls, inspect full dialogue transcripts, and analyze sentiment logs."
        actions={
          <Button variant="outline"><Download className="mr-2 h-4 w-4" /> Export CSV</Button>
        }
      />

      <div className="flex items-center justify-between w-full">
        <div className="relative w-full max-w-sm">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground pointer-events-none" />
          <Input
            placeholder="Search calls by phone or contact..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="pl-9 bg-card"
          />
        </div>
        <Button variant="outline"><Filter className="mr-2 h-4 w-4" /> Filter Logs</Button>
      </div>

      <DataTable
        columns={columns}
        data={filteredCalls}
        getRowId={(row) => row.id}
        emptyTitle="No call records found"
        emptyDescription="Calls will appear here automatically once initiated."
      />

      {/* Transcript & AI Summary Modal Dialog */}
      <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
        <DialogContent className="sm:max-w-[550px]">
          <DialogHeader>
            <DialogTitle className="flex items-center gap-2">
              <PhoneCall className="h-5 w-5 text-primary" /> Call Analysis & Transcript Log
            </DialogTitle>
            <DialogDescription>
              Dial Target: <span className="font-mono text-foreground font-semibold">{selectedCall?.to_number || "Unknown Target"}</span>
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
            {parsedTranscript.length === 0 ? (
              <div className="p-8 text-center text-xs text-muted-foreground italic">
                No speech transcript turns recorded for this call session.
              </div>
            ) : (
              <div className="space-y-4">
                {parsedTranscript.map((msg: any, idx: number) => (
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
            )}
          </ScrollArea>

          <div className="flex justify-end pt-2">
            <Button variant="secondary" onClick={() => setIsDialogOpen(false)}>Close</Button>
          </div>
        </DialogContent>
      </Dialog>
    </motion.div>
  )
}
