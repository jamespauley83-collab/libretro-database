#!/usr/bin/env python3
"""Minimal web viewer for the libretro-database repository.

Serves a browsable directory listing of the repo contents on port 3000
so the database (CHT cheats, RDB files, DAT metadata) can be inspected
in a web preview.
"""

import html
import os
import posixpath
from http.server import HTTPServer, SimpleHTTPRequestHandler

REPO_ROOT = os.path.dirname(os.path.abspath(__file__))
PORT = int(os.environ.get("PORT", "3000"))


class DatabaseHandler(SimpleHTTPRequestHandler):
    """Serve files from REPO_ROOT with a clean directory listing."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=REPO_ROOT, **kwargs)

    def list_directory(self, path):
        """Override to produce a friendlier HTML listing."""
        try:
            entries = os.listdir(path)
        except OSError:
            self.send_error(404, "No permission to list directory")
            return None

        rel = os.path.relpath(path, REPO_ROOT)
        rel = "" if rel == "." else rel

        entries.sort(key=lambda e: (not os.path.isdir(os.path.join(path, e)), e.lower()))

        title = f"/{rel}" if rel else "/"
        rows = []
        if rel:
            rows.append(
                '<li><a href="../">../</a></li>'
            )
        for name in entries:
            full = os.path.join(path, name)
            href = name
            if os.path.isdir(full):
                href += "/"
                label = name + "/"
                icon = "\U0001F4C1"
            else:
                label = name
                ext = os.path.splitext(name)[1].lower()
                icon = {
                    ".cht": "\U0001F3AE",
                    ".rdb": "\U0001F4BE",
                    ".dat": "\U0001F4CA",
                    ".py": "\U0001F40D",
                    ".lua": "\U0001F40D",
                }.get(ext, "\U0001F4C4")
            rows.append(
                f'<li><span class="icon">{icon}</span> '
                f'<a href="{html.escape(href)}">{html.escape(label)}</a></li>'
            )

        body = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>libretro-database{html.escape(title)}</title>
<style>
  :root {{ --bg:#1a1a2e; --fg:#e0e0e0; --accent:#0f3460; --link:#4ea8de; --visited:#9d4edd; }}
  * {{ box-sizing:border-box; }}
  body {{ margin:0; font-family:system-ui,-apple-system,sans-serif; background:var(--bg); color:var(--fg); }}
  header {{ background:var(--accent); padding:1.5rem 2rem; }}
  header h1 {{ margin:0; font-size:1.4rem; }}
  header p {{ margin:.3rem 0 0; color:#a0a0c0; font-size:.85rem; }}
  .breadcrumb {{ padding:.8rem 2rem; font-size:.9rem; color:#888; }}
  .breadcrumb a {{ color:var(--link); text-decoration:none; }}
  main {{ padding:0 2rem 2rem; }}
  ul {{ list-style:none; padding:0; max-width:900px; }}
  li {{ padding:.4rem .6rem; border-bottom:1px solid #2a2a4e; }}
  li a {{ color:var(--link); text-decoration:none; }}
  li a:hover {{ text-decoration:underline; }}
  li a:visited {{ color:var(--visited); }}
  .icon {{ display:inline-block; width:1.6rem; }}
  footer {{ padding:1rem 2rem; color:#666; font-size:.8rem; }}
</style>
</head>
<body>
<header>
  <h1>Libretro Database</h1>
  <p>Cheat codes, game databases, and metadata for RetroArch</p>
</header>
<div class="breadcrumb">Path: {html.escape(title)}</div>
<main>
<ul>
{chr(10).join(rows)}
</ul>
</main>
<footer>Serving from libretro-database repository</footer>
</body>
</html>"""

        encoded = body.encode("utf-8", "surrogateescape")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)
        return None

    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        super().end_headers()


def main():
    server = HTTPServer(("0.0.0.0", PORT), DatabaseHandler)
    print(f"Serving libretro-database on http://0.0.0.0:{PORT}")
    server.serve_forever()


if __name__ == "__main__":
    main()
