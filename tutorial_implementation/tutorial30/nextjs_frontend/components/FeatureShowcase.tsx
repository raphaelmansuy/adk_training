import { useState } from "react";
import { ProductCard } from "./ProductCard";

interface FeatureShowcaseProps {
  userData: {
    name: string;
    email: string;
    accountType: string;
    orders: string[];
    memberSince: string;
  };
}

export function FeatureShowcase({ userData }: FeatureShowcaseProps) {
  const [activeTab, setActiveTab] = useState<"generative" | "hitl" | "state">("generative");

  return (
    <div className="border-t bg-muted/30">
      <div className="container mx-auto px-4 py-8">
        <div className="mb-6">
          <h2 className="text-2xl font-bold mb-2">Advanced Features Demo</h2>
          <p className="text-muted-foreground">
            Explore the capabilities of this AI assistant powered by Google ADK
          </p>
        </div>

        {/* Feature Tabs */}
        <div className="flex gap-2 mb-6 flex-wrap">
          <button
            onClick={() => setActiveTab("generative")}
            className={`px-4 py-2 rounded-lg font-medium transition-colors ${
              activeTab === "generative"
                ? "bg-primary text-primary-foreground"
                : "bg-background border hover:bg-accent"
            }`}
          >
            🎨 Generative UI
          </button>
          <button
            onClick={() => setActiveTab("hitl")}
            className={`px-4 py-2 rounded-lg font-medium transition-colors ${
              activeTab === "hitl"
                ? "bg-primary text-primary-foreground"
                : "bg-background border hover:bg-accent"
            }`}
          >
            🔐 Human-in-the-Loop
          </button>
          <button
            onClick={() => setActiveTab("state")}
            className={`px-4 py-2 rounded-lg font-medium transition-colors ${
              activeTab === "state"
                ? "bg-primary text-primary-foreground"
                : "bg-background border hover:bg-accent"
            }`}
          >
            👤 Shared State
          </button>
        </div>

        {/* Feature Content */}
        <div className="bg-background rounded-lg border p-6">
          {activeTab === "generative" && (
            <div>
              <h3 className="text-xl font-semibold mb-3">Generative UI</h3>
              <p className="text-muted-foreground mb-4">
                The agent can render rich, interactive React components directly in the chat.
                Try asking: <strong>"Show me product PROD-001"</strong>
              </p>
              <div className="grid md:grid-cols-2 gap-4">
                <ProductCard
                  name="Widget Pro"
                  price={99.99}
                  image="https://placehold.co/400x400/6366f1/fff.png"
                  rating={4.5}
                  inStock={true}
                />
                <ProductCard
                  name="Gadget Plus"
                  price={149.99}
                  image="https://placehold.co/400x400/8b5cf6/fff.png"
                  rating={4.8}
                  inStock={true}
                />
              </div>
              <div className="mt-4 p-4 bg-muted rounded-lg">
                <p className="text-sm font-mono">
                  <strong>How it works:</strong> When the agent calls{" "}
                  <code className="bg-background px-1 rounded">create_product_card()</code>, the
                  frontend receives structured data and renders it as a React component instead of
                  plain text.
                </p>
              </div>
            </div>
          )}

          {activeTab === "hitl" && (
            <div>
              <h3 className="text-xl font-semibold mb-3">Human-in-the-Loop (HITL)</h3>
              <p className="text-muted-foreground mb-4">
                Sensitive operations require explicit user approval before execution. Try asking:{" "}
                <strong>"I want a refund for order ORD-12345"</strong>
              </p>
              <div className="space-y-4">
                <div className="border rounded-lg p-4 bg-card">
                  <h4 className="font-semibold mb-2">🔔 Refund Approval Required</h4>
                  <div className="space-y-2 text-sm">
                    <p>
                      <strong>Order ID:</strong> ORD-12345
                    </p>
                    <p>
                      <strong>Amount:</strong> $99.99
                    </p>
                    <p>
                      <strong>Reason:</strong> Product defect
                    </p>
                  </div>
                  <div className="flex gap-2 mt-4">
                    <button className="px-4 py-2 bg-red-100 dark:bg-red-900 text-red-800 dark:text-red-200 rounded-lg text-sm">
                      ❌ Cancel
                    </button>
                    <button className="px-4 py-2 bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-200 rounded-lg text-sm">
                      ✅ Approve
                    </button>
                  </div>
                </div>
                <div className="p-4 bg-muted rounded-lg">
                  <p className="text-sm font-mono">
                    <strong>How it works:</strong> When the agent tries to process a refund, it
                    pauses and shows a confirmation dialog. The agent only proceeds if you approve.
                    You can also cancel the operation.
                  </p>
                </div>
              </div>
            </div>
          )}

          {activeTab === "state" && (
            <div>
              <h3 className="text-xl font-semibold mb-3">Shared State</h3>
              <p className="text-muted-foreground mb-4">
                The agent has real-time access to your user context without needing to ask. Try:{" "}
                <strong>"What's my account status?"</strong>
              </p>
              <div className="space-y-4">
                <div className="border rounded-lg p-4 bg-card">
                  <h4 className="font-semibold mb-3">Your Account Information</h4>
                  <div className="grid gap-2 text-sm">
                    <div className="flex justify-between">
                      <span className="text-muted-foreground">Name:</span>
                      <span className="font-medium">{userData.name}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-muted-foreground">Email:</span>
                      <span className="font-medium">{userData.email}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-muted-foreground">Account Type:</span>
                      <span className="font-medium bg-primary/10 text-primary px-2 py-1 rounded">
                        {userData.accountType}
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-muted-foreground">Recent Orders:</span>
                      <span className="font-medium">{userData.orders.join(", ")}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-muted-foreground">Member Since:</span>
                      <span className="font-medium">{userData.memberSince}</span>
                    </div>
                  </div>
                </div>
                <div className="p-4 bg-muted rounded-lg">
                  <p className="text-sm font-mono">
                    <strong>How it works:</strong> The frontend shares this data with the agent
                    using{" "}
                    <code className="bg-background px-1 rounded">useCopilotReadable()</code>. The
                    agent can reference it in responses without asking you questions.
                  </p>
                </div>
              </div>
            </div>
          )}
        </div>

        <div className="mt-6 text-center">
          <a
            href="/advanced"
            className="inline-flex items-center gap-2 text-sm text-primary hover:underline"
          >
            View implementation details →
          </a>
        </div>
      </div>
    </div>
  );
}
