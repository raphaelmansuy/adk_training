# Tutorial 08: State & Memory Management

A personal learning tutor that demonstrates comprehensive state management and memory capabilities in ADK agents.

## 🚀 Quick Start

```bash
# Install dependencies
make setup

# Start the agent
make dev

# Open http://localhost:8000 and select 'personal_tutor'
```

## 💬 What It Does

This agent showcases ADK's state management system with three types of state:

- **Persistent State** (`user:` prefix): User preferences and learning history
- **Session State** (no prefix): Current learning session tracking
- **Temporary State** (`temp:` prefix): Quiz calculations and intermediate results

### Key Features

- 🎯 **User Preferences**: Language and difficulty level settings
- 📚 **Progress Tracking**: Completed topics and quiz scores
- 🧠 **Memory Search**: Find past learning sessions
- 📊 **Learning Analytics**: Progress summaries and statistics
- 🔄 **Session Management**: Track current learning topics

## 📁 Project Structure

```
tutorial08/
├── personal_tutor/        # Agent implementation
│   ├── __init__.py        # Package marker
│   ├── agent.py           # Agent with 6 state management tools
│   └── .env.example       # API key template
├── tests/                 # Comprehensive test suite (21 tests)
├── requirements.txt       # Dependencies
└── Makefile              # Build commands
```

## 🔧 Setup

1. **Get API Key**: Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. **Install**: `make setup`
3. **Configure**: Copy `.env.example` to `.env` and add your API key
4. **Run**: `make dev`

## 🧪 Testing

```bash
make test    # Run comprehensive test suite
make demo    # See demo conversation flows
```

## 🎯 Try These Conversation Flows

### 1. Set Preferences

```text
User: Set my language to Spanish and difficulty to intermediate
Agent: Preferences saved: es, intermediate level
```

### 2. Start Learning

```text
User: Start learning Python classes
Agent: Started learning session: Python Classes at intermediate level
```

### 3. Complete Quiz

```text
User: I got 8 out of 10 on my quiz
Agent: Quiz grade: B (80.0%)
```

### 4. Check Progress

```text
User: Show me my progress
Agent: Topics completed: 1, Average score: 80.0
```

### 5. Search Memory

```text
User: What have I learned about Python?
Agent: Found 1 past sessions related to "python": Python Classes
```

## 🛠️ State Management Tools

| Tool                      | Purpose                   | State Type            |
| ------------------------- | ------------------------- | --------------------- |
| `set_user_preferences`    | Store language/difficulty | Persistent (`user:`)  |
| `record_topic_completion` | Track completed topics    | Persistent (`user:`)  |
| `get_user_progress`       | Show learning statistics  | Read persistent state |
| `start_learning_session`  | Begin new topic           | Session state         |
| `calculate_quiz_grade`    | Grade quizzes             | Temporary (`temp:`)   |
| `search_past_lessons`     | Find past sessions        | Memory simulation     |

## 📊 State Prefixes Explained

- **`user:`** - Persistent across sessions (user preferences, history)
- **No prefix** - Session-scoped (current topic, session data)
- **`temp:`** - Invocation-scoped (calculations, discarded after use)

## 🧪 Test Coverage

- ✅ **21 comprehensive tests** covering all functionality
- ✅ **Unit tests** for each tool function
- ✅ **Integration tests** for complete workflows
- ✅ **State management** validation
- ✅ **Memory operations** testing
- ✅ **Agent configuration** verification

## 📚 Learning Objectives

After completing this tutorial, you'll understand:

- How to use ADK's state management system
- Different state persistence levels
- Memory service integration patterns
- Building agents with learning capabilities
- Comprehensive testing strategies

## 🎓 Next Steps

- **Tutorial 09**: Callbacks and guardrails
- **Tutorial 10**: Evaluation and testing
- **Tutorial 11**: Built-in tools and grounding

Built with ❤️ using Google ADK.
