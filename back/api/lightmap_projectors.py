from flask import jsonify, request, abort

from models.lightmap import Lightmap
from models.projector import Projector, LightmapProjector
from models.db import db
from . import api_bp


@api_bp.post("/lightmaps/<int:lightmap_id>/projectors")
def add_projector_to_lightmap(lightmap_id: int):
    lm = Lightmap.query.get(lightmap_id)
    if not lm:
        abort(404, description="Lightmap not found")

    payload = request.get_json(silent=True) or {}
    projector_id = payload.get("projector_id")
    label = payload.get("label")
    x = payload.get("x")
    y = payload.get("y")
    z_level = payload.get("z_level", 0)
    angle = payload.get("angle", 0.0)
    size = payload.get("size", 1.0)
    gelatine = payload.get("gelatine")
    mode_id = payload.get("mode_id")
    channel = payload.get("channel")
    universe = payload.get("universe")
    address = payload.get("address")

    if not projector_id:
        abort(400, description="'projector_id' is required")
    if not label:
        abort(400, description="'label' is required")
    if x is None or y is None:
        abort(400, description="'x' and 'y' are required")

    projector = Projector.query.get(projector_id)
    if not projector:
        abort(404, description="Projector not found")

    lm_proj = LightmapProjector(
        label=label,
        projector_id=projector_id,
        lightmap_id=lightmap_id,
        x=x,
        y=y,
        z_level=z_level,
        angle=angle,
        size=size,
        gelatine=gelatine,
        mode_id=mode_id,
        channel=channel,
        universe=universe,
        address=address,
    )
    db.session.add(lm_proj)
    db.session.commit()
    return jsonify(lm_proj.to_dict()), 201


@api_bp.put("/lightmaps/<int:lightmap_id>/projectors/<int:projector_id>")
def update_lightmap_projector(lightmap_id: int, projector_id: int):
    lm = Lightmap.query.get(lightmap_id)
    if not lm:
        abort(404, description="Lightmap not found")

    lm_proj = LightmapProjector.query.filter_by(
        id=projector_id, lightmap_id=lightmap_id
    ).first()
    if not lm_proj:
        abort(404, description="Projector not found in this lightmap")

    payload = request.get_json(silent=True) or {}

    # Update fields if present
    if "label" in payload:
        lm_proj.label = payload["label"]
    if "x" in payload:
        lm_proj.x = payload["x"]
    if "y" in payload:
        lm_proj.y = payload["y"]
    if "z_level" in payload:
        lm_proj.z_level = payload["z_level"]
    if "angle" in payload:
        lm_proj.angle = payload["angle"]
    if "size" in payload:
        lm_proj.size = payload["size"]
    if "gelatine" in payload:
        lm_proj.gelatine = payload["gelatine"]
    if "mode_id" in payload:
        lm_proj.mode_id = payload["mode_id"]
    if "channel" in payload:
        lm_proj.channel = payload["channel"]
    if "universe" in payload:
        lm_proj.universe = payload["universe"]
    if "address" in payload:
        lm_proj.address = payload["address"]

    db.session.commit()
    return jsonify(lm_proj.to_dict())


@api_bp.delete("/lightmaps/<int:lightmap_id>/projectors/<int:projector_id>")
def delete_lightmap_projector(lightmap_id: int, projector_id: int):
    lm = Lightmap.query.get(lightmap_id)
    if not lm:
        abort(404, description="Lightmap not found")

    lm_proj = LightmapProjector.query.filter_by(
        id=projector_id, lightmap_id=lightmap_id
    ).first()
    if not lm_proj:
        abort(404, description="Projector not found in this lightmap")

    db.session.delete(lm_proj)
    db.session.commit()
    return "", 204
