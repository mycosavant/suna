# Key Findings & Observations

## Agent Persona & Capabilities
- Defines the agent ("suna.so") as autonomous, capable of complex tasks
- Uses specified Linux environment (`/workspace`), file system, terminal, browser, data providers, and web search

## Environment & Tools
- **CLI tools**: grep, jq, pdftotext, etc.
- **Runtimes**: Python 3.11, Node 20
- **Permissions**: Explicitly mentions sudo privileges
- **Path requirements**: Mandates relative paths within `/workspace`

## Methodology & Best Practices

### Tool Preference
- Strongly prefers CLI tools over Python scripts for efficiency
- Especially for file/text/system operations

### CLI Usage
- Provides detailed guidance on:
    - Using sessions
    - Background processes (`&`, `nohup`)
    - Command chaining (`&&`, `|`)
    - Output redirection
    - Avoiding blocking/interactive commands

### Coding
- Mandates saving code to files
- Uses search for unknowns
- Specific advice for HTML/CSS creation order
- Guidelines for image sourcing

### Deployment
- Restricts deploy tool usage to explicit user requests
- Requires confirmation via `ask`

### Data Verification (CRITICAL)
- Never assumes or hallucinates data
- Always extract, save, verify, and use only verified data
- Use `ask` if verification fails

### Data Providers
- Encourages using specific data providers (LinkedIn, Zillow, etc.)
- Prefers providers over generic web scraping when available

## Workflow (todo.md System)
- Mandates strict workflow centered around a todo.md file
- Agent must:
    - Create this file
    - Break down tasks
    - Work through them sequentially
    - Consult it before every action
    - Mark progress (`[ ]` -> `[x]`)
    - Use `complete` or `ask` immediately upon finishing all tasks
- Includes rule to `ask` if stuck (3 todo.md updates without task completion)

## Communication Protocol

### Narrative Updates
- Requires frequent, Markdown-formatted narrative updates within responses
- Non-blocking explanations of actions and reasoning

### ask Tool
- Restricted to essential user input (clarification, confirmation)
- BLOCKS execution

### complete Tool
- Used only when all todo.md tasks are done
- Terminates execution

### Attachments
- Mandates attaching ALL visual/viewable files when using `ask`
- Includes HTML, PDF, MD, images, charts

## Content Creation
- Specifies detailed writing style (paragraphs, long-form unless specified, citations)
- Design workflow (HTML+CSS first, print-friendly, PDF output)

## Completion
- Extremely strict rules about using `complete` or `ask` immediately after the last task
- No extra steps allowed after todo.md completion

## Overall Assessment
The prompt is highly detailed and prescriptive, defining a specific persona, a strict workflow (todo.md), clear communication rules, and strong emphasis on data verification. The rigidity of the todo.md system and completion rules are notable. The availability of sudo is a key security point for the sandbox.