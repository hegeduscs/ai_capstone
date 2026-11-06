"""preToolUse hook: determinisztikus védőkorlát a coding agent köré.

stdin:  {"toolName": ..., "toolArgs": ...}  (Copilot preToolUse esemény)
stdout: {} (nincs döntés) | {"permissionDecision": "deny"|"ask", "permissionDecisionReason": "..."}
"""
import json
import re
import sys

DENY = [
    (r"git\s+push\b.*(?:\s-f\b|--force)", "Force push tilos – a csapat közös repójában mások munkáját írná felül."),
    (r"rm\s+-rf|Remove-Item\s+.*-Recurse", "Rekurzív törlés tiltott."),
    (r"(?:^|[\s/\\\"'])(?:scenarios|eval[/\\]cases)[/\\]", "A forgatókönyveket és a golden setet nem módosíthatja agent."),
    (r"@pytest\.mark\.skip|deleted file mode .*tests/", "Teszt kikapcsolása vagy törlése tiltott."),
]
ASK_TOOLS = ("create_issue", "propose_patch")
ASK = [(r"git\s+push\b", "Push a csapat közös repójába – nézd át, mit küld fel (csak a saját szereped fájljai?).")]


def main():
    try:
        event = json.load(sys.stdin)
    except json.JSONDecodeError:
        print("{}")
        return
    name = str(event.get("toolName", ""))
    args = json.dumps(event.get("toolArgs", ""), ensure_ascii=False)
    for rx, reason in DENY:
        if re.search(rx, args):
            print(json.dumps({"permissionDecision": "deny", "permissionDecisionReason": reason}, ensure_ascii=False))
            return
    for rx, reason in ASK:
        if re.search(rx, args):
            print(json.dumps({"permissionDecision": "ask", "permissionDecisionReason": reason}, ensure_ascii=False))
            return
    if name.endswith(ASK_TOOLS):
        print(json.dumps({"permissionDecision": "ask",
                          "permissionDecisionReason": "Mellékhatással járó MCP tool – nézd át a tartalmát."}, ensure_ascii=False))
        return
    print("{}")


if __name__ == "__main__":
    main()
