# Backend Code Review Findings

This document details the findings of the code review for the backend service.

## Summary

The backend is a Python/FastAPI application using Poetry for dependency management, deployed via Docker/Gunicorn on Fly.io. It leverages Supabase for database/auth, Redis for caching/pubsub, LiteLLM for LLM interaction, and Daytona for sandboxing. The agent architecture relies on a `ThreadManager` and `ResponseProcessor` to handle conversation flow, tool execution (XML & native formats), and state management. Key areas for review include Dockerfile security/optimizations, robustness of Redis-based state management, the strict `todo.md` workflow defined in the prompt, and specific tool implementations (especially file reading and browser interaction).

## Detailed Findings

### Security

*   **Dockerfile:** Copies `.env` file directly into the image, exposing secrets. Secrets should be injected at runtime. (**Critical**)
*   **Sandbox:** The system prompt mentions `sudo` privileges are enabled by default in the sandbox, which requires careful review of sandbox isolation and tool capabilities (especially `SandboxShellTool`) to prevent potential misuse or escape.

### Performance

*   **Dockerfile:** Gunicorn worker count (`--workers 24`) seems excessively high for likely CPU resources (1 or 8 CPUs on Fly.io), potentially causing context-switching overhead. Timeouts (`--timeout 600`) are very long, risking worker starvation. Keep-alive (`--keep-alive 250`) is unusually high. Max requests (`--max-requests 0`) disables worker recycling, which can lead to memory leaks over time.
*   **`api.py`:** Commented-out IP-based rate limiting is insufficient for distributed environments and has a very low limit (`MAX_CONCURRENT_IPS = 25`). A Redis-based implementation is recommended.
*   **`run.py`:** Performing a database billing check on *every* agent loop iteration might be inefficient. Consider less frequent checks.

### Reliability & Error Handling

*   **`run.py`:** Agent completion detection relies partly on checking if the last message was from the assistant, which could be fragile. Relying solely on `<complete>` tag or explicit status messages might be more robust.
*   **`response_processor.py`:** The streaming logic is complex and manages state across chunks (tool calls, content). Requires thorough testing for edge cases and potential race conditions.
*   **`data_providers_tool.py`:** Contains an unprofessional error message (`YOU FUCKING IDIOT!`) that needs removal/rephrasing.
*   **General:** Robustness of interactions with the internal browser API (`sb_browser_tool.py`) and Daytona sandbox needs verification.

### Code Quality & Maintainability

*   **Architecture:** Generally well-structured with separation of concerns (API, Agent Core, Tools, Services). `ThreadManager` and `ResponseProcessor` are central components.
*   **`sb_files_tool.py`:** The `str_replace` function's limitation (only replaces single occurrences) makes it prone to failure if the target string isn't unique.
*   **`sb_files_tool.py`:** The `read_file` function is commented out. This is a significant gap, as reading files is fundamental. It's unclear how the agent reads files currently (perhaps via `cat` in `SandboxShellTool`?). This needs clarification and likely reinstatement of a dedicated file reading tool.
*   **`sb_browser_tool.py`:** Several actions (`search_google`, `open_tab`, `extract_content`) are commented out, potentially limiting functionality or indicating incomplete features.
*   **`web_search_tool.py`:** Class docstring incorrectly mentions "Exa API" instead of the used "Tavily API".
*   **Testing:** Some testing code is commented out within `run.py`; should be moved to dedicated test files in `tests/`. Coverage and types of tests should be reviewed.

### Configuration & Deployment

*   **Dockerfile:** Inconsistent dependency installation (`pip install -r requirements.txt` instead of using Poetry). Hardcoded `ENV_MODE="production"` reduces image flexibility. Could benefit from multi-stage builds and a `.dockerignore` file.
*   **Secrets:** `.env` handling in Dockerfile is insecure. Fly.io secrets management should be used.
*   **Fly.io Config:** `fly.production.toml` specifies 8 CPUs / 16GB RAM, while `fly.staging.toml` uses 1 CPU / 1GB RAM. Gunicorn worker settings in the Dockerfile (24 workers) are not optimized for either configuration.

## Recommendations

Based on the findings, the following actions are recommended, prioritized by impact:

**Critical Path / Highest Priority:**

1.  **Security - Fix Secret Handling (Dockerfile):**
    *   **Action:** Remove `COPY .env .` from the `Dockerfile`.
    *   **Reason:** Prevents embedding sensitive credentials in the Docker image. (**Critical Security Risk**)
    *   **Implementation:** Inject secrets at runtime using Fly.io secrets (`fly secrets set KEY=VALUE`) or another secrets management solution. Update configuration loading (`utils/config.py`) to read from environment variables.
