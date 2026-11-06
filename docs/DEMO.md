# Demó – csapatonként 5 perc

Négy rész, szerepenként egy ember mondja:

1. **Agent** – élőben egy rejtett hiba (az oktatók adják a run ID-t): `uv run python -m agent.run <run>` –
   milyen kategória, milyen bizonyíték (fájl, sor, idézet). – 2 perc
2. **n8n + Copilot** – ugyanez webhookból az n8n-ben (`uv run python scripts/simulate_failure.py <run>`), vagy a
   Copilot Build Doctor agent válasza. – 1 perc
3. **V&V** – a mérés: baseline → saját agent, a Definition of Done (1. szint) táblázata. – 1 perc
4. **MCP** – a toolok és egy korlát, amit megtaláltatok (miért döntöttetek így – ADR). – 1 perc

Ellenőrzőlista a demó előtt:
- [ ] `uv run pytest -m "not level2"` → 32 passed
- [ ] eval riport az `eval/results/` alatt, a DoD (1. szint) táblázattal
- [ ] az n8n starter flow egy webhookból végigfut
- [ ] `docs/adr/0001-*.md` és `docs/AGENT_CARD.md` (1. szint) kitöltve
