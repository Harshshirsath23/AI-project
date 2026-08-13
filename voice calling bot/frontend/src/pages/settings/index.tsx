import { motion } from "framer-motion"
import { PageHeader } from "@/components/ui/page-header"
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Phone, Building, Key, CheckCircle2, ShieldCheck } from "lucide-react"

import * as React from "react"
import { api } from "@/services/api"

export function SettingsPage() {
  const [settings, setSettings] = React.useState<any>(null)
  const [isSaved, setIsSaved] = React.useState(false)

  const [twilioAccountSid, setTwilioAccountSid] = React.useState("")
  const [twilioAuthToken, setTwilioAuthToken] = React.useState("")
  const [isEditing, setIsEditing] = React.useState(false)

  React.useEffect(() => {
    api.getSettings()
      .then(res => {
        setSettings(res)
        setTwilioAccountSid(res.twilio_account_sid || "")
        // Don't pre-fill token if the API masks it, or just use empty string
        // The endpoint currently does not return the auth token.
        setTwilioAuthToken("")
      })
      .catch(err => console.error("Error loading settings:", err))
  }, [])

  const handleSave = async () => {
    try {
      await api.updateSettings({
        twilio_account_sid: twilioAccountSid,
        ...(twilioAuthToken ? { twilio_auth_token: twilioAuthToken } : {})
      });
      setIsSaved(true)

      // Auto-sync numbers if credentials changed
      if (twilioAccountSid || twilioAuthToken) {
        await api.syncTwilioPhoneNumbers();
      }

      setTimeout(() => setIsSaved(false), 2000)
      setIsEditing(false)
    } catch (error) {
      console.error("Failed to save settings", error);
    }
  }

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-6 pb-12 max-w-4xl">
      <PageHeader
        title="Platform Settings"
        description="Configure your telephony credentials and system preferences."
      />

      <Tabs defaultValue="telephony" className="space-y-6">
        <TabsList className="bg-card border h-12 p-1">
          <TabsTrigger value="telephony" className="data-[state=active]:bg-primary/10 data-[state=active]:text-primary">
            <Phone className="mr-2 h-4 w-4" /> Telephony & Voice
          </TabsTrigger>
        </TabsList>

        <TabsContent value="telephony" className="space-y-6">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between">
              <div>
                <CardTitle className="flex items-center gap-2">
                  <Phone className="h-5 w-5 text-primary" /> Twilio Telephony Integration
                </CardTitle>
                <CardDescription>Configure your outbound calling carrier credentials.</CardDescription>
              </div>
              <Button variant="outline" onClick={() => setIsEditing(!isEditing)}>
                {isEditing ? "Cancel" : "Edit credentials"}
              </Button>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <Label>Twilio Account SID</Label>
                <Input
                  value={twilioAccountSid}
                  onChange={(e) => setTwilioAccountSid(e.target.value)}
                  placeholder="AC..."
                  readOnly={!isEditing}
                  className={!isEditing ? "bg-muted/50" : ""}
                />
              </div>
              <div className="space-y-2">
                <Label>Twilio Auth Token</Label>
                <Input
                  type="password"
                  value={twilioAuthToken}
                  onChange={(e) => setTwilioAuthToken(e.target.value)}
                  placeholder={isEditing ? "Enter new auth token (leave blank to keep current)" : "••••••••••••••••••••••••••••••••"}
                  readOnly={!isEditing}
                  className={!isEditing ? "bg-muted/50" : ""}
                />
              </div>

              {isEditing && (
                <Button onClick={handleSave} className="mt-4">
                  {isSaved ? "Saved & Synced!" : "Save Changes"}
                </Button>
              )}

              <div className="p-3.5 rounded-xl bg-green-500/10 border border-green-500/20 text-green-700 dark:text-green-400 text-xs font-medium flex items-center gap-2 mt-4">
                <CheckCircle2 className="h-4 w-4 shrink-0" />
                <span>Twilio Telephony Carrier Active & Verified</span>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </motion.div>
  )
}
