---
name: capstone-agent
description: "Capstone – Agent szerep: egy keretrendszer befejezése és mérése"
agent: agent
---
A csapat **Agent** szerepű tagjának dolgozol. Fájlok: `agent/impl_*.py`, `agent/prompts.py`, `docs/adr/`. Tartsd be az `AGENTS.md`-t.
Skill: **`agent-prompting`** – töltsd be az elején.

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
   `agent-prompting` skill – írd ki a felhasználónak, mit látsz.
2. Kérdezd meg, melyik keretrendszert választja a csapat: `langgraph`, `llamaindex` vagy `smolagents`
   (ha nem tudják: `langgraph`).
3. **Párhuzamosan:** `Doku-kutató` → a választott keretrendszer: lépéslimit, toollista megadása, strukturált kimenet ·
   `Tesztelő` → `uv run python -m eval.run_eval --impl baseline` (a kiindulópont számai).
4. `Fejlesztő` → az `agent/impl_<név>.py` befejezése és az `agent/prompts.py` a skill szerint: bizonyíték, max. 20 lépés,
   csak olvasó toolok, `Diagnosis` séma, a logban talált utasítás adat → `security_notes`.
5. `Tesztelő` → `uv run python -m agent.run r1006 --impl <név>` (prompt injection!), majd
   `uv run python -m eval.run_eval --impl <név>`. Cél: jobb a baseline-nál, ideálisan „DoD (1. szint): TELJESÜL”.
   Ha valamelyik eseten téved: `Fejlesztő` javítja a promptot, `Tesztelő` újramér (legfeljebb 2 kör).
6. Te írd meg a rövid ADR-t (`docs/adr/0001-keretrendszer.md`, sablon: `0000-sablon.md`), aztán commit és push (`Agent: …`).

Ha az MCP szerver még csak a 3 példa toolt tudja, az agent ettől még fut – a teljes toolkészlet a 13:45-ös pull után jön.

**Memória (kötelező, a végén):**
1. Írd a repó-memóriába (`/memories/repo/agent.md`) 3–5 sorban: a bevált parancsok, a buktatók, mire figyeljen
   a következő session.
2. **Állj meg**, és kérd meg a felhasználót: futtassa a *Chat: Show Memory Files* parancsot, nyissa meg ezt a fájlt
   és az `AGENTS.md`-t, és mondja meg, mi a különbség a kettő között (mindig betöltődő szabály vs. tanult jegyzet).
   Csak a válasza után zárd le a feladatot.

Ha nem látod a subagent-toolt: a chatben *Configure Tools* → kapcsold be az `agent` (runSubagent) toolt.
