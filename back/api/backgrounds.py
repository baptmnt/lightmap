from flask import jsonify

from models.background import Background
from . import api_bp


@api_bp.get("/backgrounds")
def list_backgrounds():
    backgrounds = Background.query.all()
    return jsonify([b.to_dict() for b in backgrounds])
