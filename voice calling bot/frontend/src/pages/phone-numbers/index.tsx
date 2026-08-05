import { motion } from "framer-motion"
import { PageHeader } from "@/components/ui/page-header"
import { DataTable, type Column } from "@/components/ui/data-table"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Search, Plus, Phone, CheckCircle2, ShieldAlert } from "lucide-react"

interface PhoneNumber {
  id: string
  number: string
  provider: string
  friendlyName: string
  country: string
  status: "active" | "verification_required" | "suspended"
  isDefault?: boolean
}

import * as React from "react"
import { api } from "@/services/api"

export function PhoneNumbersPage() {
  const [numbers, setNumbers] = React.useState<any[]>([])

  React.useEffect(() => {
    api.getPhoneNumbers()
      .then(data => setNumbers(data))
      .catch(err => console.error("Error loading phone numbers:", err))
  }, [])

  const columns: Column<PhoneNumber>[] = [
    {
      key: "number",
      header: "Phone Number",
      cell: (row) => (
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-lg bg-primary/10 text-primary flex items-center justify-center shrink-0">
            <Phone className="h-4 w-4" />
          </div>
          <div>
            <div className="font-medium font-mono">{row.number}</div>
            <div className="text-xs text-muted-foreground">{row.friendlyName}</div>
          </div>
        </div>
      ),
    },
    {
      key: "status",
      header: "Status",
      cell: (row) => {
        if (row.status === "active") return <Badge variant="secondary" className="bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400"><CheckCircle2 className="mr-1 h-3 w-3" /> Active</Badge>
        if (row.status === "verification_required") return <Badge variant="destructive"><ShieldAlert className="mr-1 h-3 w-3" /> Verification Req.</Badge>
        return <Badge variant="outline">Suspended</Badge>
      },
    },
    {
      key: "provider",
      header: "Provider",
      cell: (row) => <Badge variant="outline">{row.provider}</Badge>,
    },
    {
      key: "country",
      header: "Country",
      cell: (row) => <span className="text-sm font-medium">{row.country}</span>,
    },
    {
      key: "isDefault",
      header: "",
      cell: (row) => row.isDefault ? <Badge variant="secondary">Default</Badge> : null,
    },
  ]

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-6">
      <PageHeader
        title="Phone Numbers"
        description="Manage your outbound phone numbers and caller IDs."
        actions={
          <Button>
            <Plus className="mr-2 h-4 w-4" /> Buy or Import Number
          </Button>
        }
      />
      <div className="flex items-center gap-3 w-full sm:w-[400px]">
        <div className="relative w-full">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground pointer-events-none" />
          <Input placeholder="Search phone numbers..." className="pl-9 bg-card" />
        </div>
      </div>
      <DataTable
        columns={columns}
        data={numbers}
        getRowId={(row) => row.id}
        emptyTitle="No phone numbers found"
      />

    </motion.div>
  )
}
