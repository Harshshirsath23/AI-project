import * as React from "react"
import { motion } from "framer-motion"
import { PageHeader } from "@/components/ui/page-header"
import { DataTable, type Column } from "@/components/ui/data-table"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import { Badge } from "@/components/ui/badge"
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog"
import { Search, Plus, FileText, CheckCircle2, Upload, Loader2, Sparkles, Eye, Edit3, Save } from "lucide-react"
import { api } from "@/services/api"

export function KnowledgeBasePage() {
  const [activeKbId, setActiveKbId] = React.useState<string>("")
  const [documents, setDocuments] = React.useState<any[]>([])
  
  // Add modal state
  const [isDialogOpen, setIsDialogOpen] = React.useState(false)
  const [scriptTitle, setScriptTitle] = React.useState("")
  const [scriptText, setScriptText] = React.useState("")
  const [isSaving, setIsSaving] = React.useState(false)

  // Edit / View modal state
  const [selectedDoc, setSelectedDoc] = React.useState<any | null>(null)
  const [editTitle, setEditTitle] = React.useState("")
  const [editContent, setEditContent] = React.useState("")
  const [isEditDialogOpen, setIsEditDialogOpen] = React.useState(false)
  const [isUpdatingScript, setIsUpdatingScript] = React.useState(false)

  const loadKbsAndDocs = async () => {
    try {
      const kbs = await api.getKnowledgeBases()
      if (kbs && kbs.length > 0) {
        const kbId = kbs[0].id
        setActiveKbId(kbId)
        fetchDocuments(kbId)
      }
    } catch (err) {
      console.error("Error loading knowledge base:", err)
    }
  }

  const fetchDocuments = async (kbId: string) => {
    try {
      const data = await api.getKbDocuments(kbId)
      setDocuments(data || [])
    } catch (e) {
      console.error("Error fetching KB documents:", e)
    }
  }

  React.useEffect(() => {
    loadKbsAndDocs()
  }, [])

  // Upload / Submit Script Document
  const handleSaveScript = async () => {
    if (!scriptTitle.trim() || !scriptText.trim() || !activeKbId) return
    setIsSaving(true)

    try {
      await api.createKbTextDocument(activeKbId, {
        title: scriptTitle,
        script_text: scriptText,
      })
      setScriptTitle("")
      setScriptText("")
      setIsDialogOpen(false)
      fetchDocuments(activeKbId)
    } catch (err) {
      console.error("Error uploading script:", err)
    } finally {
      setIsSaving(false)
    }
  }

  const handleOpenEdit = (doc: any) => {
    setSelectedDoc(doc)
    setEditTitle(doc.title || doc.file_name)
    setEditContent(doc.content || doc.meta_data || doc.content_preview || "")
    setIsEditDialogOpen(true)
  }

  const handleUpdateScript = async () => {
    if (!selectedDoc || !editContent.trim()) return
    setIsUpdatingScript(true)
    try {
      await api.updateKbDocument(selectedDoc.id, {
        title: editTitle,
        content: editContent,
      })
      setIsEditDialogOpen(false)
      fetchDocuments(activeKbId)
    } catch (e) {
      console.error("Error updating script:", e)
    } finally {
      setIsUpdatingScript(false)
    }
  }

  const columns: Column<any>[] = [
    {
      key: "title",
      header: "Document / Script Title",
      cell: (row) => (
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-lg bg-primary/10 flex items-center justify-center text-primary shrink-0">
            <FileText className="h-4 w-4" />
          </div>
          <div>
            <div className="font-medium text-foreground">{row.title || row.file_name}</div>
            <div className="text-xs text-muted-foreground font-mono">{row.file_name} ({row.file_size} bytes)</div>
          </div>
        </div>
      ),
    },
    {
      key: "status",
      header: "Embedding Status",
      cell: () => (
        <Badge variant="secondary" className="bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400 gap-1">
          <CheckCircle2 className="h-3 w-3" /> Extracted & Embedded
        </Badge>
      ),
    },
    {
      key: "preview",
      header: "Extracted Text Preview",
      cell: (row) => (
        <p className="text-xs text-muted-foreground truncate max-w-[300px] font-mono">
          {row.content_preview || row.content || "Script text stored in PostgreSQL"}
        </p>
      ),
    },
    {
      key: "actions",
      header: "Actions",
      cell: (row) => (
        <div className="flex items-center gap-2">
          <Button variant="outline" size="sm" onClick={() => handleOpenEdit(row)}>
            <Eye className="mr-1.5 h-3.5 w-3.5" /> View / Edit Script
          </Button>
        </div>
      ),
    },
  ]

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-6">
      <PageHeader
        title="Knowledge Base & Conversation Scripts"
        description="Upload documents or write structured scripts for AI Agents to execute during live calls."
        actions={
          <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
            <DialogTrigger asChild>
              <Button>
                <Plus className="mr-2 h-4 w-4" /> Add Script / Upload Document
              </Button>
            </DialogTrigger>
            <DialogContent className="sm:max-w-[550px]">
              <DialogHeader>
                <DialogTitle className="flex items-center gap-2">
                  <Sparkles className="h-5 w-5 text-primary" /> Add Agent Conversation Script Document
                </DialogTitle>
                <DialogDescription>
                  Enter your call script (greeting, qualifying questions, answers). Text will be extracted, embedded, and stored in PostgreSQL.
                </DialogDescription>
              </DialogHeader>

              <div className="grid gap-4 py-4">
                <div className="space-y-2">
                  <label className="text-xs font-semibold">Script Document Title</label>
                  <Input
                    placeholder="e.g., Enterprise SDR Outbound Sales Script 2026"
                    value={scriptTitle}
                    onChange={(e) => setScriptTitle(e.target.value)}
                  />
                </div>
                <div className="space-y-2">
                  <label className="text-xs font-semibold">Script Content & Guidelines (Extracted Text)</label>
                  <Textarea
                    placeholder={`Step 1: Greet the lead using name.\nStep 2: Ask about current call volume.\nStep 3: Answer questions about latency (<500ms) and pricing ($0.05/min).\nStep 4: Book qualifying demo meeting.`}
                    className="min-h-[180px] font-mono text-xs"
                    value={scriptText}
                    onChange={(e) => setScriptText(e.target.value)}
                  />
                </div>
              </div>

              <div className="flex justify-end gap-2">
                <Button variant="outline" onClick={() => setIsDialogOpen(false)}>Cancel</Button>
                <Button onClick={handleSaveScript} disabled={isSaving || !scriptTitle.trim() || !scriptText.trim()}>
                  {isSaving ? <Loader2 className="mr-2 h-4 w-4 animate-spin" /> : <Upload className="mr-2 h-4 w-4" />}
                  Extract & Save to DB
                </Button>
              </div>
            </DialogContent>
          </Dialog>
        }
      />

      <div className="flex items-center justify-between w-full">
        <div className="relative w-full max-w-sm">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground pointer-events-none" />
          <Input placeholder="Search knowledge base scripts..." className="pl-9 bg-card" />
        </div>
        <p className="text-xs text-muted-foreground font-mono">
          Knowledge Base ID: <span className="text-primary font-bold">{activeKbId || "Default KB"}</span>
        </p>
      </div>

      <DataTable
        columns={columns}
        data={documents}
        getRowId={(row) => row.id}
        emptyTitle="No knowledge base documents found"
        emptyDescription="Add a conversation script or document to get started."
      />


      {/* Edit / View Script Modal Dialog */}
      <Dialog open={isEditDialogOpen} onOpenChange={setIsEditDialogOpen}>
        <DialogContent className="sm:max-w-[650px]">
          <DialogHeader>
            <DialogTitle className="flex items-center gap-2">
              <Edit3 className="h-5 w-5 text-primary" /> View & Edit Script Document
            </DialogTitle>
            <DialogDescription>
              View or modify the exact script content used by AI agents during live phone calls.
            </DialogDescription>
          </DialogHeader>

          <div className="grid gap-4 py-4">
            <div className="space-y-2">
              <label className="text-xs font-semibold">Document Title</label>
              <Input
                value={editTitle}
                onChange={(e) => setEditTitle(e.target.value)}
              />
            </div>
            <div className="space-y-2">
              <label className="text-xs font-semibold">Full Script Content (Extracted Text Stored in PostgreSQL)</label>
              <Textarea
                className="min-h-[250px] font-mono text-xs leading-relaxed"
                value={editContent}
                onChange={(e) => setEditContent(e.target.value)}
              />
            </div>
          </div>

          <div className="flex justify-end gap-2">
            <Button variant="outline" onClick={() => setIsEditDialogOpen(false)}>Cancel</Button>
            <Button onClick={handleUpdateScript} disabled={isUpdatingScript || !editContent.trim()}>
              {isUpdatingScript ? <Loader2 className="mr-2 h-4 w-4 animate-spin" /> : <Save className="mr-2 h-4 w-4" />}
              Save Script Changes
            </Button>
          </div>
        </DialogContent>
      </Dialog>
    </motion.div>
  )
}
