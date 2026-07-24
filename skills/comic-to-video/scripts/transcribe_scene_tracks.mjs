#!/usr/bin/env node

import fs from "node:fs/promises";
import path from "node:path";
import process from "node:process";

function usage() {
  return `Usage:
  node transcribe_scene_tracks.mjs --timing <file> --source-manifest <file> --input <dir> --output <dir> [options]

Options:
  --env <file>       Load OPENAI_API_KEY from an env file
  --overwrite        Replace existing per-scene transcription responses
  --dry-run          Validate inputs without calling the API
  --help             Show this help
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
    } else if (
      argument === "--timing" ||
      argument === "--source-manifest" ||
      argument === "--input" ||
      argument === "--output" ||
      argument === "--env"
    ) {
      const value = argv[index + 1];
      if (!value || value.startsWith("--")) throw new Error(`${argument} requires a value`);
      const optionName = argument === "--source-manifest" ? "sourceManifest" : argument.slice(2);
      options[optionName] = value;
      index += 1;
    } else {
      throw new Error(`Unknown argument: ${argument}`);
    }
  }

  if (
    !options.help &&
    (!options.timing || !options.sourceManifest || !options.input || !options.output)
  ) {
    throw new Error("--timing, --source-manifest, --input, and --output are required");
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

function normalizeWord(value) {
  return String(value)
    .normalize("NFKD")
    .replace(/[\u0300-\u036f]/g, "")
    .toLowerCase()
    .replace(/[^a-z0-9']/g, "")
    .replace(/'/g, "");
}

function sourceWords(scene) {
  return scene.utterances.flatMap((utterance) => utterance.text.trim().split(/\s+/));
}

function editDistance(left, right) {
  let previous = Array.from({ length: right.length + 1 }, (_, index) => index);

  for (let leftIndex = 1; leftIndex <= left.length; leftIndex += 1) {
    const current = [leftIndex];
    for (let rightIndex = 1; rightIndex <= right.length; rightIndex += 1) {
      const substitution = previous[rightIndex - 1] +
        (left[leftIndex - 1] === right[rightIndex - 1] ? 0 : 1);
      current[rightIndex] = Math.min(
        previous[rightIndex] + 1,
        current[rightIndex - 1] + 1,
        substitution,
      );
    }
    previous = current;
  }

  return previous[right.length];
}

function qualityScore(expected, actual) {
  const expectedNormalized = expected.map(normalizeWord).filter(Boolean);
  const actualNormalized = actual.map(normalizeWord).filter(Boolean);
  const denominator = Math.max(expectedNormalized.length, actualNormalized.length, 1);
  return 1 - editDistance(expectedNormalized, actualNormalized) / denominator;
}

function repairWordDurations(words) {
  const repaired = words.map((word) => ({
    ...word,
    start: Number(word.start),
    end: Number(word.end),
  }));
  let repairCount = 0;

  for (let index = 0; index < repaired.length;) {
    const clusterStart = repaired[index].start;
    let clusterEnd = index + 1;
    while (
      clusterEnd < repaired.length &&
      Math.abs(repaired[clusterEnd].start - clusterStart) < 0.001
    ) {
      clusterEnd += 1;
    }

    const cluster = repaired.slice(index, clusterEnd);
    const hasInvalidDuration = cluster.some((word) => word.end <= word.start);
    if (hasInvalidDuration) {
      let targetEnd = Math.max(...cluster.map((word) => word.end));
      if (targetEnd <= clusterStart + 0.01) {
        const nextStart = repaired[clusterEnd]?.start;
        targetEnd = Number.isFinite(nextStart) && nextStart > clusterStart
          ? nextStart
          : clusterStart + 0.16 * cluster.length;
      }

      const step = Math.max(0.06, (targetEnd - clusterStart) / cluster.length);
      for (let offset = 0; offset < cluster.length; offset += 1) {
        const word = repaired[index + offset];
        word.start = Number((clusterStart + step * offset).toFixed(3));
        word.end = Number(
          (offset === cluster.length - 1 ? targetEnd : clusterStart + step * (offset + 1))
            .toFixed(3),
        );
        repairCount += 1;
      }
    }

    index = clusterEnd;
  }

  return { words: repaired, repairCount };
}

function wait(milliseconds) {
  return new Promise((resolve) => setTimeout(resolve, milliseconds));
}

async function requestTranscription(apiKey, audioPath, sourceText, label) {
  for (let attempt = 1; attempt <= 3; attempt += 1) {
    const form = new FormData();
    const audio = await fs.readFile(audioPath);
    form.append("file", new Blob([audio], { type: "audio/mpeg" }), path.basename(audioPath));
    form.append("model", "whisper-1");
    form.append("language", "en");
    form.append("response_format", "verbose_json");
    form.append("timestamp_granularities[]", "word");
    form.append("prompt", sourceText);

    const response = await fetch("https://api.openai.com/v1/audio/transcriptions", {
      method: "POST",
      headers: { Authorization: `Bearer ${apiKey}` },
      body: form,
    });

    if (response.ok) return response.json();

    const detail = (await response.text()).slice(0, 500);
    const retryable = response.status === 429 || response.status >= 500;
    if (!retryable || attempt === 3) {
      throw new Error(`${label}: OpenAI API returned ${response.status}: ${detail}`);
    }
    await wait(1000 * 2 ** (attempt - 1));
  }

  throw new Error(`${label}: transcription failed`);
}

function validateTiming(timing, sourceManifest) {
  if (!Array.isArray(timing.scenes) || timing.scenes.length === 0) {
    throw new Error("Timing manifest scenes must be a non-empty array");
  }
  const sourceIds = new Set(sourceManifest.scenes.map((scene) => scene.id));
  const seen = new Set();

  for (const scene of timing.scenes) {
    if (typeof scene.id !== "string" || !scene.id.trim()) {
      throw new Error("Each timing scene requires an id");
    }
    if (seen.has(scene.id)) throw new Error(`Duplicate timing scene: ${scene.id}`);
    seen.add(scene.id);
    if (!sourceIds.has(scene.id)) throw new Error(`Missing source scene: ${scene.id}`);
    if (!Number.isFinite(scene.audio_start) || scene.audio_start < 0) {
      throw new Error(`${scene.id}: audio_start must be a non-negative number`);
    }
  }
}

async function main() {
  const options = parseArgs(process.argv.slice(2));
  if (options.help) {
    process.stdout.write(usage());
    return;
  }

  const timing = JSON.parse(await fs.readFile(path.resolve(options.timing), "utf8"));
  const sourceManifest = JSON.parse(
    await fs.readFile(path.resolve(options.sourceManifest), "utf8"),
  );
  validateTiming(timing, sourceManifest);

  const inputDir = path.resolve(options.input);
  const outputDir = path.resolve(options.output);
  const rawDir = path.join(outputDir, "raw");
  await fs.mkdir(rawDir, { recursive: true });

  await loadEnv(options.env);
  if (!options.dryRun && !process.env.OPENAI_API_KEY) {
    throw new Error("OPENAI_API_KEY is not available");
  }

  const sourceById = new Map(sourceManifest.scenes.map((scene) => [scene.id, scene]));
  const combined = [];
  const sceneReports = [];

  for (const timingScene of timing.scenes) {
    const sourceScene = sourceById.get(timingScene.id);
    const expected = sourceWords(sourceScene);
    const audioFilename = timingScene.file || `${timingScene.id}.mp3`;
    const audioPath = path.join(inputDir, audioFilename);
    const rawPath = path.join(rawDir, `${timingScene.id}.openai.json`);
    await fs.access(audioPath);

    if (options.dryRun) {
      process.stdout.write(
        `Would transcribe ${audioFilename} at +${timingScene.audio_start.toFixed(3)}s\n`,
      );
      continue;
    }

    let response;
    try {
      if (options.overwrite) throw new Error("overwrite");
      response = JSON.parse(await fs.readFile(rawPath, "utf8"));
      process.stdout.write(`Reusing ${path.basename(rawPath)}\n`);
    } catch {
      response = await requestTranscription(
        process.env.OPENAI_API_KEY,
        audioPath,
        expected.join(" "),
        timingScene.id,
      );
      await fs.writeFile(rawPath, `${JSON.stringify(response, null, 2)}\n`);
      process.stdout.write(`Transcribed ${audioFilename}\n`);
    }

    if (!Array.isArray(response.words) || response.words.length === 0) {
      throw new Error(`${timingScene.id}: response did not include word timestamps`);
    }

    const cleanWords = response.words.filter((word) => normalizeWord(word.word));
    const repaired = repairWordDurations(cleanWords);
    const score = qualityScore(expected, cleanWords.map((word) => word.word));
    sceneReports.push({
      scene: timingScene.id,
      expected_words: expected.length,
      transcribed_words: cleanWords.length,
      similarity: Number(score.toFixed(4)),
      repaired_word_spans: repaired.repairCount,
      needs_review: score < 0.95,
    });

    for (const word of repaired.words) {
      combined.push({
        id: `w${combined.length}`,
        scene: timingScene.id,
        text: String(word.word).trim(),
        start: Number((timingScene.audio_start + Number(word.start)).toFixed(3)),
        end: Number((timingScene.audio_start + Number(word.end)).toFixed(3)),
      });
    }
  }

  if (options.dryRun) return;

  const report = {
    model: "whisper-1",
    words: combined.length,
    scenes: sceneReports,
    minimum_similarity: Math.min(...sceneReports.map((scene) => scene.similarity)),
    review_required: sceneReports.some((scene) => scene.needs_review),
  };

  await fs.writeFile(
    path.join(outputDir, "transcript.json"),
    `${JSON.stringify(combined, null, 2)}\n`,
  );
  await fs.writeFile(
    path.join(outputDir, "transcription-report.json"),
    `${JSON.stringify(report, null, 2)}\n`,
  );
  process.stdout.write(
    `Wrote ${combined.length} word timestamps; minimum similarity ${report.minimum_similarity}\n`,
  );
}

main().catch((error) => {
  process.stderr.write(`${error.message}\n`);
  process.exitCode = 1;
});
