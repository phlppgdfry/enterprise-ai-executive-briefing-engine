"""Mock Gamma Simulator: Provides deterministic offline execution without consuming credits."""

import uuid
from typing import Dict, Any


class MockGammaService:
    """Simulates Gamma Public API and MCP behavior deterministically."""

    def __init__(self):
        self.generations: Dict[str, Dict[str, Any]] = {}

    def create_generation(self, prompt: str, theme: str = "enterprise_dark") -> Dict[str, Any]:
        gen_id = f"mock-gamma-{uuid.uuid4().hex[:8]}"
        record = {
            "id": gen_id,
            "status": "COMPLETED",
            "progress": 100,
            "title": "Executive Briefing Deck",
            "url": f"https://gamma.app/docs/{gen_id}",
            "theme": theme,
            "created_at": "2026-11-07T03:55:00Z",
            "export_urls": {
                "pdf": f"https://gamma.app/export/{gen_id}/presentation.pdf",
                "pptx": f"https://gamma.app/export/{gen_id}/presentation.pptx"
            }
        }
        self.generations[gen_id] = record
        return record

    def get_generation_status(self, gen_id: str) -> Dict[str, Any]:
        return self.generations.get(gen_id, {
            "error": True,
            "message": f"Generation {gen_id} not found."
        })

    def export_deck(self, gen_id: str, export_format: str = "pdf") -> Dict[str, Any]:
        if gen_id not in self.generations:
            return {"error": True, "message": f"Generation {gen_id} not found."}
        return {
            "generation_id": gen_id,
            "format": export_format,
            "status": "READY",
            "download_url": f"https://gamma.app/export/{gen_id}/presentation.{export_format}"
        }
