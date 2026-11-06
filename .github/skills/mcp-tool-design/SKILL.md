---
name: mcp-tool-design
description: Hogyan írj jó MCP toolt a ci-tools szerverbe (FastMCP 4) – annotációk, audit, leírás, hibakezelés, dry-run, tiltások. Használd, ha a ci_tools_mcp/server.py-ban toolt írsz vagy javítasz.
---
# MCP tool írása – ellenőrzőlista

**Váz** (a fájl kész példa toolai szerint):
```python
@mcp.tool(annotations=READ)          # író toolnál: WRITE
@audited("read")                     # író toolnál: "write"
def get_log_excerpt(run_id: str, pattern: str = "", max_lines: int = 300) -> dict:
    """Az elbukott futás logjának releváns része.
    Mikor: ha a bukó teszt neve nem elég, vagy telepítési / konfigurációs hibát keresel.
    Vissza: {"lines": [...], "truncated": bool}. Legfeljebb max_lines sor."""
    return _get(f"/runs/{run_id}/log", params={"pattern": pattern, "max_lines": max_lines})
```

**A docstring a modell promptja:** mit ad vissza, *mikor* kell használni, és mi a korlátja. Egy mondat a „mikor”-ra
többet ér, mint a system prompt bármelyik bekezdése.

**Szabályok**
- Kevés, feladat-szintű tool – ne 1:1 REST-wrapper. Tömör kimenet (sorlimit), mert minden token a kontextusba megy.
- Hibánál strukturált válasz (`{"error": "...", "hint": "..."}`), ne kivétel – a modell tudjon belőle tovább lépni.
- Író tool (`create_issue`, `propose_patch`): `WRITE_MODE=dry-run` alapból; utasítsa el a titkot (`SECRET_RX`) tartalmazó
  szöveget és a tesztet törlő vagy kikapcsoló (`skip`, `xfail`) patch-et.
- Minden hívás az audit naplóba megy (`@audited`) – az eval ebből méri a safety-t.

**Ellenőrzés:** `uv run pytest -m "not level2"` → 32 passed; Inspector: `npx @modelcontextprotocol/inspector`,
Streamable HTTP, `http://localhost:8000/mcp`.
