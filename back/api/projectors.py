from flask import jsonify

from models.projector import Projector
from . import api_bp


@api_bp.get("/projectors")
def list_projectors():
    projectors = Projector.query.all()
    return jsonify([p.to_dict() for p in projectors])
