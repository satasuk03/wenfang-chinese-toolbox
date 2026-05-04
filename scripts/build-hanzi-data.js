/**
 * Build script: extracts unique characters from vocabs/1.csv,
 * copies hanzi-writer.min.js and per-character JSON data into public/.
 */

/* eslint-disable no-undef */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

const CSV_PATH = path.join(__dirname, '..', 'vocabs', '1.csv');
const PUBLIC_DIR = path.join(__dirname, '..', 'public');
const HANZI_DATA_DIR = path.join(PUBLIC_DIR, 'hanzi-data');
const HW_DIST = path.join(__dirname, '..', 'node_modules', 'hanzi-writer', 'dist');
const HW_DATA = path.join(__dirname, '..', 'node_modules', 'hanzi-writer-data');

function parseCsvChars(csvPath) {
  const text = fs.readFileSync(csvPath, 'utf-8');
  const lines = text.trim().split('\n');
  const headers = lines[0].split(',');
  const charIndex = headers.indexOf('character');
  if (charIndex === -1) throw new Error('Missing "character" column in CSV');

  const chars = new Set();
  for (let i = 1; i < lines.length; i++) {
    const row = lines[i];
    // Simple CSV parsing: first field is character
    const firstComma = row.indexOf(',');
    const character = firstComma === -1 ? row : row.slice(0, firstComma);
    for (const ch of character) {
      const cp = ch.codePointAt(0);
      const isCJK =
        (cp >= 0x4e00 && cp <= 0x9fff) ||
        (cp >= 0x3400 && cp <= 0x4dbf) ||
        (cp >= 0x20000 && cp <= 0x2a6df);
      if (isCJK) chars.add(ch);
    }
  }
  return Array.from(chars).sort();
}

function main() {
  if (!fs.existsSync(HW_DIST)) {
    console.error('hanzi-writer not found. Run: npm install hanzi-writer');
    process.exit(1);
  }
  if (!fs.existsSync(HW_DATA)) {
    console.error('hanzi-writer-data not found. Run: npm install -D hanzi-writer-data');
    process.exit(1);
  }

  const chars = parseCsvChars(CSV_PATH);
  console.log(`Found ${chars.length} unique CJK characters in vocab.`);

  if (!fs.existsSync(PUBLIC_DIR)) fs.mkdirSync(PUBLIC_DIR, { recursive: true });
  if (!fs.existsSync(HANZI_DATA_DIR)) fs.mkdirSync(HANZI_DATA_DIR, { recursive: true });

  // Copy hanzi-writer.min.js
  const srcJs = path.join(HW_DIST, 'hanzi-writer.min.js');
  const destJs = path.join(PUBLIC_DIR, 'hanzi-writer.min.js');
  if (fs.existsSync(srcJs)) {
    fs.copyFileSync(srcJs, destJs);
    console.log('Copied hanzi-writer.min.js → public/');
  } else {
    console.error('hanzi-writer.min.js not found in node_modules');
    process.exit(1);
  }

  // Copy character data
  let copied = 0;
  let missing = 0;
  for (const ch of chars) {
    const src = path.join(HW_DATA, `${ch}.json`);
    const dest = path.join(HANZI_DATA_DIR, `${ch}.json`);
    if (fs.existsSync(src)) {
      fs.copyFileSync(src, dest);
      copied++;
    } else {
      missing++;
      console.warn(`  Missing data for: ${ch}`);
    }
  }

  console.log(`Copied ${copied} character data files → public/hanzi-data/`);
  if (missing > 0) console.warn(`Missing ${missing} character(s) (punctuation or unsupported).`);
}

main();
