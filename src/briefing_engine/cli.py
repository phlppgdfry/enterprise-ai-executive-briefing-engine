"""Command Line Interface for the Enterprise AI Executive Briefing Engine."""

import argparse
import sys
import os
from pathlib import Path

# Ensure src root is in sys.path when invoked directly
_SRC_DIR = Path(__file__).resolve().parent.parent
if str(_SRC_DIR) not in sys.path:
    sys.path.insert(0, str(_SRC_DIR))

from briefing_engine.orchestrator import BriefingOrchestrator
from briefing_engine.integrations.gamma_mcp import GammaMcpClient


def print_banner():
    banner = """
========================================================================
   🚀 ENTERPRISE AI EXECUTIVE BRIEFING ENGINE  (Gamma MCP / API)
   Automated Multi-Agent Presentation & Mathematical KPI Assurance
========================================================================
"""
    print(banner)


def cmd_run(args):
    """Execute end-to-end multi-agent pipeline."""
    print_banner()
    print(f"[*] Ingesting enterprise datasets...")
    print(f"    - Financials CSV: {args.csv}")
    print(f"    - Project JSON:   {args.project}")
    print(f"    - Repo Brief MD:  {args.repo}")
    print(f"    - Transport:      {args.provider.upper()}\n")

    orchestrator = BriefingOrchestrator(provider=args.provider, api_key=args.api_key)
    bundle = orchestrator.load_bundle_from_files(
        csv_path=args.csv,
        json_path=args.project,
        md_path=args.repo
    )

    print("[*] Running Business Analyst Agent (KPI reconciliation)...")
    print("[*] Running Strategy Consultant Agent (Pyramid Principle structuring)...")
    print("[*] Running Presentation Planner Agent (Gamma card blueprinting)...")
    print("[*] Running Quality Assurance Agent (Anti-hallucination audit gate)...")

    results = orchestrator.execute_pipeline(bundle)
    audit = results["audit_report"]
    analysis = results["analysis"]
    deck = results["deck"]
    publish = results["publish_result"]

    print("\n----------------- 📊 AUDIT & KPI REPORT -----------------")
    print(f"Operational Health Score:  {analysis.operational_health_score}/100")
    print(f"Audited Metrics Count:     {len(analysis.kpis)}")
    print(f"Claims Verified:           {audit.verified_claims_count}/{audit.total_claims_audited} ({audit.audit_score_pct}%)")
    print(f"Audit Gate Status:         {audit.summary_status()}")

    print("\n----------------- 🎨 GAMMA PRESENTATION DECK ------------")
    print(f"Deck Title:                {deck.title}")
    print(f"Total Cards Generated:     {deck.total_cards()}")
    print(f"Target Theme:              {deck.theme}")

    if publish.get("url"):
        print(f"Gamma Online Deck URL:     {publish['url']}")
    if publish.get("export_urls"):
        print(f"PDF Export Download:       {publish['export_urls'].get('pdf')}")
        print(f"PPTX Export Download:      {publish['export_urls'].get('pptx')}")

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    md_file = out_dir / "executive_briefing.md"
    html_file = out_dir / "executive_briefing.html"

    md_file.write_text(results["markdown"], encoding="utf-8")
    html_file.write_text(results["html"], encoding="utf-8")

    print(f"\n[+] Artifacts successfully exported:")
    print(f"    - Markdown Deck: {md_file}")
    print(f"    - Interactive HTML Preview: {html_file}")
    print("---------------------------------------------------------\n")


def cmd_mcp_status(args):
    """Check connectivity to the official Gamma MCP endpoint."""
    print_banner()
    print("[*] Checking Gamma MCP server status at https://mcp.gamma.app/mcp ...")
    client = GammaMcpClient()
    res = client.list_tools()

    if res.get("error"):
        if res.get("requires_auth"):
            print("[-] HTTP 401: OAuth authentication required by Gamma MCP server.")
            print("[+] Endpoint is active and accepting connections!")
            print("[i] In Claude Code / Codex, authorization will prompt on first use.")
        else:
            print(f"[-] MCP Error: {res.get('message')}")
    else:
        print("[+] Successfully connected to Gamma MCP server!")
        print(f"[+] Server Response: {res}")


def main():
    parser = argparse.ArgumentParser(
        description="Enterprise AI Executive Briefing Engine - Multi-agent Gamma generator."
    )
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # 'run' subcommand
    run_parser = subparsers.add_parser("run", help="Execute complete briefing generation")
    run_parser.add_argument("--csv", default="data/sample_financial_kpis.csv", help="Path to financial CSV")
    run_parser.add_argument("--project", default="data/sample_project_status.json", help="Path to project JSON")
    run_parser.add_argument("--repo", default="data/sample_github_repo_brief.md", help="Path to repo markdown")
    run_parser.add_argument("--provider", default="mock", choices=["mock", "api", "mcp"], help="Generation transport")
    run_parser.add_argument("--api-key", default="", help="Gamma API Key (or set GAMMA_API_KEY)")
    run_parser.add_argument("--out", default="output", help="Directory for exported artifacts")

    # 'mcp-status' subcommand
    subparsers.add_parser("mcp-status", help="Test connectivity to Gamma MCP server")

    args = parser.parse_args()

    if not args.command or args.command == "run":
        # Default to run if no subcommand given
        if not hasattr(args, "csv"):
            args.csv = "data/sample_financial_kpis.csv"
            args.project = "data/sample_project_status.json"
            args.repo = "data/sample_github_repo_brief.md"
            args.provider = "mock"
            args.api_key = ""
            args.out = "output"
        cmd_run(args)
    elif args.command == "mcp-status":
        cmd_mcp_status(args)


if __name__ == "__main__":
    main()
