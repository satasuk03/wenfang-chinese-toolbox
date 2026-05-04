#!/usr/bin/env python3
"""
Translate the Chinese 'character' column of vocabs/*.csv into Thai using Kimi.
Outputs src/data/vocab-1a.json with full per-entry shape:
    { character, pinyin, partOfSpeech, chapter, meaning_th }

Saves partial progress to .cache/vocab-translations.json so reruns resume.

Usage:
    python3 scripts/translate-vocab.py
"""
import csv
import json
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC_CSV = ROOT / "vocabs" / "1.csv"
OUT_JSON = ROOT / "src" / "data" / "vocab-1a.json"
CACHE = ROOT / ".cache" / "vocab-translations.json"
BATCH = 15

PROMPT_TMPL = (
    "Translate each Chinese vocabulary word to a short, natural Thai gloss "
    "(1–4 Thai words, no romanization, no English, no explanation). For proper "
    "nouns (people, places, countries), give the standard Thai equivalent. "
    "Return ONLY a JSON array of strings, in the SAME ORDER as the input. "
    "No prose, no code fences. The output array MUST have exactly {n} items.\n\n"
    "Input: {payload}"
)


def kimi(prompt: str) -> str:
    res = subprocess.run(
        ["kimi", "-p", prompt, "--quiet"],
        capture_output=True,
        text=True,
        timeout=240,
    )
    out = (res.stdout or "").strip()
    err = (res.stderr or "").strip()
    lines = [ln for ln in out.splitlines() if not ln.startswith("To resume this session:")]
    cleaned = "\n".join(lines).strip()
    if not cleaned:
        raise RuntimeError(f"empty stdout. exit={res.returncode}. stderr={err[:200]}")
    return cleaned


def parse_json_array(text: str) -> list[str]:
    s = text.strip()
    if s.startswith("```"):
        s = s.strip("`")
        first_nl = s.find("\n")
        if first_nl != -1 and not s[:first_nl].lstrip().startswith("["):
            s = s[first_nl + 1 :]
        if s.endswith("```"):
            s = s[:-3]
    return json.loads(s.strip())


def translate_batch(words: list[str]) -> list[str]:
    payload = json.dumps(words, ensure_ascii=False)
    prompt = PROMPT_TMPL.format(payload=payload, n=len(words))
    raw = kimi(prompt)
    arr = parse_json_array(raw)
    if len(arr) != len(words):
        raise ValueError(f"length mismatch: asked {len(words)}, got {len(arr)}")
    return arr


def load_cache() -> dict[str, str]:
    if CACHE.exists():
        return json.loads(CACHE.read_text(encoding="utf-8"))
    return {}


def save_cache(d: dict[str, str]) -> None:
    CACHE.parent.mkdir(parents=True, exist_ok=True)
    CACHE.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")


def main():
    with SRC_CSV.open(encoding="utf-8") as f:
        rows = [r for r in csv.DictReader(f) if r["character"].strip()]

    uniq = sorted({r["character"] for r in rows})
    translations = load_cache()
    todo = [c for c in uniq if c not in translations]
    print(
        f"{len(uniq)} unique characters; {len(translations)} cached; "
        f"{len(todo)} to translate (batch={BATCH})"
    )

    for i in range(0, len(todo), BATCH):
        chunk = todo[i : i + BATCH]
        last_err = None
        for attempt in range(1, 6):
            try:
                out = translate_batch(chunk)
                for ch, th in zip(chunk, out):
                    translations[ch] = th
                save_cache(translations)
                print(f"  batch {i//BATCH + 1}: +{len(chunk)} ({len(translations)}/{len(uniq)})")
                last_err = None
                break
            except Exception as e:
                last_err = e
                print(f"    attempt {attempt} failed: {e}", file=sys.stderr)
                time.sleep(min(30, 5 * attempt))
        if last_err:
            print(f"FAILED batch starting at {i}: {last_err}", file=sys.stderr)
            sys.exit(1)

    out_rows = []
    for r in rows:
        out_rows.append(
            {
                "character": r["character"],
                "pinyin": r["pinyin"],
                "partOfSpeech": r["part_of_speech"],
                "chapter": int(r["chapter"]) if r["chapter"].strip().isdigit() else None,
                "meaning_th": translations[r["character"]],
            }
        )

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(
        json.dumps(out_rows, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {len(out_rows)} entries to {OUT_JSON.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
