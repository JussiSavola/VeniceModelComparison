#!/usr/bin/env python3
import json
import math
import os
import sys
import urllib.request


VENICE_MODELS_URL = "https://api.venice.ai/api/v1/models"

HELP = """\
Usage: venice_model_analyzer.py [OPTIONS] [FILE]

Analyze and sort Venice AI models from a JSON file or the Venice API.

Input (pick one):
  FILE          Read model JSON from FILE
  (no FILE)     Read model JSON from stdin
  -fetch        Fetch live model data from the Venice API
                Requires VENICE_API_KEY environment variable

Sort (default: capability count desc, then input price asc):
  -price        Sort by output price asc (tiebreaker: input price asc)

Other:
  -help         Show this help message

Examples:
  python3 venice_model_analyzer.py venice.models.json
  cat venice.models.json | python3 venice_model_analyzer.py
  python3 venice_model_analyzer.py -fetch
  python3 venice_model_analyzer.py -fetch -price
  python3 venice_model_analyzer.py -price venice.models.json
"""


def fetch_models() -> list:
    api_key = os.environ.get("VENICE_API_KEY")
    if not api_key:
        print("Error: VENICE_API_KEY environment variable not set.", file=sys.stderr)
        sys.exit(1)
    req = urllib.request.Request(
        VENICE_MODELS_URL,
        headers={"Authorization": f"Bearer {api_key}"},
    )
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode())
    return data.get("data", data) if isinstance(data, dict) else data


def load_models(source) -> list:
    data = json.load(source)
    return data.get("data", data) if isinstance(data, dict) else data


def cap_score(caps: dict) -> int:
    return sum(1 for v in caps.values() if v is True)


def fmt_price(val) -> str:
    return "—" if val is None else f"${val:.3f}"


def fmt_bool(val) -> str:
    return "✓" if val else " "


def fmt_ctx(tokens) -> str:
    if tokens is None:
        return "—"
    k = tokens // 1000
    return f"{k // 1000}M" if k >= 1000 else f"{k}K"


def build_rows(models: list) -> list[dict]:
    rows = []
    for m in models:
        spec = m.get("model_spec", {})
        caps = spec.get("capabilities", {})
        pricing = spec.get("pricing", {})
        input_usd = pricing.get("input", {}).get("usd") if pricing else None
        output_usd = pricing.get("output", {}).get("usd") if pricing else None

        name = spec.get("name") or m.get("id", "?")
        if spec.get("deprecation"):
            name += " (dep)"
        if spec.get("betaModel"):
            name += " (β)"

        rows.append({
            "name": name,
            "id": m.get("id", ""),
            "vis": fmt_bool(caps.get("supportsVision")),
            "reason": fmt_bool(caps.get("supportsReasoning")),
            "code": fmt_bool(caps.get("optimizedForCode")),
            "fncall": fmt_bool(caps.get("supportsFunctionCalling")),
            "web": fmt_bool(caps.get("supportsWebSearch")),
            "ctx": fmt_ctx(spec.get("availableContextTokens")),
            "input": fmt_price(input_usd),
            "output": fmt_price(output_usd),
            "caps": cap_score(caps),
            "_input_usd": input_usd if input_usd is not None else math.inf,
            "_output_usd": output_usd if output_usd is not None else math.inf,
        })
    return rows


def render_table(rows: list[dict]) -> None:
    headers = {
        "name": "Model",
        "id": "ID",
        "vis": "Vis",
        "reason": "Reason",
        "code": "Code",
        "fncall": "FnCall",
        "web": "Web",
        "ctx": "Ctx",
        "input": "Input $/M",
        "output": "Output $/M",
        "caps": "Caps",
    }
    cols = list(headers.keys())
    right_cols = {"input", "output", "caps", "ctx"}

    widths = {c: len(headers[c]) for c in cols}
    for row in rows:
        for c in cols:
            widths[c] = max(widths[c], len(str(row[c])))

    def fmt_row(values: dict) -> str:
        parts = []
        for c in cols:
            v = str(values[c])
            parts.append(v.rjust(widths[c]) if c in right_cols else v.ljust(widths[c]))
        return " | ".join(parts)

    print(fmt_row({c: headers[c] for c in cols}))
    print("-+-".join("-" * widths[c] for c in cols))
    for row in rows:
        print(fmt_row(row))


def main():
    args = sys.argv[1:]

    if "-help" in args:
        print(HELP, end="")
        sys.exit(0)

    do_fetch = "-fetch" in args
    sort_price = "-price" in args
    file_args = [a for a in args if not a.startswith("-")]

    if do_fetch:
        models = fetch_models()
    elif file_args:
        with open(file_args[0], encoding="utf-8") as f:
            models = load_models(f)
    else:
        models = load_models(sys.stdin)

    rows = build_rows(models)

    if sort_price:
        rows.sort(key=lambda r: (r["_output_usd"], r["_input_usd"]))
    else:
        rows.sort(key=lambda r: (-r["caps"], r["_input_usd"]))

    render_table(rows)


if __name__ == "__main__":
    main()
