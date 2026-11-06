---
name: capstone-n8n-copilot
description: "Capstone – n8n + Copilot szerep: a flow végigfut, a Copilot custom agent diagnosztizál"
agent: agent
---
A csapat **n8n + Copilot** szerepű tagjának dolgozol. Fájlok: `n8n/*.json`, `.github/agents/`, `.github/skills/`. Tartsd be az `AGENTS.md`-t.
Skill: **`n8n-flow`** – töltsd be az elején.

**Így dolgozz (ezt mutatjuk be):**
- **Subagentek:** a fő szál tervez, átnéz és commitol; a munkát kiszervezed – `Doku-kutató` (könyvtár-dokumentáció
  a Context7-ből, kis modell), `Fejlesztő` (kódolás, közepes modell), `Tesztelő` (tesztek, eval, a legkisebb modell).
  Ami független, azt **párhuzamosan** indítsd (egy üzenetben több subagent-hívás) – de két subagent soha ne írja
  ugyanazt a fájlt.
- **MCP:** könyvtár-API-hoz a Context7, a CI-hoz a `ci-tools` szerver.
- **Skill:** a szerepedhez tartozó skillt töltsd be (lent).
- **Memória:** a végén a tanulságot a repó-memóriába írod, és a felhasználó megnézi.

**Lépések:**
1. `git pull --rebase`. Nézd meg a References / Chat Debug nézetben, hogy betöltődött-e az `AGENTS.md` és az
   `n8n-flow` skill – írd ki a felhasználónak, mit látsz.
2. Indítsd el az agent API-t egy külön terminálban: `uv run uvicorn agent.api:app --port 8080 --host 0.0.0.0`;
   az MCP szerver `MCP_HOST=0.0.0.0`-val fusson.
3. **Párhuzamosan:** `Doku-kutató` → „n8n: Webhook node és HTTP Request node timeout, workflow publikálás” ·
   `Tesztelő` → `curl -s localhost:8080/health` és `curl -s localhost:9000/health` (él-e minden?).
4. Vezesd végig a felhasználót az n8n-ben (a skill lépései): import → Publish → próba:
   `uv run python scripts/simulate_failure.py r1003` → *Executions*.
5. Copilot: *MCP: List Servers* → `ci-tools` → Start; a chatben a **Build Doctor** custom agent: „Miért bukott el az r1003?”
   Mutasd meg a felhasználónak, melyik MCP toolokat hívta.
6. Ha a flow változott: a felhasználó exportálja az `n8n/` mappába, te commitolod és pusholod (`n8n: …`).

**Memória (kötelező, a végén):**
1. Írd a repó-memóriába (`/memories/repo/n8n-copilot.md`) 3–5 sorban: a bevált parancsok, a buktatók, mire figyeljen
   a következő session.
2. **Állj meg**, és kérd meg a felhasználót: futtassa a *Chat: Show Memory Files* parancsot, nyissa meg ezt a fájlt
   és az `AGENTS.md`-t, és mondja meg, mi a különbség a kettő között (mindig betöltődő szabály vs. tanult jegyzet).
   Csak a válasza után zárd le a feladatot.

Ha nem látod a subagent-toolt: a chatben *Configure Tools* → kapcsold be az `agent` (runSubagent) toolt.
