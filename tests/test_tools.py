from tools.terminal import run


def test_terminal_allowlist():
    result = run("python -c \"print(123)\"")
    assert result["returncode"] == 0
    assert "123" in result["stdout"]
