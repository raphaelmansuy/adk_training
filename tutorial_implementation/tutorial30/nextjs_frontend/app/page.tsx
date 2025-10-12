"use client";

import { CopilotKit } from "@copilotkit/react-core";
import { CopilotChat } from "@copilotkit/react-ui";
import "@copilotkit/react-ui/styles.css";

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <CopilotKit runtimeUrl="/api/copilotkit" agent="my_agent">
        {/* Header */}
        <div className="container mx-auto px-4 py-8">
          <div className="max-w-4xl mx-auto">
            <h1 className="text-4xl font-bold text-gray-900 mb-2">
              Customer Support
            </h1>
            <p className="text-lg text-gray-600 mb-8">
              Hi! I'm your AI support assistant. How can I help you today?
            </p>
          </div>
        </div>

        {/* Chat Interface */}
        <div className="container mx-auto px-4 pb-8">
          <div className="max-w-4xl mx-auto bg-white rounded-lg shadow-xl overflow-hidden">
            <CopilotChat
              instructions="You are a customer support agent. Be helpful, empathetic, and professional."
              labels={{
                title: "Support Chat",
                initial:
                  "Hi! I'm here to help with your questions about our products, policies, and services. What can I assist you with today?",
              }}
              className="h-[600px]"
            />
          </div>
        </div>
      </CopilotKit>
    </div>
  );
}
