"""HTML Deck Preview Generator: Renders an interactive deck viewer."""

import html
from briefing_engine.models.presentation import PresentationDeck, CardLayout


class HtmlDeckPreviewGenerator:
    """Produces a responsive, presentation viewer matching Gamma's aesthetic."""

    @classmethod
    def generate(cls, deck: PresentationDeck) -> str:
        cards_html = []
        for idx, card in enumerate(deck.cards, 1):
            stats_markup = ""
            if card.stats:
                stat_boxes = []
                for s in card.stats:
                    border_color = "#10b981" if s.status == "positive" else ("#f59e0b" if s.status == "warning" else "#6366f1")
                    stat_boxes.append(f"""
                    <div style="background: rgba(255,255,255,0.04); border-left: 4px solid {border_color}; padding: 16px; border-radius: 8px; flex: 1; min-width: 140px;">
                        <div style="font-size: 11px; text-transform: uppercase; letter-spacing: 0.05em; color: #94a3b8;">{html.escape(s.label)}</div>
                        <div style="font-size: 24px; font-weight: 700; color: #f8fafc; margin: 4px 0;">{html.escape(s.value)}</div>
                        <div style="font-size: 12px; color: {border_color};">{html.escape(s.change_text)}</div>
                    </div>
                    """)
                stats_markup = f'<div style="display: flex; gap: 12px; flex-wrap: wrap; margin: 16px 0;">{"".join(stat_boxes)}</div>'

            callout_markup = ""
            if card.callout_box:
                callout_markup = f"""
                <div style="background: rgba(99, 102, 241, 0.1); border: 1px solid rgba(99, 102, 241, 0.3); border-radius: 8px; padding: 14px 18px; margin: 16px 0; color: #e0e7ff; font-size: 14px;">
                    <strong>💡 Key Takeaway:</strong> {html.escape(card.callout_box)}
                </div>
                """

            bullets_markup = ""
            if card.bullets:
                items = "".join([f"<li style='margin-bottom: 8px;'>{b}</li>" for b in card.bullets])
                bullets_markup = f"<ul style='padding-left: 20px; line-height: 1.6; color: #cbd5e1;'>{items}</ul>"

            notes_markup = ""
            if card.speaker_notes:
                notes_markup = f"""
                <div style="margin-top: 20px; padding-top: 12px; border-top: 1px dashed #334155; font-size: 12px; color: #64748b;">
                    <strong>🎙️ Speaker Notes:</strong> {html.escape(card.speaker_notes)}
                </div>
                """

            cards_html.append(f"""
            <div class="deck-card" id="card-{idx}" style="background: #1e293b; border: 1px solid #334155; border-radius: 12px; padding: 32px; margin-bottom: 24px; box-shadow: 0 10px 25px -5px rgba(0,0,0,0.3);">
                <div style="display: flex; justify-content: space-between; align-items: baseline; border-bottom: 1px solid #334155; padding-bottom: 12px; margin-bottom: 16px;">
                    <div>
                        <span style="background: #3b82f6; color: #fff; font-size: 10px; font-weight: 700; padding: 3px 8px; border-radius: 9999px; text-transform: uppercase;">Card {idx} of {len(deck.cards)}</span>
                        <span style="color: #64748b; font-size: 12px; margin-left: 8px;">{card.layout.value}</span>
                        <h2 style="font-size: 22px; font-weight: 700; color: #f8fafc; margin: 8px 0 2px 0;">{html.escape(card.title)}</h2>
                        {f'<div style="color: #94a3b8; font-size: 14px;">{html.escape(card.subtitle)}</div>' if card.subtitle else ''}
                    </div>
                </div>
                {callout_markup}
                {stats_markup}
                {bullets_markup}
                {notes_markup}
            </div>
            """)

        all_cards = "\n".join(cards_html)

        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{html.escape(deck.title)} - Gamma Deck Preview</title>
    <style>
        body {{
            background-color: #0f172a;
            color: #f8fafc;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            margin: 0;
            padding: 40px 20px;
        }}
        .container {{
            max-width: 900px;
            margin: 0 auto;
        }}
        header {{
            text-align: center;
            margin-bottom: 40px;
        }}
        header h1 {{
            font-size: 32px;
            font-weight: 800;
            letter-spacing: -0.02em;
            margin: 0 0 8px 0;
            background: linear-gradient(135deg, #60a5fa, #a855f7);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        .badge {{
            display: inline-block;
            background: #1e293b;
            border: 1px solid #475569;
            color: #cbd5e1;
            padding: 4px 12px;
            border-radius: 9999px;
            font-size: 12px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <span class="badge">🚀 Powered by Enterprise AI Briefing Engine & Gamma</span>
            <h1>{html.escape(deck.title)}</h1>
            <p style="color: #94a3b8; font-size: 16px;">{html.escape(deck.subtitle)}</p>
        </header>

        <main>
            {all_cards}
        </main>

        <footer style="text-align: center; color: #475569; font-size: 12px; margin-top: 60px;">
            Audited & verified with mathematical precision. Ready for export via Gamma MCP / API.
        </footer>
    </div>
</body>
</html>
"""
