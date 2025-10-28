# Testing with Specific User Identities in ADK

**How to test multi-user isolation and preferences with the commerce agent**

## ⚠️ Important: No UI for User ID Configuration

**The `adk web` interface does NOT provide a UI panel for setting User ID or Session ID.**

The ADK web interface uses a **fixed default user ID ("user")** for all browser-based sessions. To test with specific user identities, you **must use the API endpoints directly**.

---

## Testing Methods

### Method 1: API Testing with curl ✅ RECOMMENDED

Use the ADK REST API to create sessions for specific users and send messages programmatically.

### Method 2: Python Scripts ✅ ALTERNATIVE

Write Python scripts that call the API endpoints with different user IDs.

### Method 3: ~~UI Panel~~ ❌ NOT AVAILABLE

There is no UI panel in `adk web` for setting custom User IDs.

---

## Method 1: API Testing with curl

### Prerequisites

```bash
# Terminal 1: Start the server
cd tutorial_implementation/commerce_agent_e2e
make dev-sqlite  # or: make dev

# Server runs on http://localhost:8000
```

### Step 1: Create Sessions for Different Users

```bash
# Create session for Alice (runner)
curl -X POST http://localhost:8000/apps/commerce_agent/users/alice/sessions/session_001 \
  -H "Content-Type: application/json" \
  -d '{"state": {}}'

# Create session for Bob (cyclist)
curl -X POST http://localhost:8000/apps/commerce_agent/users/bob/sessions/session_002 \
  -H "Content-Type: application/json" \
  -d '{"state": {}}'
```

**Response:**
```json
{"id":"session_001","appName":"commerce_agent","userId":"alice","state":{},"events":[],"lastUpdateTime":1730000000.0}
```

### Step 2: Send Messages as Specific Users

**Alice (running shoes under €150):**
```bash
curl -X POST http://localhost:8000/run \
  -H "Content-Type: application/json" \
  -d '{
    "app_name": "commerce_agent",
    "user_id": "alice",
    "session_id": "session_001",
    "new_message": {
      "role": "user",
      "parts": [{"text": "I want running shoes under 150 euros"}]
    }
  }'
```

**Bob (cycling gear, budget €200):**
```bash
curl -X POST http://localhost:8000/run \
  -H "Content-Type: application/json" \
  -d '{
    "app_name": "commerce_agent",
    "user_id": "bob",
    "session_id": "session_002",
    "new_message": {
      "role": "user",
      "parts": [{"text": "I am into cycling. My budget is 200 euros"}]
    }
  }'
```

### Step 3: Verify User Isolation

**Check Alice's preferences (should be running, NOT cycling):**
```bash
curl -X POST http://localhost:8000/run \
  -H "Content-Type: application/json" \
  -d '{
    "app_name": "commerce_agent",
    "user_id": "alice",
    "session_id": "session_001",
    "new_message": {
      "role": "user",
      "parts": [{"text": "What are my preferences?"}]
    }
  }'
```

**Expected:** Agent responds with running preferences, NO mention of cycling.

### Step 4: Inspect Session State

```bash
# Get Alice's session
curl -X GET http://localhost:8000/apps/commerce_agent/users/alice/sessions/session_001

# Get Bob's session
curl -X GET http://localhost:8000/apps/commerce_agent/users/bob/sessions/session_002
```

**Response shows isolated state:**
```json
{
  "id": "session_001",
  "appName": "commerce_agent",
  "userId": "alice",
  "state": {
    "user:sport": "running",
    "user:budget": 150,
    "user:experience": "beginner"
  },
  "events": [...],
  "lastUpdateTime": 1730000000.0
}
```

---

## Method 2: Python Script Testing

Create a test script to automate multi-user testing:

