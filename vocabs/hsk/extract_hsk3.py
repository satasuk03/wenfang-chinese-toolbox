import pdfplumber
import json

pdf_path = "/Users/satasuk/Desktop/dev/wenfang-chinese-toolbox/vocabs/hsk/新HSK(三级）词汇--（汉泰）.pdf"
output_path = "/Users/satasuk/Desktop/dev/wenfang-chinese-toolbox/vocabs/hsk/hsk3_raw.json"

entries = []
current_entry = None

with pdfplumber.open(pdf_path) as pdf:
    print(f"Total pages: {len(pdf.pages)}")
    for page_idx, page in enumerate(pdf.pages):
        tables = page.extract_tables()
        if not tables:
            print(f"Warning: No table found on page {page_idx + 1}")
            continue
        table = tables[0]
        for row_idx, row in enumerate(table):
            # Skip header rows
            if row[0] and ("序号" in str(row[0]) or "ล ำดับที่" in str(row[0]) or "词类" in str(row[0])):
                continue
            # Check if this is a new entry (has a number in first column)
            num = row[0]
            word = row[1]
            pinyin = row[2]
            pos = row[3]
            meaning = row[4]
            example = row[5]

            # Clean word: remove 【】 brackets
            if word:
                word = word.replace("【", "").replace("】", "").strip()
            if pinyin:
                pinyin = pinyin.strip()
            if pos:
                pos = pos.strip()
            if meaning:
                meaning = meaning.strip()

            if num and num.strip():  # New entry
                if current_entry:
                    entries.append(current_entry)
                current_entry = {
                    "character": word,
                    "pinyin": pinyin,
                    "partOfSpeech": pos,
                    "meaning_th": meaning,
                    "chapter": None,
                }
            elif current_entry is not None:  # Continuation row (multiple meanings for same word)
                # Append additional meaning
                if pos:
                    current_entry["partOfSpeech"] += f", {pos}"
                if meaning:
                    current_entry["meaning_th"] += f", {meaning}"
        
        if page_idx % 5 == 0:
            print(f"Processed page {page_idx + 1}/{len(pdf.pages)}, entries so far: {len(entries)}")

    # Don't forget the last entry
    if current_entry:
        entries.append(current_entry)

print(f"\nTotal entries extracted: {len(entries)}")

# Save to JSON
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(entries, f, ensure_ascii=False, indent=2)

print(f"Saved to {output_path}")

# Print sample entries
print("\n=== Sample entries ===")
for e in entries[:10]:
    print(e)
print("...")
for e in entries[-5:]:
    print(e)

# Check for any entries with empty character or pinyin
empty_entries = [e for e in entries if not e["character"] or not e["pinyin"]]
print(f"\nEntries with empty character or pinyin: {len(empty_entries)}")
for e in empty_entries[:10]:
    print(e)
