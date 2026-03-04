from io import BytesIO
from pathlib import Path

from flask import abort, request, send_file
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

def _resolve_projector_path(filename: str) -> Path:
    base_dir = Path(__file__).resolve().parent.parent
    path = base_dir / filename
    if not path.exists():
        abort(500, description="Projector file not found on server")
    return path


def _position_to_pixels(value: float, maximum: int) -> float:
    # If coordinates are normalized (0..1), scale to pixels; otherwise assume absolute pixels.
    return value * maximum if value <= 1 else value


@api_bp.get("/lightmaps/<int:lightmap_id>/export/pdf")
def export_lightmap_pdf(lightmap_id: int):
    print("="*20)
    lm = Lightmap.query.get(lightmap_id)
    if not lm:
        abort(404, description="Lightmap not found")
    if not lm.background or not lm.background.filename:
        abort(400, description="Lightmap has no background to export")
    

    # Paramètre optionnel z_level
    z_level = request.args.get('z_level')
    if z_level is not None:
        try:
            z_level = int(z_level)
            if z_level < 0 or z_level > 2:
                abort(400, description="z_level parameter must be between 0 and 2")
        except ValueError:
            abort(400, description="Invalid z_level parameter. Must be an integer between 0 and 2.")

    bg_path = _resolve_background_path(lm.background.filename)
    background_img = Image.open(bg_path)
    bg_width, bg_height = background_img.size

    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=(bg_width, bg_height))
    pdf.drawImage(str(bg_path), 0, 0, width=bg_width, height=bg_height)

    def _draw_projector(lp):
        px = _position_to_pixels(lp.x, bg_width)
        py = _position_to_pixels(lp.y, bg_height)
        py = background_img.height - py  # Invert Y axis for PDF coordinates

        # insert projector icon
        proj_icon_path = _resolve_projector_path(lp.projector.filename)
        print(proj_icon_path)

        # Get image dimensions
        proj_img = Image.open(proj_icon_path)
        width, height = proj_img.size
        
        # Apply rotation if angle is set
        if lp.angle != 0:
            pdf.saveState()
            # Translate to center of the image
            center_x = px + width / 2
            center_y = py + height / 2
            pdf.translate(center_x, center_y)
            # Rotate (angle is in degrees)
            pdf.rotate(lp.angle)
            # Draw image centered on rotation point
            pdf.drawImage(str(proj_icon_path), -width / 2, -height / 2, width=width, height=height)
            pdf.restoreState()
        else:
            pdf.drawImage(str(proj_icon_path), px, py, width=width, height=height)
        
        print(width, height)

        if lp.universe and lp.address and lp.channel:
            label = f"{lp.universe}/{lp.address} => {lp.channel}"
        elif lp.channel:
            label = f"{lp.channel}"


        pdf.setFont("Helvetica", 12)
        string_size = pdf.stringWidth(label, "Helvetica", 12)
        label_x = px + width / 2 - string_size / 2
        label_y = py +height + 5
        pdf.setFillColor(colors.white)
        pdf.rect(label_x - 2, label_y - 2, string_size + 4, 14, fill=1, stroke=0)
        pdf.setFillColor(colors.black)
        pdf.drawString(label_x, label_y, label)

        # for each gelatine, draw the name and a little circle with color (at the bottom of the projector)
        if getattr(lp, "gelatines", None):
            for i, g in enumerate(lp.gelatines):
                gel_label = g.number
                gel_string_size = pdf.stringWidth(gel_label, "Helvetica", 10)

                radius = 6

                gel_x = px + width/2 - gel_string_size/2 + radius
                gel_y = py - height +30  + i * 15

                pdf.setFillColor(colors.white)
                pdf.rect(gel_x - 1, gel_y - 2, gel_string_size +3, 13, fill=1, stroke=0)

                pdf.setFillColor(colors.black)
                pdf.setFont("Helvetica", 10)
                pdf.drawString(gel_x, gel_y, gel_label)

                # draw color circle
                circle_x = gel_x - radius - 2
                circle_y = gel_y + 4


                pdf.setFillColor(colors.HexColor(g.hex_color))
                stroke = 1 if g.is_diffuser else 0
                pdf.circle(circle_x, circle_y, radius, stroke=stroke, fill=1)

    for lp in sorted(lm.projectors, key=lambda p: p.z_level):
        if z_level is None or lp.z_level == z_level:
            _draw_projector(lp)

    pdf.showPage()
    pdf.save()
    buffer.seek(0)

    filename = f"Plan de feu - {lm.name}"
    if lm.date:
        filename += f" - {lm.date}"
    
    if z_level is not None:
        if z_level == 0:
            filename += " - Sol"
        elif z_level == 1:
            filename += " - Perroq"
        elif z_level == 2:
            filename += " - Plafond"

    filename += ".pdf"

    return send_file(
        buffer,
        mimetype="application/pdf",
        as_attachment=True,
        download_name=filename,
    )
