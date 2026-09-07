from src.parser import parse_usernames

def test_parse_markdown_table(tmp_path):
    p = tmp_path / "users.md"
    p.write_text("| GitHub Username |\n|---|\n| alice |\n| No username |\n| alice |\n| bad_user |\n", encoding="utf-8")
    assert parse_usernames(str(p)) == ["alice"]
