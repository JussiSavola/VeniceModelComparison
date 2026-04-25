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
| Model | Human-readable model name. `(β)` = beta, `(dep)` = deprecated. |
| ID | Technical model ID used in API calls (e.g. `qwen-3-6-plus`) |
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
jsavola@ai:~/mygitrepos/VeniceModelComparison$ python venice_model_analyzer.py -fetch
Model                           | ID                                   | Vis | Reason | Code | FnCall | Web |  Ctx | Input $/M | Output $/M | Caps
--------------------------------+--------------------------------------+-----+--------+------+--------+-----+------+-----------+------------+-----
Qwen 3.5 397B                   | qwen3-5-397b-a17b                    | ✓   | ✓      | ✓    | ✓      | ✓   | 128K |    $0.750 |     $4.500 |   10
Qwen 3.5 35B A3B (β)            | qwen3-5-35b-a3b                      | ✓   | ✓      | ✓    | ✓      | ✓   | 256K |    $0.312 |     $1.250 |    9
Gemini 3 Flash Preview          | gemini-3-flash-preview               | ✓   | ✓      |      | ✓      | ✓   | 256K |    $0.700 |     $3.750 |    9
Gemini 3.1 Pro Preview          | gemini-3-1-pro-preview               | ✓   | ✓      |      | ✓      | ✓   |   1M |    $2.500 |    $15.000 |    9
Google Gemma 4 26B A4B Instruct | google-gemma-4-26b-a4b-it            | ✓   | ✓      |      | ✓      | ✓   | 256K |    $0.163 |     $0.500 |    8
Google Gemma 4 31B Instruct     | google-gemma-4-31b-it                | ✓   | ✓      |      | ✓      | ✓   | 256K |    $0.175 |     $0.500 |    8
Mistral Small 4 (β)             | mistral-small-2603                   | ✓   | ✓      | ✓    | ✓      | ✓   | 256K |    $0.188 |     $0.750 |    8
Qwen3.6 27B (β)                 | qwen3-6-27b                          | ✓   | ✓      | ✓    | ✓      | ✓   | 256K |    $0.325 |     $3.250 |    8
Qwen3.5 122B A10B (β)           | e2ee-qwen3-5-122b-a10b               | ✓   | ✓      |      | ✓      | ✓   | 128K |    $0.500 |     $4.000 |    8
Kimi K2.5                       | kimi-k2-5                            | ✓   | ✓      | ✓    | ✓      | ✓   | 256K |    $0.560 |     $3.500 |    8
Qwen 3.6 Plus Uncensored (β)    | qwen-3-6-plus                        | ✓   | ✓      | ✓    | ✓      | ✓   |   1M |    $0.625 |     $3.750 |    8
Kimi K2.6                       | kimi-k2-6                            | ✓   | ✓      | ✓    | ✓      | ✓   | 256K |    $0.745 |     $4.655 |    8
GLM 5V Turbo (β)                | z-ai-glm-5v-turbo                    | ✓   | ✓      | ✓    | ✓      | ✓   | 200K |    $1.500 |     $5.000 |    8
GPT-5.2 Codex                   | openai-gpt-52-codex                  | ✓   | ✓      | ✓    | ✓      | ✓   | 256K |    $2.190 |    $17.500 |    8
GPT-5.3 Codex (β)               | openai-gpt-53-codex                  | ✓   | ✓      | ✓    | ✓      | ✓   | 400K |    $2.190 |    $17.500 |    8
Claude Sonnet 4.6 (β)           | claude-sonnet-4-6                    | ✓   | ✓      | ✓    | ✓      | ✓   |   1M |    $3.600 |    $18.000 |    8
Claude Sonnet 4.5               | claude-sonnet-4-5                    | ✓   | ✓      | ✓    | ✓      | ✓   | 198K |    $3.750 |    $18.750 |    8
Claude Opus 4.7                 | claude-opus-4-7                      | ✓   | ✓      | ✓    | ✓      | ✓   |   1M |    $6.000 |    $30.000 |    8
Claude Opus 4.6 (β)             | claude-opus-4-6                      | ✓   | ✓      | ✓    | ✓      | ✓   |   1M |    $6.000 |    $30.000 |    8
Claude Opus 4.5                 | claude-opus-4-5                      | ✓   | ✓      | ✓    | ✓      | ✓   | 198K |    $6.000 |    $30.000 |    8
Claude Opus 4.6 Fast (β)        | claude-opus-4-6-fast                 | ✓   | ✓      | ✓    | ✓      | ✓   |   1M |   $36.000 |   $180.000 |    8
Qwen 3.5 9B                     | qwen3-5-9b                           | ✓   | ✓      |      | ✓      | ✓   | 256K |    $0.100 |     $0.150 |    7
GPT-5.4 Mini (β)                | openai-gpt-54-mini                   | ✓   | ✓      |      | ✓      | ✓   | 400K |    $0.938 |     $5.625 |    7
Grok 4.20 (β)                   | grok-4-20                            | ✓   | ✓      |      | ✓      | ✓   |   2M |    $2.270 |     $6.800 |    7
GPT-5.4 (β)                     | openai-gpt-54                        | ✓   | ✓      |      | ✓      | ✓   |   1M |    $3.130 |    $18.800 |    7
GPT-5.5 (β)                     | openai-gpt-55                        | ✓   | ✓      |      | ✓      | ✓   |   1M |    $6.250 |    $37.500 |    7
GPT-5.4 Pro (β)                 | openai-gpt-54-pro                    | ✓   | ✓      |      | ✓      | ✓   |   1M |   $37.500 |   $225.000 |    7
GPT-5.5 Pro (β)                 | openai-gpt-55-pro                    | ✓   | ✓      |      | ✓      | ✓   |   1M |   $37.500 |   $225.000 |    7
DeepSeek V4 Flash               | deepseek-v4-flash                    |     | ✓      | ✓    | ✓      | ✓   |   1M |    $0.175 |     $0.350 |    6
GPT-4o Mini                     | openai-gpt-4o-mini-2024-07-18        | ✓   |        |      | ✓      | ✓   | 128K |    $0.188 |     $0.750 |    6
Grok 4.1 Fast                   | grok-41-fast                         | ✓   | ✓      |      | ✓      | ✓   |   1M |    $0.230 |     $0.570 |    6
Trinity Large Thinking          | arcee-trinity-large-thinking         |     | ✓      | ✓    | ✓      | ✓   | 256K |    $0.312 |     $1.125 |    6
Kimi K2 Thinking (dep)          | kimi-k2-thinking                     |     | ✓      | ✓    | ✓      | ✓   | 256K |    $0.750 |     $3.200 |    6
GLM 5 Turbo                     | z-ai-glm-5-turbo                     |     | ✓      | ✓    | ✓      | ✓   | 200K |    $1.200 |     $4.000 |    6
DeepSeek V4 Pro                 | deepseek-v4-pro                      |     | ✓      | ✓    | ✓      | ✓   |   1M |    $2.175 |     $4.350 |    6
Grok 4.20 Multi-Agent (β)       | grok-4-20-multi-agent                | ✓   | ✓      |      |        | ✓   |   2M |    $2.270 |     $6.800 |    6
GPT-4o                          | openai-gpt-4o-2024-11-20             | ✓   |        |      | ✓      | ✓   | 128K |    $3.125 |    $12.500 |    6
Google Gemma 3 27B Instruct     | google-gemma-3-27b-it                | ✓   |        |      | ✓      | ✓   | 198K |    $0.120 |     $0.200 |    5
GLM 4.7 Flash                   | zai-org-glm-4.7-flash                |     | ✓      |      | ✓      | ✓   | 128K |    $0.125 |     $0.500 |    5
Gemma 4 Uncensored              | gemma-4-uncensored                   | ✓   |        |      | ✓      | ✓   | 256K |    $0.163 |     $0.500 |    5
Venice Uncensored 1.2           | venice-uncensored-1-2                | ✓   |        |      | ✓      | ✓   | 128K |    $0.200 |     $0.900 |    5
Qwen3 VL 235B                   | qwen3-vl-235b-a22b                   | ✓   |        |      | ✓      | ✓   | 256K |    $0.250 |     $1.500 |    5
Qwen3 VL 30B A3B (β)            | e2ee-qwen3-vl-30b-a3b-p              | ✓   |        |      | ✓      | ✓   | 128K |    $0.250 |     $0.900 |    5
Mercury 2 (β)                   | mercury-2                            |     | ✓      |      | ✓      | ✓   | 128K |    $0.312 |     $0.938 |    5
MiniMax M2.5                    | minimax-m25                          |     | ✓      | ✓    | ✓      | ✓   | 198K |    $0.340 |     $1.190 |    5
Qwen 3 Coder 480B Turbo (β)     | qwen3-coder-480b-a35b-instruct-turbo |     |        | ✓    | ✓      | ✓   | 256K |    $0.350 |     $1.500 |    5
MiniMax M2.7                    | minimax-m27                          |     | ✓      | ✓    | ✓      | ✓   | 198K |    $0.375 |     $1.500 |    5
Venice Role Play Uncensored     | venice-uncensored-role-play          | ✓   |        |      | ✓      | ✓   | 128K |    $0.500 |     $2.000 |    5
GLM 5                           | zai-org-glm-5                        |     | ✓      | ✓    | ✓      | ✓   | 198K |    $1.000 |     $3.200 |    5
GLM 4.7 (β)                     | e2ee-glm-4-7-p                       |     | ✓      | ✓    |        | ✓   | 128K |    $1.100 |     $4.150 |    5
GPT-5.2                         | openai-gpt-52                        |     | ✓      |      | ✓      | ✓   | 256K |    $2.190 |    $17.500 |    5
GPT OSS 20B (β)                 | e2ee-gpt-oss-20b-p                   |     | ✓      |      |        | ✓   | 128K |    $0.050 |     $0.190 |    4
GLM 4.7 Flash (β)               | e2ee-glm-4-7-flash-p                 |     |        | ✓    |        | ✓   | 198K |    $0.130 |     $0.550 |    4
GPT OSS 120B (β)                | e2ee-gpt-oss-120b-p                  |     | ✓      |      |        | ✓   | 128K |    $0.130 |     $0.650 |    4
GLM 4.7 Flash Heretic           | olafangensan-glm-4.7-flash-heretic   |     | ✓      |      | ✓      | ✓   | 200K |    $0.140 |     $0.800 |    4
Nemotron Cascade 2 30B A3B (β)  | nvidia-nemotron-cascade-2-30b-a3b    |     | ✓      |      | ✓      | ✓   | 256K |    $0.140 |     $0.800 |    4
Qwen3 30B A3B (β)               | e2ee-qwen3-30b-a3b-p                 |     |        |      | ✓      | ✓   | 256K |    $0.190 |     $0.690 |    4
DeepSeek V3.2                   | deepseek-v3.2                        |     | ✓      |      | ✓      | ✓   | 160K |    $0.330 |     $0.480 |    4
Qwen 3 235B A22B Thinking 2507  | qwen3-235b-a22b-thinking-2507        |     | ✓      |      | ✓      | ✓   | 128K |    $0.450 |     $3.500 |    4
GLM 4.7                         | zai-org-glm-4.7                      |     | ✓      |      | ✓      | ✓   | 198K |    $0.550 |     $2.650 |    4
Qwen 3 Coder 480b (dep)         | qwen3-coder-480b-a35b-instruct       |     |        | ✓    | ✓      | ✓   | 256K |    $0.750 |     $3.000 |    4
GLM 4.6                         | zai-org-glm-4.6                      |     | ✓      |      | ✓      | ✓   | 198K |    $0.850 |     $2.750 |    4
GLM 5.1 (β)                     | e2ee-glm-5-1                         |     | ✓      |      |        | ✓   | 200K |    $1.100 |     $4.150 |    4
GLM 5 (β)                       | e2ee-glm-5                           |     | ✓      |      |        | ✓   | 198K |    $1.100 |     $4.150 |    4
GLM 5.1 (β)                     | zai-org-glm-5-1                      |     | ✓      |      | ✓      | ✓   | 200K |    $1.750 |     $5.500 |    4
Qwen 2.5 7B (β)                 | e2ee-qwen-2-5-7b-p                   |     |        |      |        | ✓   |  32K |    $0.050 |     $0.130 |    3
NVIDIA Nemotron 3 Nano 30B (β)  | nvidia-nemotron-3-nano-30b-a3b       |     |        |      | ✓      | ✓   | 128K |    $0.075 |     $0.300 |    3
Mistral Small 3.2 24B Instruct  | mistral-small-3-2-24b-instruct       |     |        |      | ✓      | ✓   | 256K |    $0.094 |     $0.250 |    3
Gemma 3 27B (β)                 | e2ee-gemma-3-27b-p                   |     |        |      |        | ✓   |  40K |    $0.140 |     $0.500 |    3
Qwen 3 235B A22B Instruct 2507  | qwen3-235b-a22b-instruct-2507        |     |        |      | ✓      | ✓   | 128K |    $0.150 |     $0.750 |    3
Venice Uncensored 1.1 (β)       | e2ee-venice-uncensored-24b-p         |     |        |      |        | ✓   |  32K |    $0.250 |     $1.150 |    3
Qwen 3 Next 80b                 | qwen3-next-80b                       |     |        |      | ✓      | ✓   | 256K |    $0.350 |     $1.900 |    3
Aion 2.0                        | aion-labs-aion-2-0                   |     | ✓      |      |        | ✓   | 128K |    $1.000 |     $2.000 |    3
OpenAI GPT OSS 120B             | openai-gpt-oss-120b                  |     |        |      | ✓      | ✓   | 128K |    $0.070 |     $0.300 |    2
Llama 3.2 3B                    | llama-3.2-3b                         |     |        |      | ✓      | ✓   | 128K |    $0.150 |     $0.600 |    2
Venice Uncensored 1.1 (dep)     | venice-uncensored                    |     |        |      |        | ✓   |  32K |    $0.200 |     $0.900 |    2
Llama 3.3 70B                   | llama-3.3-70b                        |     |        |      | ✓      | ✓   | 128K |    $0.700 |     $2.800 |    2
Hermes 3 Llama 3.1 405b         | hermes-3-llama-3.1-405b              |     |        |      |        | ✓   | 128K |    $1.100 |     $3.000 |    1

...
```

## Data source

Model data follows the Venice AI API format (`GET /api/v1/models`). The tool works with any JSON file that matches this structure — either fetched live with `-fetch` or saved locally for offline use.
