from contextlib import asynccontextmanager
from uuid import uuid4
from ..engine.graph_engine import GRAPHS

@asynccontextmanager
async def lifespan(app):
    # Create sample default graph
    graph_id = str(uuid4())
    GRAPHS[graph_id] = {
        "nodes": ["extract_functions", "check_complexity", "detect_issues", "suggest_improvements"],
        "edges": {
            "extract_functions": "check_complexity",
            "check_complexity": "detect_issues",
            "detect_issues": "suggest_improvements"
        },
        "start_node": "extract_functions"
    }
    GRAPHS["__sample__"] = GRAPHS[graph_id]


    yield
