import ast

def parse_code(code: str, filename: str = "main.py"):
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        return {"filename": filename, "error": str(e), "functions": [], "classes": [], "missing": [], "score": 0}
    functions = []
    classes = []
    missing = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            has_doc = ast.get_docstring(node) is not None
            args = [a.arg for a in node.args.args]
            functions.append({"name": node.name, "args": args, "docstring": ast.get_docstring(node) or "", "has_doc": has_doc, "line": node.lineno})
            if not has_doc:
                missing.append({"type": "function", "name": node.name, "line": node.lineno})
        if isinstance(node, ast.ClassDef):
            has_doc = ast.get_docstring(node) is not None
            methods = [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
            classes.append({"name": node.name, "methods": methods, "docstring": ast.get_docstring(node) or "", "has_doc": has_doc, "line": node.lineno})
            if not has_doc:
                missing.append({"type": "class", "name": node.name, "line": node.lineno})
    total = len(functions) + len(classes)
    documented = sum(1 for f in functions if f["has_doc"]) + sum(1 for c in classes if c["has_doc"])
    score = round((documented / total * 100) if total else 100, 1)
    return {"filename": filename, "functions": functions, "classes": classes, "missing": missing, "score": score, "total_items": total}

def to_markdown(result: dict) -> str:
    lines = [f"# Documentation for {result['filename']}", "", f"Quality Score: {result['score']}%", ""]
    lines.append("## Functions")
    for f in result["functions"]:
        lines.append(f"### {f['name']}({', '.join(f['args'])})")
        lines.append(f"{f['docstring'] or '_No documentation_'}")
        lines.append("")
    lines.append("## Classes")
    for c in result["classes"]:
        lines.append(f"### {c['name']}")
        lines.append(f"Methods: {', '.join(c['methods']) or 'none'}")
        lines.append(f"{c['docstring'] or '_No documentation_'}")
        lines.append("")
    lines.append("## Missing Documentation")
    for m in result["missing"]:
        lines.append(f"- {m['type']}: {m['name']} (line {m['line']})")
    return "\n".join(lines)
