# Venice Model Analyzer

A command-line tool that fetches or reads Venice AI model data and renders a sorted, human-readable table of models with their capabilities and pricing.

## Requirements

- Python 3.10+ (no third-party dependencies)

## Usage

```
python3 venice_model_analyzer.py [OPTIONS] [FILE]
```

### Input sources

| Method | Command |
|--------|---------|
| From file | `python3 venice_model_analyzer.py venice.models.json` |
| From stdin | `cat venice.models.json \| python3 venice_model_analyzer.py` |
| From Venice API | `python3 venice_model_analyzer.py -fetch` |

### Options

| Flag | Description |
|------|-------------|
| `-fetch` | Fetch live model data from the Venice API. Requires `VENICE_API_KEY` environment variable. |
| `-price` | Sort by output price ascending (tiebreaker: input price). Default sort is capability count descending, then input price ascending. |
| `-help` | Print usage instructions. |

Flags can be combined freely:

```bash
python3 venice_model_analyzer.py -fetch -price
python3 venice_model_analyzer.py -price venice.models.json
```

### API key setup

```bash
export VENICE_API_KEY=your_api_key_here
python3 venice_model_analyzer.py -fetch
```

## Output

The tool prints a table with the following columns:

| Column | Description |
|--------|-------------|
| Model | Model name. `(β)` = beta, `(dep)` = deprecated. |
| Vis | Supports vision / image input |
| Reason | Supports reasoning |
| Code | Optimized for code |
| FnCall | Supports function calling |
| Web | Supports web search |
| Ctx | Available context window (K = thousands, M = millions of tokens) |
| Input $/M | Input price per million tokens (USD) |
| Output $/M | Output price per million tokens (USD) |
| Caps | Total capability score (count of enabled boolean capabilities) |

### Example output

```
Model                           | Vis | Reason | Code | FnCall | Web |  Ctx | Input $/M | Output $/M | Caps
--------------------------------+-----+--------+------+--------+-----+------+-----------+------------+-----
Qwen 3.5 397B                   | ✓   | ✓      | ✓    | ✓      | ✓   | 128K |    $0.750 |     $4.500 |   10
Qwen 3.5 35B A3B (β)            | ✓   | ✓      | ✓    | ✓      | ✓   | 256K |    $0.312 |     $1.250 |    9
Gemini 3 Flash Preview          | ✓   | ✓      |      | ✓      | ✓   | 256K |    $0.700 |     $3.750 |    9
...
```

## Data source

Model data follows the Venice AI API format (`GET /api/v1/models`). The tool works with any JSON file that matches this structure — either fetched live with `-fetch` or saved locally for offline use.
