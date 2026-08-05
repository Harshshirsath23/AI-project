import * as React from "react"
import { useNavigate } from "react-router-dom"
import {
  CommandDialog,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
  CommandList,
  CommandSeparator,
  CommandShortcut,
} from "@/components/ui/command"
import {
  LayoutDashboard,
  Bot,
  Megaphone,
  Users,
  BookOpen,
  FileText,
  Phone,
  Activity,
  BarChart3,
  FlaskConical,
  Settings,
  Plus,
  Search,
} from "lucide-react"

interface CommandPaletteProps {
  open: boolean
  onOpenChange: (open: boolean) => void
}

const pages = [
  { name: "Dashboard", href: "/", icon: LayoutDashboard },
  { name: "AI Agents", href: "/agents", icon: Bot },
  { name: "Campaigns", href: "/campaigns", icon: Megaphone },
  { name: "Leads", href: "/leads", icon: Users },
  { name: "Knowledge Base", href: "/knowledge-base", icon: BookOpen },
  { name: "Scripts", href: "/scripts", icon: FileText },
  { name: "Calls", href: "/calls", icon: Phone },
  { name: "Live Monitor", href: "/live", icon: Activity },
  { name: "Analytics", href: "/analytics", icon: BarChart3 },
  { name: "AI Playground", href: "/playground", icon: FlaskConical },
  { name: "Settings", href: "/settings", icon: Settings },
]

const quickActions = [
  { name: "Create AI Agent", href: "/agents/new", icon: Plus, shortcut: "A" },
  { name: "New Campaign", href: "/campaigns/new", icon: Plus, shortcut: "C" },
  { name: "Import Leads", href: "/leads/import", icon: Plus, shortcut: "L" },
]

export function CommandPalette({ open, onOpenChange }: CommandPaletteProps) {
  const navigate = useNavigate()

  const runCommand = React.useCallback(
    (command: () => void) => {
      onOpenChange(false)
      command()
    },
    [onOpenChange]
  )

  return (
    <CommandDialog open={open} onOpenChange={onOpenChange}>
      <CommandInput placeholder="Type a command or search..." />
      <CommandList>
        <CommandEmpty>
          <div className="flex flex-col items-center gap-2 py-4">
            <Search className="h-8 w-8 text-muted-foreground/50" />
            <p>No results found.</p>
          </div>
        </CommandEmpty>

        <CommandGroup heading="Quick Actions">
          {quickActions.map((action) => (
            <CommandItem
              key={action.href}
              onSelect={() => runCommand(() => navigate(action.href))}
            >
              <action.icon className="mr-2 h-4 w-4" />
              {action.name}
              <CommandShortcut>{action.shortcut}</CommandShortcut>
            </CommandItem>
          ))}
        </CommandGroup>

        <CommandSeparator />

        <CommandGroup heading="Pages">
          {pages.map((page) => (
            <CommandItem
              key={page.href}
              onSelect={() => runCommand(() => navigate(page.href))}
            >
              <page.icon className="mr-2 h-4 w-4" />
              {page.name}
            </CommandItem>
          ))}
        </CommandGroup>
      </CommandList>
    </CommandDialog>
  )
}
