---
description: "Capstone – V&V szerep: mérés minden lépés után, saját tesztek, agent card"
agent: agent
---
A csapat V&V-s tagjának dolgozol. Fájlok: `tests/test_sajat.py`, `docs/SPEC.md`, `docs/AGENT_CARD.md`,
`docs/MERESEK.md`, `eval/results/`. Tartsd be az `AGENTS.md`-t.

1. `git pull --rebase`.
2. Első mérés: `uv run python -m eval.run_eval --impl baseline`. Hozd létre a `docs/MERESEK.md`-t egy táblázattal
   (időpont, impl, category_acc, evidence_valid, safety_violations, avg_steps, $/diagnózis, DoD) – ez az első sor.
3. Töltsd ki röviden a `docs/SPEC.md`-t (cél, bemenet, kimenet, NFR-ek) a `FELADATLEIRAS.md` alapján.
4. Írj **2 saját tesztet** LLM nélkül a `tests/test_sajat.py`-ba, például: nem létező run ID-re a mock CI 404-et ad;
   a `create_issue` elutasítja a tokent tartalmazó body-t (ez az MCP-s munkája után zöld). `uv run pytest tests/test_sajat.py`.
5. Ha a csapat agentje kész (`git pull`): `uv run python -m eval.run_eval --impl <név>` – új sor a táblázatba.
6. Töltsd ki a `docs/AGENT_CARD.md` 1. szintű részét a mért számokkal, és írd le, hol téved az agent.
7. Commit és push (`V&V: …`).
