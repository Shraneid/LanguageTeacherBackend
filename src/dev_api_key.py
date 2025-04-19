from pathlib import Path


def get_key():
    path = Path(__file__).parent / ".." / ".env.list"
    with open(path) as f:
        text = f.readline()
        return text.split("=")[1]