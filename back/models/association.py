from __future__ import annotations

from sqlalchemy import Column, ForeignKey, Table
from .db import db


group_association_table = Table(
    'group_projector_association',
    db.metadata,
    Column('group_id', ForeignKey('groups.id'), primary_key=True),
    Column('projector_id', ForeignKey('lightmap_projectors.id'), primary_key=True)
)

gelatine_association_table = Table(
    'lightmap_projector_gelatine_association',
    db.metadata,
    Column('lightmap_projector_id', ForeignKey('lightmap_projectors.id'), primary_key=True),
    Column('gelatine_id', ForeignKey('gelatines.id'), primary_key=True)
)