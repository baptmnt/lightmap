from io import BytesIO
from pathlib import Path

from flask import abort, send_file
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib import colors

from models.lightmap import Lightmap
from . import api_bp


def _resolve_background_path(filename: str) -> Path:
    base_dir = Path(__file__).resolve().parent.parent
    path = base_dir / filename
    if not path.exists():
        abort(500, description="Background file not found on server")
    return path


def _position_to_pixels(value: float, maximum: int) -> float:
    # If coordinates are normalized (0..1), scale to pixels; otherwise assume absolute pixels.
    return value * maximum if value <= 1 else value


@api_bp.get("/lightmaps/<int:lightmap_id>/export/pdf")
def export_lightmap_pdf(lightmap_id: int):
    lm = Lightmap.query.get(lightmap_id)
    if not lm:
        abort(404, description="Lightmap not found")
    if not lm.background or not lm.background.filename:
        abort(400, description="Lightmap has no background to export")

    bg_path = _resolve_background_path(lm.background.filename)
    background_img = Image.open(bg_path)
    bg_width, bg_height = background_img.size

    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=(bg_width, bg_height))
    pdf.drawImage(str(bg_path), 0, 0, width=bg_width, height=bg_height)

    def _draw_projector(lp):
        px = _position_to_pixels(lp.x, bg_width)
        py = _position_to_pixels(lp.y, bg_height)
        radius = 8
        fill_color = colors.green if lp.projector and getattr(lp.projector, "is_led", False) else colors.red
        pdf.setFillColor(fill_color)
        pdf.circle(px, py, radius, fill=1, stroke=0)

        label = lp.label
        if getattr(lp, "gelatines", None):
            gels = ", ".join(g.number for g in lp.gelatines)
            label = f"{label} ({gels})"

        pdf.setFillColor(colors.black)
        pdf.setFont("Helvetica", 8)
        pdf.drawString(px + radius + 2, py, label)

    for lp in sorted(lm.projectors, key=lambda p: p.z_level):
        _draw_projector(lp)

    pdf.showPage()
    pdf.save()
    buffer.seek(0)

    filename = f"Plan de feu - {lm.name}"
    if lm.date:
        filename += f" - {lm.date}"
    filename += ".pdf"

    return send_file(
        buffer,
        mimetype="application/pdf",
        as_attachment=True,
        download_name=filename,
    )
