#!/usr/bin/env python3
"""
Build src/data/topik-vocab.json from vocabs/topik.csv.

CSV columns: word, level, meaning_en

Usage:
    python3 scripts/build-topik-vocab.py
"""
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC_CSV = ROOT / "vocabs" / "topik.csv"
OUT_JSON = ROOT / "src" / "data" / "topik-vocab.json"


def main():
    with SRC_CSV.open(encoding="utf-8") as f:
        rows = [r for r in csv.DictReader(f) if r["word"].strip()]

    out = []
    for r in rows:
        out.append(
            {
                "word": r["word"].strip(),
                "level": r["level"].strip(),
                "meaning": r.get("meaning_en", "").strip(),
            }
        )

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(
        f"Wrote {len(out)} entries to {OUT_JSON.relative_to(ROOT)} "
        f"({sum(1 for r in out if r['level'] == 'I')} TOPIK I, "
        f"{sum(1 for r in out if r['level'] == 'II')} TOPIK II)"
    )


if __name__ == "__main__":
    main()
