def github_score(profile: dict) -> int:
    """Transparent heuristic score; not a hiring or quality judgment."""
    score = 0
    score += min(profile.get("followers", 0), 1000) * 0.01
    score += min(profile.get("public_repos", 0), 100) * 0.5
    score += min(profile.get("total_stars", 0), 500) * 0.05
    score += min(profile.get("total_forks", 0), 200) * 0.1
    if profile.get("bio"):
        score += 2
    if profile.get("company"):
        score += 1
    if profile.get("blog"):
        score += 1
    return round(min(score, 100), 2)