```python
# test_multi_user.py
import requests
import json

BASE_URL = "http://localhost:8000"

def create_session(user_id, session_id):
    """Create a new session for a user"""
    url = f"{BASE_URL}/apps/commerce_agent/users/{user_id}/sessions/{session_id}"
    response = requests.post(url, json={"state": {}})
    print(f"✅ Created session for {user_id}: {response.status_code}")
    return response.json()

def send_message(user_id, session_id, message):
    """Send a message as a specific user"""
    url = f"{BASE_URL}/run"
    payload = {
        "app_name": "commerce_agent",
        "user_id": user_id,
        "session_id": session_id,
        "new_message": {
            "role": "user",
            "parts": [{"text": message}]
        }
    }
    response = requests.post(url, json=payload)
    events = response.json()
    
    # Extract agent's text response
    for event in events:
        if event.get("content", {}).get("role") == "model":
            parts = event["content"]["parts"]
            for part in parts:
                if "text" in part:
                    return part["text"]
    return "No response"

def get_session_state(user_id, session_id):
    """Get session state"""
    url = f"{BASE_URL}/apps/commerce_agent/users/{user_id}/sessions/{session_id}"
    response = requests.get(url)
    return response.json()

# Test multi-user isolation
if __name__ == "__main__":
    print("🧪 Testing Multi-User Isolation\n")
    
    # Setup Alice (runner)
    print("👤 ALICE (Runner)")
    create_session("alice", "session_001")
    response = send_message("alice", "session_001", "I want running shoes under 150 euros")
    print(f"Agent: {response[:100]}...\n")
    
    # Setup Bob (cyclist)
    print("👤 BOB (Cyclist)")
    create_session("bob", "session_002")
    response = send_message("bob", "session_002", "I am into cycling. Budget 200 euros")
    print(f"Agent: {response[:100]}...\n")
    
    # Verify Alice's preferences (should NOT mention cycling)
    print("🔍 Verifying Alice's Preferences")
    response = send_message("alice", "session_001", "What are my preferences?")
    print(f"Agent: {response}\n")
    
    if "cycling" in response.lower():
        print("❌ FAILURE: Alice's preferences contaminated with Bob's data!")
    else:
        print("✅ SUCCESS: User isolation working correctly!")
    
    # Show state
    print("\n📊 Session States:")
    alice_state = get_session_state("alice", "session_001")
    bob_state = get_session_state("bob", "session_002")
    print(f"Alice state: {alice_state.get('state', {})}")
    print(f"Bob state: {bob_state.get('state', {})}")
```

**Run the script:**
```bash
python test_multi_user.py
```

---

## SQLite Persistence Testing

### Test Session Persistence Across Restarts

```bash
# 1. Start with SQLite
make dev-sqlite

# 2. Create session for athlete_test
curl -X POST http://localhost:8000/apps/commerce_agent/users/athlete_test/sessions/persistent_session \
  -H "Content-Type: application/json" \
  -d '{"state": {}}'

# 3. Save preferences
curl -X POST http://localhost:8000/run \
  -H "Content-Type: application/json" \
  -d '{
    "app_name": "commerce_agent",
    "user_id": "athlete_test",
    "session_id": "persistent_session",
    "new_message": {
      "role": "user",
      "parts": [{"text": "I prefer running shoes under 150 euros"}]
    }
  }'

# 4. Stop server (Ctrl+C in Terminal 1)

# 5. Restart server
make dev-sqlite

# 6. Verify data persists
curl -X GET http://localhost:8000/apps/commerce_agent/users/athlete_test/sessions/persistent_session

# 7. Send new message (should remember preferences)
curl -X POST http://localhost:8000/run \
  -H "Content-Type: application/json" \
  -d '{
    "app_name": "commerce_agent",
    "user_id": "athlete_test",
    "session_id": "persistent_session",
    "new_message": {
      "role": "user",
      "parts": [{"text": "What do you recommend?"}]
    }
  }'
```

**Expected:** Agent remembers running preferences and budget after restart. ✅

---

## Using ADK Web UI (Limited to Default User)

The `adk web` browser interface can still be used for testing, but it will **always use user ID "user"**:

```bash
# Start server
make dev

# Open browser: http://localhost:8000
# Chat in the UI

# All browser sessions use:
#   User ID: "user"
#   Session ID: auto-generated by UI
```

**Limitation:** Cannot test multi-user isolation through the UI alone.

**Workaround:** Use the UI for initial testing, then switch to API endpoints for multi-user scenarios.

---

## Common Test Scenarios

### Scenario 1: New User Onboarding

