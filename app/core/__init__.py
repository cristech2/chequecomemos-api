# app/core/__init__.py
# Expone los módulos principales de la capa core.

from .db import Base, SessionLocal, engine  # noqa: F401

__all__ = ("Base", "SessionLocal", "engine")
