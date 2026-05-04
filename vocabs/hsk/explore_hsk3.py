import pdfplumber
import json
import re

pdf_path = "/Users/satasuk/Desktop/dev/wenfang-chinese-toolbox/vocabs/hsk/新HSK(三级）词汇--（汉泰）.pdf"

# Let's try table extraction first
with pdfplumber.open(pdf_path) as pdf:
    print(f"Total pages: {len(pdf.pages)}")
    for i in [0, 1, 5, 10, 20, 30]:
        if i >= len(pdf.pages):
            break
        page = pdf.pages[i]
        tables = page.extract_tables()
        print(f"\n=== Page {i+1} ===")
        print(f"Number of tables: {len(tables)}")
        if tables:
            for ti, table in enumerate(tables):
                print(f"\nTable {ti} ({len(table)} rows):")
                for row in table[:5]:
                    print(row)
        print("=" * 50)
