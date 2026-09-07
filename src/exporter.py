import csv
from pathlib import Path

FIELDS = [
    "username", "name", "bio", "profile_url", "location", "company", "blog",
    "followers", "following", "public_repos", "total_stars", "total_forks",
    "languages", "account_created", "last_activity", "top_repositories", "github_score", "error"
]

def write_csv(rows: list[dict], path: str) -> None:
    target = Path(path); target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS, extrasaction="ignore")
        writer.writeheader(); writer.writerows(rows)

def write_xlsx(rows: list[dict], path: str) -> None:
    from openpyxl import Workbook
    target = Path(path); target.parent.mkdir(parents=True, exist_ok=True)
    wb = Workbook(); ws = wb.active; ws.title = "Profiles"
    ws.append(FIELDS)
    for row in rows: ws.append([row.get(k, "") for k in FIELDS])
    ws.freeze_panes = "A2"; ws.auto_filter.ref = ws.dimensions
    for column in ws.columns:
        letter = column[0].column_letter
        width = min(max(len(str(cell.value or "")) for cell in column) + 2, 45)
        ws.column_dimensions[letter].width = width
    wb.save(target)
