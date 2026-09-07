# GitHub Profile Analyzer

Bulk-analyze GitHub profiles and their public repositories from a username list, then export a sortable CSV and Excel report.

> **Important:** The score is a transparent heuristic for exploration. It is **not** a measure of developer quality, employability, or hiring suitability.

## Why this exists

Checking hundreds of GitHub profiles manually is slow. This tool turns a list of usernames into structured data so you can compare public signals such as followers, public repositories, stars, forks, languages, account age, and top repositories.

## Features

- Parse plain username lists and Markdown tables
- Remove duplicates and obvious placeholders
- Query public GitHub profile data through the GitHub API
- Collect repository-level stars, forks, and languages
- Identify up to five highest-starred repositories per profile
- Calculate a bounded 0–100 heuristic score
- Export both CSV and XLSX
- Retry common rate-limit responses
- Parallelize requests with a configurable worker count
- Keep tokens out of source control with environment variables

## Project structure

```text
github-profile-analyzer/
├── README.md
├── LICENSE
├── .gitignore
├── requirements.txt
├── .env.example
├── data/
│   └── usernames.example.txt
├── src/
│   ├── __init__.py
│   ├── analyzer.py
│   ├── exporter.py
│   ├── github_api.py
│   ├── parser.py
│   └── scoring.py
├── output/
│   └── .gitkeep
└── tests/
    ├── test_parser.py
    └── test_scoring.py
```

## Requirements

- Python 3.10+
- Internet access
- A GitHub personal access token is strongly recommended for larger batches because authenticated API requests have a higher rate limit than unauthenticated requests.

## Installation

### Windows PowerShell

```powershell
git clone https://github.com/vallabhatech/github-profile-analyzer.git
cd github-profile-analyzer
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### macOS / Linux

```bash
git clone https://github.com/vallabhatech/github-profile-analyzer.git
cd github-profile-analyzer
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## GitHub token

Set the token as an environment variable. Do **not** commit a real token.

PowerShell:

```powershell
$env:GITHUB_TOKEN="YOUR_TOKEN_HERE"
```

Command Prompt:

```cmd
set GITHUB_TOKEN=YOUR_TOKEN_HERE
```

The program only needs access to public GitHub data. Use the minimum permissions possible for your token and never paste the token into an issue, README, source file, or commit.

## Input format

Plain text is simplest:

```text
octocat
torvalds
gvanrossum
```

A Markdown table is also accepted:

```markdown
| GitHub Username |
|---|
| octocat |
| torvalds |
```

`data/usernames.example.txt` contains a tiny safe test list. For your real batch, save your cleaned usernames as `data/usernames.txt` locally. The parser also accepts your original Markdown table directly.

## Run

```powershell
python -m src.analyzer data/usernames.txt
```

Useful options:

```powershell
python -m src.analyzer data/usernames.txt --workers 4 --output-dir output
```

For a small test:

```powershell
python -m src.analyzer data/usernames.example.txt --workers 2
```

## Output

The analyzer writes:

```text
output/github_profiles.csv
output/github_profiles.xlsx
```

Important columns include:

| Column | Meaning |
|---|---|
| `username` | GitHub login |
| `name` | Public profile name |
| `bio` | Public profile bio |
| `profile_url` | GitHub profile URL |
| `followers` | Public follower count |
| `following` | Public following count |
| `public_repos` | Public repositories shown by the profile API |
| `total_stars` | Sum of stars across owned repositories retrieved by the tool |
| `total_forks` | Sum of forks across owned repositories retrieved by the tool |
| `languages` | Unique repository languages found |
| `account_created` | Account creation timestamp |
| `last_activity` | Profile update timestamp returned by GitHub |
| `top_repositories` | Up to five highest-starred repositories |
| `github_score` | 0–100 exploratory heuristic |
| `error` | Error information when a profile could not be analyzed |

## Scoring methodology

The score is intentionally simple and inspectable:

- Followers: small capped contribution
- Public repositories: contribution capped at 100 repositories
- Stars: contribution capped at 500 stars
- Forks: contribution capped at 200 forks
- Small bonuses for a public bio, company, and blog
- Final score is capped at 100

This prevents a single popular repository or a huge follower count from dominating the result. Use it only as a convenience for sorting profiles for manual review.

## API rate limits

Large batches can consume GitHub API quota quickly, especially because repository information is fetched for every username. Use an authenticated token, keep the worker count reasonable, and expect the run to take time for hundreds of accounts.

If GitHub returns a rate-limit response, the client waits and retries a limited number of times. A very large batch may still need to be split into smaller runs.

## Privacy and responsible use

This project reads public GitHub information. Use it responsibly:

- Respect GitHub's Terms and API limits.
- Do not use the score as an automated hiring or rejection decision.
- Do not infer sensitive characteristics from profiles.
- Do not collect or publish private information.
- Keep access tokens secret.
- Re-check important information directly on GitHub before making decisions.

## Limitations

- Only public GitHub API data is analyzed.
- Repository stars and forks are not a proxy for engineering ability.
- The repository list can require multiple API requests per user.
- GitHub API data changes over time.
- Deleted, suspended, renamed, or unavailable accounts may fail lookup.
- Language detection reflects GitHub's repository metadata rather than a detailed code audit.

## Testing

Run:

```powershell
python -m pytest
```

The tests cover username parsing and score bounds.

## Future improvements

- GitHub GraphQL support for more efficient queries
- Configurable scoring profiles
- Organization/team analysis
- Repository quality signals such as README presence and recent commits
- Retry/backoff telemetry and progress checkpoints
- SQLite storage for historical snapshots
- Optional web dashboard
- GitHub Actions scheduled analysis

## Contributing

1. Fork the repository.
2. Create a feature branch.
3. Add or update tests.
4. Run the test suite.
5. Open a pull request with a clear description.

## License

MIT License. See [LICENSE](LICENSE).
