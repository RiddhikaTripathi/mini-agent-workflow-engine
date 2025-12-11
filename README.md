# Minimal Agent Workflow Engine (FastAPI)

A lightweight, modular, and extensible workflow/graph engine — inspired by LangGraph — built as part of the AI Engineering Internship Assignment.

This project demonstrates:

- Clean backend architecture  
- Async Python patterns  
- A functional workflow engine with branching & looping  
- Clean FastAPI API design  
- Modular node registration system  
- Real execution logs and shared state transitions  

It includes a fully working example:  
### **Code Review Mini-Agent**  
that loops until the code's quality score reaches a defined threshold.

---

# 🚀 Features

### ✔ Workflow Engine  
- Nodes are simple Python functions (`@tool`)  
- Shared mutable state flows through nodes  
- Supports:
  - Sequential execution  
  - Conditional routing (`return {"next": "node"}`)  
  - Looping until condition met  
- Prevents infinite loops with a max steps safeguard  
- Each execution generates logs for transparency  

### ✔ Tool Registry  
Nodes self-register via:

```python
@tool("node_name")
async def my_node(state, tools):
    ...
```
## ✔ FastAPI APIs

- **POST /graph/create** → Register new workflows  
- **POST /graph/run** → Execute a workflow  
- **GET /graph/state/{run_id}** → Inspect logs and state of a run  

---

## ✔ Async Support

You can choose between:

- **Synchronous execution** (`async_run: false`)  
- **Background execution** (`async_run: true`)  

---

## ✔ Example Workflow Included

Implements **Option A: Code Review Mini-Agent** from the assignment:

1. Extract functions  
2. Compute complexity  
3. Detect issues  
4. Suggest improvements  
5. Loop until `quality_score >= threshold`  

---

## 📁 Project Structure
project/
│
├── app/
│ ├── main.py
│ │
│ ├── engine/
│ │ ├── graph_engine.py
│ │ ├── executor.py
│ │ └── registry.py
│ │
│ ├── nodes/
│ │ └── code_review_nodes.py
│ │
│ ├── routes/
│ │ └── graph_routes.py
│ │
│ ├── models/
│ │ └── schemas.py
│ │
│ └── config/
│ └── lifespan.py
│
├── requirements.txt
└── README.md


---

## 📂 Directory responsibilities

| Folder       | Purpose                                              |
|--------------|------------------------------------------------------|
| `engine/`    | Core workflow runtime (execution + registry + store) |
| `nodes/`     | Node implementations (“tools”)                       |
| `routes/`    | REST API endpoints                                   |
| `models/`    | Pydantic schemas                                     |
| `config/`    | Startup logic (sample graph registration)            |
| `main.py`    | Application entrypoint                               |

---

# 🧠 Architecture Overview

### 🔹 1. Node System

Each node receives:

- `state: dict`  
- `tools: dict` (registered functions)

Nodes may mutate state and must return:

```json
{"next": "<node_name>"}   // continue workflow
{"next": null}            // stop workflow
```
### 🔹 2. Graph Execution

The executor:

- Loads the graph configuration  
- Executes nodes step-by-step  
- Determines the next node via:  
  - Node return value  
  - **OR** fallback edges  
- Executes async node functions  
- Updates `RUNS[run_id]` with:  
  - current state  
  - logs  
  - status  
  - current node  

---

### 🔹 3. State Flow

Example of an evolving state:

```json
{
  "functions": [...],
  "issues": [],
  "suggestions": [],
  "quality_score": 75,
  "meta": { "iteration": 4 }
}
```
This structured state makes debugging and reasoning extremely easy.

---

## 🧪 How to Run

### 1️⃣ Install dependencies
```
pip install -r requirements.txt
```

### 2️⃣ Start FastAPI server
```
uvicorn app.main:app --reload
```

### 3️⃣ Open API docs

Visit:
```
http://localhost:8000/docs
```

Swagger UI allows you to test all endpoints interactively.

---

## 📝 Example Request: Run the Sample Graph 

**POST → `/graph/run`**

```
{
  "graph_id": "__sample__",
  "initial_state": {
    "code": "def foo():\n    pass\n\ndef bar(x):\n        for i in range(x):\n            print(i)"
  },
  "async_run": false
}
```
## Example Output (Actual)
```
{
  "status": "completed",
  "state": {
    "functions": [...],
    "issues": [],
    "suggestions": [],
    "quality_score": 80,
    "meta": { "iteration": 6 }
  },
  "log": [
    "Run started for graph __sample__",
    "Running node: extract_functions",
    "extract_functions -> check_complexity",
    "Running node: check_complexity",
    "check_complexity -> detect_issues",
    "...",
    "suggest_improvements -> None",
    "Execution completed successfully"
  ]
}
```
This demonstrates the full workflow running with multiple loops until the quality threshold is met.

## 🧱 Design Choices (Explained)
### ✔ Dictionary-based state

Easy to extend, serialize, mutate, and debug.

### ✔ ToolsRegistry as pluggable registry

Enables dynamic addition of tools, ideal for flexible agent-style execution.

### ✔ Pure Python functions as nodes

Lightweight and test-friendly — no class overhead.

### ✔ Separation of concerns

Clear, modular folder structure:

engine/

nodes/

models/

routes/

config/

### ✔ Lifespan hook for startup graph

Keeps main.py clean and reusable.

## 🔮 Potential Future Enhancements

Database persistence (SQLite/Postgres)

- Real-time WebSocket log streaming

- DAG visualization UI

- Role-based access control

- Safe sandbox execution for nodes

- Plugin architecture for custom nodes

- Additional workflows (summarization, data quality, etc.)

## 📦 Requirements
```
fastapi
uvicorn
pydantic
```
## 👤 Author
Riddhika Tripathi
