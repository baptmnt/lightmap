from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING

from .db import db
from .background import Background
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, Integer, Date

if TYPE_CHECKING:
    from .projector import LightmapProjector

class Lightmap(db.Model):
    __tablename__ = 'lightmaps'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    date: Mapped[date] = mapped_column(Date, nullable=True)

    background_id: Mapped[int] = mapped_column(ForeignKey('backgrounds.id'), nullable=False)
    background: Mapped["Background"] = relationship()
    
    projectors: Mapped[list["LightmapProjector"]] = relationship(back_populates="lightmap")
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'date': self.date.isoformat() if self.date else None,
            'background': self.background.to_dict() if self.background else None,
            'projectors': [lp.to_dict() for lp in self.projectors] if self.projectors else []
        }

    def to_summary(self):
        return {
            'id': self.id,
            'name': self.name,
            'date': self.date.isoformat() if self.date else None,
        }