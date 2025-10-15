# Tutorial 31 - Chart Visualization Fix - Testing Guide

## Date: October 15, 2025
## Status: READY FOR TESTING

## Problem Identified
Charts were not displaying because the frontend was only listening for `TEXT_MESSAGE_CONTENT` events but NOT for `TOOL_CALL_RESULT` events where the agent sends chart data.

## Solution Implemented

### Key Changes to App.tsx

1. **Added Tool Result Event Handling**
   ```typescript
   // Handle tool call results (where chart data lives!)
   if (jsonData.type === "TOOL_CALL_RESULT") {
     const resultContent = typeof jsonData.content === 'string' 
       ? JSON.parse(jsonData.content) 
       : jsonData.content;
     
     if (resultContent && resultContent.chart_type) {
       setCurrentChart(resultContent);
       // Attach to message
       setMessages((prev) => {
         const newMessages = [...prev];
         const lastMsg = newMessages[newMessages.length - 1];
         if (lastMsg && lastMsg.role === "assistant") {
           lastMsg.chartData = resultContent;
         }
         return newMessages;
       });
     }
   }
   ```

2. **Added Enhanced Console Logging**
   - All incoming events are logged with type and content
   - Tool results specifically show "📊 Received TOOL_CALL_RESULT"
   - Chart data extraction shows "📈 Chart data found in tool result"
   - Fallback extraction shows "📊 Chart data extracted from text (fallback)"

3. **Fallback Chart Extraction**
   - If tool results don't contain charts, try parsing text content
   - Ensures charts work even if event format changes

## Testing Instructions

### Step 1: Reload the Frontend

**IMPORTANT**: Clear your browser cache or do a hard refresh:
- **Chrome/Edge**: `Cmd+Shift+R` (Mac) or `Ctrl+Shift+R` (Windows)
- **Firefox**: `Cmd+Shift+R` (Mac) or `Ctrl+Shift+R` (Windows)  
- **Safari**: `Cmd+Option+R`

### Step 2: Open Browser DevTools
1. Open Developer Tools (F12 or Cmd+Option+I)
2. Go to the **Console** tab
3. Keep it open to see the debug logs

### Step 3: Test Chart Generation

#### Test 1: Line Chart
```
Create a line chart of revenue over time
```

**Expected Results:**
- Console shows: `📡 Received event: TOOL_CALL_RESULT`
- Console shows: `📊 Received TOOL_CALL_RESULT:` with tool data
- Console shows: `📈 Chart data found in tool result:`
- **Chart appears in sidebar** showing Revenue vs Date
- **Chart also appears inline** within the assistant's message

#### Test 2: Bar Chart
```
Create a bar chart comparing sales by region
```

**Expected Results:**
- Bar chart appears in sidebar
- Shows different regions on x-axis
- Shows sales values on y-axis

#### Test 3: Statistical Summary (No Chart)
```
Show me statistical summary of the data
```

**Expected Results:**
- Text response with markdown formatting
- **No chart** (as none was generated)
- No chart-related console logs

## What to Look For

### ✅ SUCCESS Indicators
1. Console log: `📊 Received TOOL_CALL_RESULT`
2. Console log: `📈 Chart data found in tool result`
3. Sidebar panel appears with "📊 Visualization" header
4. Chart.js visualization renders properly
5. Chart metadata shows (Type, X-Axis, Y-Axis, Data Points)
6. Chart also appears inline in the message

### ❌ FAILURE Indicators
1. Console error: `Failed to extract chart data`
2. No `TOOL_CALL_RESULT` events in console
3. Sidebar doesn't appear when chart requested
4. Agent says it created a chart but nothing shows

## Debugging

### Check Event Types Received
Look at console output for:
```
📡 Received event: TEXT_MESSAGE_CONTENT
📡 Received event: TOOL_CALL_RESULT
```

If you ONLY see `TEXT_MESSAGE_CONTENT` and no `TOOL_CALL_RESULT`, the agent isn't calling the tools.

### Check Agent Backend Logs
In the terminal where agent is running, you should see:
```
INFO: Both GOOGLE_API_KEY and GEMINI_API_KEY are set. Using GOOGLE_API_KEY.
```

