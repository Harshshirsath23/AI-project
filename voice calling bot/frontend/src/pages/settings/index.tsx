import { motion } from "framer-motion"
import { PageHeader } from "@/components/ui/page-header"
import { Card, CardContent, CardHeader, CardTitle, CardDescription, CardFooter } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Phone, Link2, Key, Users, Building, ShieldCheck, Webhook, CheckCircle2 } from "lucide-react"

import * as React from "react"
import { api } from "@/services/api"

export function SettingsPage() {
  const [settings, setSettings] = React.useState<any>(null)

  React.useEffect(() => {
    api.getSettings()
      .then(res => setSettings(res))
      .catch(err => console.error("Error loading settings:", err))
  }, [])

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-6 pb-12 max-w-5xl">
      <PageHeader
        title="Settings & Integrations"
        description="Manage your organization, billing, and third-party integrations."
      />

      <Tabs defaultValue="integrations" className="space-y-6">
        <TabsList className="bg-card border h-12 p-1">
          <TabsTrigger value="integrations" className="data-[state=active]:bg-primary/10 data-[state=active]:text-primary">
            <Link2 className="mr-2 h-4 w-4" /> Integrations
          </TabsTrigger>
          <TabsTrigger value="org" className="data-[state=active]:bg-primary/10 data-[state=active]:text-primary">
            <Building className="mr-2 h-4 w-4" /> Organization
          </TabsTrigger>
          <TabsTrigger value="apikeys" className="data-[state=active]:bg-primary/10 data-[state=active]:text-primary">
            <Key className="mr-2 h-4 w-4" /> API Keys
          </TabsTrigger>
        </TabsList>

        <TabsContent value="integrations" className="space-y-6">
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
            {[
              { name: "Twilio", type: "Telephony", status: "connected", icon: Phone },
              { name: "ElevenLabs", type: "Voice TTS", status: "connected", icon: ShieldCheck },
              { name: "OpenAI", type: "LLM Engine", status: "connected", icon: ShieldCheck },
              { name: "Salesforce", type: "CRM", status: "disconnected", icon: Users },
              { name: "HubSpot", type: "CRM", status: "disconnected", icon: Users },
              { name: "Custom Webhook", type: "API", status: "disconnected", icon: Webhook },
            ].map((integration, i) => (
              <Card key={i} className={`border-2 ${integration.status === 'connected' ? 'border-primary/20' : ''}`}>
                <CardContent className="p-6">
                  <div className="flex items-start justify-between mb-4">
                    <div className="w-12 h-12 rounded-xl bg-muted flex items-center justify-center">
                      <integration.icon className="h-6 w-6 text-foreground" />
                    </div>
                    {integration.status === "connected" && (
                      <span className="flex items-center gap-1 text-xs font-medium text-green-600 dark:text-green-400 bg-green-100 dark:bg-green-900/30 px-2 py-1 rounded-full">
                        <CheckCircle2 className="h-3 w-3" /> Connected
                      </span>
                    )}
                  </div>
                  <h3 className="font-semibold text-lg">{integration.name}</h3>
                  <p className="text-sm text-muted-foreground">{integration.type}</p>
                </CardContent>
                <CardFooter className="p-4 bg-muted/20 border-t">
                  <Button variant={integration.status === 'connected' ? 'outline' : 'default'} className="w-full">
                    {integration.status === 'connected' ? 'Configure' : 'Connect'}
                  </Button>
                </CardFooter>
              </Card>
            ))}
          </div>
        </TabsContent>

        <TabsContent value="org" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Organization Details</CardTitle>
              <CardDescription>Manage your company information and branding.</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4 max-w-xl">
              <div className="space-y-2">
                <Input defaultValue={settings?.app_name || "Voxera AI Calling Platform"} />
              </div>
              <div className="space-y-2">
                <Label>Twilio Account SID</Label>
                <Input defaultValue={settings?.twilio_account_sid || "ACbb3cd69ae8979164dd994177807ebb31"} readOnly />
              </div>
              <div className="space-y-2">
                <Label>Assigned Phone Number</Label>
                <Input defaultValue={settings?.twilio_phone_number || "+17372212163"} readOnly />
              </div>

              <Button>Save Changes</Button>
            </CardContent>
          </Card>
        </TabsContent>
        
        <TabsContent value="apikeys" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>API Keys</CardTitle>
              <CardDescription>Manage your secret API keys to authenticate requests.</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="p-4 border rounded-lg bg-muted flex items-center justify-between">
                <div className="font-mono text-sm">pk_live_**********************a8f9</div>
                <Button variant="outline" size="sm">Revoke</Button>
              </div>
              <Button>
                <Key className="mr-2 h-4 w-4" /> Generate New Key
              </Button>
            </CardContent>
          </Card>
        </TabsContent>

      </Tabs>
    </motion.div>
  )
}
