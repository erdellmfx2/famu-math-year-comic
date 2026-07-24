#!/usr/bin/env node

import fs from "node:fs/promises";
import path from "node:path";
import process from "node:process";

const supportedFormats = new Set(["mp3", "opus", "aac", "flac", "wav", "pcm"]);

function usage() {
  return `Usage:
  node generate_full_cast_voiceover.mjs --manifest <file> --output <dir> [options]

Options:
  --env <file>     Load OPENAI_API_KEY from an env file
  --pronunciations <file>
                   Apply matching character-name pronunciation instructions
  --match-text <text>
                   Generate only utterances containing this text (case-insensitive)
  --overwrite      Replace existing utterance audio
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
    } else if (
      argument === "--manifest" ||
      argument === "--output" ||
      argument === "--env" ||
      argument === "--pronunciations" ||
      argument === "--match-text"
    ) {
      const value = argv[index + 1];
      if (!value || value.startsWith("--")) throw new Error(`${argument} requires a value`);
      const optionName = argument === "--match-text" ? "matchText" : argument.slice(2);
      options[optionName] = value;
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
    process.env[match[1]] = match[2].trim().replace(/^(['"])(.*)\1$/, "$2");
  }
}

function safeId(value, label) {
  if (typeof value !== "string" || !/^[A-Za-z0-9][A-Za-z0-9._-]*$/.test(value)) {
    throw new Error(`${label} must use only letters, digits, periods, underscores, or hyphens`);
  }
}

function validateManifest(manifest) {
  if (!manifest || typeof manifest !== "object") throw new Error("Manifest must be an object");
  if (typeof manifest.model !== "string" || !manifest.model.trim()) {
    throw new Error("Manifest model is required");
  }
  if (!manifest.speakers || typeof manifest.speakers !== "object") {
    throw new Error("Manifest speakers are required");
  }
  if (!Array.isArray(manifest.scenes) || manifest.scenes.length === 0) {
    throw new Error("Manifest scenes must be a non-empty array");
  }

  const format = manifest.response_format || "mp3";
  if (!supportedFormats.has(format)) throw new Error(`Unsupported response_format: ${format}`);

  for (const [speakerId, speaker] of Object.entries(manifest.speakers)) {
    safeId(speakerId, `Speaker id ${speakerId}`);
    if (!speaker || typeof speaker.voice !== "string" || !speaker.voice.trim()) {
      throw new Error(`${speakerId}: voice is required`);
    }
    if (typeof speaker.instructions !== "string" || !speaker.instructions.trim()) {
      throw new Error(`${speakerId}: instructions are required`);
    }
  }

  const sceneIds = new Set();
  for (const scene of manifest.scenes) {
    safeId(scene.id, "Scene id");
    if (sceneIds.has(scene.id)) throw new Error(`Duplicate scene id: ${scene.id}`);
    sceneIds.add(scene.id);
    if (!Array.isArray(scene.utterances) || scene.utterances.length === 0) {
      throw new Error(`${scene.id}: utterances must be a non-empty array`);
    }

    for (const [index, utterance] of scene.utterances.entries()) {
      if (!manifest.speakers[utterance.speaker]) {
        throw new Error(`${scene.id} utterance ${index + 1}: unknown speaker ${utterance.speaker}`);
      }
      if (typeof utterance.text !== "string" || !utterance.text.trim()) {
        throw new Error(`${scene.id} utterance ${index + 1}: text is required`);
      }
      if (utterance.text.length > 4000) {
        throw new Error(`${scene.id} utterance ${index + 1}: text exceeds 4,000 characters`);
      }
    }
  }

  return format;
}

function utteranceFilename(sceneId, index, speakerId, format) {
  return `${sceneId}-${String(index + 1).padStart(3, "0")}-${speakerId}.${format}`;
}

function wait(milliseconds) {
  return new Promise((resolve) => setTimeout(resolve, milliseconds));
}

async function requestSpeech(apiKey, body, label) {
  for (let attempt = 1; attempt <= 3; attempt += 1) {
    const response = await fetch("https://api.openai.com/v1/audio/speech", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${apiKey}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify(body),
    });

    if (response.ok) return Buffer.from(await response.arrayBuffer());

    const detail = (await response.text()).slice(0, 500);
    const retryable = response.status === 429 || response.status >= 500;
    if (!retryable || attempt === 3) {
      throw new Error(`${label}: OpenAI API returned ${response.status}: ${detail}`);
    }
    await wait(1000 * 2 ** (attempt - 1));
  }

  throw new Error(`${label}: voice generation failed`);
}

function escapeRegExp(value) {
  return value.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

function validatePronunciations(lexicon) {
  if (!lexicon || !Array.isArray(lexicon.characters)) {
    throw new Error("Pronunciation lexicon must contain a characters array");
  }
  for (const [index, character] of lexicon.characters.entries()) {
    if (!character.id || !Array.isArray(character.match) || character.match.length === 0) {
      throw new Error(`Pronunciation entry ${index + 1} requires id and match values`);
    }
    if (!character.instruction || typeof character.instruction !== "string") {
      throw new Error(`Pronunciation entry ${character.id} requires an instruction`);
    }
  }
}

function matchingPronunciations(text, lexicon) {
  if (!lexicon) return [];
  return lexicon.characters.filter((character) =>
    character.match.some((value) => {
      const pattern = new RegExp(`(^|[^A-Za-z])${escapeRegExp(value)}(?=$|[^A-Za-z])`, "i");
      return pattern.test(text);
    }),
  );
}

function withPronunciationInstructions(baseInstructions, matches) {
  if (matches.length === 0) return baseInstructions;
  return [
    baseInstructions,
    "Pronunciation locks for this line:",
    ...matches.map((character) => `- ${character.instruction}`),
    "Keep the supplied written words unchanged.",
  ].join("\n");
}

async function main() {
  const options = parseArgs(process.argv.slice(2));
  if (options.help) {
    process.stdout.write(usage());
    return;
  }

  const manifest = JSON.parse(await fs.readFile(path.resolve(options.manifest), "utf8"));
  const format = validateManifest(manifest);
  const outputDir = path.resolve(options.output);
  const pronunciationLexicon = options.pronunciations
    ? JSON.parse(await fs.readFile(path.resolve(options.pronunciations), "utf8"))
    : null;
  if (pronunciationLexicon) validatePronunciations(pronunciationLexicon);

  await loadEnv(options.env);
  if (!options.dryRun && !process.env.OPENAI_API_KEY) {
    throw new Error("OPENAI_API_KEY is not available");
  }

  await fs.mkdir(outputDir, { recursive: true });
  const report = [];

  for (const scene of manifest.scenes) {
    for (const [index, utterance] of scene.utterances.entries()) {
      const speaker = manifest.speakers[utterance.speaker];
      const filename = utteranceFilename(scene.id, index, utterance.speaker, format);
      const destination = path.join(outputDir, filename);
      const item = {
        scene: scene.id,
        order: index + 1,
        speaker: utterance.speaker,
        voice: speaker.voice,
        text: utterance.text,
        file: filename,
        pronunciations: matchingPronunciations(utterance.text, pronunciationLexicon).map(
          (character) => character.id,
        ),
      };
      report.push(item);

      if (
        options.matchText &&
        !utterance.text.toLowerCase().includes(options.matchText.toLowerCase())
      ) {
        process.stdout.write(`Skipping unselected ${filename}\n`);
        continue;
      }

      if (options.dryRun) {
        process.stdout.write(`Would generate ${filename} with ${utterance.speaker}/${speaker.voice}\n`);
        continue;
      }

      try {
        await fs.access(destination);
        if (!options.overwrite) {
          process.stdout.write(`Skipping existing ${filename}\n`);
          continue;
        }
      } catch {
        // Missing output is the normal generation path.
      }

      const pronunciationMatches = matchingPronunciations(
        utterance.text,
        pronunciationLexicon,
      );
      const audio = await requestSpeech(
        process.env.OPENAI_API_KEY,
        {
          model: manifest.model,
          voice: speaker.voice,
          instructions: withPronunciationInstructions(
            utterance.instructions || speaker.instructions,
            pronunciationMatches,
          ),
          input: utterance.text,
          response_format: format,
        },
        `${scene.id}/${index + 1}/${utterance.speaker}`,
      );

      const temporary = `${destination}.tmp`;
      await fs.writeFile(temporary, audio);
      if (options.overwrite) await fs.rm(destination, { force: true });
      await fs.rename(temporary, destination);
      const pronunciationLabel = pronunciationMatches.length > 0
        ? `; pronunciations=${pronunciationMatches.map((character) => character.id).join(",")}`
        : "";
      process.stdout.write(
        `Generated ${filename} with ${utterance.speaker}/${speaker.voice}${pronunciationLabel}\n`,
      );
    }
  }

  if (!options.dryRun) {
    await fs.writeFile(
      path.join(outputDir, "generation-report.json"),
      `${JSON.stringify({
        project: manifest.project,
        model: manifest.model,
        pronunciation_lexicon: options.pronunciations || null,
        match_text: options.matchText || null,
        items: report,
      }, null, 2)}\n`,
    );
  }
}

main().catch((error) => {
  process.stderr.write(`${error.message}\n`);
  process.exitCode = 1;
});