And when tools are called:
```
INFO: Tool call: create_chart
```

### Common Issues

#### Issue 1: No Events at All
**Symptom**: No console logs
**Solution**: 
- Check backend is running: `curl http://localhost:8000/health`
- Verify frontend port: Should be http://localhost:5174
- Check browser console for CORS errors

#### Issue 2: TEXT_MESSAGE_CONTENT Only
**Symptom**: Only text events, no TOOL_CALL_RESULT
**Solution**:
- Agent may not be calling tools
- Check if CSV data was uploaded successfully
- Try a more explicit prompt: "Use the create_chart tool to make a line chart"

#### Issue 3: TOOL_CALL_RESULT but No Chart
**Symptom**: Events received but sidebar doesn't show
**Solution**:
- Check console for parsing errors
- Verify tool result has `chart_type` field
- Check if `currentChart` state is being set

## Current Server Status

### Backend
- **Status**: ✅ Running
- **URL**: http://localhost:8000
- **Health**: http://localhost:8000/health
- **Process**: Active in terminal

### Frontend
- **Status**: Needs reload
- **URL**: http://localhost:5174
- **Note**: Must hard refresh to get new code

## Expected Console Output (Success Case)

When you ask "Create a line chart of revenue over time", you should see:

```
📡 Received event: TEXT_MESSAGE_CONTENT {type: "TEXT_MESSAGE_CONTENT", delta: "I", ...}
📡 Received event: TEXT_MESSAGE_CONTENT {type: "TEXT_MESSAGE_CONTENT", delta: " have", ...}
...
📡 Received event: TOOL_CALL_RESULT {type: "TOOL_CALL_RESULT", tool_call_id: "...", content: "{...}", ...}
📊 Received TOOL_CALL_RESULT: {type: "TOOL_CALL_RESULT", ...}
📈 Chart data found in tool result: {chart_type: "line", data: {...}, options: {...}}
```

## Files Modified
- ✅ `/frontend/src/App.tsx` - Added TOOL_CALL_RESULT handling
- ✅ Enhanced logging for debugging
- ✅ Fixed chartData reference bug

## Next Steps After Testing

### If It Works ✅
1. Test all chart types (line, bar, scatter)
2. Test with different datasets
3. Verify chart updates when new data uploaded
4. Test multiple charts in conversation
5. Remove excessive console.log statements (optional)

### If It Doesn't Work ❌
1. Share console output
2. Share agent backend logs
3. Share screenshot of what you see
4. Verify all steps were followed correctly

## Architecture Notes

### AG-UI ADK Event Flow
```
User Request
    ↓
Frontend (POST /api/copilotkit)
    ↓
AG-UI ADK Middleware
    ↓
Google ADK Agent
    ↓
Tool Execution (create_chart)
    ↓
Tool Result
    ↓
AG-UI Event Translator
    ↓
SSE Stream (TOOL_CALL_RESULT event)
    ↓
Frontend Event Handler
    ↓
Chart Visualization
```

### Event Types in AG-UI ADK
- `TEXT_MESSAGE_CONTENT`: Streaming text delta
- `TOOL_CALL_RESULT`: Tool execution result (contains chart data!)
- `TOOL_CALL_START`: Tool execution started
- `MESSAGE_COMPLETED`: Message finished
- `AGENT_STATE_UPDATE`: State changed

## Additional Resources
- AG-UI ADK Source: `/Users/raphaelmansuy/.venv/lib/python3.12/site-packages/ag_ui_adk/`
- Event Types: `ag_ui/core/events.py`
- Event Translator: `ag_ui_adk/event_translator.py`
- Tutorial Agent: `/tutorial_implementation/tutorial31/agent/agent.py`

## Success Criteria
✅ Charts display in sidebar when agent creates them
✅ Charts display inline in messages
✅ Multiple chart types work (line, bar, scatter)
✅ Console logs show proper event flow
✅ No TypeScript errors
✅ No runtime errors

**STATUS**: Ready for testing! Please refresh browser and test chart generation.
