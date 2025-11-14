# PyPI Package Setup Guide

## Current Issue

The current directory structure has Python code files mixed with virtualenv directories:
```
memory_mori/ (virtualenv root)
├── api.py, config.py, __init__.py (package files)
├── core/, stores/, utils/ (packages)
├── bin/, lib/, include/, share/ (virtualenv files)
```

## Recommended Structure for PyPI

For proper PyPI distribution, you should:

### Option 1: Restructure (Recommended)

Create a clean project structure outside the virtualenv:

```bash
# Create new project structure
mkdir ~/memory-mori-package
cd ~/memory-mori-package

# Create package directory
mkdir memory_mori

# Copy package files
cp /home/daha/Python/memory_mori/{api.py,config.py,__init__.py} memory_mori/
cp -r /home/daha/Python/memory_mori/{core,stores,utils} memory_mori/

# Copy project files
cp /home/daha/Python/memory_mori/{README.md,LICENSE,pyproject.toml,MANIFEST.in} .
cp -r /home/daha/Python/memory_mori/{examples,tests} .
cp /home/daha/Python/memory_mori/requirements.txt .
```

Final structure:
```
memory-mori-package/
├── pyproject.toml
├── README.md
├── LICENSE
├── MANIFEST.in
├── requirements.txt
├── memory_mori/          # The actual package
│   ├── __init__.py
│   ├── api.py
│   ├── config.py
│   ├── core/
│   ├── stores/
│   └── utils/
├── examples/
└── tests/
```

Then update `pyproject.toml`:
```toml
[tool.setuptools.packages.find]
where = ["."]
include = ["memory_mori*"]
exclude = ["tests*", "examples*"]
```

### Option 2: Build from Current Location

If you want to build from the current location, you need to:

1. Ensure virtual environment is deactivated
2. Use explicit package configuration (already done in pyproject.toml)
3. Build will automatically exclude virtualenv directories

## Building and Publishing

### 1. Install build tools
```bash
pip install build twine
```

### 2. Download spaCy model (required for package functionality)
```bash
python -m spacy download en_core_web_lg
```

Note: Users will need to run this after installing your package.
Add to README installation instructions!

### 3. Build the package
```bash
# From project root
python -m build
```

This creates:
- `dist/memory-mori-0.1.0.tar.gz` (source distribution)
- `dist/memory_mori-0.1.0-py3-none-any.whl` (wheel)

### 4. Test the package locally
```bash
pip install dist/memory-mori-0.1.0.tar.gz
```

### 5. Upload to TestPyPI (for testing)
```bash
twine upload --repository testpypi dist/*
```

### 6. Upload to PyPI (production)
```bash
twine upload dist/*
```

## Important Notes

1. **spaCy Model**: Users must download the spaCy model after installation:
   ```bash
   pip install memory-mori
   python -m spacy download en_core_web_lg
   ```

2. **Update README**: Add clear installation instructions including the spaCy model download

3. **Version Updates**: Remember to update version in both:
   - `pyproject.toml`
   - `__init__.py`

4. **Email**: Update your email in `pyproject.toml` before publishing

## Testing After Installation

```python
from memory_mori import MemoryMori, MemoryConfig

mm = MemoryMori()
mm.store("Test message")
results = mm.retrieve("Test")
print(results)
```
