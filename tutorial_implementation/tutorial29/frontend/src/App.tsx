import { CopilotKit } from "@copilotkit/react-core";
import { CopilotChat } from "@copilotkit/react-ui";
import "@copilotkit/react-ui/styles.css";

function App() {
  return (
    <div style={{ height: "100vh", display: "flex", flexDirection: "column" }}>
      <CopilotKit runtimeUrl="http://localhost:8000/api/copilotkit">
        {/* Header */}
        <div
          style={{
            padding: "2rem",
            borderBottom: "1px solid #e5e7eb",
            backgroundColor: "#f9fafb",
          }}
        >
          <h1 style={{ margin: "0 0 0.5rem 0", fontSize: "1.875rem", fontWeight: "bold" }}>
            🚀 ADK + AG-UI Quickstart
          </h1>
          <p style={{ margin: 0, color: "#6b7280" }}>
            A minimal example demonstrating Google ADK integration with React using the AG-UI Protocol.
          </p>
        </div>

        {/* Main Content */}
        <div style={{ flex: 1, padding: "2rem" }}>
          <div style={{ maxWidth: "48rem", margin: "0 auto" }}>
            <h2 style={{ fontSize: "1.25rem", fontWeight: "600", marginBottom: "1rem" }}>
              Welcome to Tutorial 29! 👋
            </h2>
            <p style={{ color: "#4b5563", marginBottom: "1rem" }}>
              This is the Quick Start example from Tutorial 29: Introduction to UI Integration.
            </p>
            <div
              style={{
                backgroundColor: "#eff6ff",
                border: "1px solid #bfdbfe",
                borderRadius: "0.5rem",
                padding: "1rem",
                marginBottom: "2rem",
              }}
            >
              <h3 style={{ fontSize: "1rem", fontWeight: "600", marginBottom: "0.5rem" }}>
                💡 Try These Prompts:
              </h3>
              <ul style={{ marginLeft: "1.5rem", color: "#1e40af" }}>
                <li>What is Google ADK?</li>
                <li>How does the AG-UI Protocol work?</li>
                <li>Explain the benefits of UI integration</li>
                <li>What can you help me with?</li>
              </ul>
            </div>

            <div
              style={{
                backgroundColor: "#f0fdf4",
                border: "1px solid #bbf7d0",
                borderRadius: "0.5rem",
                padding: "1rem",
              }}
            >
              <h3 style={{ fontSize: "1rem", fontWeight: "600", marginBottom: "0.5rem" }}>
                ✅ What's Working Here:
              </h3>
              <ul style={{ marginLeft: "1.5rem", color: "#166534" }}>
                <li>Python ADK Agent (Gemini 2.0 Flash)</li>
                <li>FastAPI Backend with AG-UI Integration</li>
                <li>React + Vite Frontend</li>
                <li>CopilotKit Chat UI Component</li>
                <li>Real-time Streaming Responses</li>
              </ul>
            </div>
          </div>
        </div>

        {/* Chat Component */}
        <CopilotChat
          instructions="You are a helpful AI assistant powered by Google ADK. Answer questions clearly and concisely."
          labels={{
            title: "ADK Assistant",
            initial:
              "Hi! I'm an AI assistant powered by Google ADK. This is a minimal Quick Start example from Tutorial 29. Ask me anything about ADK, AI, or UI integration!",
          }}
        />
      </CopilotKit>
    </div>
  );
}

export default App;
