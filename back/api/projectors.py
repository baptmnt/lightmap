from flask import jsonify, request

from models.projector import Projector
from . import api_bp


@api_bp.get("/projectors")
def list_projectors():
    query = Projector.query
    
    # Filtre optionnel par is_led
    is_led = request.args.get('is_led')
    if is_led is not None:
        is_led_bool = is_led.lower() in ('true', '1', 'yes')
        query = query.filter_by(is_led=is_led_bool)
    
    projectors = query.all()
    return jsonify([p.to_dict() for p in projectors])
