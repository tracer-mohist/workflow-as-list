#!/usr/bin/env python3
# scripts/calc-task-range.py
# Task Token Range Calculator
# Formula: [sqrt(N * 0.618), sqrt(N)]
# N = context_max (total tokens)
# 0.618 = golden ratio (effective context ratio)
# https://github.com/tracer-mohist/workflow-as-list

import json
import math
import re
import sys

parse_ctx = lambda s: (
    int(float(m.group(1)) * {"k": 1e3, "m": 1e6, None: 1}[m.group(2)])
    if (m := re.match(r"^(\d+(?:\.\d+)?)\s*([km])?$", s.strip().lower()))
    else None
)


def calc(ctx):
    limit = int(ctx * 0.80)  # 80% safe operating limit
    effective = int(ctx * 0.618)  # 61.8% golden ratio
    t_min, t_max = math.sqrt(effective), math.sqrt(ctx)

    return {
        "context_max": ctx,
        "context_limit": limit,
        "context_effective": effective,
        "overflow_cache": limit - effective,
        "task_token_min": round(t_min, 2),
        "task_token_max": round(t_max, 2),
        "recommended": [math.ceil(t_min), math.floor(t_max)],
    }


if __name__ == "__main__":
    if len(sys.argv) < 2 or not (ctx := parse_ctx(sys.argv[-1])):
        sys.stderr.write("Usage: calc-task-range.py <context>\n")
        sys.stderr.write("Examples: 128k, 32K, 1m, 512000\n")
        sys.exit(1)

    print(json.dumps(calc(ctx)))
