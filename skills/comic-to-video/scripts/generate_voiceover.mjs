#!/usr/bin/env node

import fs from "node:fs/promises";
import path from "node:path";
import process from "node:process";

const supportedFormats = new Set(["mp3", "opus", "aac", "flac", "wav", "pcm"]);

function usage() {
  return `Usage:
  node generate_voiceover.mjs --manifest <file> --output <dir> [options]

Options:
  --env <file>     Load OPENAI_API_KEY from an env file
  --overwrite      Replace existing clips
  --dry-run        Validate and list outputs without calling the API
  --help           Show this help
`;
}

function parseArgs(argv) {
  const options = { overwrite: false, dryRun: false };

  for (let index = 0; index < argv.length; index += 1) {
    const argument = argv[index];

    if (argument === "--overwrite") {
      options.overwrite = true;
    } else if (argument === "--dry-run") {
      options.dryRun = true;
    } else if (argument === "--help") {
      options.help = true;
    } else if (argument === "--manifest" || argument === "--output" || argument === "--env") {
      const value = argv[index + 1];
      if (!value || value.startsWith("--")) {
        throw new Error(`${argument} requires a value`);
      }
      options[argument.slice(2)] = value;
      index += 1;
    } else {
      throw new Error(`Unknown argument: ${argument}`);
    }
  }

  if (!options.help && (!options.manifest || !options.output)) {
    throw new Error("--manifest and --output are required");
  }

  return options;
}

async function loadEnv(envPath) {
  if (!envPath) return;

  const source = await fs.readFile(path.resolve(envPath), "utf8");
  for (const line of source.split(/\r?\n/)) {
    const match = line.match(/^\s*(?:export\s+)?([A-Za-z_][A-Za-z0-9_]*)=(.*)\s*$/);
    if (!match || process.env[match[1]]) continue;

    const value = match[2].trim().replace(/^(['"])(.*)\1$/, "$2");
    process.env[match[1]] = value;
  }
}

function validateManifest(manifest) {
  if (!manifest || typeof manifest !== "object") {
    throw new Error("Manifest must be a JSON object");
  }
  if (typeof manifest.model !== "string" || !manifest.model.trim()) {
    throw new Error("Manifest model is required");
  }
  if (!Array.isArray(manifest.clips) || manifest.clips.length === 0) {
    throw new Error("Manifest clips must be a non-empty array");
  }

  const format = manifest.response_format || "mp3";
  if (!supportedFormats.has(format)) {
    throw new Error(`Unsupported response_format: ${format}`);
  }

  const seenIds = new Set();
  for (const [index, clip] of manifest.clips.entries()) {
    if (!clip || typeof clip !== "object") {
      throw new Error(`Clip ${index + 1} must be an object`);
    }
    if (typeof clip.id !== "string" || !/^[A-Za-z0-9][A-Za-z0-9._-]*$/.test(clip.id)) {
      throw new Error(`Clip ${index + 1} has an invalid id`);
    }
    if (seenIds.has(clip.id)) {
      throw new Error(`Duplicate clip id: ${clip.id}`);
    }
    seenIds.add(clip.id);

    if (typeof clip.text !== "string" || !clip.text.trim()) {
      throw new Error(`${clip.id}: text is required`);
    }
    if (clip.text.length > 4000) {
      throw new Error(`${clip.id}: text exceeds the 4,000-character production limit`);
    }
    if (typeof (clip.voice || manifest.voice) !== "string") {
      throw new Error(`${clip.id}: voice is required at the clip or manifest level`);
    }
  }

  return format;
}

function wait(milliseconds) {
  return new Promise((resolve) => setTimeout(resolve, milliseconds));
}

async function requestSpeech(apiKey, body, clipId) {
  for (let attempt = 1; attempt <= 3; attempt += 1) {
    const response = await fetch("https://api.openai.com/v1/audio/speech", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${apiKey}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify(body),
    });

    if (response.ok) {
      return Buffer.from(await response.arrayBuffer());
    }

    const detail = (await response.text()).slice(0, 500);
    const retryable = response.status === 429 || response.status >= 500;
    if (!retryable || attempt === 3) {
      throw new Error(`${clipId}: OpenAI API returned ${response.status}: ${detail}`);
    }

    await wait(1000 * 2 ** (attempt - 1));
  }

  throw new Error(`${clipId}: voice generation failed`);
}

async function main() {
  const options = parseArgs(process.argv.slice(2));
  if (options.help) {
    process.stdout.write(usage());
    return;
  }

  const manifestPath = path.resolve(options.manifest);
  const outputDir = path.resolve(options.output);
  const manifest = JSON.parse(await fs.readFile(manifestPath, "utf8"));
  const format = validateManifest(manifest);

  await loadEnv(options.env);
  if (!options.dryRun && !process.env.OPENAI_API_KEY) {
    throw new Error("OPENAI_API_KEY is not available");
  }

  await fs.mkdir(outputDir, { recursive: true });

  for (const clip of manifest.clips) {
    const destination = path.join(outputDir, `${clip.id}.${format}`);

    if (options.dryRun) {
      process.stdout.write(`Would generate ${destination}\n`);
      continue;
    }

    try {
      await fs.access(destination);
      if (!options.overwrite) {
        process.stdout.write(`Skipping existing ${destination}\n`);
        continue;
      }
    } catch {
      // A missing output is the normal generation path.
    }

    const body = {
      model: manifest.model,
      voice: clip.voice || manifest.voice,
      input: clip.text,
      response_format: format,
    };

    const instructions = clip.instructions || manifest.instructions;
    if (instructions) body.instructions = instructions;

    const speed = clip.speed ?? manifest.speed;
    if (speed !== undefined) body.speed = speed;

    const audio = await requestSpeech(process.env.OPENAI_API_KEY, body, clip.id);
    const temporary = `${destination}.tmp`;
    await fs.writeFile(temporary, audio);
    if (options.overwrite) await fs.rm(destination, { force: true });
    await fs.rename(temporary, destination);
    process.stdout.write(`Generated ${destination}\n`);
  }
}

main().catch((error) => {
  process.stderr.write(`${error.message}\n`);
  process.exitCode = 1;
});
