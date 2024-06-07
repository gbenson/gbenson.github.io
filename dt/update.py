import os
import requests
import sys

from urllib.parse import quote as urllib_quote

SHIELDS_PORT = 3000
SHIELDS = f"http://localhost:{SHIELDS_PORT}"


def quote(token):
    return "__".join(
        urllib_quote(piece, safe="")
        for piece in token.split("_")
    )


def get_badge(token, color, extra="?style=flat-square", timeout=5):
    basename = f"{quote(token)}-{color:06X}"
    url = f"{SHIELDS}/badge/{basename}{extra}"
    r = requests.get(url, timeout=5)
    r.raise_for_status()
    assert r.headers.get("content-type").startswith("image/svg")
    return basename, r.text


try:
    get_badge("hello world", 0xaaff00)
except requests.ConnectionError:
    print(f"no generator? run this:\n"
          f"docker run --rm -p {SHIELDS_PORT}:{SHIELDS_PORT} "
          f"--env PORT={SHIELDS_PORT} --name shields "
          f"gbenson/token-shields", file=sys.stderr)
    exit(1)


COLORS = [0xccbfee, 0xbeedc6, 0xf6d9ab, 0xf4aeb1, 0xa4dcf3]
TOKENS = [
    "<", "html", ">",
    "<", "head", ">",

    "<", "meta",
    "_", "http", "equiv",
    "=", "content", "type",
    "_", "content",
    "=", "text", "html", "charset", "UTF", "8", ">",

    "<", "meta",
    "_", "name",
    "=", "viewport",
    "_", "content",
    "=", "width", "device", "width", ">",

    "<", "title", ">",
    "hello", "world",
    "</", "title", ">",

    "<", "script", ">",
    "document", "getElementById", "demo", "innerHTML", "Hello",
    "JavaScript",
    "</", "script", ">",

    "...",
]

for i, token in enumerate(TOKENS):
    color = 0xffffff if token == "..." else COLORS[i % len(COLORS)]
    basename, imagedata = get_badge(token, color)
    basename, dirname = basename.split("-")
    dirname = dirname.lower()
    basename = basename.replace("%", "").replace("...", "dotdotdot")
    os.makedirs(dirname, exist_ok=True)
    filename = f"{dirname}/{basename}.svg"
    with open(filename, "w") as fp:
        fp.write(imagedata)
    url = f"https://gbenson.github.io/dt/{filename}"
    print(f"![{token}]({url})", end="")
print()
