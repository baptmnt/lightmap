from __future__ import annotations

from typing import TYPE_CHECKING

from .db import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean

if TYPE_CHECKING:
    from .projector import LightmapProjector

class Gelatine(db.Model):
    __tablename__ = 'gelatines'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    number: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    hex_color: Mapped[str] = mapped_column(String(7), nullable=False)
    is_diffuser: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'number': self.number,
            'name': self.name,
            'hex_color': self.hex_color,
            'is_diffuser': self.is_diffuser,
        }
