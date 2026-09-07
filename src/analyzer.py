import argparse
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from .github_api import GitHubAPI
from .parser import parse_usernames
from .scoring import github_score
from .exporter import write_csv, write_xlsx

def analyze_one(username: str, token: str | None) -> dict:
    api = GitHubAPI(token)
    profile = api.profile(username)
    if not profile:
        return {"username": username, "error": "User not found"}
    repos = api.repositories(username)
    stars = sum(r.get("stargazers_count", 0) for r in repos)
    forks = sum(r.get("forks_count", 0) for r in repos)
    langs = sorted({r.get("language") for r in repos if r.get("language")})
    top = sorted(repos, key=lambda r: (r.get("stargazers_count", 0), r.get("forks_count", 0)), reverse=True)[:5]
    row = {
        "username": profile.get("login"), "name": profile.get("name") or "", "bio": profile.get("bio") or "",
        "profile_url": profile.get("html_url"), "location": profile.get("location") or "", "company": profile.get("company") or "",
        "blog": profile.get("blog") or "", "followers": profile.get("followers", 0), "following": profile.get("following", 0),
        "public_repos": profile.get("public_repos", 0), "total_stars": stars, "total_forks": forks,
        "languages": ", ".join(langs), "account_created": profile.get("created_at", ""),
        "last_activity": profile.get("updated_at", ""),
        "top_repositories": "; ".join(f"{r['name']} ({r.get('stargazers_count',0)}★)" for r in top),
    }
    row["github_score"] = github_score(row)
    return row

def main():
    parser = argparse.ArgumentParser(description="Bulk analyze GitHub profiles and repositories.")
    parser.add_argument("input", help="Text/Markdown file containing GitHub usernames")
    parser.add_argument("--output-dir", default="output")
    parser.add_argument("--workers", type=int, default=4)
    args = parser.parse_args()
    token = os.getenv("GITHUB_TOKEN")
    usernames = parse_usernames(args.input)
    if not usernames: raise SystemExit("No valid GitHub usernames found in input.")
    rows = []
    with ThreadPoolExecutor(max_workers=max(1, min(args.workers, 8))) as pool:
        futures = {pool.submit(analyze_one, u, token): u for u in usernames}
        for i, future in enumerate(as_completed(futures), 1):
            username = futures[future]
            try: rows.append(future.result())
            except Exception as exc: rows.append({"username": username, "error": str(exc)})
            print(f"[{i}/{len(usernames)}] {username}")
    rows.sort(key=lambda r: r.get("github_score", 0), reverse=True)
    out = Path(args.output_dir)
    write_csv(rows, out / "github_profiles.csv")
    write_xlsx(rows, out / "github_profiles.xlsx")
    print(f"Analyzed {len(rows)} profiles. Results: {out}/github_profiles.csv and {out}/github_profiles.xlsx")

if __name__ == "__main__": main()
