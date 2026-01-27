from flask import jsonify, request

from models.gelatine import Gelatine
from . import api_bp


@api_bp.get("/gelatines")
def list_gelatines():
    query = Gelatine.query
    
    # Filtre optionnel par is_diffuser
    is_diffuser = request.args.get('is_diffuser')
    if is_diffuser is not None:
        is_diffuser_bool = is_diffuser.lower() in ('true', '1', 'yes')
        query = query.filter_by(is_diffuser=is_diffuser_bool)
    
    gelatines = query.all()
    return jsonify([g.to_dict() for g in gelatines])
