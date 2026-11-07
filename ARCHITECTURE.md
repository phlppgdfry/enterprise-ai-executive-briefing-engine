# Technical Architecture: Enterprise AI Executive Briefing Engine

---

## 1. Component Diagram

```text
+-------------------------------------------------------------------------+
|                              CLI LAYER                                  |
|   `briefing run`   |   `briefing mcp-status`   |   `briefing preview`   |
+------------------------------------+------------------------------------+
                                     |
                                     v
+-------------------------------------------------------------------------+
|                         BRIEFING ORCHESTRATOR                           |
|  - Ingestion Coordinator (CSV, JSON, Markdown)                          |
|  - Pipeline Sequencer (BA -> Strategy -> Planner -> QA -> Bridge)       |
+---------+------------------+------------------+-----------------+-------+
          |                  |                  |                 |
          v                  v                  v                 v
   +--------------+   +--------------+   +--------------+  +--------------+
   |   Business   |   |   Strategy   |   | Presentation |  |   Quality    |
   |   Analyst    |   |  Consultant  |   |   Planner    |  |  Assurance   |
   |    Agent     |   |    Agent     |   |    Agent     |  |    Agent     |
   +--------------+   +--------------+   +--------------+  +--------------+
          |                  |                  |                 |
          +------------------+------------------+-----------------+
                                     |
                                     v
+-------------------------------------------------------------------------+
|                              GAMMA BRIDGE                               |
|        Handles protocol routing based on `--provider` flag              |
+-------------------+--------------------+--------------------------------+
                    |                    |
                    v                    v
      +---------------------------+ +----------------------------+
      |      Gamma MCP Client     | |    Gamma REST API Client   |
      |  https://mcp.gamma.app/   | |  https://public-api...     |
      |  JSON-RPC 2.0 over HTTP   | |  v1.0 API-Key / Bearer     |
      +---------------------------+ +----------------------------+
```

---

## 2. Gamma MCP JSON-RPC Specification

Gamma's official MCP endpoint operates over HTTP at `https://mcp.gamma.app/mcp`.

### Tools Schema:

#### 1. `generate_presentation`
```json
{
  "name": "generate_presentation",
  "description": "Generates a complete multi-card presentation from markdown content and layout specifications.",
  "parameters": {
    "type": "object",
    "properties": {
      "title": { "type": "string" },
      "content": { "type": "string", "description": "Markdown formatted presentation content" },
      "theme": { "type": "string", "enum": ["enterprise_dark", "modern_light", "boardroom"] },
      "format": { "type": "string", "default": "presentation" }
    },
    "required": ["title", "content"]
  }
}
```

#### 2. `export_presentation`
```json
{
  "name": "export_presentation",
  "description": "Exports a Gamma presentation to downloadable document formats.",
  "parameters": {
    "type": "object",
    "properties": {
      "presentation_id": { "type": "string" },
      "format": { "type": "string", "enum": ["pdf", "pptx"] }
    },
    "required": ["presentation_id", "format"]
  }
}
```

---

## 3. Gamma Public REST API v1.0 Specification

Base URL: `https://public-api.gamma.app/v1.0`

### Headers:
```http
X-API-KEY: <your-gamma-api-key>
Content-Type: application/json
Accept: application/json
```

### Endpoints:
- `POST /generations`: Dispatches async presentation generation job. Returns `generation_id` and initial status.
- `GET /generations/{id}`: Polls generation progress, status, and generated URL.
- `POST /generations/{id}/export`: Requests PDF or PPTX generation and returns direct CDN download URLs.

---

## 4. Anti-Hallucination & Mathematical Verification Contract

The `QualityAssuranceAgent` enforces a strict mathematical verification rule:
- **Numerical Extraction**: Every numeric literal, percentage, and currency value across all generated cards is extracted via deterministic regex.
- **Reference Catalog Match**: Each number must match either:
  1. An audited primary ledger figure from `bundle.financials` or `bundle.project`.
  2. A verified derived metric from `BusinessAnalystOutput` (e.g., variance, growth rate, ratio).
  3. A known structural identifier (e.g., milestone numbers, card indices, year dates).
- **Threshold**: An audit pass requires `>= 85%` strict numeric verification with `0` critical discrepancies.
