"""Data models for Gamma cards, slide layouts, and presentation decks."""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Any, Optional


class CardLayout(str, Enum):
    """Layout types mapping to Gamma presentation card structures."""
    TITLE_HERO = "title_hero"
    EXECUTIVE_SUMMARY = "executive_summary"
    METRIC_GRID = "metric_grid"
    TWO_COLUMN = "two_column"
    THREE_COLUMN = "three_column"
    TIMELINE_ROADMAP = "timeline_roadmap"
    RISK_MATRIX = "risk_matrix"
    RECOMMENDATION = "recommendation"
    APPENDIX = "appendix"


@dataclass
class StatCallout:
    """A highlighted metric callout box inside a Gamma card."""
    label: str
    value: str
    change_text: str = ""
    status: str = "neutral"  # positive, warning, negative, neutral


@dataclass
class GammaCard:
    """A single card in a Gamma deck with rich formatting and layout rules."""
    card_id: str
    title: str
    subtitle: Optional[str] = None
    layout: CardLayout = CardLayout.EXECUTIVE_SUMMARY
    bullets: List[str] = field(default_factory=list)
    stats: List[StatCallout] = field(default_factory=list)
    callout_box: Optional[str] = None
    table_data: Optional[Dict[str, Any]] = None
    speaker_notes: Optional[str] = None
    accent_color: str = "indigo"

    def to_gamma_markdown(self) -> str:
        """Render card content in Gamma-compatible Markdown card blocks."""
        lines = [f"## {self.title}"]
        if self.subtitle:
            lines.append(f"*{self.subtitle}*\n")

        if self.stats:
            stat_line = " | ".join([f"**{s.value}** ({s.label})" for s in self.stats])
            lines.append(f"> 📊 {stat_line}\n")

        if self.callout_box:
            lines.append(f"> 💡 **Key Takeaway**: {self.callout_box}\n")

        for bullet in self.bullets:
            lines.append(f"- {bullet}")

        if self.speaker_notes:
            lines.append(f"\n<!-- notes: {self.speaker_notes} -->")

        return "\n".join(lines)


@dataclass
class PresentationDeck:
    """Complete presentation structure ready for export to Gamma API / MCP."""
    title: str
    subtitle: str
    theme: str = "enterprise_dark"  # or 'modern_light', 'boardroom'
    author: str = "Enterprise AI Executive Briefing Engine"
    cards: List[GammaCard] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def total_cards(self) -> int:
        return len(self.cards)

    def to_gamma_payload(self) -> Dict[str, Any]:
        """Convert deck to standard Gamma API / MCP generation payload."""
        cards_md = "\n\n---\n\n".join([card.to_gamma_markdown() for card in self.cards])
        return {
            "title": self.title,
            "theme": self.theme,
            "export_formats": ["pdf", "pptx"],
            "card_count": len(self.cards),
            "markdown_content": cards_md,
            "cards": [
                {
                    "card_id": c.card_id,
                    "title": c.title,
                    "layout": c.layout.value,
                    "bullets_count": len(c.bullets),
                    "stats_count": len(c.stats),
                }
                for c in self.cards
            ]
        }
