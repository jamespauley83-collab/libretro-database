# AGENTS.md

## Project Overview

This is the **libretro-database** repository — a data repository for RetroArch
containing cheat files (`.cht`), compiled database files (`.rdb`), DAT metadata
files (`.dat`), cursors, and maintenance scripts. It is **not** a web application;
it has no package.json, no frontend, and no backend.

## Why It "Failed to Start"

The repository contains only data files. There was no web server to serve on
port 3000, so the Base44 preview could not start. The fix was adding `app.py`,
a minimal Python HTTP server that browses the repository contents.

## Running the Preview

```sh
docker compose -f docker-compose.base44.yml up -d
```

Serves a browsable directory listing on port 3000 using `python:3.12-slim`.
The source is bind-mounted, so file changes are immediately visible (call
`reload_preview` after edits since there is no live-reload dev server).

## Building RDB Files (not needed for preview)

The Makefile's `make build` target compiles `.rdb` files from `.dat` files via
`libretro-super`. This requires cloning RetroArch and is not needed for the
preview to work.

## Secrets

No external secrets are required.
