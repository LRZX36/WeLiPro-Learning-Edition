"""Import hook: apply runtime patches without file logging."""
from __future__ import annotations

import importlib
import sys

_INSTALLED = False


def _patch_engine_runtime(mod) -> None:
    try:
        import start_templates_stub

        start_templates_stub.apply(mod)
    except Exception:
        pass


def _on_import(name: str, mod) -> None:
    if mod is None or getattr(mod, "_patch_hook_done", False):
        return
    if name.split(".")[0] != "engine_runtime":
        return
    _patch_engine_runtime(mod)
    mod._patch_hook_done = True  # type: ignore[attr-defined]


def install() -> None:
    global _INSTALLED
    if _INSTALLED:
        return
    _INSTALLED = True

    original_import = importlib.import_module

    def hooked_import(name, package=None):
        mod = original_import(name, package)
        _on_import(name, mod)
        return mod

    importlib.import_module = hooked_import

    for name, mod in list(sys.modules.items()):
        if mod is not None:
            _on_import(name, mod)
