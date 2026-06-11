"""
models/__init__.py
Export TransformerLM và HyenaLM để dùng từ train.py
"""
from .transformer import TransformerLM
from .hyena import HyenaLM

__all__ = ["TransformerLM", "HyenaLM"]
