#!/usr/bin/env node

import fs from "node:fs/promises";
import path from "node:path";
import process from "node:process";

function parseArgs(argv) {
  const options = { reuseExisting: false };
  for (let index = 0; index < argv.length; index += 1) {
    const argument = argv[index];
    if (argument === "--reuse-existing") {
      options.reuseExisting = true;
    } else if (["--project", "--plan", "--output", "--env"].includes(argument)) {
      const value = argv[index + 1];
      if (!value || value.startsWith("--")) throw new Error(`${argument} requires a value`);
      options[argument.slice(2)] = value;
      index += 1;
    } else {
      throw new Error(`Unknown argument: ${argument}`);
    }
  }
  for (const key of ["project", "plan", "output"]) {
    if (!options[key]) throw new Error(`--${key} is required`);
  }
  return options;
}

async function loadEnv(envPath) {
  if (!envPath) return;
  const source = await fs.readFile(path.resolve(envPath), "utf8");
  for (const line of source.split(/\r?\n/)) {
    const match = line.match(/^\s*(?:export\s+)?([A-Za-z_][A-Za-z0-9_]*)=(.*)\s*$/);
    if (!match || process.env[match[1]]) continue;
    process.env[match[1]] = match[2].trim().replace(/^(['"])(.*)\1$/, "$2");
  }
}

function scriptedWords(text) {
  return text.trim().split(/\s+/).filter(Boolean);
}

function alignWords(text, apiWords, audioDuration) {
  const expected = scriptedWords(text);
  const usable = (apiWords || []).filter(
    (word) => word.word && Number.isFinite(word.start) && Number.isFinite(word.end),
  );

  if (usable.length === expected.length) {
    return expected.map((word, index) => ({
      text: word,
      start: usable[index].start,
      end: usable[index].end,
    }));
  }

  const first = usable.length > 0 ? usable[0].start : 0;
  const last = usable.length > 0 ? usable.at(-1).end : audioDuration;
  const span = Math.max(last - first, 0.1);
  const weights = expected.map((word) => Math.max(word.replace(/[^A-Za-z0-9]/g, "").length, 2));
  const totalWeight = weights.reduce((sum, weight) => sum + weight, 0);
  let cursor = first;
  return expected.map((word, index) => {
    const duration = span * (weights[index] / totalWeight);
    const result = { text: word, start: cursor, end: cursor + duration };
    cursor += duration;
    return result;
  });
}

async function transcribe(apiKey, filePath) {
  const audio = await fs.readFile(filePath);
  const form = new FormData();
  form.append("file", new Blob([audio]), path.basename(filePath));
  form.append("model", "whisper-1");
  form.append("language", "en");
  form.append("response_format", "verbose_json");
  form.append("timestamp_granularities[]", "word");

  const response = await fetch("https://api.openai.com/v1/audio/transcriptions", {
    method: "POST",
    headers: { Authorization: `Bearer ${apiKey}` },
    body: form,
  });
  if (!response.ok) {
    throw new Error(`OpenAI transcription failed (${response.status}): ${(await response.text()).slice(0, 500)}`);
  }
  return response.json();
}

async function main() {
  const options = parseArgs(process.argv.slice(2));
  await loadEnv(options.env);
  if (!process.env.OPENAI_API_KEY) throw new Error("OPENAI_API_KEY is not available");

  const projectRoot = path.resolve(options.project);
  const plan = JSON.parse(await fs.readFile(path.resolve(options.plan), "utf8"));
  const transcriptDir = path.join(projectRoot, "assets", "audio", "transcripts");
  await fs.mkdir(transcriptDir, { recursive: true });

  const lines = [];
  let wordId = 0;
  for (const line of plan.lines) {
    const filePath = path.join(projectRoot, line.file);
    const transcriptPath = path.join(
      transcriptDir,
      `${path.parse(line.file).name}.openai.json`,
    );
    let response;
    if (options.reuseExisting) {
      try {
        response = JSON.parse(await fs.readFile(transcriptPath, "utf8"));
        process.stdout.write(`Reused ${path.basename(transcriptPath)}\n`);
      } catch (error) {
        if (error.code !== "ENOENT") throw error;
      }
    }
    if (!response) {
      response = await transcribe(process.env.OPENAI_API_KEY, filePath);
      await fs.writeFile(transcriptPath, `${JSON.stringify(response, null, 2)}\n`);
    }

    const aligned = alignWords(line.text, response.words, line.duration).map((word) => ({
      id: `w${wordId++}`,
      text: word.text,
      start: Number((line.start + word.start).toFixed(3)),
      end: Number((line.start + word.end).toFixed(3)),
    }));
    lines.push({ ...line, words: aligned, transcript_text: response.text });
    process.stdout.write(`Transcribed ${path.basename(filePath)}: ${aligned.length} words\n`);
  }

  const output = {
    model: "whisper-1",
    language: "en",
    generated_at: new Date().toISOString(),
    lines,
    words: lines.flatMap((line) => line.words),
  };
  await fs.writeFile(path.resolve(options.output), `${JSON.stringify(output, null, 2)}\n`);
}

main().catch((error) => {
  process.stderr.write(`${error.message}\n`);
  process.exitCode = 1;
});
