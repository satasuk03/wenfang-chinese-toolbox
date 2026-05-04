import pdfplumber
import json

pdf_path = "/Users/satasuk/Desktop/dev/wenfang-chinese-toolbox/vocabs/hsk/新HSK(四级）词汇--（汉泰）.pdf"
output_path = "/Users/satasuk/Desktop/dev/wenfang-chinese-toolbox/vocabs/hsk/hsk4_raw.json"

entries = []
current_entry = None

with pdfplumber.open(pdf_path) as pdf:
    for page_num, page in enumerate(pdf.pages):
        tables = page.extract_tables()
        for table in tables:
            for row in table:
                # Skip header row
                if row[0] and "序号" in str(row[0]):
                    continue
                
                seq, word, pinyin, pos, meaning, example = row
                
                # Clean whitespace and newlines
                if word:
                    word = word.replace("【", "").replace("】", "").strip()
                    word = " ".join(word.split())  # normalize whitespace
                if pinyin:
                    pinyin = " ".join(pinyin.split())
                if pos:
                    pos = pos.strip()
                if meaning:
                    meaning = " ".join(meaning.split())
                
                # If we have a sequence number and word, this is a new entry
                if seq and str(seq).strip() and word:
                    # Save previous entry if exists
                    if current_entry:
                        entries.append(current_entry)
                    
                    current_entry = {
                        "character": word,
                        "pinyin": pinyin,
                        "partOfSpeech": pos,
                        "meaning_th": meaning,
                        "chapter": None
                    }
                elif current_entry and not seq and not word and not pinyin:
                    # This is a continuation row for the previous word
                    if pos:
                        current_entry["partOfSpeech"] += "; " + pos if current_entry["partOfSpeech"] else pos
                    if meaning:
                        current_entry["meaning_th"] += "; " + meaning if current_entry["meaning_th"] else meaning
                elif seq and str(seq).strip() and not word:
                    # Edge case: sequence number but no word - might be continuation
                    if pos:
                        current_entry["partOfSpeech"] += "; " + pos if current_entry["partOfSpeech"] else pos
                    if meaning:
                        current_entry["meaning_th"] += "; " + meaning if current_entry["meaning_th"] else meaning
                else:
                    print(f"Warning on page {page_num + 1}: unexpected row {row}")
    
    # Don't forget the last entry
    if current_entry:
        entries.append(current_entry)

# Save to JSON
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(entries, f, ensure_ascii=False, indent=2)

print(f"Total entries extracted: {len(entries)}")

# Report stats
empty_pinyin = [e for e in entries if not e["pinyin"]]
empty_pos = [e for e in entries if not e["partOfSpeech"]]
empty_meaning = [e for e in entries if not e["meaning_th"]]

print(f"Entries with empty pinyin: {len(empty_pinyin)}")
print(f"Entries with empty partOfSpeech: {len(empty_pos)}")
print(f"Entries with empty meaning_th: {len(empty_meaning)}")

# Check for true duplicates (same character, pinyin, pos, meaning)
seen = set()
duplicates = []
for e in entries:
    key = (e["character"], e["pinyin"], e["partOfSpeech"], e["meaning_th"])
    if key in seen:
        duplicates.append(e)
    else:
        seen.add(key)

print(f"True duplicate entries: {len(duplicates)}")
if duplicates:
    print("Duplicate entries:")
    for d in duplicates:
        print(f"  {d}")

# Print first and last few entries
print("\n--- First 5 entries ---")
for e in entries[:5]:
    print(e)

print("\n--- Last 5 entries ---")
for e in entries[-5:]:
    print(e)
