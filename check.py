#!/usr/bin/env python3
"""Quick checks for contributors: python3 check.py

Needs only Python 3 and PyYAML (pip install pyyaml). It does not run the
rules — that needs the engine — but it catches what most pull requests get
wrong:

  * every YAML file parses;
  * every rule in content/<lang>/lexicon/*.yaml has an id, a match (or an
    absence/length check), an ask, and tests with at least one hit AND one
    miss; rule ids are unique within a language;
  * every rule in content/<lang>/safety.yaml has hits, and the file has a
    top-level `misses` list of look-alikes;
  * every item in ifthen.yaml has say, answer, repair, keywords and tests;
  * every language directory holds the same set of files, and lenses.yaml,
    cards/cards.json and background/<lang>/ share the same keys across
    languages;
  * corpus entries (examples, impacts, requests, openings) have the keys
    their file announces and a non-empty text.

Exit status 0 means all checks passed. Findings are printed one per line as
file:path: message.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.exit("PyYAML is missing: pip install pyyaml")

ROOT = Path(__file__).resolve().parent
LANGS = sorted(p.name for p in (ROOT / "content").iterdir() if p.is_dir())
problems: list[str] = []


def bad(where: str, msg: str) -> None:
    problems.append(f"{where}: {msg}")


def load(path: Path):
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as e:
        bad(str(path.relative_to(ROOT)), f"YAML does not parse: {e}")
        return None


def rel(p: Path) -> str:
    return str(p.relative_to(ROOT))


# ── Same file set per language ──────────────────────────────────────────

def check_file_sets() -> None:
    sets = {}
    for lang in LANGS:
        d = ROOT / "content" / lang
        sets[lang] = sorted(rel(p).split("/", 2)[2] for p in d.rglob("*.yaml"))
    ref_lang, ref = LANGS[0], sets[LANGS[0]]
    for lang, files in sets.items():
        if files != ref:
            only_here = sorted(set(files) - set(ref))
            missing = sorted(set(ref) - set(files))
            bad(f"content/{lang}", f"file set differs from {ref_lang}: missing {missing}, extra {only_here}")
    bg = {lang: sorted(p.name for p in (ROOT / "background" / lang).glob("*.md")) for lang in LANGS
          if (ROOT / "background" / lang).is_dir()}
    if bg and len({tuple(v) for v in bg.values()}) > 1:
        bad("background", f"page sets differ across languages: { {k: len(v) for k, v in bg.items()} }")


# ── Rules ───────────────────────────────────────────────────────────────

def check_tests(where: str, rule: dict, need_misses: bool) -> None:
    tests = rule.get("tests")
    if not isinstance(tests, dict):
        bad(where, "has no tests")
        return
    if not tests.get("hits"):
        bad(where, "tests.hits is empty — a rule must show at least one sentence it catches")
    if need_misses and not tests.get("misses"):
        bad(where, "tests.misses is empty — a rule must show at least one sentence it leaves alone")


def check_lexicon(path: Path) -> None:
    d = load(path)
    if d is None:
        return
    where = rel(path)
    if d.get("layer") not in ("example", "impact", "request", "any"):
        bad(where, f"layer must be example|impact|request|any, got {d.get('layer')!r}")
    ids: set[str] = set()
    for gi, g in enumerate(d.get("groups") or []):
        gw = f"{where}:groups[{gi}]"
        for key in ("kind", "severity", "source", "why"):
            if not g.get(key):
                bad(gw, f"group lacks {key}")
        if g.get("severity") not in ("block", "warn", "info"):
            bad(gw, f"severity must be block|warn|info, got {g.get('severity')!r}")
        rules = list(g.get("rules") or [])
        for special in ("absence_check", "length_check"):
            if special in g:
                rules.append(g[special])
        if not rules:
            bad(gw, "group has no rules")
        for r in rules:
            rid = r.get("id")
            rw = f"{where}:{rid or '?'}"
            if not rid:
                bad(gw, "rule without id")
            elif rid in ids:
                bad(rw, "duplicate rule id")
            ids.add(rid)
            if not (r.get("match") or r.get("vocabulary") or r.get("max_words")):
                bad(rw, "rule needs match, vocabulary (absence check) or max_words (length check)")
            if not r.get("ask"):
                bad(rw, "rule without ask — a finding without a way forward is a reprimand")
            if "match" in r and "\\b" in str(r["match"]):
                bad(rw, "do not write \\b in match — the loader adds Unicode word boundaries itself")
            check_tests(rw, r, need_misses=True)
    return ids


def check_safety(path: Path) -> None:
    d = load(path)
    if d is None:
        return
    where = rel(path)
    for r in d.get("rules") or []:
        rw = f"{where}:{r.get('id', '?')}"
        if r.get("kind") not in ("crisis", "violence"):
            bad(rw, f"kind must be crisis|violence, got {r.get('kind')!r}")
        if not r.get("match"):
            bad(rw, "rule without match")
        check_tests(rw, r, need_misses=False)
    if not d.get("misses"):
        bad(where, "top-level `misses` (look-alikes no rule may catch) is empty")
    help_ = d.get("help") or {}
    for kind in ("crisis", "violence"):
        h = help_.get(kind) or {}
        for key in ("title", "lead", "lines", "note"):
            if not h.get(key):
                bad(f"{where}:help.{kind}", f"lacks {key}")


def check_ifthen(path: Path) -> None:
    d = load(path)
    if d is None:
        return
    where = rel(path)
    for it in d.get("items") or []:
        iw = f"{where}:{it.get('id', '?')}"
        for key in ("say", "answer", "repair", "keywords", "tests"):
            if not it.get(key):
                bad(iw, f"item lacks {key}")


CORPUS_KEYS = {
    "examples.yaml": ("entries", ({"relationship", "situation"},)),
    "impacts.yaml": ("entries", ({"situation", "state"},)),
    "requests.yaml": ("entries", ({"goal", "risk"}, {"situation", "goal", "risk"})),
}


def check_corpus(path: Path) -> None:
    d = load(path)
    if d is None:
        return
    where = rel(path)
    key, shapes = CORPUS_KEYS[path.name]
    for i, e in enumerate(d.get(key) or []):
        ew = f"{where}:{key}[{i}]"
        if not str(e.get("text", "")).strip():
            bad(ew, "entry without text")
        have = set(e) - {"text"}
        if have not in shapes:
            bad(ew, f"keys {sorted(have)} do not match {[sorted(s) for s in shapes]}")


def check_openings(path: Path) -> None:
    d = load(path)
    if d is None:
        return
    where = rel(path)
    for i, o in enumerate(d.get("openings") or []):
        ow = f"{where}:openings[{i}]"
        for key in ("style", "tone", "template"):
            if not o.get(key):
                bad(ow, f"lacks {key}")
        for ph in ("{example}", "{impact}", "{request}"):
            if ph not in str(o.get("template", "")):
                bad(ow, f"template lacks {ph}")


def shape(obj, depth: int = 2):
    """Key structure of a mapping down to `depth` levels, for cross-language comparison."""
    if depth == 0 or not isinstance(obj, dict):
        return "·"
    return {k: shape(v, depth - 1) for k, v in obj.items()}


def check_lenses() -> None:
    shapes = {}
    for lang in LANGS:
        p = ROOT / "content" / lang / "lenses.yaml"
        if p.exists():
            d = load(p)
            if d is not None:
                shapes[lang] = shape(d, 2)
    if len(shapes) > 1:
        ref_lang, ref = next(iter(shapes.items()))
        for lang, s in shapes.items():
            if s != ref:
                diff = sorted(set(json.dumps(s, sort_keys=True).split('"')) ^ set(json.dumps(ref, sort_keys=True).split('"')))
                bad(f"content/{lang}/lenses.yaml", f"keys differ from {ref_lang}: {diff[:12]}")


def check_cards() -> None:
    p = ROOT / "cards" / "cards.json"
    if not p.exists():
        return
    try:
        d = json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        bad("cards/cards.json", f"JSON does not parse: {e}")
        return
    order = d.get("order") or []
    for lang in (k for k in d if k not in ("_about", "order")):
        cards = d[lang]
        if sorted(cards) != sorted(order):
            bad(f"cards/cards.json:{lang}", f"card ids differ from `order`: {sorted(set(cards) ^ set(order))}")
        for cid, c in cards.items():
            for key in ("title", "text", "credit", "labels"):
                if key not in c:
                    bad(f"cards/cards.json:{lang}.{cid}", f"lacks {key}")
            if len(str(c.get("text", "")).split()) > 70:
                bad(f"cards/cards.json:{lang}.{cid}", "text is over 70 words — a card holds one idea, 60 words at most")
            png = ROOT / "cards" / lang / f"{cid}.png"
            if not png.exists():
                bad(f"cards/{lang}/{cid}.png", "rendered card missing")


def main() -> int:
    if not LANGS:
        sys.exit("no content/<lang> directories found")
    check_file_sets()
    for lang in LANGS:
        d = ROOT / "content" / lang
        for p in sorted((d / "lexicon").glob("*.yaml")):
            check_lexicon(p)
        if (d / "safety.yaml").exists():
            check_safety(d / "safety.yaml")
        if (d / "ifthen.yaml").exists():
            check_ifthen(d / "ifthen.yaml")
        for name in CORPUS_KEYS:
            if (d / name).exists():
                check_corpus(d / name)
        if (d / "openings.yaml").exists():
            check_openings(d / "openings.yaml")
    check_lenses()
    check_cards()
    load(ROOT / "catalog.yaml")

    rules = sum(len(list((ROOT / "content" / l / "lexicon").glob("*.yaml"))) for l in LANGS)
    if problems:
        print("\n".join(problems))
        print(f"\n{len(problems)} problem(s)")
        return 1
    print(f"OK — {len(LANGS)} languages ({', '.join(LANGS)}), {rules} lexicon files, all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
