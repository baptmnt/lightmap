from __future__ import annotations

from typing import TYPE_CHECKING

from .db import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Integer, String

if TYPE_CHECKING:
    from .projector import Projector

class Mode(db.Model):
    __tablename__ = 'modes'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    eos_name: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    channel_count: Mapped[int] = mapped_column(Integer, nullable=False)
    projector_id: Mapped[int] = mapped_column(ForeignKey('projectors.id'), nullable=False)
    projector: Mapped["Projector"] = relationship(back_populates="modes")
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'eos_name': self.eos_name,
            'channel_count': self.channel_count,
            'projector': self.projector.to_dict() if self.projector else None
        }
    
