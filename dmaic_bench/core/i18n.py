"""English release contract and checks for unexpected source-language text.

Cases and generated blocks are maintained directly in English. The language selector
is retained for callers, but translations must be separately versioned extensions;
the official build never discovers overlays or silently substitutes another language.
"""
from __future__ import annotations
import re
from typing import Any

DEFAULT_LANGUAGE = "en"
LANGUAGES = ("en",)
_CJK_RE = re.compile(r"[\u3400-\u9fff\u3000-\u303f\uff00-\uffef]")

class OverlayError(ValueError):
    """A requested language is not available in the official release."""

def require_language(lang: str) -> str:
    if lang not in LANGUAGES:
        raise OverlayError(f"Unsupported language {lang!r}; this release supports English only. "
                           "Other languages require a separately versioned extension.")
    return lang

def has_cjk(text: str) -> bool:
    """Detect CJK text or punctuation on an English release surface."""
    return bool(_CJK_RE.search(text or ""))

def languages_for(meta) -> tuple:
    require_language(meta.language)
    return LANGUAGES

def localize_meta(meta, lang: str):
    """Compatibility selector: return canonical English metadata without rewriting it."""
    require_language(lang)
    require_language(meta.language)
    return meta

def localize_case(case, lang: str):
    """Compatibility selector: no metadata or generator translation is performed."""
    localize_meta(case.meta, lang)
    return case

def residual_source_strings(obj: Any, path: str = "") -> list:
    """``[(json path, string)]`` for every string still carrying CJK on a release surface.

    Scan both data keys and values so untranslated field names cannot pass unnoticed.
    """
    out = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            if has_cjk(str(k)):
                out.append((f"{path}.<key>", str(k)))
            out.extend(residual_source_strings(v, f"{path}.{k}"))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            out.extend(residual_source_strings(v, f"{path}[{i}]"))
    elif isinstance(obj, str) and has_cjk(obj):
        out.append((path, obj))
    return out
