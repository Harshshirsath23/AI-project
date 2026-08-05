import * as React from "react"
import { useNavigate } from "react-router-dom"
import { motion, AnimatePresence } from "framer-motion"
import { PageHeader } from "@/components/ui/page-header"
import { Card, CardContent } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { ArrowLeft, UploadCloud, FileType, CheckCircle2, AlertCircle } from "lucide-react"

export function ImportLeadsPage() {
  const navigate = useNavigate()
  const [dragActive, setDragActive] = React.useState(false)
  const [file, setFile] = React.useState<File | null>(null)
  const [uploading, setUploading] = React.useState(false)
  const [success, setSuccess] = React.useState(false)

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
      setFile(e.dataTransfer.files[0])
    }
  }

  const handleSimulateUpload = async () => {
    if (!file) return
    setUploading(true)
    await new Promise(r => setTimeout(r, 2000))
    setUploading(false)
    setSuccess(true)
  }

  return (
    <div className="max-w-3xl mx-auto space-y-8 pb-12">
      <PageHeader
        title="Import Leads"
        description="Upload a CSV file to import contacts in bulk."
        breadcrumbs={[{ label: "Leads", href: "/leads" }, { label: "Import" }]}
        actions={
          <Button variant="outline" onClick={() => navigate("/leads")}>
            <ArrowLeft className="mr-2 h-4 w-4" /> Back to Leads
          </Button>
        }
      />

      <Card className="overflow-hidden border-2 shadow-sm">
        <CardContent className="p-8">
          <AnimatePresence mode="wait">
            {!success ? (
              <motion.div
                key="upload"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0, scale: 0.95 }}
                className="space-y-6"
              >
                {!file ? (
                  <div
                    onDragEnter={handleDrag}
                    onDragLeave={handleDrag}
                    onDragOver={handleDrag}
                    onDrop={handleDrop}
                    className={`border-2 border-dashed rounded-2xl p-12 text-center transition-colors ${
                      dragActive ? "border-primary bg-primary/5" : "border-border hover:border-primary/50 hover:bg-muted/50"
                    }`}
                  >
                    <div className="w-16 h-16 rounded-full bg-primary/10 text-primary flex items-center justify-center mx-auto mb-4">
                      <UploadCloud className="h-8 w-8" />
                    </div>
                    <h3 className="text-xl font-semibold mb-2">Drag & drop your CSV file</h3>
                    <p className="text-muted-foreground text-sm mb-6 max-w-sm mx-auto">
                      Ensure your CSV includes a "Phone" column. Other columns will be imported as metadata.
                    </p>
                    <label htmlFor="file-upload" className="cursor-pointer inline-block">
                      <Button type="button" className="pointer-events-none">Browse Files</Button>
                    </label>

                    <input
                      id="file-upload"
                      type="file"
                      accept=".csv"
                      className="hidden"
                      onChange={(e) => e.target.files && setFile(e.target.files[0])}
                    />
                  </div>
                ) : (
                  <div className="space-y-6">
                    <div className="p-6 border-2 border-primary/20 bg-primary/5 rounded-2xl flex items-center gap-4">
                      <div className="h-12 w-12 rounded-xl bg-background flex items-center justify-center border shadow-sm">
                        <FileType className="h-6 w-6 text-blue-500" />
                      </div>
                      <div className="flex-1 min-w-0">
                        <p className="font-semibold text-lg truncate">{file.name}</p>
                        <p className="text-sm text-muted-foreground">{(file.size / 1024).toFixed(1)} KB • CSV Document</p>
                      </div>
                      <Button variant="ghost" size="icon" onClick={() => setFile(null)}>
                        <AlertCircle className="h-5 w-5 text-destructive" />
                      </Button>
                    </div>

                    <div className="flex justify-end gap-3 pt-4 border-t">
                      <Button variant="ghost" onClick={() => setFile(null)}>Cancel</Button>
                      <Button onClick={handleSimulateUpload} loading={uploading} className="min-w-[120px]">
                        Import Leads
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
                <motion.div
                  initial={{ scale: 0 }}
                  animate={{ scale: 1 }}
                  transition={{ type: "spring", damping: 12, delay: 0.1 }}
                  className="w-20 h-20 rounded-full bg-green-100 dark:bg-green-900/30 text-green-600 dark:text-green-400 flex items-center justify-center mx-auto"
                >
                  <CheckCircle2 className="h-10 w-10" />
                </motion.div>
                <div>
                  <h3 className="text-2xl font-bold mb-2">Import Successful!</h3>
                  <p className="text-muted-foreground max-w-sm mx-auto">
                    Successfully imported 5,000 leads from <span className="font-medium text-foreground">{file?.name}</span>.
                  </p>
                </div>
                <div className="pt-4 flex items-center justify-center gap-3">
                  <Button variant="outline" onClick={() => { setFile(null); setSuccess(false) }}>
                    Import Another
                  </Button>
                  <Button onClick={() => navigate("/leads")}>
                    View Leads
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
