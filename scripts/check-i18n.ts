#!/usr/bin/env tsx
import th from '../src/i18n/th.json' with { type: 'json' };
import en from '../src/i18n/en.json' with { type: 'json' };

type Json = string | number | boolean | null | Json[] | { [k: string]: Json };

function flatten(obj: Json, prefix = ''): string[] {
  if (Array.isArray(obj)) {
    return obj.flatMap((item, i) => flatten(item as Json, `${prefix}[${i}]`));
  }
  if (obj && typeof obj === 'object') {
    return Object.entries(obj).flatMap(([k, v]) =>
      flatten(v as Json, prefix ? `${prefix}.${k}` : k),
    );
  }
  return [prefix];
}

const thKeys = new Set(flatten(th as Json));
const enKeys = new Set(flatten(en as Json));

const missingInTh = [...enKeys].filter((k) => !thKeys.has(k));
const missingInEn = [...thKeys].filter((k) => !enKeys.has(k));

if (missingInTh.length || missingInEn.length) {
  if (missingInTh.length) {
    console.error('Missing in th.json:');
    missingInTh.forEach((k) => console.error(`  ${k}`));
  }
  if (missingInEn.length) {
    console.error('Missing in en.json:');
    missingInEn.forEach((k) => console.error(`  ${k}`));
  }
  process.exit(1);
}

console.log(`✓ i18n parity OK (${thKeys.size} keys × 2 locales)`);
