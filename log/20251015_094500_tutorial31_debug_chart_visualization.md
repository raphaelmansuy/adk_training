# Tutorial 31 - Chart Visualization Debugging Session

## Date: October 15, 2025
## Status: IN PROGRESS - Enhanced Debug Logging Added

## Problem Statement
User reported: "It cool but I don't see any chart."

The agent successfully generates chart data (evidenced by text like "Okay, I've created a bar chart...") but the chart visualization does not appear in the sidebar.

## Root Cause Analysis

### What We Know
1. **Agent is working**: Agent responds to prompts and says it created charts
2. **Backend is running**: Port 8000 is active and responding
3. **Frontend is running**: Port 5173 is active (shown in screenshot)
4. **Tool is executing**: The `create_chart()` tool is being called successfully
5. **Event handling exists**: Code has TOOL_CALL_RESULT handler implemented

### What We Don't Know (Yet)
1. **Are TOOL_CALL_RESULT events being received?** Need to check console logs
2. **What is the exact event structure?** Need to see the actual JSON
3. **Is `chart_type` at the right level?** Could be nested differently
4. **Is the chart data being set?** State updates might not be triggering

## Investigation Strategy

### Phase 1: Enhanced Logging (COMPLETED)

Added comprehensive console logging to trace event flow:

```typescript
// Main event loop logging
console.log("📡 Received event:", jsonData.type, jsonData);

// TOOL_CALL_RESULT specific logging
console.log("🔧 TOOL_CALL_RESULT Event Received!");
console.log("   Full event object:", JSON.stringify(jsonData, null, 2));
console.log("   Content type:", typeof jsonData.content);
console.log("   Content value:", jsonData.content);
console.log("   Parsed content:", resultContent);
console.log("   Has chart_type?:", !!resultContent.chart_type);

// When chart found
console.log("✅ CHART DATA FOUND!");
console.log("   Chart type:", resultContent.chart_type);
console.log("   Set currentChart state");

// When chart NOT found
console.log("❌ No chart_type found in result");
console.log("   Result keys:", Object.keys(resultContent));
```

### Phase 2: Browser Testing (NEXT STEP)

**Instructions for User:**

1. **Hard Refresh Browser**
   - Mac: `Cmd + Shift + R`
   - Windows: `Ctrl + Shift + R`
   - Or clear browser cache completely

2. **Open Developer Console**
   - Press F12 or `Cmd + Option + I` (Mac)
   - Click on "Console" tab
   - Keep it open and visible

3. **Test Chart Generation**
   - Upload `sample_sales_data.csv`
   - Type: "Create a bar chart of Product vs Revenue"
   - Watch console output carefully

4. **Capture Information**
   - Look for "📡 Received event:" lines
   - Look for "🔧 TOOL_CALL_RESULT Event Received!"
   - Look for "✅ CHART DATA FOUND!" or "❌ No chart_type found"
   - Take screenshot of console output

## Expected Event Flow

Based on AG-UI protocol documentation:

```
1. RunStarted event
   type: "RUN_STARTED"
   
2. TextMessageStart event
   type: "TEXT_MESSAGE_START"
   messageId: "msg-xxx"
   role: "assistant"
   
3. TextMessageContent events (streaming)
   type: "TEXT_MESSAGE_CONTENT"
   messageId: "msg-xxx"
   delta: "I" / " have" / " created" / ...
   
4. ToolCallStart event
   type: "TOOL_CALL_START"
   toolCallId: "tool-xxx"
   toolCallName: "create_chart"
   
5. ToolCallArgs events (streaming)
   type: "TOOL_CALL_ARGS"
   toolCallId: "tool-xxx"
   delta: argument JSON fragments
   
6. ToolCallEnd event
   type: "TOOL_CALL_END"
   toolCallId: "tool-xxx"
   
7. ToolCallResult event ⭐ (THIS IS WHERE CHART DATA IS!)
   type: "TOOL_CALL_RESULT"
   toolCallId: "tool-xxx"
   content: JSON string or object with chart data
   
8. TextMessageEnd event
   type: "TEXT_MESSAGE_END"
   messageId: "msg-xxx"
   
9. RunFinished event
   type: "RUN_FINISHED"
```

## Chart Data Structure

From `agent.py`, the `create_chart()` tool returns:

```json
{
  "status": "success",
  "report": "Generated bar chart for Revenue vs Product...",
  "chart_type": "bar",
  "data": {
    "labels": ["Widget A", "Widget B", "Widget C"],
    "values": [2400, 3200, 2800]
  },
  "options": {
    "x_label": "Product",
    "y_label": "Revenue",
    "title": "Revenue vs Product"
  }
}
```

