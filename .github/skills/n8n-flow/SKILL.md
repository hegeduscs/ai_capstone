---
name: n8n-flow
description: Az n8n starter workflow importja, próbája és exportja a Build Doctorhoz, és a tipikus hibák (host.docker.internal, publish, webhook). Használd, ha az n8n-ben kell valamit beállítani vagy a flow nem fut végig.
---
# n8n – Build Doctor flow

**A lánc:** mock CI webhook → n8n *Webhook* → *HTTP Request* `POST http://host.docker.internal:8080/diagnose` →
*IF* (magas bizonyosság, nincs gyanú?) → issue (automatikus, dry-run) vagy review sor.

**Lépések (a felhasználó kattint, te mondod):**
1. Agent API: `uv run uvicorn agent.api:app --port 8080 --host 0.0.0.0`; MCP szerver: `MCP_HOST=0.0.0.0 uv run python -m ci_tools_mcp.server`.
2. http://localhost:5678 → első alkalommal helyi fiók (bármilyen e-mail) → *Workflows* → *Import from file* →
   `n8n/build-doctor-starter.workflow.json`.
3. *Publish* (különben a production webhook nem él).
4. Próba: `uv run python scripts/simulate_failure.py r1003` → *Executions*: minden node zöld?
5. Módosítás után: *Download* → mentés az `n8n/` mappába → commit.

**Hibák**
| Tünet | Ok |
|---|---|
| `ECONNREFUSED host.docker.internal:8080` | az agent API nem `0.0.0.0`-n fut, vagy nem fut |
| a webhook 404 | a workflow nincs publikálva, vagy a teszt-URL-t hívod |
| az agent hívása időtúllépés | az n8n HTTP node timeoutja < agent futásidő – emeld 120 s-ra |
| az agent nem lát toolt | az MCP szerver nem fut, vagy nem `MCP_HOST=0.0.0.0` |
