from __future__ import annotations

from typing import TYPE_CHECKING

from .db import db
from .association import group_association_table, gelatine_association_table
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey

if TYPE_CHECKING:
    from .mode import Mode
    from .group import Group
    from .lightmap import Lightmap
    from .gelatine import Gelatine

class Projector(db.Model):
    __tablename__ = 'projectors'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    filename: Mapped[str] = mapped_column(String(120), nullable=True)
    size: Mapped[int] = mapped_column(Integer, nullable=True, default=512)
    is_led: Mapped[bool] = mapped_column(nullable=False, default=False)
    modes: Mapped[list["Mode"]] = relationship()
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'filename': self.filename,
            'size': self.size,
            'is_led': self.is_led,
            'modes': [mode.to_dict() for mode in self.modes],
        }

class LightmapProjector(db.Model):
    __tablename__ = 'lightmap_projectors'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    label: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)

    projector_id: Mapped[int] = mapped_column(ForeignKey('projectors.id'), nullable=False)
    projector: Mapped["Projector"] = relationship()

    lightmap_id: Mapped[int] = mapped_column(ForeignKey('lightmaps.id'), nullable=False)
    lightmap: Mapped["Lightmap"] = relationship(back_populates="projectors") 

    x: Mapped[float] = mapped_column(nullable=False)
    y: Mapped[float] = mapped_column(nullable=False)
    z_level: Mapped[int] = mapped_column(Integer, nullable=False)
    angle: Mapped[float] = mapped_column(nullable=False, default=0.0)
    size: Mapped[float] = mapped_column(nullable=False, default=1.0)

    gelatines: Mapped[list["Gelatine"]] = relationship(secondary=gelatine_association_table, backref="lightmap_projectors")

    mode_id: Mapped[int] = mapped_column(ForeignKey('modes.id'), nullable=True)
    mode: Mapped["Mode"] = relationship()

    channel: Mapped[int] = mapped_column(Integer, nullable=True)

    universe: Mapped[int] = mapped_column(Integer, nullable=True)
    address: Mapped[int] = mapped_column(Integer, nullable=True)

    groups: Mapped[list["Group"]] = relationship(secondary=group_association_table, back_populates="lightmap_projectors")
    
    def to_dict(self):
        return {
            'id': self.id,
            'label': self.label,
            'lightmap_id': self.lightmap_id,
            'projector': self.projector.to_dict() if self.projector else None,
            'x': self.x,
            'y': self.y,
            'z_level': self.z_level,
            'gelatines': [g.to_dict() for g in self.gelatines],
            'mode': self.mode.to_dict() if self.mode else None,
            'channel': self.channel,
            'universe': self.universe,
            'address': self.address,
            'groups': [group.to_dict() for group in self.groups]
        }