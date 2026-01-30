# agent-aegis

An AI-powered coding agent that uses Google's Gemini 2.0 Flash with function calling capabilities to interact with your codebase. This agent can autonomously read files, list directories, write code, and execute Python scripts through a conversational interface.

**Key Features:**

- Autonomous function calling with feedback loop (iterates until task completion)
- Safe file operations (read/list/write) with working directory constraints
- Python script execution with argument support
- Path validation to prevent directory traversal attacks
- Natural language interaction with your codebase

Note: The `calculator/` folder is for testing the agent's capabilities.

---

## How It Works

The agent uses a **feedback loop** to accomplish tasks:

1. You provide a natural language prompt
2. The LLM analyzes the task and calls appropriate functions
3. Function results are fed back to the LLM
4. Process repeats until the LLM has enough information to answer
5. Final response is displayed (up to 20 iterations)

### Available Functions

The agent can autonomously call these functions:

- **`get_files_info`** — List files and directories with metadata
- **`get_file_content`** — Read file contents safely
- **`write_file`** — Create or overwrite files
- **`run_python_file`** — Execute Python scripts with arguments

All operations are scoped to `./calculator` directory for security.

---

## Project Layout

```
agent-aegis/
├── main.py                    # Main agent with feedback loop
├── config.py                  # Configuration (e.g., max_chars)
├── path_validation.py         # Security: path validation utilities
├── functions/
│   ├── get_files_info.py      # List directory contents
│   ├── get_file_content.py    # Read files safely
│   ├── write_file.py          # Write/create files
│   └── run_python_file.py     # Execute Python scripts
├── calculator/                # Test workspace
└── pyproject.toml             # Dependencies & metadata
```

---

## Requirements

- Python 3.10+
- A Google AI Studio API key

Create a `.env` file in the repository root with:

```bash
GEMINI_API_KEY=your_api_key_here
```

---

## Installation

Use either uv (recommended) or pip.

### Option A: uv

```bash
# Install uv (if not already installed)
brew install uv

# From repository root
uv sync
```

Quick check:

```bash
uv run python --version
```

### Option B: pip

```bash
python -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install google-genai==1.12.1 python-dotenv==1.1.0
```

---

## Usage

### Basic Examples

Ask the agent to interact with your code using natural language:

```bash
# Analyze code structure
uv run main.py "how does the calculator render results to the console?"

# Investigate functionality
uv run main.py "what functions are available in the pkg module?"

# Write or modify files
uv run main.py "create a new function that adds two numbers"

# Execute code
uv run main.py "run the tests and show me the results"
```

### Verbose Mode

See detailed function calls, arguments, and token usage:

```bash
uv run main.py "analyze the main.py structure" --verbose
```

**Verbose output includes:**

- Iteration count
- Function names and arguments
- Function responses
- Token usage (prompt + completion)

### How the Agent Works

The agent iteratively calls functions until it has enough context to answer:

```
User: "how does the calculator work?"
  → Agent calls: get_files_info()
  → Agent calls: get_file_content("main.py")
  → Agent calls: get_file_content("pkg/calculator.py")
  → Agent responds with analysis
```

The agent stops when no more function calls are needed (or after 20 iterations).

---

## Function Schemas

Each function is exposed to the LLM through a schema definition. The agent autonomously decides when to call these functions.

### `get_files_info`

Lists files and directories with metadata (size, type).

**Schema:**

- `working_directory` (auto-injected): Security-scoped directory
- `directory`: Relative path to list

**Returns:** Formatted string with file names, sizes, and directory flags

### `get_file_content`

Reads file contents safely (up to `config.max_chars`).

**Schema:**

- `working_directory` (auto-injected): Security-scoped directory
- `file_path`: Relative path to read

**Returns:** File contents or error message

### `write_file`

Creates or overwrites files with validation.

**Schema:**

- `working_directory` (auto-injected): Security-scoped directory
- `file_path`: Relative path to write
- `content`: String content to write

**Returns:** Success or error message

### `run_python_file`

Executes Python scripts with optional arguments.

**Schema:**

- `working_directory` (auto-injected): Security-scoped directory
- `file_path`: Relative path to Python file
- `args` (optional): List of command-line arguments

**Returns:** Script output or error message

### Security Note

All functions receive `working_directory="./calculator"` automatically via injection in [main.py](main.py#L137). The agent cannot escape this directory.

---

## Architecture

### Feedback Loop Implementation

The agent runs a loop (max 20 iterations) in [main.py](main.py#L59-L73):

1. **Generate content** with available function schemas
2. **Check for function calls** in response
3. **Execute functions** and append results to message history
4. **Continue loop** until LLM returns text-only response
5. **Display final answer** and exit

### Message History

The `messages` list maintains conversation context:

- User prompt
- LLM responses (with function calls)
- Function execution results

Each iteration, the LLM sees all previous context, enabling multi-step reasoning.

