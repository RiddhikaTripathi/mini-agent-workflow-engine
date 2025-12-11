import asyncio
from uuid import uuid4
from .graph_engine import GRAPHS, RUNS
from .registry import ToolsRegistry

async def execute_graph(run_id: str):
    run = RUNS[run_id]
    graph = GRAPHS[run["graph_id"]]
    state = run["state"]
    edges = graph.get("edges", {})
    current = graph["start_node"]

    run["status"] = "running"
    run["current_node"] = current
    run["log"].append(f"Run started for graph {run['graph_id']}")

    state.setdefault("meta", {}).setdefault("iteration", 0)

    max_steps = 200
    steps = 0

    while current is not None:
        steps += 1
        if steps > max_steps:
            run["status"] = "failed"
            run["log"].append("Max steps exceeded")
            return

        if current not in ToolsRegistry:
            run["status"] = "failed"
            run["log"].append(f"Node {current} missing in ToolsRegistry")
            return

        run["log"].append(f"Running node: {current}")
        node_fn = ToolsRegistry[current]

        result = node_fn(state, ToolsRegistry)
        if asyncio.iscoroutine(result):
            result = await result

        next_node = result.get("next") if isinstance(result, dict) else edges.get(current)
        run["log"].append(f"{current} -> {next_node}")

        current = next_node
        run["current_node"] = current

        await asyncio.sleep(0)

    run["status"] = "completed"
    run["log"].append("Execution completed successfully")
