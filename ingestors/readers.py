def read_text_file(path: str) -> str:
    with open(path, "r") as f:
        text = f.read()
    return text