2.  **Core Functionality - Implement `read_file` Tool (`sb_files_tool.py`):**
    *   **Action:** Uncomment and verify/refactor the `read_file` function in `SandboxFilesTool`.
    *   **Reason:** Reading files is a fundamental agent capability currently missing from the dedicated file tool, forcing potential reliance on less safe/efficient methods (like `cat` via `execute_command`).
    *   **Implementation:** Ensure the tool correctly handles paths relative to `/workspace`, decodes text files, handles potential errors (file not found, binary files), and supports optional line ranges as originally designed.
3.  **Deployment - Fix Dependency Installation (Dockerfile):**
    *   **Action:** Modify the `Dockerfile` to install dependencies using Poetry (`poetry install --no-root --no-dev`).
    *   **Reason:** Ensures reproducible builds using the exact dependencies specified in `poetry.lock`, preventing potential runtime inconsistencies.
    *   **Implementation:** Replace `pip install -r requirements.txt` with appropriate Poetry commands, potentially within a multi-stage build to keep the final image clean. Ensure `requirements.txt` is either removed or kept in sync automatically if needed for other purposes.

**High Priority:**

4.  **Performance - Optimize Gunicorn Settings (Dockerfile):**
    *   **Action:** Adjust `--workers`, `--timeout`, `--keep-alive`, and `--max-requests` in the `CMD` line.
    *   **Reason:** Current settings (24 workers, 600s timeout, 0 max requests) are likely suboptimal for Fly.io environments and can lead to performance issues or memory leaks.
    *   **Implementation:** Start with `workers = 2 * CPU_COUNT + 1` (adjust based on Fly.io plan), reduce timeouts significantly (e.g., 60-120s, consider background tasks for longer operations), reset keep-alive to default (or ~5s), and enable worker recycling (e.g., `--max-requests 1000 --max-requests-jitter 50`).
5.  **Reliability - Implement Robust Rate Limiting (`api.py`):**
    *   **Action:** Implement rate limiting using Redis.
    *   **Reason:** The current commented-out IP-based approach is insufficient for distributed environments.
    *   **Implementation:** Use a Redis-based library (like `redis-py-cluster`'s rate limiting features or `limits`) to track requests per user/IP across instances. Configure sensible limits.
6.  **Security - Review Sandbox `sudo` Access:**
    *   **Action:** Carefully audit the necessity of `sudo` privileges within the sandbox and the implementation of tools (especially `SandboxShellTool`) that might leverage it.
    *   **Reason:** Unnecessary `sudo` increases the attack surface if sandbox isolation is compromised.
    *   **Implementation:** Determine if `sudo` is truly required. If so, ensure commands using it are strictly controlled and validated. If not, configure the sandbox environment to run as a non-root user or restrict `sudo` access.

**Medium Priority:**

7.  **Code Quality - Refine Agent Stopping Logic (`run.py`):**
    *   **Action:** Make the agent loop termination rely primarily on explicit signals (e.g., `<complete>` tag, `finish_reason` from `ResponseProcessor`) rather than just checking if the last message was from the assistant.
    *   **Reason:** Improves robustness and clarity of agent completion.
8.  **Code Quality - Improve `str_replace` Tool (`sb_files_tool.py`):**
    *   **Action:** Consider enhancing `str_replace` to handle multiple occurrences (e.g., replace first, replace all, or require line numbers for targeting) or guide the agent to use more robust methods (like `sed` via `execute_command` or full rewrites) when uniqueness isn't guaranteed.
    *   **Reason:** The current "exactly once" limitation is fragile.
9.  **Code Quality - Remove Unprofessional Error (`data_providers_tool.py`):**
    *   **Action:** Replace the unprofessional error message.
    *   **Reason:** Maintain professional code standards.
10. **Configuration - Externalize `ENV_MODE` (Dockerfile):**
    *   **Action:** Remove `ENV ENV_MODE="production"` from the Dockerfile.
    *   **Reason:** Increases image flexibility for different environments.
    *   **Implementation:** Set `ENV_MODE` via the deployment environment (e.g., `fly.toml`'s `[env]` section).
11. **Testing - Organize Test Code:**
    *   **Action:** Move commented-out test code from `run.py` to the `tests/` directory.
    *   **Reason:** Improves code organization. Review overall test coverage.

**Low Priority:**

12. **Performance - Optimize Billing Checks (`run.py`):**
    *   **Action:** Evaluate if the billing check needs to run on *every* iteration.
    *   **Reason:** Potential minor performance gain.
    *   **Implementation:** Implement checks based on time elapsed or number of tokens processed if appropriate.
13. **Documentation - Correct `WebSearchTool` Docstring:**
    *   **Action:** Update the class docstring to mention Tavily API instead of Exa API.
14. **Code Quality - Review Commented-Out Browser Actions (`sb_browser_tool.py`):**
    *   **Action:** Determine the status of commented-out actions (`search_google`, `open_tab`, `extract_content`). Remove or implement them.
15. **Deployment - Optimize Docker Image:**
    *   **Action:** Implement multi-stage builds and add a `.dockerignore` file.
    *   **Reason:** Reduces final image size and build time.
