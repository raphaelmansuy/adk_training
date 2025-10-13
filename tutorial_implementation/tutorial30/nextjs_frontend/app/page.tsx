"use client";

import { CopilotKit } from "@copilotkit/react-core";
import { CopilotChat } from "@copilotkit/react-ui";
import "@copilotkit/react-ui/styles.css";
import { ThemeToggle } from "@/components/ThemeToggle";

export default function Home() {
  return (
    <div className="min-h-screen bg-background">
      <CopilotKit runtimeUrl="/api/copilotkit" agent="my_agent">
        <div className="flex flex-col h-screen">
          {/* Header */}
          <header className="border-b">
            <div className="container mx-auto px-4 py-4">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <div className="flex items-center justify-center w-10 h-10 bg-primary rounded-md">
                    <svg
                      className="w-5 h-5 text-primary-foreground"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z"
                      />
                    </svg>
                  </div>
                  <div>
                    <h1 className="text-lg font-semibold">Support Assistant</h1>
                    <p className="text-xs text-muted-foreground">AI-Powered Help</p>
                  </div>
                </div>
                <ThemeToggle />
              </div>
            </div>
          </header>

          {/* Main Content */}
          <main className="flex-1 overflow-hidden">
            <div className="container mx-auto px-4 py-6 h-full">
              <div className="h-full border rounded-lg bg-card">
                <CopilotChat
                  instructions="You are a friendly and professional customer support agent. Be helpful, empathetic, and provide clear, actionable solutions."
                  labels={{
                    title: "Support Chat",
                    initial:
                      "👋 Hi! I'm your AI support assistant.\n\nI can help you with:\n• Product information\n• Order tracking\n• Support tickets\n• General questions\n\nHow can I assist you today?",
                  }}
                  className="h-full"
                />
              </div>
            </div>
          </main>
        </div>
      </CopilotKit>
    </div>
  );
}
