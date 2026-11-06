# Build Doctor – szabályok coding agenteknek (Copilot, Claude Code, Codex)

## Mi ez a repó?
Capstone projekt: agentic asszisztens, ami elbukott CI futások okát deríti ki.
- `mock_ci/` – hamis CI szerver (NE módosítsd a viselkedését a forgatókönyvekhez igazítva)
- `scenarios/` – generált CI futások (log, junit, overlay). **Kézzel nem szerkesztjük.**
- `target_repo/` – a "célrepó", aminek a buildje elbukik. **Nem javítjuk**, ez a vizsgált rendszer.
- `ci_tools_mcp/` – MCP szerver (a csapat írja)
- `agent/` – agent-implementációk; a szerződés: `agent/schema.py` (Diagnosis, Trace)
- `eval/` – golden set és eval-futtató; `tests/` – LLM nélküli tesztek

## Parancsok
- Telepítés: `uv sync --extra <smolagents|llamaindex|langgraph|all>`
- Tesztek (LLM nélkül): `uv run pytest`
- Mock CI: `docker compose up -d mock-ci` vagy `uv run uvicorn mock_ci.app:app --port 9000`
- MCP szerver: `uv run python -m ci_tools_mcp.server` (http://localhost:8000/mcp)
- Egy diagnózis: `uv run python -m agent.run r1001 --impl baseline`
- Eval (ma, 1. szint): `uv run python -m eval.run_eval --impl <impl>` – a végén a Definition of Done
- Eval (otthon, 2. szint): `uv run python -m eval.run_eval --impl <impl> --level 2 --repeat 2`
- Csak az 1. szintű MCP-tesztek: `uv run pytest -m "not level2"`

## Konvenciók
- Python 3.11+, típusannotáció mindenhol, `pydantic` modellek a határokon.
- MCP tool: `@mcp.tool(annotations=READ|WRITE)` + `@audited("read"|"write")`; a docstring a modellnek szól.
- Új tool vagy agent-viselkedés = új teszt a `tests/` alatt.
- Titok (API kulcs, token) soha nem kerül kódba, logba, promptba, diagnózisba vagy issue-ba. `.env` nincs commitolva.
- Javítás (`fix_patch`, `propose_patch`) csak `verify_patch`-csel ellenőrizve; a sandbox: `POST /runs/{id}/verify`.

## Tilos
- Tesztet törölni, `skip`-pelni vagy az elvárt értéket átírni, hogy zöld legyen.
- A `scenarios/` és `eval/cases/` tartalmát a saját agentedhez igazítani.
- Write toolt (create_issue, propose_patch) hívni diagnózis közben.
- Force push, vagy egy másik szerep fájljainak módosítása (lásd lent).

## Szerepek – ki melyik fájlon dolgozik
A felhasználó megmondja a szerepét (vagy elindítja a szerephez tartozó promptot: `.github/prompts/capstone-<szerep>.prompt.md`).
Csak az adott szerep fájljait módosítsd. Ha másik szerep fájlja is változna, állj meg és kérdezz.

| Szerep | Fájlok | Feladat (ma: 1. szint) |
|---|---|---|
| MCP | `ci_tools_mcp/server.py` | a hiányzó read és write toolok – `uv run pytest -m "not level2"` → 32 passed |
| Agent | `agent/impl_*.py`, `agent/prompts.py`, `docs/adr/0001-*.md` | egy keretrendszer befejezése, prompt, ADR |
| n8n + Copilot | `n8n/*.json`, `.github/agents/`, `.github/skills/` | a starter flow végigfut, a Copilot custom agent diagnosztizál |
| V&V | `tests/test_sajat.py`, `docs/SPEC.md`, `docs/AGENT_CARD.md`, `docs/MERESEK.md`, `eval/results/` | mérés minden lépés után, 2 saját teszt, agent card |

Közös fájlok (`agent/schema.py`, `pyproject.toml`, `uv.lock`, `AGENTS.md`): csak akkor nyúlj hozzájuk, ha a felhasználó
kifejezetten kéri – új függőséget ne vegyél fel.

## Közös munka (git) – ezt te intézed
A csapat egy közös repóban dolgozik, mindenki a saját gépén. A git-műveleteket te végzed, a felhasználó jóváhagyja a pusht.
1. **Munka előtt:** `git pull --rebase`.
2. **Minden kész, ellenőrzött lépés után** (a szerep ellenőrző parancsa zöld):
   - `git add` csak a szerep fájljaira – soha ne `git add -A` / `git add .`;
   - `git commit -m "<szerep>: <mit csináltál>"` (pl. `MCP: get_diff és read_file`);
   - `git pull --rebase`, majd `git push`.
3. **Ütközésnél:** ha a saját fájlodban van, oldd fel és futtasd újra az ellenőrzést; ha más fájljában, állj meg, és
   mondd el a felhasználónak, kivel kell egyeztetnie. Soha ne force pusholj, ne írd át más commitját.
4. **Pull után:** ha a `ci_tools_mcp/` változott, szólj: „Állítsd le és indítsd újra az MCP szervert.”
5. `.env`, `eval/results/` (kivéve, ha a V&V kéri), `audit/` nem kerül commitba.

## Munkamódszer: subagentek, MCP, skillek, memória
- **Subagentek** (`.github/agents/`): a fő szál tervez, átnéz, commitol – a munkát kiszervezi:
  `Doku-kutató` (Context7 / Microsoft Learn, kis modell), `Fejlesztő` (kódolás, közepes modell),
  `Tesztelő` (pytest, eval, a legkisebb modell). Független feladatokat párhuzamosan indíts; ugyanazt a fájlt két
  subagent soha ne írja egyszerre. A subagent rövid összefoglalót ad vissza – a fő szál kontextusa tiszta marad.
- **MCP** (`.vscode/mcp.json`): `ci-tools` (a CI), `context7` (könyvtár-dokumentáció – emlékezetből ne írj API-t),
  `microsoft-learn` (Azure).
- **Skillek** (`.github/skills/`): `ci-triage`, `mcp-tool-design`, `agent-prompting`, `n8n-flow`, `eval-measurement` –
  a szerephez tartozót töltsd be.
- **Memória:** ez a fájl mindig betöltődik (szabályok). A tanulságokat a repó-memóriába írd
  (`/memories/repo/<szerep>.md`) – a felhasználó a *Chat: Show Memory Files* paranccsal nézi meg.