```bash
# User: new_customer_123
# Goal: Test first-time preference collection

curl -X POST http://localhost:8000/apps/commerce_agent/users/new_customer_123/sessions/onboarding_001 \
  -H "Content-Type: application/json" \
  -d '{"state": {}}'

curl -X POST http://localhost:8000/run \
  -H "Content-Type: application/json" \
  -d '{
    "app_name": "commerce_agent",
    "user_id": "new_customer_123",
    "session_id": "onboarding_001",
    "new_message": {
      "role": "user",
      "parts": [{"text": "I want running shoes"}]
    }
  }'
```

**Expected:** Agent asks about budget, experience level, preferences.

### Scenario 2: Returning Customer

```bash
# Same user, new session
curl -X POST http://localhost:8000/apps/commerce_agent/users/new_customer_123/sessions/returning_002 \
  -H "Content-Type: application/json" \
  -d '{"state": {}}'

curl -X POST http://localhost:8000/run \
  -H "Content-Type: application/json" \
  -d '{
    "app_name": "commerce_agent",
    "user_id": "new_customer_123",
    "session_id": "returning_002",
    "new_message": {
      "role": "user",
      "parts": [{"text": "Show me new products"}]
    }
  }'
```

**Expected:** Agent recalls preferences from previous session (if using SQLite or user: state).

### Scenario 3: Multi-User Household

```bash
# Family members sharing a device
# User: parent_runner
# User: child_beginner
# User: partner_cyclist

# Each gets isolated preferences
curl -X POST http://localhost:8000/apps/commerce_agent/users/parent_runner/sessions/s001 \
  -H "Content-Type: application/json" -d '{"state": {}}'

curl -X POST http://localhost:8000/apps/commerce_agent/users/child_beginner/sessions/s001 \
  -H "Content-Type: application/json" -d '{"state": {}}'

curl -X POST http://localhost:8000/apps/commerce_agent/users/partner_cyclist/sessions/s001 \
  -H "Content-Type: application/json" -d '{"state": {}}'
```

**Expected:** Complete data isolation between family members.

---

## Debugging Tips

### Issue: Preferences Not Saving

**Check session state:**
```bash
curl -X GET http://localhost:8000/apps/commerce_agent/users/YOUR_USER_ID/sessions/YOUR_SESSION_ID
```

**Verify state contains `user:` prefixed keys:**
```json
{
  "state": {
    "user:sport": "running",
    "user:budget": 150
  }
}
```

### Issue: Preferences Mixing Between Users

**Verify using different User IDs:**
```bash
# Wrong - same user ID
user_id: "alice" → session_001
user_id: "alice" → session_002  # Same user, different session

# Correct - different user IDs
user_id: "alice" → session_001
user_id: "bob" → session_002   # Different users
```

### Issue: Preferences Lost After Restart

**Check persistence mode:**

| Mode | Behavior |
|------|----------|
| `make dev` | ADK state - preferences may NOT persist across restarts |
| `make dev-sqlite` | SQLite DB - preferences SHOULD persist across restarts |

**Verify SQLite database:**
```bash
sqlite3 commerce_sessions.db
> SELECT id, user_id FROM sessions;
> .quit
```

---

## Summary

### ✅ What Works

- **API Endpoints**: Full control over User ID and Session ID
- **Python Scripts**: Automate multi-user testing
- **SQLite Persistence**: Session data survives restarts

### ❌ What Doesn't Work

- **UI Panel**: No UI control for User ID (uses fixed "user")
- **Browser Testing**: Limited to default user without API calls

### 🎯 Best Practice

**For multi-user testing:**
1. Use `make dev-sqlite` for persistence
2. Create sessions via API with specific User IDs
3. Send messages via API for each user
4. Verify isolation by checking session states
5. Use Python scripts to automate test scenarios

---

## Reference Links

- **Official ADK Testing Guide**: https://google.github.io/adk-docs/get-started/testing/
- **ADK API Reference**: https://google.github.io/adk-docs/api-reference/rest/
- **Session Management**: https://google.github.io/adk-docs/sessions/
- **SQLite Persistence Guide**: `docs/SQLITE_SESSION_PERSISTENCE_GUIDE.md`

---

**Last Updated**: 2025-10-27  
**ADK Version**: 1.17.0+
