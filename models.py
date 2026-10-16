from typing import List

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base

class User(Base):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    nome: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)

    livros: Mapped[List["Book"]] = relationship(back_populates="usuarios")


class Book(Base):
    __tablename__ = "livros"

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    titulo: Mapped[str] = mapped_column(nullable=False)
    id_usuario: Mapped[int] = mapped_column(ForeignKey("usuarios.id"))

    usuarios: Mapped["User"] = relationship(back_populates="livros")