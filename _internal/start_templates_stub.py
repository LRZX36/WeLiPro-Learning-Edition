"""Bypass cloud start_templates download; use local tp.dat templates instead."""
from __future__ import annotations

import glob
import os

_PATCHED = False


def _local_start_template_paths(shared_helper) -> list[str]:
    paths: list[str] = []
    seen: set[str] = set()

    def add_from_dir(directory: str) -> None:
        if not directory or not os.path.isdir(directory):
            return
        for path in sorted(glob.glob(os.path.join(directory, "start-*.png"))):
            norm = os.path.normcase(os.path.abspath(path))
            if norm not in seen:
                seen.add(norm)
                paths.append(path)

    add_from_dir(shared_helper.resource_path("tp/hangxian"))
    add_from_dir(shared_helper.resource_path("tp/1920-1080/hangxian"))

    for rel in ("kaishipipei.png", "start-kashi.png", "bugei-start1.png", "bugei-start-queren.png"):
        path = shared_helper.resource_path(f"tp/{rel}")
        if os.path.isfile(path):
            norm = os.path.normcase(os.path.abspath(path))
            if norm not in seen:
                seen.add(norm)
                paths.append(path)

    return paths


def apply(engine_runtime) -> None:
    global _PATCHED
    if _PATCHED or engine_runtime is None:
        return
    if not hasattr(engine_runtime, "ensure_start_templates_loaded"):
        return

    _PATCHED = True
    orig_check = getattr(engine_runtime, "check_start_button", None)

    def ensure_start_templates_loaded(*args, **kwargs):
        try:
            import shared_helper

            paths = _local_start_template_paths(shared_helper)
            for attr in ("_start_templates_loaded", "_START_TEMPLATES_LOADED"):
                if hasattr(engine_runtime, attr):
                    setattr(engine_runtime, attr, True)
            for attr in ("_start_template_paths", "_START_TEMPLATE_PATHS", "_start_templates"):
                if hasattr(engine_runtime, attr):
                    setattr(engine_runtime, attr, list(paths))
            return True
        except Exception:
            return False

    def check_start_button(region, is_competitive=False, *args, **kwargs):
        try:
            import shared_helper

            threshold = kwargs.get("threshold", 0.7)
            find_fn = engine_runtime.find_template_in_region
            for path in _local_start_template_paths(shared_helper):
                hit = find_fn(region, path, threshold=threshold)
                if hit is not None:
                    return hit
            return None
        except Exception:
            if callable(orig_check):
                return orig_check(region, is_competitive, *args, **kwargs)
            return None

    engine_runtime.ensure_start_templates_loaded = ensure_start_templates_loaded
    if callable(orig_check):
        engine_runtime.check_start_button = check_start_button
