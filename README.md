# Memory Mori

Memory Mori is a Python library that provides persistent, searchable memory for Large Language Models (LLMs). It remembers past conversations, user preferences, and important context, then intelligently retrieves relevant information when needed.

**Key capabilities:**
- 🧠 **Persistent Memory**: Store and retrieve conversation history across sessions
- 🔍 **Smart Retrieval**: Hybrid search combines semantic understanding with keyword matching
- 👤 **User Profiles**: Automatically learns and remembers user preferences, skills, and context
- ⏰ **Time Awareness**: Recent memories are prioritized, old ones fade naturally
- 🏷️ **Entity Tracking**: Remembers people, organizations, tools, and technologies mentioned
- 🚀 **Easy Integration**: Works with OpenAI, Claude, Ollama, and any LLM


## Installation

```bash
# Install Memory Mori from PyPI
pip install memory-mori

# Download spaCy language model (required)
python -m spacy download en_core_web_lg
```

## Configuration

```python
from memory_mori import MemoryConfig

# Custom configuration
config = MemoryConfig(
    alpha=0.8,                    # 80% semantic, 20% keyword
    lambda_decay=0.05,            # Slow decay rate
    entity_model="en_core_web_md", # Entity extraction model
    enable_entities=True,         # Enable entity extraction
    enable_profile=True,          # Enable profile learning
    device="auto"                 # Device: "auto", "cpu", or "cuda"
)

mm = MemoryMori(config)

# Or use presets
config = MemoryConfig.from_preset('standard')     # Balanced
config = MemoryConfig.from_preset('high_accuracy') # Uses larger model
config = MemoryConfig.from_preset('minimal')      # Lightweight
```

## API Reference

### MemoryMori

#### `store(text, metadata=None) -> str`
Store a memory.

```python
doc_id = mm.store(
    "Python is great for data science",
    metadata={"source": "conversation"}
)
```

#### `retrieve(query, filters=None, max_items=3, min_score=0.3) -> List[Memory]`
Retrieve relevant memories.

```python
# Basic retrieval
results = mm.retrieve("Python programming")

# With filters and thresholds
results = mm.retrieve(
    "web development",
    max_items=5,
    min_score=0.5,
    filters={"entity_type": "PRODUCT"}
)
```

#### `get_context(query, max_items=3, include_profile=True) -> str`
Get formatted context for LLM prompts.

```python
context = mm.get_context("What technologies do I use?")
# Returns formatted string with relevant memories and profile
```

#### `update_profile(facts: Dict)`
Manually update profile facts.

```python
mm.update_profile({
    "job_title": ("Software Engineer", "role", 0.9),
    "likes_coffee": ("true", "preference", 0.8)
})
```

#### `get_profile(category=None) -> Dict`
Get profile facts.

```python
profile = mm.get_profile()
# Or filter by category
preferences = mm.get_profile(category="preference")
```

#### `cleanup(threshold=0.01) -> int`
Clean up stale memories.

```python
removed_count = mm.cleanup(threshold=0.01)
```

## Examples

See the [examples/](examples/) folder for minimal integration examples:
- **[example_openai.py](examples/example_openai.py)** - OpenAI/GPT integration
- **[example_claude.py](examples/example_claude.py)** - Claude/Anthropic integration
- **[example_ollama.py](examples/example_ollama.py)** - Ollama/Local models integration


## Project Structure

```
memory_mori/
├── api.py                      # Main MemoryMori class
├── config.py                   # Configuration and data classes
├── core/
│   ├── search.py              # Hybrid search
│   ├── entities.py            # Entity extraction with tech patterns
│   ├── profile.py             # Profile management
│   ├── decay.py               # Time-based decay
│   └── device.py              # GPU/CPU device management
├── stores/
│   ├── vector_store.py        # ChromaDB wrapper
│   └── profile_store.py       # SQLite profile storage
├── examples/
│   ├── example_openai.py      # Minimal OpenAI integration
│   ├── example_claude.py      # Minimal Claude integration
│   └── example_ollama.py      # Minimal Ollama integration
├── tests/                      # Testing and benchmarking tools
└── utils/                      # Utility functions
```

## Requirements

- Python 3.8+
- chromadb
- sentence-transformers
- spacy (with en_core_web_md)
- rank_bm25

## Contributing

This is a personal project, but suggestions and feedback are welcome!

## License

MIT License

## Author

David Halvarson

---

**Note**: For production use, consider:
- Using environment variables for API keys
- Implementing proper error handling
- Adding logging
- Setting up proper data persistence paths
- Monitoring memory usage and performance
