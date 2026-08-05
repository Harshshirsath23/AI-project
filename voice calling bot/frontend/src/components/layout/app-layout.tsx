import * as React from "react"
import { Outlet } from "react-router-dom"
import { motion } from "framer-motion"
import { Sidebar } from "@/components/layout/sidebar"
import { TopNav } from "@/components/layout/top-nav"
import { CommandPalette } from "@/components/layout/command-palette"
import { TooltipProvider } from "@/components/ui/tooltip"

export function AppLayout() {
  const [sidebarCollapsed, setSidebarCollapsed] = React.useState(false)
  const [commandOpen, setCommandOpen] = React.useState(false)

  // Keyboard shortcuts
  React.useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      // Cmd+K — open command palette
      if ((e.metaKey || e.ctrlKey) && e.key === "k") {
        e.preventDefault()
        setCommandOpen((prev) => !prev)
      }
      // [ — toggle sidebar
      if (e.key === "[" && !e.metaKey && !e.ctrlKey && !e.altKey) {
        const tag = (e.target as HTMLElement)?.tagName
        if (tag === "INPUT" || tag === "TEXTAREA" || (e.target as HTMLElement)?.isContentEditable) return
        e.preventDefault()
        setSidebarCollapsed((prev) => !prev)
      }
    }
    window.addEventListener("keydown", handleKeyDown)
    return () => window.removeEventListener("keydown", handleKeyDown)
  }, [])

  return (
    <TooltipProvider delayDuration={200}>
      <div className="min-h-screen bg-background">
        <Sidebar collapsed={sidebarCollapsed} onToggle={() => setSidebarCollapsed((p) => !p)} />

        <motion.div
          initial={false}
          animate={{ marginLeft: sidebarCollapsed ? 72 : 260 }}
          transition={{ type: "spring", damping: 25, stiffness: 200 }}
          className="flex flex-col min-h-screen"
        >
          <TopNav onSearchOpen={() => setCommandOpen(true)} />

          <main className="flex-1 p-6">
            <motion.div
              key={undefined}
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.3, ease: "easeOut" }}
            >
              <Outlet />
            </motion.div>
          </main>
        </motion.div>

        <CommandPalette open={commandOpen} onOpenChange={setCommandOpen} />
      </div>
    </TooltipProvider>
  )
}
