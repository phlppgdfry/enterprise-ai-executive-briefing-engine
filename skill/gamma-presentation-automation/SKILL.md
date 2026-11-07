---
name: gamma-presentation-automation
description: "Orchestrate executive presentations, board decks, and business proposals using the official Gamma MCP server (https://mcp.gamma.app/mcp) and Gamma REST API v1.0. Use when generating, updating, or exporting presentations, slides, documents, or pitches with verified business data and anti-hallucination audit gates."
---

# Gamma Presentation Automation Skill

Use this skill when asked to create, update, or export executive presentations, consulting pitch decks, or roadmaps using **Gamma.app** via its official MCP server or REST API.

## 1. Official Endpoints & Authentication

- **Official Gamma MCP Server**: `https://mcp.gamma.app/mcp`
  - Protocol: JSON-RPC 2.0 over HTTP
  - Supported in: Claude Code, OpenAI Codex, Antigravity, Cursor
  - Transport: OAuth / HTTP transport
- **Official Gamma REST API (v1.0)**: `https://public-api.gamma.app/v1.0/`
  - Authentication: Header `X-API-KEY: <your-key>` or Bearer token

## 2. Core Best Practices

### A. Anti-Hallucination & Numerical Verification
1. **Never allow LLMs to invent financial metrics, client counts, or ROI figures.**
2. When creating a presentation from company data, general ledger, or project logs, explicitly verify:
   - Revenue, margin, and burn rate arithmetic.
   - Project milestone completion percentages.
   - Risk severity and impact owners.
3. If an input data point is absent, mark it as `[UNVERIFIED / DATA_GAP]` instead of extrapolating.

### B. Executive Narrative Structuring (Pyramid Principle)
Organize C-level presentations strictly according to the Pyramid Principle:
- **Card 1: Title Hero**: Objective, period, and governance context.
- **Card 2: Executive Summary**: Core thesis (Situation -> Complication -> Resolution).
- **Card 3: Audited KPI Dashboard**: Top 4 visual stat cards + metric provenance table.
- **Card 4: Delivery Roadmap**: Milestones, status indicators (✅, 🔄, ⏳), completion %.
- **Card 5: Risk Governance**: Risk register with impact, likelihood, and mitigation.
- **Card 6: Strategic Pillars**: 3 focused value drivers aligned with growth targets.
- **Card 7: Board Decisions**: Clear motions for executive sign-off and approval.
- **Card 8: Appendix / Data Lineage**: Audit trail and source reconciliation manifest.

## 3. Gamma Card Format Guidelines

Gamma cards render Markdown cleanly. Use the following formatting for optimal visual cards:

```markdown
## Slide Title
*Optional Subtitle or Context*

> 📊 **€1.95M** (Revenue) | **78.5%** (Gross Margin) | **21.8 mo** (Cash Runway)

> 💡 **Key Takeaway**: Concise, high-impact executive insight.

- **Primary Driver**: Specific verifiable action item.
- **Secondary Driver**: Operational metric.

<!-- notes: Speaker notes for the presenter. -->
```

## 4. Local CLI & Repository Reference

For automated end-to-end execution, use the local engine:
```bash
python3 /Users/philippegodfroy/enterprise-ai-executive-briefing-engine/src/briefing_engine/cli.py run \
  --csv <path-to-financials.csv> \
  --project <path-to-project.json> \
  --provider [mock|api|mcp]
```
