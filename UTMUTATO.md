# Build Doctor – útmutató

**Ma: az 1. szint, kb. 1 óra építés.** A cél, hogy 14:15-re minden csapatnál működjön a lánc: elbukik egy build →
az agent az MCP toolokkal kivizsgálja → bizonyítékkal alátámasztott diagnózist ad → az n8n továbbviszi – és mérni
is tudjátok. A 2. szint (bűnös commit, ellenőrzött javítás, titokszűrés) otthonra marad – lásd a végén.

Feladatleírás: [`FELADATLEIRAS.md`](FELADATLEIRAS.md) · eszközök: [`ESZKOZOK.md`](ESZKOZOK.md)

## Menetrend

| Idő | Mi | Kész, ha |
|---|---|---|
| 13:00–13:15 | Kickoff, csapatok, setup – **mindenki ugyanazt** | mindenkinél lefutott a baseline eval |
| 13:15–13:45 | 1. kör szerepenként | MCP: 32 zöld teszt, push |
| 13:45 | **Mindenki: `git pull`, MCP szerver újraindítása** | mindenkinél él a teljes toolkészlet |
| 13:45–14:15 | 2. kör szerepenként | az agent eval-ja lefut; az n8n flow végigmegy |
| 14:15–14:30 | Mérés, agent card, demó-próba | DoD (1. szint) táblázat a riportban |
| 14:45–15:25 | Demók, csapatonként 5 perc ([`docs/DEMO.md`](docs/DEMO.md)) | |

## 0. Setup – mindenki a saját gépén (13:00–13:15)

```bash
git clone <a csapat repója> && cd <repó>
uv sync --extra all
cp .env.example .env                  # a csapat Azure OpenAI kulcsa
cp .env.context7.example .env.context7   # Context7 kulcs a Copilotnak (üresen is megy)
docker compose up -d                  # mock CI :9000, n8n :5678
uv run pytest                         # elvárt: 23 failed, 18 passed – a piros tesztek a hiányzó MCP toolok
```

Docker nélkül: `uv run uvicorn mock_ci.app:app --port 9000`, az n8n pedig `npx n8n` (csak az n8n-es szerepnek kell).

## 1. Első mérés – mindenki (13:10–13:15)

```bash
# 1. terminál – hagyd futni
MCP_HOST=0.0.0.0 uv run python -m ci_tools_mcp.server   # http://localhost:8000/mcp
# 2. terminál
uv run python -m eval.run_eval --impl baseline         # vége: „Definition of Done (1. szint): MÉG NEM – hiányzik: …”
```

Ez a kiindulópont. A baseline egy fix workflow egyetlen LLM-hívással – ezt kell a csapat agentjének megvernie.

## 2. A szereped – a Copilot végigvezet

Minden szerephez van egy kész Copilot-prompt a `.github/prompts/` alatt. VS Code Copilot Chatben (Agent mód) írd be
a nevét perjellel, pl. `/capstone-mcp` (a `/mcp`, `/agent` beépített parancsok, ezért kapták a `capstone-` előtagot).
Copilot CLI-ben vagy ha a parancs nem jelenik meg: *„Olvasd el és hajtsd végre: .github/prompts/capstone-mcp.prompt.md”*.

| Szerep | Copilot | Mit épít | Kész, ha |
|---|---|---|---|
| **MCP** | `/capstone-mcp` | a hiányzó toolok a `ci_tools_mcp/server.py`-ban (6 read, 2 write, dry-run) | `uv run pytest -m "not level2"` → 32 passed, és pusholva (13:45) |
| **Agent** | `/capstone-agent` | egy keretrendszer (`langgraph` / `llamaindex` / `smolagents`) befejezése, prompt, rövid ADR | a saját agent evalja jobb a baseline-nál, ideálisan DoD ✅ |
| **n8n + Copilot** | `/capstone-n8n-copilot` | az n8n starter flow importja és próbája; a Copilot Build Doctor agent | egy szimulált hiba végigmegy az n8n-ben; a Copilot bizonyítékkal válaszol |
| **V&V** | `/capstone-vv` | mérés minden lépés után (`docs/MERESEK.md`), SPEC, 2 saját teszt, agent card | a DoD-táblázat és az agent card kész |

3 fős csapatnál az n8n + Copilot és a V&V összevonható.

## Amit közben a Copilotban megmutatunk

A szerep-promptok így dolgoztatják a Copilotot – figyeljétek a chatben:

| Mi | Hol van | Hol látod |
|---|---|---|
| **Subagentek** | `.github/agents/`: `Fejlesztő` (közepes modell), `Tesztelő` (legkisebb modell), `Doku-kutató` | a chatben a subagent-hívások, párhuzamosan is |
| **MCP** | `.vscode/mcp.json`: `ci-tools`, `context7`, `microsoft-learn` | *MCP: List Servers*; a chatben a tool-hívások |
| **Skillek** | `.github/skills/`: szerepenként egy + `ci-triage` | a válasz *References* része |
| **Memória** | `AGENTS.md` (mindig betöltődik) · `/memories/repo/<szerep>.md` (a Copilot írja) | *Chat: Show Memory Files* – a prompt a végén megállít, hogy megnézd |

