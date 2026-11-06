---
name: capstone-vv
description: "Capstone – V&V szerep: mérés minden lépés után, saját tesztek, agent card"
agent: agent
---
A csapat **V&V** szerepű tagjának dolgozol. Fájlok: `tests/test_sajat.py`, `docs/SPEC.md`, `docs/AGENT_CARD.md`, `docs/MERESEK.md`, `eval/results/`. Tartsd be az `AGENTS.md`-t.
Skill: **`eval-measurement`** – töltsd be az elején.

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
   `eval-measurement` skill – írd ki a felhasználónak, mit látsz.
2. **Párhuzamosan, három szálon:**
   - `Tesztelő` → `uv run python -m eval.run_eval --impl baseline` (az első mérés),
   - `Fejlesztő` → 2 saját teszt LLM nélkül a `tests/test_sajat.py`-ba (a skill példái szerint),
   - te: a `docs/SPEC.md` rövid kitöltése (cél, bemenet, kimenet, szabályok) a `FELADATLEIRAS.md` alapján.
3. Hozd létre a `docs/MERESEK.md`-t a skill táblázatával; az első sor a baseline.
4. `Tesztelő` → `uv run pytest tests/test_sajat.py`.
5. Ha a csapat agentje kész (`git pull`): `Tesztelő` → `uv run python -m eval.run_eval --impl <név>` – új sor a táblázatba.
6. Töltsd ki a `docs/AGENT_CARD.md` 1. szintű részét a mért számokkal; commit és push (`V&V: …`).

**Memória (kötelező, a végén):**
1. Írd a repó-memóriába (`/memories/repo/vv.md`) 3–5 sorban: a bevált parancsok, a buktatók, mire figyeljen
   a következő session.
2. **Állj meg**, és kérd meg a felhasználót: futtassa a *Chat: Show Memory Files* parancsot, nyissa meg ezt a fájlt
   és az `AGENTS.md`-t, és mondja meg, mi a különbség a kettő között (mindig betöltődő szabály vs. tanult jegyzet).
   Csak a válasza után zárd le a feladatot.

Ha nem látod a subagent-toolt: a chatben *Configure Tools* → kapcsold be az `agent` (runSubagent) toolt.
