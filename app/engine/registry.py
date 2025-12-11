from typing import Callable, Dict

ToolsRegistry: Dict[str, Callable] = {}

def tool(name: str):
    def decorator(fn):
        ToolsRegistry[name] = fn
        return fn
    return decorator
