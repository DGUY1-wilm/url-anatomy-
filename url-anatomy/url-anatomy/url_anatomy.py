"""url-anatomy: break a URL into its parts and explain what each one means.

Usage:
    python url_anatomy.py "https://example.com/path?x=1#top"
    python url_anatomy.py --simple
    python url_anatomy.py --complex
"""
import argparse
from urllib.parse import urlsplit, parse_qsl, unquote

# Tiny sample of multi-label public suffixes. For full accuracy use the
# Public Suffix List (https://publicsuffix.org).
TWO_PART_SUFFIXES = {"co.uk", "org.uk", "ac.uk", "gov.uk", "com.au", "co.jp", "co.nz", "com.br"}

DEFAULT_PORTS = {"http": 80, "https": 443, "ftp": 21, "ssh": 22, "ws": 80, "wss": 443}

SIMPLE_EXAMPLE = "https://www.example.com/blog/hello-world"
COMPLEX_EXAMPLE = (
    "https://user:secret@shop.eu.example.co.uk:8443"
    "/products/shoes/running%20shoes/index.html;session=abc"
    "?q=red+shoes&page=2&tag=sale&tag=new&lang=en#reviews"
)


def analyze(url):
    """Return a list of (part, value, explanation) tuples for the given URL."""
    p = urlsplit(url)
    rows = []

    if p.scheme:
        note = "The protocol used to talk to the server."
        if p.scheme == "https":
            note += " HTTPS means the connection is encrypted."
        elif p.scheme == "http":
            note += " HTTP is unencrypted."
        rows.append(("scheme", p.scheme, note))

    if p.username:
        rows.append(("username", p.username, "Login name embedded in the URL (rarely used, discouraged)."))
    if p.password:
        rows.append(("password", p.password, "Password in plain text. Never put real secrets in URLs!"))

    if p.hostname:
        rows.append(("host", p.hostname, "The server's address on the internet."))
        labels = p.hostname.split(".")
        if len(labels) >= 2:
            suffix_len = 2 if ".".join(labels[-2:]) in TWO_PART_SUFFIXES else 1
            suffix = ".".join(labels[-suffix_len:])
            rows.append(("  suffix", suffix, "Top-level domain / public suffix (e.g. com, co.uk)."))
            if len(labels) > suffix_len:
                rows.append(("  domain", labels[-suffix_len - 1],
                             "The registrable name you would buy from a registrar."))
                if len(labels) > suffix_len + 1:
                    rows.append(("  subdomain", ".".join(labels[:-suffix_len - 1]),
                                 "Everything left of the domain; often selects a site section or server."))

    if p.port:
        rows.append(("port", str(p.port), "The network door on the server to connect to."))
    elif p.scheme in DEFAULT_PORTS:
        rows.append(("port", f"(implied {DEFAULT_PORTS[p.scheme]})",
                     f"Not written, so the default for {p.scheme} is used."))

    if p.path:
        rows.append(("path", p.path, "Which resource on the server you want."))
        path = p.path
        params = ""
        if ";" in path.rsplit("/", 1)[-1]:
            path, params = path.rsplit(";", 1)
        segments = [s for s in path.split("/") if s]
        for i, seg in enumerate(segments, 1):
            decoded = unquote(seg)
            extra = f" (decoded from '{seg}')" if decoded != seg else ""
            is_file = i == len(segments) and "." in decoded
            kind = "file" if is_file else "segment"
            what = "The file being requested" if is_file else "One level of the path"
            rows.append((f"  {kind} {i}", decoded, f"{what}{extra}."))
        if params:
            rows.append(("  path params", params, "Legacy ';key=value' data attached to a path segment."))

    if p.query:
        rows.append(("query", p.query, "Extra key=value inputs, separated by '&'."))
        for key, value in parse_qsl(p.query):
            rows.append((f"  {key}", value, "A query parameter ('+' and %XX are decoded to text)."))

    if p.fragment:
        rows.append(("fragment", p.fragment,
                     "Points to a spot inside the page. Never sent to the server; the browser handles it."))

    return rows


def render(url):
    lines = [f"URL: {url}", "-" * 60]
    for part, value, note in analyze(url):
        lines.append(f"{part:<16} {value}")
        lines.append(f"{'':<16} -> {note}")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description="Explain the parts of a URL.")
    ap.add_argument("url", nargs="?", help="URL to analyze")
    ap.add_argument("--simple", action="store_true", help="run the simple example")
    ap.add_argument("--complex", action="store_true", help="run the complex example")
    args = ap.parse_args()

    if args.simple:
        print(render(SIMPLE_EXAMPLE))
    elif args.complex:
        print(render(COMPLEX_EXAMPLE))
    elif args.url:
        print(render(args.url))
    else:
        ap.print_help()


if __name__ == "__main__":
    main()
