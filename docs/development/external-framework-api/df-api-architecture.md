## 4. API Specifications

### 4.1 Event Schemas

```typescript
// Core event types
interface Event {
  id: string;
  type: string;
  timestamp: string;
  sequence: number;
  payload: any;
  source: string;
  correlation_id?: string;
}

// Code analysis events
interface CodeAnalysisRequestedEvent {
  file_path: string;
  related_files?: string[];
  analysis_type?: string;
  options?: {
    include_dependencies?: boolean;
    include_documentation?: boolean;
    include_complexity_metrics?: boolean;
    include_security_checks?: boolean;
  };
}

interface CodeAnalysisCompletedEvent {
  context_id: string;
  analysis_id: string;
  file_path: string;
  summary: string;
  components: number;
  related_files: string[];
}

// Implementation events
interface ImplementationRequestedEvent {
  description: string;
  file_path?: string;
  related_files?: string[];
  constraints?: {
    language: string;
    style_guide?: string;
    max_complexity?: number;
  };
}

interface ImplementationCompletedEvent {
  implementation_id: string;
  file_path: string;
  changes: {
    created: boolean;
    modified: boolean;
    diff?: string;
  };
  summary: string;
}

// Test generation events
interface TestGenerationRequestedEvent {
  file_path: string;
  test_type: "unit" | "integration" | "e2e";
  options?: {
    framework?: string;
    coverage_target?: number;
    include_edge_cases?: boolean;
  };
}

interface TestGenerationCompletedEvent {
  test_id: string;
  test_file_path: string;
  coverage_estimate: number;
  test_count: number;
  summary: string;
}

// Documentation events
interface DocumentationRequestedEvent {
  file_path: string;
  doc_type: "function" | "class" | "module" | "readme" | "api";
  options?: {
    format?: string;
    include_examples?: boolean;
    audience?: string;
  };
}

interface DocumentationCompletedEvent {
  doc_id: string;
  file_path: string;
  generated_files?: string[];
  summary: string;
}

// HITL events
interface HITLRequestEvent {
  request_id: string;
  request_type: "approval" | "feedback" | "selection" | "information";
  description: string;
  options?: string[];
  context: any;
  timeout_seconds?: number;
}

interface HITLResponseEvent {
  request_id: string;
  response: any;
  notes?: string;
  responded_by: string;
}

// Workflow events
interface WorkflowStartEvent {
  workflow_id: string;
  context: any;
}

interface WorkflowCompletedEvent {
  workflow_id: string;
  instance_id: string;
  context: any;
}

interface WorkflowFailedEvent {
  workflow_id: string;
  instance_id: string;
  error: string;
}
```

### 4.2 REST API

