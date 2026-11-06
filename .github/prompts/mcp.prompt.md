---
description: "Capstone – MCP szerep: a ci-tools MCP szerver 1. szintje"
agent: agent
---
A csapat **MCP** szerepű tagjának dolgozol. Fájlok: `ci_tools_mcp/server.py`. Tartsd be az `AGENTS.md`-t.
Skill: **`mcp-tool-design`** – töltsd be az elején.

**Így dolgozz (ezt mutatjuk be):**
- **Subagentek:** a fő szál tervez, átnéz és commitol; a munkát kiszervezed – `Doku-kutató` (könyvtár-dokumentáció
  a Context7-ből, kis modell), `Fejlesztő` (kódolás, közepes modell), `Tesztelő` (tesztek, eval, a legkisebb modell).
  Ami független, azt **párhuzamosan** indítsd (egy üzenetben több subagent-hívás) – de két subagent soha ne írja
  ugyanazt a fájlt.
- **MCP:** könyvtár-API-hoz a Context7, a CI-hoz a `ci-tools` szerver.
- **Skill:** a szerepedhez tartozó skillt töltsd be (lent).
- **Memória:** a végén a tanulságot a repó-memóriába írod, és a felhasználó megnézi.

**Lépések:**
1. `git pull --rebase`. Nézd meg a References / Chat Debug nézetben, hogy betöltődött-e az `AGENTS.md` és a
   `mcp-tool-design` skill – írd ki a felhasználónak, mit látsz.
2. **Párhuzamosan:** `Doku-kutató` → „FastMCP 4: tool-annotációk (readOnlyHint, destructiveHint) és tool-leírás” ·
   `Tesztelő` → `uv run pytest -m "not level2"` (kiinduló állapot: mi piros?).
3. `Fejlesztő` → a 6 **read** tool a `ci_tools_mcp/server.py`-ban: `get_log_excerpt`, `get_diff`, `get_recent_commits`,
   `read_file`, `search_code`, `get_test_history` (a skill szerint; a mock CI végpontjai a `mock_ci/app.py`-ban).
4. `Fejlesztő` → a 2 **write** tool: `create_issue`, `propose_patch` – dry-run alapból, titkot és teszttörlést elutasít.
5. `Tesztelő` → `uv run pytest -m "not level2"` → cél: **32 passed**. Ha piros: újra `Fejlesztő` a hibával – a kódot
   javítsa, ne a tesztet.
6. Nézd át a diffet (te, a fő szál), aztán commit és push az `AGENTS.md` szerint (`MCP: …`), és mondd:
   „Szóljatok a csapatnak: git pull, és indítsák újra az MCP szervert.”

Ne foglalkozz a `verify_patch`-csel, a commitonkénti diffel és a titokkitakarással – ez a 2. szint.

**Memória (kötelező, a végén):**
1. Írd a repó-memóriába (`/memories/repo/mcp.md`) 3–5 sorban: a bevált parancsok, a buktatók, mire figyeljen
   a következő session.
2. **Állj meg**, és kérd meg a felhasználót: futtassa a *Chat: Show Memory Files* parancsot, nyissa meg ezt a fájlt
   és az `AGENTS.md`-t, és mondja meg, mi a különbség a kettő között (mindig betöltődő szabály vs. tanult jegyzet).
   Csak a válasza után zárd le a feladatot.

Ha nem látod a subagent-toolt: a chatben *Configure Tools* → kapcsold be az `agent` (runSubagent) toolt.
