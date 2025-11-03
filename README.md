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

### Gemini prompt runner (`main.py`)

Sends your prompt to Gemini 2.0 Flash and prints the response. Requires `GEMINI_API_KEY` in `.env`.

```bash
# Basic
python main.py "How can I improve my Python skills?"

# Verbose token usage output
python main.py "Explain decorators with examples" --verbose
```

Notes:

- Uses model `gemini-2.0-flash-001`.
- If the prompt is missing, the script exits with guidance.

---

## File utilities (in `functions/`)

All helpers enforce that operations stay within a provided `working_directory`.

- `get_file_content(working_directory: str, file_path: str) -> str`

  - Returns file contents (up to a configured limit in `config.max_chars`) or an error message.

- `get_files_info(working_directory: str, directory: str) -> str`

  - Lists entries in a directory with size and directory flag, or returns an error message. Output starts with `"Results for current directory:"`.

- `write_file(working_directory: str, file_path: str, content: str) -> str`
  - Creates parent folders as needed, writes the file, and returns a status message. Blocks writes outside the working directory.

Example snippet:

```python
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file

print(get_files_info(".", "."))
print(write_file(".", "docs/example.txt", "hello"))
print(get_file_content(".", "docs/example.txt"))
```

---

## Troubleshooting

- Missing API key / auth errors
  - Ensure `.env` exists with `GEMINI_API_KEY=...`
- `ModuleNotFoundError: google.genai` or `google-genai`
  - Re-install dependencies (`uv sync` or reinstall via pip) and confirm Python 3.10+ is active.
- Filesystem errors
  - Paths must be under your chosen `working_directory`. Access outside is intentionally blocked.

---

## Roadmap / Notes

- The file read helper currently reads up to `max_chars`. Consider improving truncation messaging and byte/encoding handling if you plan to read large files.
- Add unit tests for the filesystem helpers and CLI.

---

## License

Add a license if you plan to share or distribute this project.
