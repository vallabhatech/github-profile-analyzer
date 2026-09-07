from pathlib import Path
import re

USERNAME_RE = re.compile(r"^[A-Za-z0-9-]{1,39}$")

def parse_usernames(path: str) -> list[str]:
    seen = set()
    result = []
    for raw in Path(path).read_text(encoding="utf-8").splitlines():
        value = raw.strip()
        if "|" in value:
            value = value.strip("|").strip().split("|")[0].strip()
        if value.lower() in {"github username", "no username", "username"}:
            continue
        if set(value) <= set("-: "):
            continue
        if USERNAME_RE.fullmatch(value) and value not in seen:
            seen.add(value)
            result.append(value)
    return result
