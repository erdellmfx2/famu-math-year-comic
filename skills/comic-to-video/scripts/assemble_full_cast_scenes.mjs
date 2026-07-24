#!/usr/bin/env node

import fs from "node:fs";
import fsp from "node:fs/promises";
import path from "node:path";
import process from "node:process";
import { spawnSync } from "node:child_process";

function usage() {
  return `Usage:
  node assemble_full_cast_scenes.mjs --manifest <file> --input <dir> --output <dir> [options]

Options:
  --ffmpeg <file>  FFmpeg executable path (default: ffmpeg)
  --overwrite      Replace existing scene audio
  --dry-run        Validate inputs and print FFmpeg work without assembling
  --help           Show this help
`;
}

function parseArgs(argv) {
  const options = { ffmpeg: "ffmpeg", overwrite: false, dryRun: false };

  for (let index = 0; index < argv.length; index += 1) {
    const argument = argv[index];
    if (argument === "--overwrite") {
      options.overwrite = true;
    } else if (argument === "--dry-run") {
      options.dryRun = true;
    } else if (argument === "--help") {
      options.help = true;
    } else if (
      argument === "--manifest" ||
      argument === "--input" ||
      argument === "--output" ||
      argument === "--ffmpeg"
    ) {
      const value = argv[index + 1];
      if (!value || value.startsWith("--")) throw new Error(`${argument} requires a value`);
      options[argument.slice(2)] = value;
      index += 1;
    } else {
      throw new Error(`Unknown argument: ${argument}`);
    }
  }

  if (!options.help && (!options.manifest || !options.input || !options.output)) {
    throw new Error("--manifest, --input, and --output are required");
  }
  return options;
}

function utteranceFilename(sceneId, index, speakerId, format) {
  return `${sceneId}-${String(index + 1).padStart(3, "0")}-${speakerId}.${format}`;
}

function buildFilter(scene, defaultPause) {
  const chains = [];
  const labels = [];

  for (const [index, utterance] of scene.utterances.entries()) {
    const pause = utterance.pause_after ?? defaultPause;
    const normalized = `[${index}:a]loudnorm=I=-20:TP=-2:LRA=7,aresample=48000,aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=stereo`;
    const chain = pause > 0 ? `${normalized},apad=pad_dur=${pause}[a${index}]` : `${normalized}[a${index}]`;
    chains.push(chain);
    labels.push(`[a${index}]`);
  }

  chains.push(`${labels.join("")}concat=n=${labels.length}:v=0:a=1[outa]`);
  return chains.join(";");
}

async function main() {
  const options = parseArgs(process.argv.slice(2));
  if (options.help) {
    process.stdout.write(usage());
    return;
  }

  const manifest = JSON.parse(await fsp.readFile(path.resolve(options.manifest), "utf8"));
  const inputDir = path.resolve(options.input);
  const outputDir = path.resolve(options.output);
  const format = manifest.response_format || "mp3";
  const defaultPause = manifest.default_pause_after ?? 0.18;

  if (!Array.isArray(manifest.scenes) || manifest.scenes.length === 0) {
    throw new Error("Manifest scenes must be a non-empty array");
  }
  if (!fs.existsSync(options.ffmpeg) && options.ffmpeg !== "ffmpeg") {
    throw new Error(`FFmpeg executable not found: ${options.ffmpeg}`);
  }

  await fsp.mkdir(outputDir, { recursive: true });

  for (const scene of manifest.scenes) {
    const output = path.join(outputDir, `${scene.id}.mp3`);
    if (fs.existsSync(output) && !options.overwrite) {
      process.stdout.write(`Skipping existing ${output}\n`);
      continue;
    }

    const inputs = scene.utterances.map((utterance, index) =>
      path.join(inputDir, utteranceFilename(scene.id, index, utterance.speaker, format)),
    );
    for (const input of inputs) {
      if (!fs.existsSync(input)) throw new Error(`Missing utterance audio: ${input}`);
    }

    if (options.dryRun) {
      process.stdout.write(`Would assemble ${scene.id} from ${inputs.length} utterances\n`);
      continue;
    }

    const temporary = `${output}.tmp.mp3`;
    const args = ["-hide_banner", "-loglevel", "error", "-y"];
    for (const input of inputs) args.push("-i", input);
    args.push(
      "-filter_complex",
      buildFilter(scene, defaultPause),
      "-map",
      "[outa]",
      "-c:a",
      "libmp3lame",
      "-b:a",
      "192k",
      temporary,
    );

    const result = spawnSync(options.ffmpeg, args, { encoding: "utf8" });
    if (result.status !== 0) {
      throw new Error(`${scene.id}: FFmpeg failed: ${result.stderr.trim()}`);
    }

    if (options.overwrite) await fsp.rm(output, { force: true });
    await fsp.rename(temporary, output);
    process.stdout.write(`Assembled ${output}\n`);
  }
}

main().catch((error) => {
  process.stderr.write(`${error.message}\n`);
  process.exitCode = 1;
});
