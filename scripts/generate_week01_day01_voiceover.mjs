import fs from "node:fs/promises";
import path from "node:path";
import process from "node:process";

const repoRoot = path.resolve(import.meta.dirname, "..");
const projectDir = path.join(repoRoot, "video", "week-01-day-01");
const manifestPath = path.join(projectDir, "narration-manifest.json");
const outputDir = path.join(projectDir, "audio");

async function loadLocalEnv() {
  const envPath = path.join(repoRoot, ".env.local");
  const source = await fs.readFile(envPath, "utf8");

  for (const line of source.split(/\r?\n/)) {
    const match = line.match(/^([A-Za-z_][A-Za-z0-9_]*)=(.*)$/);
    if (!match || process.env[match[1]]) continue;
    process.env[match[1]] = match[2].replace(/^['"]|['"]$/g, "");
  }
}

async function generateClip(manifest, clip) {
  const response = await fetch("https://api.openai.com/v1/audio/speech", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${process.env.OPENAI_API_KEY}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      model: manifest.model,
      voice: manifest.voice,
      instructions: manifest.instructions,
      input: clip.text,
    }),
  });

  if (!response.ok) {
    throw new Error(`${clip.id}: OpenAI API returned ${response.status} ${await response.text()}`);
  }

  const destination = path.join(outputDir, `${clip.id}.mp3`);
  await fs.writeFile(destination, Buffer.from(await response.arrayBuffer()));
  process.stdout.write(`Generated ${path.relative(repoRoot, destination)}\n`);
}

await loadLocalEnv();
if (!process.env.OPENAI_API_KEY) {
  throw new Error("OPENAI_API_KEY is missing from .env.local");
}

const manifest = JSON.parse(await fs.readFile(manifestPath, "utf8"));
await fs.mkdir(outputDir, { recursive: true });

for (const clip of manifest.clips) {
  await generateClip(manifest, clip);
}
