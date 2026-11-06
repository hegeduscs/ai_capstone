---
description: "Capstone – MCP szerep: a ci-tools MCP szerver 1. szintje"
agent: agent
---
A csapat MCP-s tagjának dolgozol. Szerep: **MCP**, fájl: `ci_tools_mcp/server.py`. Tartsd be az `AGENTS.md`-t.

1. `git pull --rebase`.
2. Olvasd el a `ci_tools_mcp/server.py` TODO-it, a kész példa toolokat és a mock CI végpontjait (`mock_ci/app.py`).
3. Írd meg a hiányzó **read** toolokat: `get_log_excerpt`, `get_diff`, `get_recent_commits`, `read_file`,
   `search_code`, `get_test_history`. Mindegyik docstringje mondja meg a modellnek, **mikor és mire** használja.
4. Írd meg a két **write** toolt: `create_issue`, `propose_patch`. Alapból `WRITE_MODE=dry-run`; utasítsák el a titkot
   (tokent) tartalmazó szöveget és a tesztet törlő vagy kikapcsoló patch-et.
5. Ellenőrzés: `uv run pytest -m "not level2"` → **32 passed**. Ha piros: a kódot javítsd, ne a tesztet.
6. Commit és push az `AGENTS.md` „Közös munka” része szerint (`MCP: …`), és mondd: „Szóljatok a csapatnak: git pull,
   és indítsák újra az MCP szervert.”

Ne foglalkozz a `verify_patch`-csel, a commitonkénti diffel és a titokkitakarással – ez a 2. szint, otthonra.
