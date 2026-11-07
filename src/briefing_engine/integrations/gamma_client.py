"""Official Gamma REST API Client: Connects to https://public-api.gamma.app/v1.0/"""

import os
import time
import json
import urllib.request
import urllib.error
from typing import Dict, Any, Optional


class GammaApiClient:
    """Production-grade client for Gamma's Public REST API."""

    BASE_URL = "https://public-api.gamma.app/v1.0"

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GAMMA_API_KEY", "")

    def _headers(self) -> Dict[str, str]:
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        if self.api_key:
            headers["X-API-KEY"] = self.api_key
        return headers

    def create_generation(self, prompt_or_markdown: str, theme: str = "enterprise_dark") -> Dict[str, Any]:
        """Trigger an asynchronous generation job in Gamma."""
        url = f"{self.BASE_URL}/generations"
        payload = {
            "prompt": prompt_or_markdown,
            "format": "presentation",
            "theme": theme,
            "text_mode": "markdown"
        }

        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers=self._headers(),
            method="POST"
        )

        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            error_body = e.read().decode("utf-8")
            return {
                "error": True,
                "status_code": e.code,
                "message": f"Gamma API error {e.code}: {error_body}"
            }
        except Exception as ex:
            return {
                "error": True,
                "message": str(ex)
            }

    def get_generation_status(self, generation_id: str) -> Dict[str, Any]:
        """Poll the status of an ongoing generation."""
        url = f"{self.BASE_URL}/generations/{generation_id}"
        req = urllib.request.Request(url, headers=self._headers(), method="GET")

        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except Exception as ex:
            return {"error": True, "message": str(ex)}

    def export_deck(self, generation_id: str, export_format: str = "pdf") -> Dict[str, Any]:
        """Trigger PDF or PPTX export for a completed Gamma deck."""
        url = f"{self.BASE_URL}/generations/{generation_id}/export"
        payload = {"format": export_format}

        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers=self._headers(),
            method="POST"
        )

        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except Exception as ex:
            return {"error": True, "message": str(ex)}
