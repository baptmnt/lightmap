from __future__ import annotations

from typing import TYPE_CHECKING

from .db import db
from .association import group_association_table
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String

if TYPE_CHECKING:
    from .projector import LightmapProjector



class Group(db.Model):
    __tablename__ = 'groups'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    lightmap_projectors: Mapped[list["LightmapProjector"]] = relationship(
        secondary=group_association_table,
        back_populates="groups",
    )
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
        }
    
