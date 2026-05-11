from pathlib import Path


def css_cache_version(request):
    """Bust browser cache when Tailwind output.css is rebuilt (mtime changes)."""
    path = Path(__file__).resolve().parent / "static" / "css" / "output.css"
    try:
        v = int(path.stat().st_mtime)
    except OSError:
        v = 0
    return {"CSS_CACHE_VERSION": v}
