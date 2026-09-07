from src.scoring import github_score

def test_score_is_bounded():
    assert 0 <= github_score({}) <= 100
    assert github_score({"public_repos": 10, "followers": 100}) > 0
