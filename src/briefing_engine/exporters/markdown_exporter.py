"""Markdown Exporter: Renders PresentationDeck to high-grade structured markdown."""

from briefing_engine.models.presentation import PresentationDeck


class MarkdownDeckExporter:
    """Serializes a PresentationDeck into readable, slide-delimited Markdown."""

    @staticmethod
    def export(deck: PresentationDeck) -> str:
        output = [
            f"# {deck.title}",
            f"**{deck.subtitle}**",
            f"*Theme: `{deck.theme}` | Total Cards: {deck.total_cards()}*",
            "\n---\n"
        ]

        for i, card in enumerate(deck.cards, 1):
            output.append(f"<!-- Slide {i}: Layout={card.layout.value} -->")
            output.append(card.to_gamma_markdown())
            output.append("\n---\n")

        return "\n".join(output)