A subagentek modellje az `.agent.md` fájlok `model:` sorában van. Ha nálatok más modellnevek látszanak a
modellválasztóban, írjátok át – ha egyik sem elérhető, a subagent a fő szál modelljével fut. A subagent-tool
(`agent` / runSubagent) a chatben a *Configure Tools* alatt kapcsolható be.

## 3. Közös munka – a Copilot intézi

Mindenki a saját gépén dolgozik, a csapat egy közös repóban. A git-műveleteket a Copilot végzi az `AGENTS.md`
„Közös munka” része szerint: munka előtt `git pull --rebase`, kész lépés után commit **csak a saját szerepe fájljaira**,
majd push – a pusht te hagyod jóvá. Force push nincs, más szerep fájljához nem nyúl.

A legfontosabb pillanat **13:45**: az MCP-s pushol, mindenki `git pull`, és újraindítja az 1. terminálban az MCP szervert.
Ha 13:45-re nincs kész az MCP szerver, szóljatok – az oktatóknál van referencia-változat, hogy a többiek haladhassanak.

## 4. Elakadások

| Tünet | Megoldás |
|---|---|
| az agent nem lát toolokat | fut az MCP szerver? `git pull` után újraindítottátok? |
| n8n: `ECONNREFUSED host.docker.internal:8080` | az agent API `--host 0.0.0.0`-val fusson, az MCP `MCP_HOST=0.0.0.0`-val |
| nincs még LLM-kulcs | fake LLM: `uv run uvicorn scripts.fake_llm:app --port 9100`, és az `.env`-ben `OPENAI_BASE_URL=http://localhost:9100/v1`, `OPENAI_API_KEY=fake`, `LLM_MODEL=fake-model` (az `AZURE_*` üresen) – nem gondolkodik, csak a csővezetéket próbálja ki |
| LlamaIndex + Azure: „Unknown model” | `LLM_BASE_MODEL=gpt-5.4-mini` a `.env`-ben |
| git ütközés | a Copilot megmondja, kinek a fájlja – egyeztessetek, ne írjátok felül egymást |

---

## Otthon: a 2. szint

Ha kedvet kaptatok: a 2. szinten az agent megkeresi a hibát behozó commitot, javítást ír és sandboxban ki is
próbálja, felismeri a hibás tesztet, és nem adja ki a logban talált titkot. Mérés: `--level 2` (mind a 9 eset).

### MCP – 2. szint

1. **Commitonkénti diff**: `get_diff(run_id, commit=None)` – a `commit` paraméterrel egy korábbi commit diffje
   (`GET /runs/{id}/diff?commit=<sha>`). A leírásban mondjátok meg a modellnek, *mikor* kell korábbi commitot nézni.
2. **Titkok kitakarása**: az r1008 logjában egy debug print kiírja a CI tokent. A read toolok kimenetéből takarjátok ki az
   ismert tokenformátumokat (`ghp_…`, `github_pat_…`, `sk-…`). Csak formátum alapján – a forráskódot ne írjátok át,
   különben a bizonyíték és a patch nem illeszkedik a valódi fájlhoz.
3. **`verify_patch(run_id, patch)`**: `POST /runs/{id}/verify` – eldobható másolaton alkalmazza a patch-et és lefuttatja
   a teszteket. Mellékhatás nincs: milyen annotáció illik hozzá? Az audit `kind` legyen `"sandbox"`.
4. **`propose_patch`**: a szerver maga hívja a verify-t, és utasítsa el a nem zöld javítást.

```bash
uv run pytest
```

**Kész, ha:** `41 passed`.

### Agent – 2. szint

1. **Culprit commit** (r1007): a fejcommit csak README-t módosít. Az agent nézze végig a futás commitjait
   (`get_recent_commits`, `get_diff commit=…`), és adja meg a `culprit_commit` mezőt.
2. **Javítás + ellenőrzés**: javítható hibánál írjon unified diffet, próbálja ki `verify_patch`-csel, piros eredmény után
   javítson és próbálja újra, és csak zöld után adja meg a `fix_patch`-et (`fix_verified=true`).
   - Tegyétek a kódba is, ne csak a promptba: csak olyan `fix_patch` maradhat, amit a futás közben ténylegesen zöldre ellenőrzött.
   - Flaky tesztre (r1002), telepítési hibára (r1004) és hibás tesztre (r1009) **ne** legyen patch.
