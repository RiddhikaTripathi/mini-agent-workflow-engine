from . import *
from ..engine.registry import tool

@tool("extract_functions")
async def extract_functions(state, tools):
    code = state.get("code", "")
    funcs = []

    for idx, part in enumerate(code.split("def ")):
        if not part.strip():
            continue
        name = part.split("(")[0].strip() if "(" in part else f"f{idx}"
        lines = len(part.splitlines())
        funcs.append({"name": name, "lines": lines})

    state["functions"] = funcs
    state.setdefault("log", []).append(f"Extracted {len(funcs)} functions")

    return {"next": "check_complexity"}

@tool("check_complexity")
async def check_complexity(state, tools):
    for f in state.get("functions", []):
        f["complexity"] = max(1, f["lines"] // 10 + 1)

    state["log"].append("Computed complexity")
    return {"next": "detect_issues"}

@tool("detect_issues")
async def detect_issues(state, tools):
    issues = []
    for f in state["functions"]:
        if f["complexity"] > 3:
            issues.append({"function": f["name"], "issue": "high_complexity"})
        if f["lines"] > 200:
            issues.append({"function": f["name"], "issue": "too_long"})

    state["issues"] = issues
    state["log"].append(f"Detected {len(issues)} issues")
    return {"next": "suggest_improvements"}

@tool("suggest_improvements")
async def suggest_improvements(state, tools):
    issues = state.get("issues", [])
    suggestions = [f"Improve {it['function']}" for it in issues]
    state["suggestions"] = suggestions

    iter_count = state["meta"].get("iteration", 0)
    quality = 50 - 10 * len(issues) + 5 * iter_count
    quality = max(0, min(100, quality))

    state["quality_score"] = quality
    state["log"].append(f"Quality score {quality}")

    threshold = state.get("threshold", 80)

    if quality >= threshold:
        return {"next": None}

    state["meta"]["iteration"] += 1
    return {"next": "check_complexity"}
