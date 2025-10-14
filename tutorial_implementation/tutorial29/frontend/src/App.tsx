import { useState, useRef, useEffect } from "react";
import "./App.css";

interface Message {
  role: "user" | "assistant";
  content: string;
}

function App() {
  const [messages, setMessages] = useState<Message[]>([
    {
      role: "assistant",
      content: "Hi! I'm powered by Google ADK with Gemini 2.0 Flash. Ask me anything!",
    },
  ]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const sendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage: Message = { role: "user", content: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setIsLoading(true);

    try {
      const response = await fetch("http://localhost:8000/api/copilotkit", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          threadId: "tutorial29-thread",
          runId: `run-${Date.now()}`,
          messages: [...messages, userMessage].map((m, i) => ({
            id: `msg-${Date.now()}-${i}`,
            role: m.role,
            content: m.content,
          })),
          state: {},
          tools: [],
          context: [],
          forwardedProps: {},
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }

      // Handle SSE streaming response
      const reader = response.body?.getReader();
      const decoder = new TextDecoder();
      let fullContent = "";

      if (reader) {
        while (true) {
          const { done, value } = await reader.read();
          if (done) break;

          const chunk = decoder.decode(value);
          const lines = chunk.split("\n");

          for (const line of lines) {
            if (line.startsWith("data: ")) {
              try {
                const jsonData = JSON.parse(line.slice(6));
                if (jsonData.type === "TEXT_MESSAGE_CONTENT") {
                  fullContent += jsonData.delta;
                  // Update message in real-time
                  setMessages((prev) => {
                    const newMessages = [...prev];
                    const lastMsg = newMessages[newMessages.length - 1];
                    if (lastMsg && lastMsg.role === "assistant") {
                      lastMsg.content = fullContent;
                    } else {
                      newMessages.push({ role: "assistant", content: fullContent });
                    }
                    return newMessages;
                  });
                }
              } catch (e) {
                // Skip invalid JSON
              }
            }
          }
        }
      }

      // Ensure final message is added if not already
      if (fullContent && messages[messages.length - 1]?.role !== "assistant") {
        const assistantMessage: Message = {
          role: "assistant",
          content: fullContent,
        };
        setMessages((prev) => [...prev, assistantMessage]);
      }
    } catch (error) {
      console.error("Error:", error);
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: "Error: Could not get response" },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 shadow-sm" role="banner">
        <div className="max-w-4xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div 
                className="w-10 h-10 bg-gradient-to-br from-indigo-600 to-purple-600 rounded-xl flex items-center justify-center text-2xl shadow-lg"
                aria-hidden="true"
              >
                🚀
              </div>
              <div>
                <h1 className="text-xl font-bold text-gray-900">ADK Quickstart</h1>
                <p className="text-sm text-gray-600">Gemini 2.0 Flash</p>
              </div>
            </div>
            <div className="flex items-center gap-2" role="status" aria-live="polite">
              <div 
                className="w-2 h-2 bg-emerald-500 rounded-full animate-pulse"
                aria-hidden="true"
              ></div>
              <span className="text-sm font-medium text-emerald-700">Connected</span>
            </div>
          </div>
        </div>
      </header>

      {/* Chat Messages */}
      <main 
        className="flex-1 overflow-y-auto" 
        role="main"
        aria-label="Chat conversation"
      >
        <div className="max-w-4xl mx-auto px-6 py-8">
          {messages.length === 1 && (
            <div 
              className="text-center py-12"
              role="status"
              aria-label="Welcome message"
            >
              <div className="text-6xl mb-4" aria-hidden="true">💬</div>
              <p className="text-lg font-semibold text-gray-700 mb-2">
                Start a conversation
              </p>
              <p className="text-sm text-gray-600">
                Try: "What is Google ADK?" or "Explain AI agents"
              </p>
            </div>
          )}
          
          <div 
            role="log" 
            aria-live="polite" 
            aria-atomic="false"
            aria-label="Chat messages"
          >
            {messages.map((message, index) => (
              <article
                key={index}
                className={`flex gap-3 mb-6 items-start animate-in slide-in-from-bottom-2 duration-300 ${
                  message.role === "user" ? "justify-end" : "justify-start"
                }`}
                role="article"
                aria-label={`${message.role === "user" ? "Your message" : "Assistant message"}`}
              >
                {message.role === "assistant" && (
                  <div 
                    className="w-8 h-8 rounded-lg bg-gradient-to-br from-indigo-600 to-purple-600 flex items-center justify-center flex-shrink-0 text-lg shadow-md"
                    aria-hidden="true"
                  >
                    🤖
                  </div>
                )}
                
                <div
                  className={`max-w-[75%] px-4 py-3 rounded-2xl leading-relaxed break-words ${
                    message.role === "user"
                      ? "bg-blue-600 text-white shadow-lg shadow-blue-600/30 rounded-br-sm"
                      : "bg-white text-gray-900 shadow-md border border-gray-100 rounded-bl-sm"
                  }`}
                  role="region"
                  aria-label={message.role === "user" ? "Your message" : "Assistant response"}
                >
                  {message.content}
                </div>
                
                {message.role === "user" && (
                  <div 
                    className="w-8 h-8 rounded-lg bg-blue-600 flex items-center justify-center flex-shrink-0 text-lg text-white shadow-md"
                    aria-hidden="true"
                  >
                    👤
                  </div>
                )}
              </article>
            ))}
          </div>
          
          {isLoading && (
            <div 
              className="flex gap-3 items-start animate-in slide-in-from-bottom-2 duration-300"
              role="status"
              aria-live="polite"
              aria-label="Assistant is typing"
            >
              <div 
                className="w-8 h-8 rounded-lg bg-gradient-to-br from-indigo-600 to-purple-600 flex items-center justify-center flex-shrink-0 text-lg shadow-md"
                aria-hidden="true"
              >
                🤖
              </div>
              <div className="px-4 py-3 rounded-2xl rounded-bl-sm bg-white shadow-md border border-gray-100">
                <div className="flex gap-1" aria-label="Loading">
                  <div className="w-2 h-2 rounded-full bg-gray-500 animate-bounce" style={{ animationDelay: "0s" }}></div>
                  <div className="w-2 h-2 rounded-full bg-gray-500 animate-bounce" style={{ animationDelay: "0.2s" }}></div>
                  <div className="w-2 h-2 rounded-full bg-gray-500 animate-bounce" style={{ animationDelay: "0.4s" }}></div>
                </div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} aria-hidden="true" />
        </div>
      </main>

      {/* Input Form */}
      <footer className="bg-white border-t border-gray-200 shadow-lg" role="contentinfo">
        <div className="max-w-4xl mx-auto px-6 py-4">
          <form 
            onSubmit={sendMessage} 
            className="flex gap-3"
            aria-label="Message input form"
          >
            <div className="flex-1 relative">
              <label htmlFor="message-input" className="sr-only">
                Type your message
              </label>
              <input
                id="message-input"
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Type your message..."
                disabled={isLoading}
                autoFocus
                autoComplete="off"
                aria-label="Message input"
                aria-describedby="message-hint"
                aria-invalid="false"
                className="w-full px-5 py-3 pr-12 border-2 border-gray-300 rounded-full text-base outline-none transition-all bg-white text-gray-900 placeholder-gray-500 focus:border-blue-600 focus:ring-4 focus:ring-blue-600/20 disabled:bg-gray-100 disabled:text-gray-500 disabled:cursor-not-allowed"
              />
              {input.length > 0 && (
                <div 
                  className="absolute right-4 top-1/2 -translate-y-1/2 text-sm text-gray-500 pointer-events-none"
                  aria-live="polite"
                  aria-atomic="true"
                >
                  <span className="sr-only">Character count: </span>
                  {input.length}
                </div>
              )}
            </div>
            <button
              type="submit"
              disabled={isLoading || !input.trim()}
              aria-label={isLoading ? "Sending message" : "Send message"}
              aria-busy={isLoading}
              className="px-6 py-3 bg-blue-600 text-white rounded-full font-semibold transition-all flex items-center gap-2 shadow-lg shadow-blue-600/30 hover:bg-blue-700 hover:-translate-y-0.5 hover:shadow-xl hover:shadow-blue-600/40 focus:outline-none focus:ring-4 focus:ring-blue-600/20 disabled:bg-gray-300 disabled:text-gray-600 disabled:cursor-not-allowed disabled:shadow-none disabled:translate-y-0"
            >
              {isLoading ? (
                <>
                  <span>Sending</span>
                  <span className="animate-spin" aria-hidden="true">⏳</span>
                </>
              ) : (
                <>
                  <span>Send</span>
                  <span aria-hidden="true">🚀</span>
                </>
              )}
            </button>
          </form>
          <p 
            id="message-hint" 
            className="text-center text-xs text-gray-500 mt-3"
            role="contentinfo"
          >
            Powered by Google ADK • Tutorial 29 Quick Start
          </p>
        </div>
      </footer>
    </div>
  );
}

export default App;
