from __future__ import annotations

from .db import db
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

class Background(db.Model):
    __tablename__ = 'backgrounds'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    filename: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'filename': self.filename,
        }