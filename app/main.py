from fastapi import FastAPI
from .routes.graph_routes import router
from .config.lifespan import lifespan

# IMPORT NODES SO THEY REGISTER THEMSELVES
from .nodes import code_review_nodes

app = FastAPI(title="Workflow Engine", lifespan=lifespan)

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
