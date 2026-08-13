import { motion } from "framer-motion"
import { PageHeader } from "@/components/ui/page-header"
import { DataTable, type Column } from "@/components/ui/data-table"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Search, Phone, CheckCircle2, ShieldAlert, RefreshCw } from "lucide-react"

import * as React from "react"
import { api } from "@/services/api"

interface PhoneNumberItem {
  id: string
  number: string
  provider: string
  status: string
  created_at?: string
}

export function PhoneNumbersPage() {
  const [numbers, setNumbers] = React.useState<PhoneNumberItem[]>([])
  const [search, setSearch] = React.useState("")
  const [isSyncing, setIsSyncing] = React.useState(false)

  const loadNumbers = React.useCallback(() => {
    api.getPhoneNumbers()
      .then(data => setNumbers(data))
      .catch(err => console.error("Error loading phone numbers:", err))
  }, [])

  React.useEffect(() => {
    loadNumbers()
  }, [loadNumbers])

  const handleFetchTwilio = async () => {
    setIsSyncing(true)
    try {
      const data = await api.syncTwilioPhoneNumbers()
      setNumbers(data)
    } catch (err) {
      console.error("Error syncing Twilio phone numbers:", err)
    } finally {
      setIsSyncing(false)
    }
  }

  const filteredNumbers = numbers.filter(n =>
    n.number.toLowerCase().includes(search.toLowerCase()) ||
    n.provider.toLowerCase().includes(search.toLowerCase())
  )

  const columns: Column<PhoneNumberItem>[] = [
    {
      key: "number",
      header: "Phone Number",
      cell: (row) => (
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-lg bg-primary/10 text-primary flex items-center justify-center shrink-0">
            <Phone className="h-4 w-4" />
          </div>
          <div>
            <div className="font-medium font-mono text-sm">{row.number}</div>
            <div className="text-[11px] text-muted-foreground uppercase font-mono tracking-wider">
              {row.provider} TELEPHONY CARRIER
            </div>
          </div>
        </div>
      ),
    },
    {
      key: "status",
      header: "Status",
      cell: (row) => {
        if (row.status === "active") return <Badge variant="secondary" className="bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400"><CheckCircle2 className="mr-1 h-3 w-3" /> Active</Badge>
        return <Badge variant="destructive"><ShieldAlert className="mr-1 h-3 w-3" /> Pending</Badge>
      },
    },
    {
      key: "provider",
      header: "Provider",
      cell: (row) => <Badge variant="outline" className="uppercase font-mono text-[11px]">{row.provider}</Badge>,
    },
    {
      key: "created_at",
      header: "Registered Date",
      cell: (row) => <span className="text-xs text-muted-foreground">{row.created_at ? new Date(row.created_at).toLocaleDateString() : "Active"}</span>,
    },
  ]

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-6">
      <PageHeader
        title="Phone Numbers"
        description="Manage your outbound Twilio phone numbers and carrier caller IDs."
        actions={
          <Button onClick={handleFetchTwilio} disabled={isSyncing} className="shadow-sm">
            <RefreshCw className={`mr-2 h-4 w-4 ${isSyncing ? 'animate-spin' : ''}`} />
            {isSyncing ? "Syncing Twilio..." : "Fetch Twilio Numbers"}
          </Button>
        }
      />
      <div className="flex items-center gap-3 w-full sm:w-[400px]">
        <div className="relative w-full">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground pointer-events-none" />
          <Input
            placeholder="Search phone numbers..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="pl-9 bg-card"
          />
        </div>
      </div>
      <DataTable
        columns={columns}
        data={filteredNumbers}
        getRowId={(row) => row.id}
        emptyTitle="No phone numbers found"
      />
    </motion.div>
  )
}
