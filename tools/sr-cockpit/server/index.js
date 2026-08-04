import express from "express";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { scanProjects } from "./scanner.js";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const rootDir = path.resolve(__dirname, "..");

function argValue(name, fallback) {
  const index = process.argv.indexOf(name);
  return index >= 0 && process.argv[index + 1] ? process.argv[index + 1] : fallback;
}

const host = argValue("--host", process.env.SR_COCKPIT_HOST || "127.0.0.1");
const port = Number(argValue("--port", process.env.SR_COCKPIT_PORT || "18787"));
const appsRoot = argValue("--apps-root", process.env.SR_COCKPIT_APPS_ROOT || "/home/ubuntu/apps");

const app = express();

app.get("/api/health", (_request, response) => {
  response.json({ ok: true, app: "Aurora SR Cockpit", appsRoot });
});

app.get("/api/projects", async (_request, response) => {
  try {
    response.json(await scanProjects({ appsRoot }));
  } catch (error) {
    response.status(500).json({ error: error.message || "scan failed" });
  }
});

const distDir = path.join(rootDir, "dist");
app.use(express.static(distDir));
app.get("*", (_request, response) => {
  response.sendFile(path.join(distDir, "index.html"));
});

app.listen(port, host, () => {
  console.log(`Aurora SR Cockpit listening on http://${host}:${port}`);
  console.log(`Scanning apps root: ${appsRoot}`);
});
