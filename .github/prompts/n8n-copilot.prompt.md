---
description: "Capstone – n8n + Copilot szerep: a flow végigfut, a Copilot custom agent diagnosztizál"
agent: agent
---
A csapat n8n + Copilot szerepű tagjának dolgozol. Fájlok: `n8n/*.json`, `.github/agents/`, `.github/skills/`.
Tartsd be az `AGENTS.md`-t. Az n8n felületét a felhasználó kezeli – te lépésenként mondd meg, mit kattintson.

1. `git pull --rebase`.
2. Indítsd el az agent API-t egy külön terminálban: `uv run uvicorn agent.api:app --port 8080 --host 0.0.0.0`
   (az n8n Dockerből a `host.docker.internal:8080`-on éri el). Az MCP szerver `MCP_HOST=0.0.0.0`-val fusson.
3. Vezesd végig a felhasználót: http://localhost:5678 → (első alkalommal helyi fiók) → *Import from file* →
   `n8n/build-doctor-starter.workflow.json` → *Publish*.
4. Próba: `uv run python scripts/simulate_failure.py r1003` – az n8n *Executions* listájában végigmegy a futás
   (webhook → agent → bizonyosság szerinti ág → issue vagy review sor, dry-run).
5. Copilot: *MCP: List Servers* → `ci-tools` → Start; a chatben a **Build Doctor** custom agent; kérdés:
   „Miért bukott el az r1003?” – bizonyítékkal kell válaszolnia.
6. Ha a csapat módosítja a flow-t: a felhasználó exportálja (*Download*) az `n8n/` mappába, te commitolod (`n8n: …`).
