import { useState } from 'react'
import { CopilotKit } from "@copilotkit/react-core"
import { CopilotChat } from "@copilotkit/react-ui"
import "@copilotkit/react-ui/styles.css"
import './App.css'

function App() {
  const [uploadedFile, setUploadedFile] = useState<string | null>(null)
  const [csvContent, setCsvContent] = useState<string | null>(null)

  const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    if (!file) return

    const reader = new FileReader()
    reader.onload = async (e) => {
      const content = e.target?.result as string
      setUploadedFile(file.name)
      setCsvContent(content)
      console.log(`✅ Loaded ${file.name}: ${content.length} bytes`)
    }
    reader.readAsText(file)
  }

  return (
    <div className="app-container">
      <CopilotKit runtimeUrl="/api/copilotkit" agent="data_analyst">
        <div className="dashboard">
          {/* Header */}
          <header className="header">
            <h1>📊 Data Analysis Dashboard</h1>
            <p>Upload CSV data and ask questions to get insights</p>
          </header>

          {/* File Upload */}
          <div className="upload-section">
            <label htmlFor="file-upload" className="upload-button">
              📁 Upload CSV File
            </label>
            <input
              id="file-upload"
              type="file"
              accept=".csv"
              onChange={handleFileUpload}
              style={{ display: 'none' }}
            />
            {uploadedFile && (
              <div className="file-info">
                <span className="file-name">✅ {uploadedFile}</span>
                {csvContent && (
                  <span className="file-size">
                    ({(csvContent.length / 1024).toFixed(1)} KB)
                  </span>
                )}
              </div>
            )}
          </div>

          {/* Chat Interface */}
          <div className="chat-container">
            <CopilotChat
              instructions="You are a data analysis assistant. Help users analyze their CSV data."
              labels={{
                title: "Data Analyst",
                initial: "Hi! Upload a CSV file and I'll help you analyze it. You can ask me to:\n\n• Summarize the data\n• Find correlations\n• Identify trends\n• Create visualizations",
              }}
            />
          </div>

          {/* Instructions */}
          <div className="instructions">
            <h3>How to use:</h3>
            <ol>
              <li>Upload a CSV file using the button above</li>
              <li>Ask questions like:
                <ul>
                  <li>"What are the key statistics?"</li>
                  <li>"Show me a summary of the data"</li>
                  <li>"Create a line chart of sales over time"</li>
                  <li>"What correlations exist in the data?"</li>
                </ul>
              </li>
              <li>Get insights and visualizations instantly!</li>
            </ol>
          </div>
        </div>
      </CopilotKit>
    </div>
  )
}

export default App