```
# DevFlow REST API Endpoints

Base URL: http://localhost:8080/api/v1

## Workflows

GET /workflows
- Get list of available workflow definitions

POST /workflows/start
- Start a new workflow
- Body: { workflow_id: string, context: object }
- Returns: { instance_id: string }

GET /workflows/instances
- Get all workflow instances

GET /workflows/instances/{instance_id}
- Get details of a specific workflow instance

## Code Analysis

POST /code/analyze
- Request code analysis
- Body: { file_path: string, related_files?: string[], options?: object }
- Returns: { context_id: string }

GET /code/analysis/{context_id}
- Get analysis results
- Returns: { file_path: string, analysis: object }

## Implementation

POST /code/implement
- Request code implementation
- Body: { description: string, file_path?: string, constraints?: object }
- Returns: { implementation_id: string }

GET /code/implementation/{implementation_id}
- Get implementation results
- Returns: { file_path: string, changes: object }

## Testing

POST /code/generate-tests
- Request test generation
- Body: { file_path: string, test_type: string, options?: object }
- Returns: { test_id: string }

GET /code/tests/{test_id}
- Get generated tests
- Returns: { test_file_path: string, tests: object }

## Documentation

POST /code/document
- Request documentation generation
- Body: { file_path: string, doc_type: string, options?: object }
- Returns: { doc_id: string }

GET /code/documentation/{doc_id}
- Get generated documentation
- Returns: { files: object }

## HITL (Human-in-the-Loop)

GET /hitl/requests
- Get pending HITL requests

GET /hitl/requests/{request_id}
- Get details of a specific HITL request

POST /hitl/requests/{request_id}/respond
- Respond to a HITL request
- Body: { response: any, notes?: string }

## System

GET /system/status
- Get system status
- Returns: { status: string, agents: object, active_workflows: number }

GET /system/metrics
- Get system metrics
- Returns: { event_count: number, workflow_metrics: object, agent_metrics: object }


----

## API Overview

The DevFlow API is built with FastAPI and provides endpoints for managing workflows, code analysis, test generation, and collaborative reviews. All endpoints are served from the base URL and require proper authentication for secured operations.

## Authentication and Authorization
As of Sprint 3, all endpoints related to collaborative reviews require JWT-based authentication. Use the `Authorization: Bearer <token>` header for requests.

- **Obtaining a Token:** Tokens are generated via an authentication service (not covered in this API). Ensure your token includes a `sub` claim with the username.
- **Example:** Include the token in requests to protected endpoints like `/api/reviews/start`.

## Endpoints

### 1. Root Endpoint
- **GET /**: Returns API status.
  - Response: {"name": "DevFlow API", "version": "0.1.0", "status": "running"}

### 2. Code Analysis
- **POST /api/code/analyze**: Analyze code files.
  - Request Body: { "file_path": "string", "related_files": ["list"], "analysis_type": "string", "options": {} }
  - Response: Analysis results.

### 3. Test Generation
- **POST /api/code/tests**: Generate tests for code.
  - Request Body: { "file_path": "string", "test_type": "string", "framework": "string", "options": {} }
  - Response: Test generation details.

### 4. Code Implementation
- **POST /api/code/implement**: Implement code based on description.
  - Request Body: { "description": "string", "file_path": "string", "language": "string", "related_files": ["list"], "constraints": {} }
  - Response: Implementation results.

### 5. Documentation Generation
- **POST /api/code/document**: Generate documentation.
  - Request Body: { "file_path": "string", "doc_type": "string", "options": {} }
  - Response: Documentation results.

### 6. Workflow Management
- **POST /api/workflows/start**: Start a workflow.
  - Request Body: { "workflow_id": "string", "context": {} }
  - Response: { "instance_id": "string" }

### 7. Collaborative Review Endpoints (New in Sprint 3)
- **POST /api/reviews/start**: Start a new review workflow.
  - Request Body: { "workflow_id": "string", "context": {} }
  - Requires Authentication.
  - Response: { "instance_id": "string" or "review_id": "string" }

- **POST /api/reviews/{review_id}/comments**: Submit a comment to a review.
  - Request Body: { "comment": "string", "file_path": "string" }
  - Requires Authentication.
  - Response: { "comment_id": "string" }

- **POST /api/reviews/{review_id}/vote**: Cast a vote on a review.
  - Request Body: { "vote": true/false }
  - Requires Authentication.
  - Response: { "status": "vote cast successfully" }

## Integration with Existing Components
The API integrates with the event bus, state manager, and agents. For example, review endpoints publish events to the event bus for processing.

## Usage Examples
- **Starting a Review:**
  ```
  curl -X POST http://localhost:8000/api/reviews/start \
  -H "Authorization: Bearer your-jwt-token" \
  -H "Content-Type: application/json" \
  -d '{"workflow_id": "test_workflow", "context": {"participants": ["user1", "user2"]}}'
  ```

- **Submitting a Comment:**
  ```
  curl -X POST http://localhost:8000/api/reviews/{review_id}/comments \
  -H "Authorization: Bearer your-jwt-token" \
  -H "Content-Type: application/json" \
  -d '{"comment": "This needs review", "file_path": "path/to/file.py"}'
  ```


----

