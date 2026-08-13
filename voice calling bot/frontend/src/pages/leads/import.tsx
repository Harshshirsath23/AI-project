import * as React from "react"
import { useNavigate } from "react-router-dom"
import { motion, AnimatePresence } from "framer-motion"
import { PageHeader } from "@/components/ui/page-header"
import { Card, CardContent } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { ArrowLeft, UploadCloud, FileType, CheckCircle2, AlertCircle, Loader2, Sparkles, Megaphone } from "lucide-react"
import { api } from "@/services/api"

interface ParsedRow {
  name: string
  phone: string
  email?: string
  company?: string
  [key: string]: any
}

export function ImportLeadsPage() {
  const navigate = useNavigate()
  const [dragActive, setDragActive] = React.useState(false)
  const [file, setFile] = React.useState<File | null>(null)
  const [previewRows, setPreviewRows] = React.useState<ParsedRow[]>([])
  const [totalRowCount, setTotalRowCount] = React.useState(0)
  const [detectedColumns, setDetectedColumns] = React.useState<string[]>([])
  const [uploading, setUploading] = React.useState(false)
  const [importedCount, setImportedCount] = React.useState<number | null>(null)
  const [errorMessage, setErrorMessage] = React.useState<string | null>(null)

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true)
    } else if (e.type === "dragleave") {
      setDragActive(false)
    }
  }

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    setDragActive(false)
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      processFile(e.dataTransfer.files[0])
    }
  }

  // Parse CSV client-side for immediate user preview
  const processFile = (selectedFile: File) => {
    if (!selectedFile.name.endsWith(".csv")) {
      setErrorMessage("Please select a valid .csv file.")
      return
    }
    setErrorMessage(null)
    setFile(selectedFile)

    const reader = new FileReader()
    reader.onload = (e) => {
      const text = e.target?.result as string
      if (!text) return

      const lines = text.split(/\r?\n/).filter(line => line.trim().length > 0)
      if (lines.length === 0) return

      // Extract headers
      const headers = lines[0].split(",").map(h => h.trim().replace(/^["']|["']$/g, ""))
      setDetectedColumns(headers)

      const rows: ParsedRow[] = []
      for (let i = 1; i < lines.length; i++) {
        const values = lines[i].split(",").map(v => v.trim().replace(/^["']|["']$/g, ""))
        if (values.length >= 1) {
          const rowObj: any = {}
          headers.forEach((h, idx) => {
            rowObj[h] = values[idx] || ""
          })

          const normRow: any = {}
          Object.keys(rowObj).forEach(k => {
            normRow[k.toLowerCase()] = rowObj[k]
          })

          rows.push({
            name: normRow.name || normRow.full_name || normRow.contact_name || "Lead",
            phone: normRow.phone || normRow.phone_number || normRow.mobile || normRow.contact_number || values[0] || "",
            email: normRow.email || normRow.email_address || "",
            company: normRow.company || normRow.organization || "",
          })
        }
      }

      setTotalRowCount(rows.length)
      setPreviewRows(rows.slice(0, 5))
    }
    reader.readAsText(selectedFile)
  }

  // Upload real file to PostgreSQL backend
  const handleRealUpload = async () => {
    if (!file) return
    setUploading(true)
    setErrorMessage(null)

    try {
      const result = await api.uploadLeadsCsv(file)
      setImportedCount(result.imported_count || totalRowCount)
    } catch (err: any) {
      console.error("Upload error:", err)
      setErrorMessage(err.message || "Failed to upload CSV leads to PostgreSQL.")
    } finally {
      setUploading(false)
    }
  }

  const resetImport = () => {
    setFile(null)
    setPreviewRows([])
    setTotalRowCount(0)
    setDetectedColumns([])
    setImportedCount(null)
    setErrorMessage(null)
  }

  return (
    <div className="max-w-4xl mx-auto space-y-8 pb-12">
      <PageHeader
        title="Import Leads"
        description="Upload a real CSV file to import and persist contacts in PostgreSQL for outbound campaigns."
        breadcrumbs={[{ label: "Leads", href: "/leads" }, { label: "Import" }]}
        actions={
          <Button variant="outline" onClick={() => navigate("/leads")}>
            <ArrowLeft className="mr-2 h-4 w-4" /> Back to Leads
          </Button>
        }
      />

      {errorMessage && (
        <div className="p-4 bg-destructive/10 border border-destructive/20 text-destructive rounded-xl text-sm flex items-center gap-2">
          <AlertCircle className="h-5 w-5 shrink-0" />
          <span>{errorMessage}</span>
        </div>
      )}

      <Card className="overflow-hidden border shadow-sm">
        <CardContent className="p-8">
          <AnimatePresence mode="wait">
            {importedCount === null ? (
              <motion.div
                key="upload"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0, scale: 0.98 }}
                className="space-y-6"
              >
                {!file ? (
                  <div
                    onDragEnter={handleDrag}
                    onDragLeave={handleDrag}
                    onDragOver={handleDrag}
                    onDrop={handleDrop}
                    className={`border-2 border-dashed rounded-2xl p-12 text-center transition-all ${
                      dragActive ? "border-primary bg-primary/5 scale-[1.01]" : "border-border hover:border-primary/50 hover:bg-muted/30"
                    }`}
                  >
                    <div className="w-16 h-16 rounded-full bg-primary/10 text-primary flex items-center justify-center mx-auto mb-4">
                      <UploadCloud className="h-8 w-8" />
                    </div>
                    <h3 className="text-xl font-semibold mb-2">Drag & drop your CSV file here</h3>
                    <p className="text-muted-foreground text-sm mb-6 max-w-md mx-auto">
                      Columns supported: <code className="text-primary font-mono font-semibold">Name</code>, <code className="text-primary font-mono font-semibold">Phone</code>, <code className="text-primary font-mono font-semibold">Email</code>, <code className="text-primary font-mono font-semibold">Company</code>.
                    </p>
                    <label htmlFor="file-upload" className="cursor-pointer inline-block">
                      <Button type="button" className="pointer-events-none">
                        Browse CSV Files
                      </Button>
                    </label>

                    <input
                      id="file-upload"
                      type="file"
                      accept=".csv"
                      className="hidden"
                      onChange={(e) => e.target.files && e.target.files[0] && processFile(e.target.files[0])}
                    />
                  </div>
                ) : (
                  <div className="space-y-6">
                    {/* File Card */}
                    <div className="p-5 border bg-muted/20 rounded-xl flex items-center justify-between">
                      <div className="flex items-center gap-4">
                        <div className="h-12 w-12 rounded-xl bg-primary/10 flex items-center justify-center border text-primary">
                          <FileType className="h-6 w-6" />
                        </div>
                        <div>
                          <p className="font-semibold text-foreground text-base">{file.name}</p>
                          <div className="flex items-center gap-2 text-xs text-muted-foreground mt-0.5">
                            <span>{(file.size / 1024).toFixed(1)} KB</span>
                            <span>•</span>
                            <span className="text-foreground font-semibold font-mono">{totalRowCount} total records</span>
                          </div>
                        </div>
                      </div>
                      <Button variant="ghost" size="sm" onClick={resetImport} className="text-destructive hover:text-destructive">
                        Remove
                      </Button>
                    </div>

                    {/* Detected Column Badges */}
                    <div className="space-y-2">
                      <div className="flex items-center justify-between">
                        <span className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">Detected Headers</span>
                        <Badge variant="outline" className="text-xs">{detectedColumns.length} Columns</Badge>
                      </div>
                      <div className="flex flex-wrap gap-1.5">
                        {detectedColumns.map((col, idx) => (
                          <Badge key={idx} variant="secondary" className="font-mono text-xs">
                            {col}
                          </Badge>
                        ))}
                      </div>
                    </div>

                    {/* Preview Table */}
                    {previewRows.length > 0 && (
                      <div className="space-y-2 border rounded-xl overflow-hidden">
                        <div className="p-3 bg-muted/40 border-b flex items-center justify-between text-xs font-semibold">
                          <span>Data Preview (First {previewRows.length} Rows)</span>
                          <span className="text-muted-foreground">Ready for PostgreSQL insert</span>
                        </div>
                        <div className="overflow-x-auto">
                          <table className="w-full text-xs text-left">
                            <thead className="bg-muted/20 border-b text-muted-foreground font-medium">
                              <tr>
                                <th className="p-2.5 pl-4">Lead Name</th>
                                <th className="p-2.5">Phone Number</th>
                                <th className="p-2.5">Email</th>
                                <th className="p-2.5 pr-4">Company</th>
                              </tr>
                            </thead>
                            <tbody className="divide-y divide-border">
                              {previewRows.map((row, idx) => (
                                <tr key={idx} className="hover:bg-muted/10">
                                  <td className="p-2.5 pl-4 font-medium">{row.name}</td>
                                  <td className="p-2.5 font-mono text-primary font-semibold">{row.phone}</td>
                                  <td className="p-2.5 text-muted-foreground">{row.email || "—"}</td>
                                  <td className="p-2.5 pr-4 text-muted-foreground">{row.company || "—"}</td>
                                </tr>
                              ))}
                            </tbody>
                          </table>
                        </div>
                      </div>
                    )}

                    <div className="flex justify-end gap-3 pt-4 border-t">
                      <Button variant="outline" onClick={resetImport} disabled={uploading}>
                        Cancel
                      </Button>
                      <Button onClick={handleRealUpload} disabled={uploading} className="min-w-[150px]">
                        {uploading ? (
                          <>
                            <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                            Importing to DB...
                          </>
                        ) : (
                          <>
                            <Sparkles className="mr-2 h-4 w-4" />
                            Import {totalRowCount} Leads
                          </>
                        )}
                      </Button>
                    </div>
                  </div>
                )}
              </motion.div>
            ) : (
              <motion.div
                key="success"
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                className="py-12 text-center space-y-6"
              >
                <div className="w-20 h-20 rounded-full bg-green-100 dark:bg-green-900/30 text-green-600 dark:text-green-400 flex items-center justify-center mx-auto shadow-sm">
                  <CheckCircle2 className="h-10 w-10" />
                </div>
                <div className="space-y-1">
                  <h3 className="text-2xl font-bold">Import Successful!</h3>
                  <p className="text-muted-foreground max-w-md mx-auto text-sm">
                    Successfully inserted <span className="font-bold text-foreground font-mono">{importedCount} leads</span> into your PostgreSQL database.
                  </p>
                </div>
                <div className="pt-4 flex items-center justify-center gap-3">
                  <Button variant="outline" onClick={resetImport}>
                    Import Another File
                  </Button>
                  <Button onClick={() => navigate("/leads")}>
                    View Leads Table
                  </Button>
                  <Button variant="default" className="bg-primary hover:bg-primary/90" onClick={() => navigate("/campaigns/new")}>
                    <Megaphone className="mr-2 h-4 w-4" /> Launch Campaign
                  </Button>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </CardContent>
      </Card>
    </div>
  )
}
