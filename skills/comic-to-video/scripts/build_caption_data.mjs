#!/usr/bin/env node

import fs from "node:fs/promises";
import path from "node:path";
import process from "node:process";

function parseArgs(argv) {
  const options = { maxWords: 5, pauseBreak: 0.32 };

  for (let index = 0; index < argv.length; index += 1) {
    const argument = argv[index];
    if (argument === "--input" || argument === "--output") {
      const value = argv[index + 1];
      if (!value || value.startsWith("--")) throw new Error(`${argument} requires a value`);
      options[argument.slice(2)] = value;
      index += 1;
    } else if (argument === "--max-words" || argument === "--pause-break") {
      const value = Number(argv[index + 1]);
      if (!Number.isFinite(value) || value <= 0) throw new Error(`${argument} requires a number`);
      options[argument === "--max-words" ? "maxWords" : "pauseBreak"] = value;
      index += 1;
    } else {
      throw new Error(`Unknown argument: ${argument}`);
    }
  }

  if (!options.input || !options.output) throw new Error("--input and --output are required");
  return options;
}

function validateWords(words) {
  if (!Array.isArray(words) || words.length === 0) {
    throw new Error("Caption transcript must be a non-empty word array");
  }
  let previousStart = -1;
  for (const [index, word] of words.entries()) {
    if (!word.text || !Number.isFinite(word.start) || !Number.isFinite(word.end)) {
      throw new Error(`Invalid word at index ${index}`);
    }
    if (word.start < previousStart || word.end <= word.start) {
      throw new Error(`Non-monotonic word timing at index ${index}`);
    }
    previousStart = word.start;
  }
}

function shouldBreak(words, index, options) {
  const current = words[index];
  const next = words[index + 1];
  if (!next) return true;
  if ((index + 1) % options.maxWords === 0) return true;
  if (next.scene !== current.scene) return true;
  if (next.start - current.end >= options.pauseBreak) return true;
  return /[.!?]["']?$/.test(current.text);
}

function groupWords(words, options) {
  const groups = [];
  let current = [];

  for (let index = 0; index < words.length; index += 1) {
    current.push(words[index]);
    if (current.length >= options.maxWords || shouldBreak(words, index, options)) {
      groups.push({
        id: `cg-${groups.length}`,
        scene: current[0].scene,
        start: current[0].start,
        end: current[current.length - 1].end,
        words: current,
      });
      current = [];
    }
  }

  for (let index = 0; index < groups.length; index += 1) {
    const previous = groups[index - 1];
    const next = groups[index + 1];
    const availableLead = previous ? Math.max(0, groups[index].start - previous.end) : 0.08;
    groups[index].show = Number(
      Math.max(0, groups[index].start - Math.min(0.08, availableLead / 2)).toFixed(3),
    );
    const availableTail = next ? Math.max(0, next.start - groups[index].end) : 0.08;
    groups[index].hide = Number(
      (groups[index].end + Math.min(0.08, availableTail / 2)).toFixed(3),
    );
  }

  return groups;
}

async function main() {
  const options = parseArgs(process.argv.slice(2));
  const words = JSON.parse(await fs.readFile(path.resolve(options.input), "utf8"));
  validateWords(words);
  const groups = groupWords(words, options);
  const source = `window.CAPTION_GROUPS = ${JSON.stringify(groups, null, 2)};\n`;
  await fs.mkdir(path.dirname(path.resolve(options.output)), { recursive: true });
  await fs.writeFile(path.resolve(options.output), source);
  process.stdout.write(`Wrote ${groups.length} caption groups from ${words.length} words\n`);
}

main().catch((error) => {
  process.stderr.write(`${error.message}\n`);
  process.exitCode = 1;
});
