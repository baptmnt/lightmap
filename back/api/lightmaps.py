from datetime import date

from flask import jsonify, request, abort

from models.lightmap import Lightmap
from models.background import Background
from models.db import db
from . import api_bp


def _parse_date(value):
    if value in (None, ""):
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        abort(400, description="Invalid date format, expected YYYY-MM-DD")


@api_bp.post("/lightmaps")
def create_lightmap():
    payload = request.get_json(silent=True) or {}
    print(request.get_json())
    name = payload.get("name")
    background_id = payload.get("background_id")
    raw_date = payload.get("date")

    if not name:
        abort(400, description="'name' is required")
    if not background_id:
        abort(400, description="'background_id' is required")

    background = Background.query.get(background_id)
    if not background:
        abort(404, description="Background not found")

    lm = Lightmap(
        name=name,
        date=_parse_date(raw_date),
        background=background,
    )
    db.session.add(lm)
    db.session.commit()
    return jsonify({"redirect": f"/lightmaps/{lm.id}"}), 201


@api_bp.get("/lightmaps")
def list_lightmaps():
    lightmaps = Lightmap.query.order_by(Lightmap.id).all()
    return jsonify([lm.to_summary() for lm in lightmaps])


@api_bp.get("/lightmaps/<int:lightmap_id>")
def get_lightmap(lightmap_id: int):
    lm = Lightmap.query.get(lightmap_id)
    if not lm:
        abort(404, description="Lightmap not found")
    return jsonify(lm.to_dict())
