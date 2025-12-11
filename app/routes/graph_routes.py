from fastapi import APIRouter, HTTPException, BackgroundTasks
from uuid import uuid4

from ..models.schemas import GraphSpec, RunRequest
from ..engine.graph_engine import GRAPHS, RUNS
from ..engine.executor import execute_graph

router = APIRouter()

@router.post("/graph/create")
async def create_graph(spec: GraphSpec):
    for n in spec.nodes:
        if n not in GRAPHS.get("__registered_nodes__", {}):
            pass  # Optional validation

    graph_id = str(uuid4())
    GRAPHS[graph_id] = spec.model_dump()
    return {"graph_id": graph_id}

@router.post("/graph/run")
async def run_graph(req: RunRequest, bg: BackgroundTasks):
    if req.graph_id not in GRAPHS:
        raise HTTPException(404, "Graph not found")

    run_id = str(uuid4())
    RUNS[run_id] = {
        "graph_id": req.graph_id,
        "state": dict(req.initial_state),
        "log": [],
        "status": "pending",
        "current_node": None
    }

    if req.async_run:
        bg.add_task(execute_graph, run_id)
        return {"run_id": run_id, "status": "running"}

    await execute_graph(run_id)
    return RUNS[run_id]

@router.get("/graph/state/{run_id}")
async def get_state(run_id: str):
    if run_id not in RUNS:
        raise HTTPException(404, "Run not found")
    return RUNS[run_id]
