from app.services.parser import parse_code, to_markdown

def test_parse_detects_function():
    r = parse_code("def add(a, b):\n    \"\"\"Add.\"\"\"\n    return a+b", "x.py")
    assert len(r["functions"]) == 1
    assert r["functions"][0]["name"] == "add"
    assert r["score"] == 100.0

def test_missing_doc():
    r = parse_code("def foo():\n    pass", "x.py")
    assert len(r["missing"]) == 1
    assert r["score"] == 0.0

def test_syntax_error():
    r = parse_code("def broken(:", "x.py")
    assert "error" in r

def test_no_invented_functions():
    r = parse_code("def real():\n    pass", "x.py")
    names = [f["name"] for f in r["functions"]]
    assert names == ["real"]

def test_markdown_export():
    r = parse_code("def add(a, b):\n    \"\"\"Add.\"\"\"\n    return a+b", "x.py")
    md = to_markdown(r)
    assert "add" in md and "Quality Score" in md
