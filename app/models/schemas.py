from pydantic import BaseModel
from typing import Dict, Any, Optional, List

class GraphSpec(BaseModel):
    nodes: List[str]
    edges: Dict[str, Optional[str]]
    start_node: str

class RunRequest(BaseModel):
    graph_id: str
    initial_state: Dict[str, Any] = {}
    async_run: Optional[bool] = False
