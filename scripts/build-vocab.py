#!/usr/bin/env python3
"""
Build src/data/vocab-1a.json from vocabs/1.csv.

Uses any existing Thai translations from .cache/vocab-translations.json,
leaves meaning_th empty for entries not yet translated.

Usage:
    python3 scripts/build-vocab.py
"""
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC_CSV = ROOT / "vocabs" / "1.csv"
OUT_JSON = ROOT / "src" / "data" / "vocab-1a.json"
CACHE = ROOT / ".cache" / "vocab-translations.json"


def main():
    cache: dict[str, str] = {}
    if CACHE.exists():
        cache = json.loads(CACHE.read_text(encoding="utf-8"))

    with SRC_CSV.open(encoding="utf-8") as f:
        rows = [r for r in csv.DictReader(f) if r["character"].strip()]

    out = []
    for r in rows:
        ch = r["character"]
        out.append(
            {
                "character": ch,
                "pinyin": r["pinyin"],
                "partOfSpeech": r["part_of_speech"],
                "chapter": int(r["chapter"]) if r["chapter"].strip().isdigit() else None,
                "meaning_th": cache.get(ch, ""),
            }
        )

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    translated = sum(1 for r in out if r["meaning_th"])
    print(f"Wrote {len(out)} entries to {OUT_JSON.relative_to(ROOT)} ({translated} translated, {len(out) - translated} pending)")


if __name__ == "__main__":
    main()