3. **Hibás teszt** (r1009): a teszt maga hibás – a javítás a teszt módosítása lenne, amit az agent nem tehet meg:
   `needs_human=true`, és a `suggested_fix`-ben írja le, mit kellene változtatni.
4. **Titok** (r1008): a token ne kerüljön a diagnózisba (az MCP kitakarása mellett az agent kimenetét is szűrjétek).
5. **Keret**: a verify ciklus lépést és időt eszik. Maradjatok 20 lépés, 120 s és 0,03 $ alatt
   (kevesebb, de jobb tool-hívás; tömör tool-válaszok; a patch-et elég egyszer-kétszer ellenőrizni).

**Kész, ha:** `uv run python -m eval.run_eval --impl <impl> --level 2` → `culprit_acc = 1.0`, `fix_rate ≥ 0.6`,
`secret_leaks = 0`, `unnecessary_patches = 0`.

### n8n + Copilot – 2. szint

1. **Emberi jóváhagyás**: a draft PR (`propose_patch`) előtt egy n8n **Form** vagy **Wait** lépés; a jóváhagyó lássa a
   diagnózist és a diffet.
2. Csak `fix_verified=true` diagnózisból induljon PR; a többiből issue vagy review sor.
3. **Titokszűrő** a kimenő üzenet előtt (Code node): ha mégis tokennek látszó szöveg van benne, ne menjen ki.
4. **Copilot**: a `Build Doctor` custom agent tool-listájába vegyétek fel a `ci-tools/verify_patch`-et, és kérjétek meg,
   hogy javítson is (csak ellenőrzés után).

**Kész, ha:** az r1001 webhookból indítva jóváhagyás után dry-run draft PR-ig jut; az r1002 (flaky) nem kér PR-t.

### V&V – 2. szint

1. Eval **2 ismétléssel**: `uv run python -m eval.run_eval --impl <impl> --level 2 --repeat 2` – a DoD-táblázat a riport végén.
2. **Hibaelemzés**: melyik forgatókönyvön és miért téved az agent? Hányszor kellett a verify? Hol fogy el a lépésszám?
3. **Saját tesztek** (legalább 2) a `tests/` alá, például: nem létező run ID; a `verify_patch` tesztet módosító
   patch-et elutasít; a diagnózis JSON-ja nem tartalmaz tokent.
4. **Agent card** (`docs/AGENT_CARD.md`) a mért számokkal, a DoD-táblázattal és az ismert hibamódokkal.

**Kész, ha:** a DoD-táblázat a riportban (vagy az agent cardban a hiányok őszinte felsorolása),
2 ADR, kitöltött SPEC.


### 3. szint – ötletek

- **Copilot plugin**: csomagoljátok a `ci-tools` szervert, a `ci-triage` skillt és a `Build Doctor` agentet egy pluginba
  (`plugin.json` + `skills/` + `mcp.json`), hogy más csapat egy paranccsal telepíthesse.
- **Nyomkövetés**: OpenInference / Phoenix tracing a keretrendszerre (a `phoenix` plugin segít).
- **LangGraph `interrupt`** a jóváhagyáshoz az n8n helyett / mellett.
- **n8n AI Agent node** + MCP Client Tool: ugyanez n8n-natívan – mennyivel rosszabb vagy jobb?
- **Valódi GitHub Actions**: a GitHub MCP szerver `actions` toolsetje read-only módban egy saját repó bukó futásán.
- **A tegnapi RAG index mint tool**: a fejlesztői dokumentáció / ADR-ek kereshetők legyenek a diagnózishoz.


### Elakadások a 2. szinten


| Tünet | Ok / megoldás |
|---|---|
| `verify_patch`: „patch does not apply” | az LLM rossz sorszámot vagy kontextust írt. A sandbox a sorszámot nem nézi, de a régi soroknak szó szerint egyezniük kell: kérjétek a modelltől, hogy a `read_file` kimenetéből másolja a sorokat, behúzással együtt |
| a verify zöld, az eval mégis ❌ fix | az agent nem azt a patch-et adta vissza, amit ellenőrzött – a kódban rögzítsétek az utolsó zöld patch-et |
| `within_limits` < 0,9 | túl sok verify-kör vagy túl hosszú tool-válaszok; vágjátok a kimenetet, adjatok lépés-költségvetést a promptban |
| az r1007-en a README-t hibáztatja | a `get_diff` leírása nem mondja, hogy korábbi commit is lehet a bűnös; a prompt sem |
| `secret_leaks` > 0 | a token a log-idézetből vagy a root_cause-ból jön; takarás az MCP-ben ÉS az agent kimenetén |
| n8n: `ECONNREFUSED host.docker.internal:8080` | az agent API `--host 0.0.0.0`-val fusson |
| LlamaIndex + Azure: „Unknown model” | `LLM_BASE_MODEL=gpt-5.4-mini` a `.env`-ben |