This structure should appear in the `content` field of the TOOL_CALL_RESULT event.

## Potential Issues & Solutions

### Issue 1: Events Not Reaching Frontend

**Symptoms:**
- No "📡 Received event:" logs in console
- No TOOL_CALL_RESULT events visible

**Possible Causes:**
- CORS blocking SSE stream
- Network error interrupting stream
- Backend not emitting events

**Solution:**
- Check Network tab for /api/copilotkit request
- Verify EventStream stays open
- Check backend logs for event emission

### Issue 2: Event Structure Different Than Expected

**Symptoms:**
- "🔧 TOOL_CALL_RESULT Event Received!" appears
- "❌ No chart_type found in result" appears
- Keys logged don't include chart_type

**Possible Causes:**
- `content` field structure is nested differently
- `chart_type` is at a different path
- Tool result wrapped in additional layer

**Solution:**
- Examine "Result keys:" console output
- Check full event JSON structure
- Adjust parsing logic to match actual structure

### Issue 3: State Not Updating

**Symptoms:**
- "✅ CHART DATA FOUND!" appears
- "Set currentChart state" appears
- But sidebar still doesn't show chart

**Possible Causes:**
- React state batch update issue
- Sidebar conditional rendering logic problem
- Chart render function error

**Solution:**
- Check for React errors in console
- Verify `currentChart` state in React DevTools
- Add logging in `renderChart()` function
- Check sidebar rendering conditions

### Issue 4: Chart Rendering Error

**Symptoms:**
- Chart data is received and state is set
- Sidebar appears but chart doesn't render
- Console shows Chart.js errors

**Possible Causes:**
- Invalid data format for Chart.js
- Missing required properties
- Chart.js configuration error

**Solution:**
- Validate data structure matches Chart.js requirements
- Check for null/undefined values
- Test renderChart() in isolation

## Testing Checklist

- [ ] Browser hard refreshed to load new code
- [ ] Developer console open and visible
- [ ] Backend agent running on port 8000
- [ ] Frontend running on correct port
- [ ] CSV file uploaded successfully
- [ ] Chart request sent to agent
- [ ] Console logs captured
- [ ] Event types identified
- [ ] TOOL_CALL_RESULT event received
- [ ] Chart data structure examined
- [ ] Parsing logic verified
- [ ] State update confirmed
- [ ] Sidebar visibility confirmed
- [ ] Chart rendering confirmed

## Code Changes Made

### File: `frontend/src/App.tsx`

1. **Added main event logging** (Line ~147)
   ```typescript
   console.log("📡 Received event:", jsonData.type, jsonData);
   ```

2. **Enhanced TOOL_CALL_RESULT logging** (Line ~157-190)
   - Full event object dump
   - Content type checking
   - Parsed content examination
   - Chart type detection logging
   - State update confirmation
   - Detailed error logging

## Next Actions

1. ✅ **User**: Hard refresh browser (Cmd+Shift+R)
2. ✅ **User**: Open developer console (F12)
3. ⏳ **User**: Request chart creation
4. ⏳ **User**: Observe console output
5. ⏳ **User**: Share findings (screenshot/text)
6. ⏳ **Agent**: Analyze actual event structure
7. ⏳ **Agent**: Fix parsing logic if needed
8. ⏳ **Agent**: Verify chart displays correctly

## Reference Documentation

- **AG-UI Events**: https://docs.ag-ui.com/concepts/events
- **AG-UI Protocol**: https://github.com/ag-ui-protocol/ag-ui
- **Google ADK**: Tutorial 31 documentation
- **Chart.js**: https://www.chartjs.org/docs/

## Success Criteria

- ✅ Console shows "🔧 TOOL_CALL_RESULT Event Received!"
- ✅ Console shows "✅ CHART DATA FOUND!"
- ✅ Console shows "Set currentChart state"
- ✅ Sidebar appears with "📊 Visualization" header
- ✅ Chart renders with correct data
- ✅ Chart metadata displays (Type, X-Axis, Y-Axis, Data Points)
- ✅ No errors in console

## Timeline

- **09:00 AM**: Issue reported - charts not displaying
- **09:15 AM**: Read AG-UI documentation on event types
- **09:30 AM**: Identified TOOL_CALL_RESULT as the key event
- **09:45 AM**: Added comprehensive debug logging
- **09:50 AM**: Waiting for user to test with enhanced logging

---

**Status**: Ready for user testing with enhanced debug logging
**Next Step**: User tests in browser and shares console output
