# Evaluation & Metrics Framework

Comprehensive testing and benchmarking suite for Memory Mori.

## Components

### Test Datasets
- **test_dataset.py**: Ground truth data for retrieval and entity extraction tests
  - 10 test documents across programming topics
  - 8 queries with relevance judgments
  - 5 entity extraction test cases

### Metrics
- **metrics.py**: Evaluation metrics implementation
  - **Retrieval Metrics**: Precision, Recall, F1, P@k, R@k
  - **Ranking Metrics**: MAP (Mean Average Precision), MRR (Mean Reciprocal Rank), NDCG
  - **Entity Metrics**: Entity-level precision, recall, F1

### Evaluators

#### 1. Retrieval Evaluator (`retrieval_evaluator.py`)
Tests retrieval quality against ground truth.

```python
from tests import run_retrieval_evaluation

results = run_retrieval_evaluation(verbose=True, max_items=5)
print(f"Mean F1: {results['aggregated_metrics']['mean_f1']:.3f}")
print(f"MAP: {results['aggregated_metrics']['MAP']:.3f}")
```

**Metrics Reported:**
- Mean Precision, Recall, F1
- P@3, P@5 (Precision at k)
- MAP (Mean Average Precision)
- MRR (Mean Reciprocal Rank)
- NDCG@3, NDCG@5

#### 2. Entity Evaluator (`entity_evaluator.py`)
Tests entity extraction accuracy.

```python
from tests import run_entity_evaluation

results = run_entity_evaluation(verbose=True)
print(f"Average F1: {results['average_f1']:.3f}")
```

**Features:**
- Precision, recall, F1 for entity extraction
- Error analysis (false positives/negatives)
- Per-entity-type breakdowns

#### 3. Decay Evaluator (`decay_evaluator.py`)
Tests time-based decay behavior.

```python
from tests import run_decay_evaluation

results = run_decay_evaluation(verbose=True)
```

**Tests:**
- Decay curve over time (0-90 days)
- Time mode comparison (creation, access, combined)
- Formula validation (half-life accuracy)
- Cleanup threshold behavior

#### 4. Performance Benchmark (`benchmark.py`)
Measures latency and throughput.

```python
from tests import run_benchmark

results = run_benchmark(verbose=True, num_docs=50)
```

**Metrics:**
- Storage throughput (docs/sec)
- Retrieval latency (ms per query)
- Context generation latency
- End-to-end workflow timing

## Usage

### Quick Evaluation
Run a fast subset of tests:

```bash
python run_evaluation.py --mode quick
```

### Full Evaluation Suite
Run all evaluations:

```bash
python run_evaluation.py --mode full
```

Options:
- `--quiet`: Suppress verbose output
- `--no-save`: Don't save results to JSON

### Individual Tests
Run specific evaluators:

```python
# Retrieval only
from tests import run_retrieval_evaluation
results = run_retrieval_evaluation(verbose=True)

# Entities only
from tests import run_entity_evaluation
results = run_entity_evaluation(verbose=True)

# Decay only
from tests import run_decay_evaluation
results = run_decay_evaluation(verbose=True)

# Benchmark only
from tests import run_benchmark
results = run_benchmark(verbose=True, num_docs=100)
```

## Important Notes

### ChromaDB Limitations
Due to ChromaDB's singleton pattern for ephemeral databases, running multiple tests with different configurations in the same process may fail. If you encounter errors about "An instance of Chroma already exists", either:

1. **Run tests separately** (recommended):
   ```python
   # Run one test at a time
   python -c "from tests import run_retrieval_evaluation; run_retrieval_evaluation()"
   python -c "from tests import run_benchmark; run_benchmark()"
   ```

2. **Restart the Python process** between test runs

3. **Use individual evaluator scripts** instead of the comprehensive runner

This is a known limitation of ChromaDB and does not affect production use where a single configuration is used throughout the application lifecycle.

## Results Format

Evaluation results are saved as JSON with the following structure:

```json
{
  "timestamp": "2025-01-15T10:30:00",
  "tests": {
    "retrieval": {
      "status": "passed",
      "results": {
        "num_queries": 8,
        "aggregated_metrics": {
          "mean_precision": 0.850,
          "mean_recall": 0.780,
          "mean_f1": 0.758,
          "MAP": 0.958,
          "MRR": 0.942
        }
      }
    },
    "entities": { "..." },
    "decay": { "..." },
    "benchmark": { "..." }
  }
}
```

## Extending the Framework

### Adding New Test Cases

Edit `test_dataset.py`:

```python
def _create_documents(self):
    return [
        {
            "id": "doc_new",
            "text": "Your test document...",
            "category": "category_name"
        }
    ]

def _create_ground_truth(self):
    return {
        "q_new": ["doc_1", "doc_new"]  # Relevant docs for query
    }
```

### Adding New Metrics

Edit `metrics.py`:

```python
class RetrievalMetrics:
    @staticmethod
    def your_metric(retrieved, relevant):
        # Your metric implementation
        return score
```

### Creating Custom Evaluators

```python
from tests import TestDataset, RetrievalMetrics

class CustomEvaluator:
    def __init__(self):
        self.dataset = TestDataset()
        self.metrics = RetrievalMetrics()

    def evaluate(self):
        # Your evaluation logic
        pass
```

## Benchmarking Guidelines

For consistent benchmarking results:

1. **Close other applications** to reduce system noise
2. **Run multiple iterations** (benchmark.py does this automatically)
3. **Use consistent document counts** across runs
4. **Consider warm-up runs** for caching effects
5. **Document system specs** when comparing results

## Interpreting Results

### Retrieval Quality
- **MAP > 0.8**: Excellent retrieval quality
- **MAP 0.6-0.8**: Good retrieval quality
- **MAP < 0.6**: Needs improvement

### Entity Extraction
- **F1 > 0.8**: Excellent entity extraction
- **F1 0.6-0.8**: Acceptable entity extraction
- **F1 < 0.6**: Review entity patterns and model

### Performance
- **Storage**: > 50 docs/sec is good for this system
- **Retrieval**: < 100ms per query is acceptable
- **Context**: < 150ms is acceptable

These benchmarks assume typical hardware (8GB RAM, modern CPU).
