# Nexora
Next-generation AI assistant ( LLM + RAG + Tools + MCP + Memory + langsmith)
<!-- 

Nexora
│
├── .venv/             ← managed by uv
├── pyproject.toml     ← dependencies
├── uv.lock            ← exact dependency versions
├── backend/
├── frontend/
├── rag/
├── expense-tracker-mcp/
└── memory/

 -->

<!-- Install uv -->
curl -LsSf https://astral.sh/uv/install.sh | sh


<!-- Intialize -->
uv init

<!-- create venv -->
uv venv nexora --python 3.12.3

<!-- activate venv -->
source .venv/bin/activate

<!-- by default it create venv -->
<!-- uv add cmd can add dependncy directly to our venv even if venv is not activated but to execute or utilize those lib we need to activate the lib  or u can run uv run python app.py-->

                 ┌── activate .venv ──→ python app.py
uv add ──→ .venv ┤
                 └── uv run app.py     ← no activation needed


uv add fastapi

<!-- run app -->
uv run python app.py


<!-- to remove any lib -->
uv remove fastapi


<!-- fast api -->
uvicorn <filename_without_.py>:<FastAPI_variable> --reload
uvicorn fast-api:app --reload
uv run uvicorn backend.fast_api:app --reload
<!-- app = FastAPI() this is FastAPI_variable -->



we will run everthing from Nexora folder
