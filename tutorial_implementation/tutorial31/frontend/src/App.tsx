import { useState, useRef, useEffect } from "react";
import { Line, Bar, Scatter } from "react-chartjs-2";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import rehypeHighlight from "rehype-highlight";
import rehypeRaw from "rehype-raw";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";
import "./App.css";
import "highlight.js/styles/github-dark.css";

// Register Chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend
);

interface Message {
  role: "user" | "assistant";
  content: string;
  chartData?: ChartData;
}

interface ChartData {
  chart_type: string;
  data: {
    labels: string[];
    values: number[];
  };
  options: {
    x_label: string;
    y_label: string;
    title: string;
  };
  status?: string;
  report?: string;
}

function App() {
  const [messages, setMessages] = useState<Message[]>([
    {
      role: "assistant",
      content: "Hi! I'm your **data analysis assistant** powered by Google ADK with Gemini 2.0 Flash. 📊\n\nUpload CSV files or ask me to analyze data!",
    },
  ]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);
  const [currentChart, setCurrentChart] = useState<ChartData | null>(null);
  const [isDragOver, setIsDragOver] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  // Extract chart data from agent response
  const extractChartData = (content: string): ChartData | null => {
    try {
      // Look for JSON object with chart_type in the response
      const jsonMatch = content.match(/\{[^{}]*"chart_type"[^{}]*"data"[^{}]*\}/s);
      if (jsonMatch) {
        const chartData = JSON.parse(jsonMatch[0]);
        if (chartData.chart_type && chartData.data) {
          return chartData;
        }
      }
    } catch (e) {
      console.error("Failed to extract chart data:", e);
    }
    return null;
  };

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
          threadId: "data-analysis-thread",
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
      let toolResults: Record<string, any> = {};

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
                console.log("📡 Received event:", jsonData.type, jsonData);
                
                // Handle text content streaming
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
                
                // Handle tool call results (where chart data lives!)
                if (jsonData.type === "TOOL_CALL_RESULT") {
                  console.log("� TOOL_CALL_RESULT Event Received!");
                  console.log("   Full event object:", JSON.stringify(jsonData, null, 2));
                  console.log("   Content type:", typeof jsonData.content);
                  console.log("   Content value:", jsonData.content);
                  
                  try {
                    // Parse the tool result content
                    const resultContent = typeof jsonData.content === 'string' 
                      ? JSON.parse(jsonData.content) 
                      : jsonData.content;
                    
                    console.log("   Parsed content:", resultContent);
                    console.log("   Has chart_type?:", !!resultContent.chart_type);
                    
                    toolResults[jsonData.tool_call_id] = resultContent;
                    
                    // Check if this is a chart creation result
                    if (resultContent && resultContent.chart_type) {
                      console.log("✅ CHART DATA FOUND!");
                      console.log("   Chart type:", resultContent.chart_type);
                      console.log("   Chart data:", resultContent);
                      
                      setCurrentChart(resultContent);
                      console.log("   Set currentChart state");
                      
                      setMessages((prev) => {
                        const newMessages = [...prev];
                        const lastMsg = newMessages[newMessages.length - 1];
                        console.log("   Last message role:", lastMsg?.role);
                        if (lastMsg && lastMsg.role === "assistant") {
                          lastMsg.chartData = resultContent;
                          console.log("   Attached chartData to message");
                        }
                        return newMessages;
                      });
                    } else {
                      console.log("❌ No chart_type found in result");
                      console.log("   Result keys:", Object.keys(resultContent));
                    }
                  } catch (e) {
                    console.error("❌ Error parsing tool result:", e);
                    console.error("   Raw content:", jsonData.content);
                  }
                }
              } catch (e) {
                // Skip invalid JSON
              }
            }
          }
        }
      }

      // Fallback: Extract chart from text content if not found in tool results
      if (!currentChart) {
        const chartData = extractChartData(fullContent);
        if (chartData) {
          console.log("📊 Chart data extracted from text (fallback):", chartData);
          setCurrentChart(chartData);
          setMessages((prev) => {
            const newMessages = [...prev];
            const lastMsg = newMessages[newMessages.length - 1];
            if (lastMsg && lastMsg.role === "assistant") {
              lastMsg.chartData = chartData;
            }
            return newMessages;
          });
        }
      }

      // Ensure final message is added if not already (this should not happen in streaming)
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
        { role: "assistant", content: "Error: Could not get response from server" },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleFileUpload = async (file: File) => {
    if (!file.name.endsWith('.csv')) {
      alert('Please upload a CSV file');
      return;
    }

    setUploadedFile(file);
    setIsLoading(true);

    try {
      const csvText = await file.text();
      
      // Send the CSV data to the agent
      const uploadMessage = `Please load this CSV data for analysis:\n\nFile: ${file.name}\nData:\n${csvText}`;
      
      const userMessage: Message = { role: "user", content: `Uploaded: ${file.name}` };
      setMessages((prev) => [...prev, userMessage]);

      const response = await fetch("http://localhost:8000/api/copilotkit", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          threadId: "data-analysis-thread",
          runId: `run-${Date.now()}`,
          messages: [...messages, { role: "user", content: uploadMessage }].map((m, i) => ({
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

      // Handle response similar to sendMessage
      const reader = response.body?.getReader();
      const decoder = new TextDecoder();
      let fullContent = "";
      let chartDataFromTool: ChartData | null = null;

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
                console.log("📡 Received event:", jsonData.type, jsonData);
                
                // Handle text content streaming
                if (jsonData.type === "TEXT_MESSAGE_CONTENT") {
                  fullContent += jsonData.delta;
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
                
                // Handle tool results (chart data)
                if (jsonData.type === "TOOL_CALL_RESULT") {
                  console.log("📊 Upload: Received TOOL_CALL_RESULT:", jsonData);
                  try {
                    const resultContent = typeof jsonData.content === 'string' 
                      ? JSON.parse(jsonData.content) 
                      : jsonData.content;
                    
                    if (resultContent && resultContent.chart_type) {
                      console.log("📈 Upload: Chart data found:", resultContent);
                      chartDataFromTool = resultContent;
                      setCurrentChart(resultContent);
                    }
                  } catch (e) {
                    console.error("Error parsing upload tool result:", e);
                  }
                }
              } catch (e) {
                // Skip invalid JSON
              }
            }
          }
        }
      }

      if (fullContent && messages[messages.length - 1]?.role !== "assistant") {
        const assistantMessage: Message = {
          role: "assistant",
          content: fullContent,
          chartData: chartDataFromTool || undefined,
        };
        setMessages((prev) => [...prev, assistantMessage]);
      }

    } catch (error) {
      console.error("Upload error:", error);
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: `Error uploading ${file.name}: ${error}` },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(false);
    
    const files = Array.from(e.dataTransfer.files);
    const csvFile = files.find(file => file.name.endsWith('.csv'));
    
    if (csvFile) {
      handleFileUpload(csvFile);
    } else {
      alert('Please drop a CSV file');
    }
  };

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(true);
  };

  const handleDragLeave = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(false);
  };

  const renderChart = (chartData: ChartData) => {
    const data = {
      labels: chartData.data.labels,
      datasets: [
        {
          label: chartData.options.y_label,
          data: chartData.data.values,
          backgroundColor: chartData.chart_type === 'line' 
            ? 'rgba(37, 99, 235, 0.1)'
            : 'rgba(37, 99, 235, 0.8)',
          borderColor: 'rgba(37, 99, 235, 1)',
          borderWidth: 2,
          tension: chartData.chart_type === 'line' ? 0.4 : 0,
          pointBackgroundColor: 'rgba(37, 99, 235, 1)',
          pointBorderColor: '#fff',
          pointHoverBackgroundColor: '#fff',
          pointHoverBorderColor: 'rgba(37, 99, 235, 1)',
        },
      ],
    };

    const options = {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'top' as const,
          labels: {
            color: '#1f2937',
            font: {
              size: 12,
              weight: 'bold' as const,
            },
          },
        },
        title: {
          display: true,
          text: chartData.options.title,
          color: '#111827',
          font: {
            size: 16,
            weight: 'bold' as const,
          },
        },
      },
      scales: {
        x: {
          title: {
            display: true,
            text: chartData.options.x_label,
            color: '#4b5563',
            font: {
              size: 12,
              weight: 'bold' as const,
            },
          },
          ticks: {
            color: '#6b7280',
          },
          grid: {
            color: 'rgba(0, 0, 0, 0.05)',
          },
        },
        y: {
          title: {
            display: true,
            text: chartData.options.y_label,
            color: '#4b5563',
            font: {
              size: 12,
              weight: 'bold' as const,
            },
          },
          ticks: {
            color: '#6b7280',
          },
          grid: {
            color: 'rgba(0, 0, 0, 0.05)',
          },
        },
      },
    };

    switch (chartData.chart_type) {
      case 'line':
        return <Line data={data} options={options} />;
      case 'bar':
        return <Bar data={data} options={options} />;
      case 'scatter':
        return <Scatter data={data} options={options} />;
      default:
        return <Line data={data} options={options} />;
    }
  };

  return (
    <div className="flex flex-col h-screen bg-gradient-to-br from-gray-50 to-blue-50 overflow-hidden">
      {/* Header */}
      <header className="bg-white/90 backdrop-blur-sm border-b border-gray-200 shadow-sm sticky top-0 z-10 flex-shrink-0" role="banner">
        <div className="max-w-6xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div 
                className="w-12 h-12 bg-gradient-to-br from-blue-600 to-indigo-700 rounded-xl flex items-center justify-center text-2xl shadow-lg"
                aria-hidden="true"
              >
                📊
              </div>
              <div>
                <h1 className="text-2xl font-bold text-gray-900">Data Analysis Dashboard</h1>
                <p className="text-sm text-gray-600">Powered by Gemini 2.0 Flash</p>
              </div>
            </div>
            <div className="flex items-center gap-4">
              {uploadedFile && (
                <div className="text-sm text-gray-600 bg-green-50 px-3 py-1 rounded-full border border-green-200">
                  📄 {uploadedFile.name}
                </div>
              )}
              <div className="flex items-center gap-2" role="status" aria-live="polite">
                <div 
                  className="w-2 h-2 bg-emerald-500 rounded-full animate-pulse"
                  aria-hidden="true"
                ></div>
                <span className="text-sm font-medium text-emerald-700">Connected</span>
              </div>
            </div>
          </div>
        </div>
      </header>

      <div className="flex-1 flex max-w-full mx-auto w-full relative">
        {/* Main Chat Area */}
        <main className={`flex-1 flex flex-col transition-all duration-300 ${(currentChart || uploadedFile) ? 'mr-96' : ''}`} style={{maxWidth: '100%'}} role="main">
          {/* File Upload Area */}
          <div className="p-6 border-b border-gray-200 bg-white/50">
            <div
              className={`relative border-2 border-dashed rounded-xl p-6 text-center transition-all duration-200 ${
                isDragOver
                  ? "border-blue-500 bg-blue-50"
                  : "border-gray-300 hover:border-blue-400 hover:bg-blue-50/50"
              }`}
              onDrop={handleDrop}
              onDragOver={handleDragOver}
              onDragLeave={handleDragLeave}
            >
              <input
                ref={fileInputRef}
                type="file"
                accept=".csv"
                onChange={(e) => {
                  const file = e.target.files?.[0];
                  if (file) handleFileUpload(file);
                }}
                className="hidden"
              />
              <div className="text-4xl mb-2">📁</div>
              <p className="text-lg font-semibold text-gray-700 mb-1">
                Drop CSV files here or{" "}
                <button
                  onClick={() => fileInputRef.current?.click()}
                  className="text-blue-600 hover:text-blue-700 underline"
                >
                  browse
                </button>
              </p>
              <p className="text-sm text-gray-500">
                Supports CSV files for data analysis and visualization
              </p>
            </div>
          </div>

          {/* Chat Messages */}
          <div className="flex-1 overflow-y-auto" aria-label="Chat conversation">
            <div className="px-6 py-4 max-w-5xl mx-auto">
              {messages.length === 1 && (
                <div 
                  className="text-center py-12"
                  role="status"
                  aria-label="Welcome message"
                >
                  <div className="text-6xl mb-4" aria-hidden="true">📈</div>
                  <p className="text-xl font-semibold text-gray-700 mb-2">
                    Ready to analyze your data
                  </p>
                  <p className="text-gray-600 mb-4">
                    Upload a CSV file or ask me to analyze data trends
                  </p>
                  <div className="flex flex-wrap gap-2 justify-center">
                    <button
                      onClick={() => setInput("Analyze sales trends")}
                      className="px-4 py-2 bg-blue-100 text-blue-700 rounded-full text-sm hover:bg-blue-200 transition-colors"
                    >
                      "Analyze sales trends"
                    </button>
                    <button
                      onClick={() => setInput("Show correlation analysis")}
                      className="px-4 py-2 bg-purple-100 text-purple-700 rounded-full text-sm hover:bg-purple-200 transition-colors"
                    >
                      "Show correlation analysis"
                    </button>
                    <button
                      onClick={() => setInput("Create a line chart")}
                      className="px-4 py-2 bg-green-100 text-green-700 rounded-full text-sm hover:bg-green-200 transition-colors"
                    >
                      "Create a line chart"
                    </button>
                  </div>
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
                    className={`flex gap-4 mb-6 items-start animate-in slide-in-from-bottom-2 duration-300 ${
                      message.role === "user" ? "justify-end" : "justify-start"
                    }`}
                    role="article"
                    aria-label={`${message.role === "user" ? "Your message" : "Assistant message"}`}
                  >
                    {message.role === "assistant" && (
                      <div 
                        className="w-10 h-10 rounded-xl bg-gradient-to-br from-blue-600 to-indigo-700 flex items-center justify-center flex-shrink-0 text-lg shadow-lg"
                        aria-hidden="true"
                      >
                        🤖
                      </div>
                    )}
                    
                    <div
                      className={`max-w-[75%] px-5 py-4 rounded-2xl leading-relaxed shadow-lg ${
                        message.role === "user"
                          ? "bg-gradient-to-r from-blue-700 to-blue-800 text-white rounded-br-md"
                          : "bg-white text-gray-900 border-2 border-gray-200 rounded-bl-md"
                      }`}
                      role="region"
                      aria-label={message.role === "user" ? "Your message content" : "Assistant response content"}
                    >
                      <div className={`prose prose-sm max-w-none ${
                        message.role === "user" 
                          ? "prose-invert" 
                          : "prose-gray prose-headings:text-gray-900 prose-p:text-gray-800 prose-strong:text-gray-900 prose-code:text-blue-700 prose-pre:bg-gray-100"
                      }`}>
                        <ReactMarkdown
                          remarkPlugins={[remarkGfm]}
                          rehypePlugins={[rehypeHighlight, rehypeRaw]}
                        >
                          {message.content}
                        </ReactMarkdown>
                      </div>
                      
                      {/* Inline chart for messages with chart data */}
                      {message.chartData && (
                        <div className="mt-4 bg-gray-50 rounded-lg p-4 border-2 border-gray-200">
                          <div className="h-64">
                            {renderChart(message.chartData)}
                          </div>
                        </div>
                      )}
                    </div>
                    
                    {message.role === "user" && (
                      <div 
                        className="w-10 h-10 rounded-xl bg-gradient-to-br from-blue-600 to-blue-700 flex items-center justify-center flex-shrink-0 text-lg text-white shadow-lg"
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
                  className="flex gap-4 items-start animate-in slide-in-from-bottom-2 duration-300"
                  role="status"
                  aria-live="polite"
                  aria-label="Assistant is typing"
                >
                  <div 
                    className="w-10 h-10 rounded-xl bg-gradient-to-br from-blue-600 to-indigo-700 flex items-center justify-center flex-shrink-0 text-lg shadow-lg"
                    aria-hidden="true"
                  >
                    🤖
                  </div>
                  <div className="px-5 py-4 rounded-2xl rounded-bl-md bg-white shadow-lg border border-gray-100">
                    <div className="flex gap-1" aria-label="Loading">
                      <div className="w-2 h-2 rounded-full bg-blue-500 animate-bounce" style={{ animationDelay: "0s" }}></div>
                      <div className="w-2 h-2 rounded-full bg-blue-500 animate-bounce" style={{ animationDelay: "0.2s" }}></div>
                      <div className="w-2 h-2 rounded-full bg-blue-500 animate-bounce" style={{ animationDelay: "0.4s" }}></div>
                    </div>
                  </div>
                </div>
              )}
              <div ref={messagesEndRef} aria-hidden="true" />
            </div>
          </div>

          {/* Input Form */}
          <footer className="bg-white/90 backdrop-blur-sm border-t border-gray-200 shadow-lg" role="contentinfo">
            <div className="px-6 py-4">
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
                    placeholder="Ask about data analysis..."
                    disabled={isLoading}
                    autoFocus
                    autoComplete="off"
                    aria-label="Message input"
                    aria-describedby="message-hint"
                    aria-invalid="false"
                    className="w-full px-6 py-4 pr-12 border-2 border-gray-300 rounded-2xl text-base outline-none transition-all bg-white text-gray-900 placeholder-gray-500 focus:border-blue-600 focus:ring-4 focus:ring-blue-600/20 disabled:bg-gray-100 disabled:text-gray-500 disabled:cursor-not-allowed shadow-sm"
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
                  aria-label={isLoading ? "Sending message, please wait" : "Send message"}
                  aria-busy={isLoading}
                  className="px-8 py-4 bg-gradient-to-r from-blue-700 to-blue-800 text-white rounded-2xl font-bold transition-all flex items-center gap-2 shadow-lg hover:from-blue-800 hover:to-blue-900 hover:-translate-y-0.5 hover:shadow-xl focus:outline-none focus:ring-4 focus:ring-blue-600/30 disabled:bg-gray-400 disabled:text-white disabled:cursor-not-allowed disabled:shadow-none disabled:translate-y-0 disabled:opacity-60"
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
                Powered by Google ADK • Tutorial 31 Data Analysis Dashboard
              </p>
            </div>
          </footer>
        </main>

        {/* Sidebar for Charts and Data - Fixed Position */}
        {(currentChart || uploadedFile) && (
          <aside 
            className="fixed right-0 top-0 w-96 h-screen bg-white border-l-2 border-gray-300 flex flex-col shadow-2xl z-20 animate-in slide-in-from-right duration-300" 
            role="complementary" 
            aria-label="Chart visualization panel"
          >
            {/* Fixed Header */}
            <div className="flex-shrink-0 p-6 border-b-2 border-gray-300 bg-gradient-to-r from-gray-50 to-blue-50">
              <div className="flex items-center justify-between">
                <h2 className="text-xl font-bold text-gray-900 flex items-center gap-2">
                  📊 Visualization
                </h2>
                <button
                  onClick={() => setCurrentChart(null)}
                  className="text-gray-500 hover:text-gray-700 hover:bg-gray-200 rounded-lg p-2 transition-colors"
                  aria-label="Close visualization panel"
                  title="Close panel"
                >
                  ✕
                </button>
              </div>
            </div>
            
            {/* Scrollable Content */}
            <div className="flex-1 overflow-y-auto p-6 space-y-6" style={{maxHeight: 'calc(100vh - 88px)'}}>
              {currentChart && (
                <div className="space-y-4">
                  {/* Chart Container */}
                  <div className="bg-gradient-to-br from-white to-gray-50 rounded-xl p-6 border-2 border-gray-300 shadow-lg">
                    <div className="h-80">
                      {renderChart(currentChart)}
                    </div>
                  </div>
                  
                  {/* Chart Metadata */}
                  <div className="bg-gradient-to-br from-blue-50 to-indigo-50 rounded-xl p-5 border-2 border-blue-200 shadow-sm space-y-3">
                    <h3 className="text-sm font-bold text-gray-700 uppercase tracking-wide mb-3 flex items-center gap-2">
                      <span className="text-blue-600">📋</span> Chart Details
                    </h3>
                    <div className="space-y-2.5">
                      <div className="flex items-start justify-between gap-2">
                        <span className="text-sm font-medium text-gray-600">Type:</span>
                        <span className="text-sm font-bold text-gray-900 capitalize">{currentChart.chart_type}</span>
                      </div>
                      <div className="flex items-start justify-between gap-2">
                        <span className="text-sm font-medium text-gray-600">X-Axis:</span>
                        <span className="text-sm font-semibold text-gray-800 text-right">{currentChart.options.x_label}</span>
                      </div>
                      <div className="flex items-start justify-between gap-2">
                        <span className="text-sm font-medium text-gray-600">Y-Axis:</span>
                        <span className="text-sm font-semibold text-gray-800 text-right">{currentChart.options.y_label}</span>
                      </div>
                      <div className="flex items-start justify-between gap-2 pt-2 border-t border-blue-200">
                        <span className="text-sm font-medium text-gray-600">Data Points:</span>
                        <span className="text-sm font-bold text-blue-700">{currentChart.data.labels.length}</span>
                      </div>
                    </div>
                  </div>
                  
                  {/* Chart Status */}
                  {currentChart.report && (
                    <div className="bg-green-50 rounded-lg p-4 border border-green-200">
                      <p className="text-sm text-green-800 leading-relaxed">
                        <span className="font-semibold">✓</span> {currentChart.report}
                      </p>
                    </div>
                  )}
                </div>
              )}
              
              {uploadedFile && (
                <div className="bg-gradient-to-br from-blue-50 to-blue-100 rounded-xl p-5 border-2 border-blue-300 shadow-sm">
                  <h3 className="font-bold text-blue-900 mb-3 flex items-center gap-2 text-sm uppercase tracking-wide">
                    <span>📄</span> Uploaded File
                  </h3>
                  <div className="space-y-2">
                    <p className="text-sm text-blue-900 font-semibold break-all">{uploadedFile.name}</p>
                    <div className="flex items-center gap-3 text-xs text-blue-700">
                      <span className="font-medium bg-blue-200 px-2 py-1 rounded">
                        {(uploadedFile.size / 1024).toFixed(1)} KB
                      </span>
                      <span className="font-medium bg-blue-200 px-2 py-1 rounded">
                        CSV Format
                      </span>
                    </div>
                  </div>
                </div>
              )}
            </div>
          </aside>
        )}
      </div>
    </div>
  );
}

export default App;
