# Repository Technical Brief: PortOps-AI Core Engine

## 1. Product Overview
PortOps-AI is a next-generation terminal logistics intelligence platform designed to optimize berth allocation, container crane routing, and gate scheduling in international deep-sea container terminals.

## 2. Architecture & Tech Stack
- **Backend Core**: Python 3.14 + FastAPI + AsyncIO microservices
- **Mathematical Optimization Engine**: OR-Tools mixed-integer linear programming (MILP)
- **Data Streaming**: Apache Kafka + DuckDB + ClickHouse for sub-second analytical aggregations
- **AI / Agent Layer**: LangGraph + Gamma API presentation exporter + Pydantic data validation
- **Frontend / Telemetry**: Next.js 15 + Tailwind CSS + Mapbox GL terminal digital twin

## 3. Engineering Metrics & Code Quality
- **Repository Size**: 48,500 LOC
- **Unit & Integration Test Coverage**: 94.6% across 382 test cases
- **CI/CD Pipeline Status**: Passing (GitHub Actions macOS / Linux dual-target)
- **Average API Latency**: 42ms p95 on container telemetry queries
- **Open PRs**: 2 (Peer review in progress)
- **Zero Critical Vulnerabilities**: Snyk & Dependabot clean audit

## 4. Business Value Propositions
- Reduces vessel idle berth time by 18.4 hours per call.
- Lowers carbon emissions from drayage trucks by 24% through automated gate flow balancing.
- Proven ROI within 4.5 months of pilot deployment at Port of Antwerp-Bruges trial terminal.
