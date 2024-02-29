from typing import List
from sqlalchemy import (
    BigInteger,
    Column,
    Integer,
    String,
    DECIMAL,
    DateTime,
    Boolean,
    ForeignKey,
)
from .base import Base

from sqlalchemy.orm import Mapped, mapped_column, relationship


class User(Base):
    __tablename__ = "users"

    id_user: Mapped[int] = mapped_column(
        BigInteger, unique=True
    )
    status: Mapped[str] = mapped_column(String(length=10), default="user")


class Recipe(Base):
    __tablename__ = "recipes"

    name: Mapped[str] = mapped_column(String(length=30))
    text: Mapped[str] = mapped_column(default="текст не задан")


class Text(Base):
    __tablename__ = "texts"

    name: Mapped[str] = mapped_column(String(length=30))  # Название текста
    text: Mapped[str] = mapped_column(default="текст не задан")  # Текст


class Button(Base):
    __tablename__ = "buttons"

    name: Mapped[str] = mapped_column(String(length=30))  # Название кнопки
    text: Mapped[str] = mapped_column(
        String(length=64), default="кнопка"
    )  # Текст кнопки


class Value(Base):
    __tablename__ = "values"

    name: Mapped[str] = mapped_column(String(length=30))  # Название значения
    value: Mapped[int] = mapped_column(Integer, default=0)  # Значение
