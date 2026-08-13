import React, { useEffect, useState } from "react";
import { PhoneOff, Activity, MessageSquare } from "lucide-react";
import { Button } from "./ui/button";

import { Card, CardHeader, CardTitle, CardContent } from "./ui/card";
import { Badge } from "./ui/badge";

interface LiveCallMonitorProps {
  callId: string;
  agentName?: string;
  customerName?: string;
}

interface TranscriptTurn {
  id: string;
  speaker: "agent" | "customer";
  text: string;
  timestamp: string;
}

export const LiveCallMonitor: React.FC<LiveCallMonitorProps> = ({
  callId,
  agentName = "AI Voice Agent",
  customerName = "Customer",
}) => {
  const [isConnected, setIsConnected] = useState(false);
  const [transcripts, setTranscripts] = useState<TranscriptTurn[]>([]);
  const [callStatus, setCallStatus] = useState<string>("connecting");

  useEffect(() => {
    // Construct WebSocket URL
    const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
    const host = window.location.host;
    const wsUrl = `${protocol}//${host}/ws/calls/${callId}`;

    const ws = new WebSocket(wsUrl);

    ws.onopen = () => {
      setIsConnected(true);
      setCallStatus("in-progress");
    };

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        if (data.event === "transcript") {
          setTranscripts((prev) => [
            ...prev,
            {
              id: String(Date.now()),
              speaker: data.speaker || "agent",
              text: data.text || "",
              timestamp: new Date().toLocaleTimeString(),
            },
          ]);
        } else if (data.event === "call_ended_by_user" || data.event === "ended") {
          setCallStatus("completed");
        }
      } catch (err) {
        console.error("Failed to parse WS event:", err);
      }
    };

    ws.onclose = () => {
      setIsConnected(false);
      setCallStatus("disconnected");
    };

    return () => {
      ws.close();
    };
  }, [callId]);

  return (
    <Card className="w-full max-w-2xl mx-auto shadow-lg border-primary/20">
      <CardHeader className="flex flex-row items-center justify-between border-b pb-4">
        <div className="space-y-1">
          <CardTitle className="text-lg font-bold flex items-center gap-2">
            <Activity className="h-5 w-5 text-primary animate-pulse" />
            Live Call Session
          </CardTitle>
          <p className="text-xs text-muted-foreground">ID: {callId}</p>
        </div>
        <div className="flex items-center gap-2">
          <Badge variant={isConnected ? "default" : "destructive"}>
            {callStatus.toUpperCase()}
          </Badge>
        </div>
      </CardHeader>
      <CardContent className="pt-6 space-y-6">
        <div className="flex justify-around items-center p-4 rounded-lg bg-muted/40 border">
          <div className="text-center">
            <p className="text-xs text-muted-foreground">Agent</p>
            <p className="font-semibold text-sm">{agentName}</p>
          </div>
          <div className="h-8 w-px bg-border" />
          <div className="text-center">
            <p className="text-xs text-muted-foreground">Customer</p>
            <p className="font-semibold text-sm">{customerName}</p>
          </div>
        </div>

        <div className="space-y-3">
          <h4 className="text-xs font-semibold uppercase text-muted-foreground tracking-wider flex items-center gap-1">
            <MessageSquare className="h-3.5 w-3.5" /> Live Transcript Feed
          </h4>
          <div className="h-64 overflow-y-auto p-4 rounded-lg border bg-background space-y-3">
            {transcripts.length === 0 ? (
              <div className="flex h-full items-center justify-center text-xs text-muted-foreground italic">
                Waiting for speech events...
              </div>
            ) : (
              transcripts.map((t) => (
                <div
                  key={t.id}
                  className={`flex flex-col ${
                    t.speaker === "agent" ? "items-end" : "items-start"
                  }`}
                >
                  <span className="text-[10px] text-muted-foreground mb-1">
                    {t.speaker === "agent" ? agentName : customerName} • {t.timestamp}
                  </span>
                  <div
                    className={`max-w-[80%] rounded-lg p-3 text-xs ${
                      t.speaker === "agent"
                        ? "bg-primary text-primary-foreground"
                        : "bg-muted text-foreground"
                    }`}
                  >
                    {t.text}
                  </div>
                </div>
              ))
            )}
          </div>
        </div>

        <div className="flex justify-center gap-3 pt-2">
          <Button variant="destructive" size="sm" className="gap-2">
            <PhoneOff className="h-4 w-4" /> End Call
          </Button>
        </div>
      </CardContent>
    </Card>
  );
};
