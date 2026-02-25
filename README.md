# agent-aegis

Lightweight Python toolkit with:

- A simple CLI to send prompts to Google AI (Gemini) and print responses
- Safe file utilities (read/list/write) that prevent escaping a working directory

Note: The `calculator/` folder is only for local testing and is not part of the project’s core scope.

---

## Features

- Gemini prompt runner using `google-genai` (model: `gemini-2.0-flash-001`)
- `.env`-based API key loading via `python-dotenv`
- Path-safe filesystem helpers:
  - `get_file_content(working_directory, file_path)`
  - `get_files_info(working_directory, directory)`
  - `write_file(working_directory, file_path, content)`

---

## Project layout

- `main.py` — Gemini prompt runner CLI
- `config.py` — basic configuration (e.g., character read cap)
- `path_validation.py` — single entry point for safe path checks
- `functions/`
  - `get_file_content.py`
  - `get_files_info.py`
  - `write_file.py`
- `pyproject.toml` — metadata and dependencies

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
curl -LsSf https://astral.sh/uv/install.sh | sh

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

## Troubleshooting

- Missing API key / auth errors
  - Ensure `.env` exists with `GEMINI_API_KEY=...`
- `ModuleNotFoundError: google.genai` or `google-genai`
  - Re-install dependencies (`uv sync` or reinstall via pip) and confirm Python 3.10+ is active.
- Filesystem errors
  - Paths must be under your chosen `working_directory`. Access outside is intentionally blocked.

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

---

## Roadmap

- [ ] Add support for more file operations (delete, move, rename)
- [ ] Implement streaming responses for long tasks
- [ ] Add multi-turn conversation support (continue from previous response)
- [ ] Improve error recovery when functions fail
- [ ] Unit tests for all function schemas
- [ ] Support multiple working directories
- [ ] Add file search/grep functionality

---

## License

MIT License - Feel free to use and modify.
