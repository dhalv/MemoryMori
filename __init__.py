"""
Memory Mori - Persistent memory for LLMs

Give your AI conversations long-term memory with intelligent context retrieval.
Perfect for building chatbots and AI assistants that remember past interactions.
"""

from .api import MemoryMori
from .config import Memory, MemoryConfig

__version__ = "0.1.3"
__all__ = ["MemoryMori", "Memory", "MemoryConfig", "__version__"]
