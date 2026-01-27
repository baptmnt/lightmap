"""Seed database from JSON files in data/ directory."""

from __future__ import annotations

import json
from pathlib import Path

from app import app
from models.db import db
from models.projector import Projector
from models.background import Background
from models.gelatine import Gelatine

DATA_DIR = Path(__file__).parent / "data"


def _load_json(filename: str):
    path = DATA_DIR / filename
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def seed_projectors() -> tuple[int, int]:
    records = _load_json("projectors.json")
    inserted = 0
    updated = 0
    for payload in records:
        name = payload["name"]
        proj = Projector.query.filter_by(name=name).first()
        if proj:
            proj.filename = payload.get("filename")
            proj.size = payload.get("size")
            updated += 1
            continue
        proj = Projector(
            name=name,
            filename=payload.get("filename"),
            size=payload.get("size"),
        )
        db.session.add(proj)
        inserted += 1
    db.session.commit()
    return inserted, updated


def seed_backgrounds() -> tuple[int, int]:
    records = _load_json("backgrounds.json")
    inserted = 0
    updated = 0
    for payload in records:
        name = payload["name"]
        bg = Background.query.filter_by(name=name).first()
        if bg:
            bg.filename = payload.get("filename")
            updated += 1
            continue
        bg = Background(
            name=name,
            filename=payload.get("filename"),
        )
        db.session.add(bg)
        inserted += 1
    db.session.commit()
    return inserted, updated


def seed_gelatines() -> tuple[int, int]:
    records = _load_json("gelatines.json")
    inserted = 0
    updated = 0
    for payload in records:
        number = payload["number"]
        gel = Gelatine.query.filter_by(number=number).first()
        if gel:
            gel.name = payload.get("name")
            gel.hex_color = payload.get("hex_color")
            gel.is_diffuser = payload.get("is_diffuser", False)
            updated += 1
            continue
        gel = Gelatine(
            number=number,
            name=payload.get("name"),
            hex_color=payload.get("hex_color"),
            is_diffuser=payload.get("is_diffuser", False),
        )
        db.session.add(gel)
        inserted += 1
    db.session.commit()
    return inserted, updated


def run():
    with app.app_context():
        inserted, updated = seed_projectors()
        print(f"Projectors: inserted={inserted}, updated={updated}")
        inserted, updated = seed_backgrounds()
        print(f"Backgrounds: inserted={inserted}, updated={updated}")
        inserted, updated = seed_gelatines()
        print(f"Gelatines: inserted={inserted}, updated={updated}")


if __name__ == "__main__":
    run()
