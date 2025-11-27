# IT Helpdesk Automation Agent (Intermediate PoC)

This repo is a self-contained proof-of-concept multi-agent IT Helpdesk Automation system.
It includes:
- Coordinator + Triage + Diagnostics + Fix + Knowledge agents
- Mock MCP servers: ping, system_info, log_search, restart_service
- Simple memory (data files)
- Observability: trace JSON files per ticket
- Demo runner and Kaggle-notebook-compatible cells

## Quick start (local)
1. Ensure Python 3.9+ is installed.
2. Create and activate a virtualenv (recommended).
3. Install requirements:
   pip install -r requirements.txt
4. In one terminal start the mock MCP servers:
   python mcp_servers/ping_server.py
   python mcp_servers/system_info_server.py
   python mcp_servers/log_search_server.py
   python mcp_servers/restart_service_server.py
5. In another terminal run the demo driver:
   python agents/run_demo.py
6. Inspect outputs in:
   - observability/traces/
   - outputs/results.json

## Kaggle
- Upload this repo (or essential files) to a Kaggle dataset and use the provided notebook cells (see notebooks/kaggle_notebook_cells.py)
- On Kaggle, start mock servers via background cell code (or simulate responses).

## Files of interest
- agents/* : agent logic
- mcp_servers/* : simulated MCP tools
- data/* : tickets, KB, logs
- observability/* : tracing helper
- outputs/* : generated results after run_demo

## Design notes
- This is a PoC. MCP servers are simulated as simple HTTP APIs (Flask).
- restart_service is considered "destructive" and the Fix Agent marks it as requiring manual approval.
- No LLM is required to run PoC. You can optionally plug an LLM for richer triage using triage_agent.py.

## License
MIT
