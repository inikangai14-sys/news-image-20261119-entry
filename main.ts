// news-image-20261119 — "The World in One Day"
// Thursday 19 November 2026: 45 stories, 6 continents, one front page and a map.
//
// The picture itself is entry.png, drawn in this session by compose.py
// (Python + PIL, flat labelled drawings). This program only delivers it:
// it copies entry.png next to this file into the grader's output
// directory, byte for byte, every time. No network, no randomness,
// no arguments read, nothing generated at run time.

import { copyFileSync, mkdirSync, readFileSync, statSync } from "node:fs";
import { createHash } from "node:crypto";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const source = join(here, "entry.png");

const outDir = process.env.MAKEFUN_OUTPUT_DIR || "/output";
mkdirSync(outDir, { recursive: true });

const target = join(outDir, "entry.png");
copyFileSync(source, target);

// Integrity check: the copy must be byte-identical to the source.
// Hash both files and refuse to report success on any mismatch.
function sha256(path: string): string {
  return createHash("sha256").update(readFileSync(path)).digest("hex");
}

const sourceHash = sha256(source);
const targetHash = sha256(target);
if (sourceHash !== targetHash) {
  throw new Error(`integrity check failed: ${target} differs from ${source}`);
}

const bytes = statSync(target).size;
console.log(`entry.png -> ${target} (${bytes} bytes, sha256 ${targetHash})`);
