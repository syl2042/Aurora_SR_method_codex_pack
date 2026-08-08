import { execFile } from "node:child_process";
import { promises as fs } from "node:fs";
import path from "node:path";
import { promisify } from "node:util";
import YAML from "yaml";

const execFileAsync = promisify(execFile);
const DEFAULT_APPS_ROOT = "/home/ubuntu/apps";
const STATUS_KEYS = ["proposed", "planned", "validated", "in_progress", "doing", "done", "user_testing", "reopened", "blocked", "deferred", "superseded", "requires_e2e", "repair"];

export async function scanProjects(options = {}) {
  const appsRoot = path.resolve(options.appsRoot || process.env.SR_COCKPIT_APPS_ROOT || DEFAULT_APPS_ROOT);
  const codexSessions = options.codexSessions || await detectCodexSessions(appsRoot);
  const entries = await safeReadDir(appsRoot);
  const projectJobs = entries.map(async (entry) => {
    if (entry.name.startsWith(".")) return null;
    const projectPath = path.join(appsRoot, entry.name);
    const stat = await safeStat(projectPath);
    if (!stat || (!stat.isDirectory() && !stat.isSymbolicLink())) return null;
    const realPath = await safeRealpath(projectPath);
    return scanProject(projectPath, realPath, appsRoot, codexSessions);
  });
  const projects = (await Promise.all(projectJobs)).filter(Boolean);

  projects.sort((a, b) => {
    if (a.codexOpen !== b.codexOpen) return a.codexOpen ? -1 : 1;
    if (a.srInstalled !== b.srInstalled) return a.srInstalled ? -1 : 1;
    return a.name.localeCompare(b.name, "fr", { sensitivity: "base" });
  });

  return {
    generatedAt: new Date().toISOString(),
    appsRoot,
    totals: summarizeProjects(projects),
    projects
  };
}

export async function scanProject(projectPath, realPath, appsRoot, codexSessions) {
  const name = path.basename(projectPath);
  const srInfo = await readSrInfo(projectPath);
  const srVersion = srInfo.version;
  const srInstalled = Boolean(
    srVersion
    || await exists(path.join(projectPath, "docs/codex/SR_METHOD.md"))
    || await exists(path.join(projectPath, "core/SR_METHOD.md"))
  );
  const git = await readGitStatus(projectPath);
  const srFiles = srInstalled ? await readSrFiles(projectPath) : emptySrFiles();
  const lotRecords = srInstalled ? parseLots(srFiles.lots.data) : [];
  const passRecords = srInstalled ? parsePasses(srFiles.passes.data) : [];
  const { lots, passes, unassignedLots } = connectLotsAndPasses(lotRecords, passRecords);
  const inbox = srInstalled ? parseInbox(srFiles.inbox.data) : [];
  const tasks = srInstalled ? await readTaskMemories(projectPath) : [];
  const statusCounts = countStatuses(lots, tasks);
  const sessions = codexSessions.filter((session) => isSameOrInside(session.cwd, projectPath) || isSameOrInside(session.cwd, realPath));
  const lastActivityAt = mostRecentIso([
    await mtimeIso(projectPath),
    await mtimeIso(path.join(projectPath, "docs/CURRENT_STATE.md")),
    await mtimeIso(path.join(projectPath, "docs/codex/SR_LOTS.yaml")),
    await mtimeIso(path.join(projectPath, "docs/codex/SR_PASSES.yaml")),
    await mtimeIso(path.join(projectPath, "docs/codex/SR_INBOX.yaml")),
    ...tasks.map((task) => task.updatedAt).filter(Boolean)
  ]);

  return {
    id: name,
    name,
    path: projectPath,
    realPath,
    srInstalled,
    srVersion: srVersion || null,
    srCompatibility: describeSrCompatibility(srInfo, srFiles, srInstalled),
    srFiles: summarizeSrFiles(srFiles),
    needsSrUpgrade: srInstalled && srVersion !== "3.4.0",
    codexOpen: sessions.length > 0,
    codexSessions: sessions,
    git,
    statusCounts,
    lots,
    passes,
    inbox,
    tasks,
    unassignedLots,
    lastActivityAt,
    currentTask: tasks[0] || null,
    nextSessionPrompt: tasks.find((task) => task.nextSessionPrompt)?.nextSessionPrompt || null
  };
}

export async function detectCodexSessions(appsRoot = DEFAULT_APPS_ROOT) {
  const procEntries = await safeReadDir("/proc");
  const sessions = [];
  for (const entry of procEntries) {
    if (!/^\d+$/.test(entry.name)) continue;
    const pid = Number(entry.name);
    const base = path.join("/proc", entry.name);
    const cmdline = await readProcCmdlineParts(path.join(base, "cmdline"));
    if (!isCodexProcess(cmdline)) continue;
    const cwd = await safeRealpath(path.join(base, "cwd"));
    if (!cwd || !isSameOrInside(cwd, appsRoot)) continue;
    sessions.push({
      pid,
      cwd,
      command: compactCommand(cmdline)
    });
  }
  return sessions;
}

export function mapCodexSessionsToProjects(projects, sessions) {
  return projects.map((project) => ({
    ...project,
    codexSessions: sessions.filter((session) => isSameOrInside(session.cwd, project.path)),
    codexOpen: sessions.some((session) => isSameOrInside(session.cwd, project.path))
  }));
}

async function readSrInfo(projectPath) {
  for (const versionPath of [
    path.join(projectPath, "docs/codex/SR_PACK_VERSION.json"),
    path.join(projectPath, "core/SR_PACK_VERSION.json")
  ]) {
    const data = await readJson(versionPath);
    if (data?.version) {
      return {
        version: String(data.version),
        features: arrayOfStrings(data.features),
        sourcePath: versionPath
      };
    }
  }
  return { version: null, features: [], sourcePath: null };
}

async function readGitStatus(projectPath) {
  if (!await exists(path.join(projectPath, ".git"))) {
    return { present: false, branch: null, dirty: false, aheadBehind: null, lastCommit: null };
  }
  const [branch, status, lastCommit] = await Promise.all([
    runGit(projectPath, ["branch", "--show-current"]),
    runGit(projectPath, ["status", "--porcelain", "--branch"]),
    runGit(projectPath, ["log", "-1", "--pretty=format:%h %s"])
  ]);
  const lines = status.stdout.trim().split("\n").filter(Boolean);
  const header = lines.find((line) => line.startsWith("##")) || "";
  return {
    present: true,
    branch: branch.stdout.trim() || null,
    dirty: lines.some((line) => !line.startsWith("##")),
    aheadBehind: header.replace(/^##\s*/, "") || null,
    lastCommit: lastCommit.stdout.trim() || null
  };
}

async function runGit(cwd, args) {
  try {
    return await execFileAsync("git", args, { cwd, timeout: 1500, maxBuffer: 128 * 1024 });
  } catch {
    return { stdout: "", stderr: "" };
  }
}

async function readSrFiles(projectPath) {
  const [lots, passes, inbox] = await Promise.all([
    readYamlDocument(path.join(projectPath, "docs/codex/SR_LOTS.yaml")),
    readYamlDocument(path.join(projectPath, "docs/codex/SR_PASSES.yaml")),
    readYamlDocument(path.join(projectPath, "docs/codex/SR_INBOX.yaml"))
  ]);
  return { lots, passes, inbox };
}

function emptySrFiles() {
  return {
    lots: emptyYamlDocument("SR_LOTS.yaml"),
    passes: emptyYamlDocument("SR_PASSES.yaml"),
    inbox: emptyYamlDocument("SR_INBOX.yaml")
  };
}

function parseLots(data) {
  const lots = Array.isArray(data?.lots) ? data.lots : [];
  return lots.filter(isObject).map((lot) => ({
    id: stringOrNull(lot.lot_id),
    title: stringOrNull(lot.title) || "Lot sans titre",
    status: stringOrNull(lot.status) || "unknown",
    priority: stringOrNull(lot.priority) || "medium",
    objective: stringOrNull(lot.objective) || "",
    description: stringOrNull(lot.description) || stringOrNull(lot.objective) || "",
    dependsOn: arrayOfStrings(lot.depends_on),
    blockedBy: arrayOfStrings(lot.blocked_by),
    acceptanceCriteria: arrayOfStrings(lot.acceptance_criteria),
    passId: null,
    passTitle: null,
    updatedAt: stringOrNull(lot.updated_at)
  }));
}

function parsePasses(data) {
  const passes = Array.isArray(data?.passes) ? data.passes : [];
  return passes.filter(isObject).map((item) => ({
    id: stringOrNull(item.pass_id),
    title: stringOrNull(item.title) || "Passe sans titre",
    status: stringOrNull(item.status) || "unknown",
    priority: stringOrNull(item.priority) || "medium",
    lots: arrayOfStrings(item.lots),
    e2eMode: stringOrNull(item.e2e_strategy?.mode) || "not_required",
    humanValidation: arrayOfStrings(item.preflight?.human_validation_required),
    stopOn: arrayOfStrings(item.stop_on),
    lotDetails: [],
    statusCounts: countStatuses([], []),
    updatedAt: stringOrNull(item.updated_at)
  }));
}

function parseInbox(data) {
  const items = Array.isArray(data?.items) ? data.items : [];
  return items.filter(isObject).map((item, index) => ({
    id: stringOrNull(item.id) || stringOrNull(item.inbox_id) || `INBOX-${index + 1}`,
    type: stringOrNull(item.type) || stringOrNull(item.kind) || "item",
    priority: stringOrNull(item.priority) || "medium",
    status: stringOrNull(item.status) || "open",
    summary: stringOrNull(item.summary) || stringOrNull(item.title) || stringOrNull(item.description) || "",
    createdAt: stringOrNull(item.created_at),
    updatedAt: stringOrNull(item.updated_at)
  }));
}

function connectLotsAndPasses(lots, passes) {
  const lotsById = new Map(lots.filter((lot) => lot.id).map((lot) => [lot.id, lot]));
  const passByLotId = new Map();
  const enrichedPasses = passes.map((passItem) => {
    const lotDetails = passItem.lots.map((lotId) => {
      const lot = lotsById.get(lotId);
      if (lot && !passByLotId.has(lotId)) {
        passByLotId.set(lotId, { id: passItem.id, title: passItem.title });
      }
      return lot ? {
        id: lot.id,
        title: lot.title,
        status: lot.status,
        priority: lot.priority,
        description: lot.description || lot.objective
      } : {
        id: lotId,
        title: "Lot reference absent",
        status: "missing",
        priority: "unknown",
        description: ""
      };
    });
    return {
      ...passItem,
      lotDetails,
      statusCounts: countStatuses(lotDetails, [])
    };
  });

  const enrichedLots = lots.map((lot) => {
    const passInfo = lot.id ? passByLotId.get(lot.id) : null;
    return {
      ...lot,
      passId: passInfo?.id || null,
      passTitle: passInfo?.title || null
    };
  });

  return {
    lots: enrichedLots,
    passes: enrichedPasses,
    unassignedLots: enrichedLots.filter((lot) => !lot.passId)
  };
}

async function readTaskMemories(projectPath) {
  const tasksRoot = path.join(projectPath, "docs/codex/tasks");
  const entries = await safeReadDir(tasksRoot);
  const tasks = [];
  for (const entry of entries) {
    if (entry.name === "_TEMPLATE" || entry.name.startsWith(".")) continue;
    const taskPath = path.join(tasksRoot, entry.name);
    const stat = await safeStat(taskPath);
    if (!stat?.isDirectory()) continue;
    const sr = await readJson(path.join(taskPath, "sr_contract.json"));
    const loop = await readJson(path.join(taskPath, "loop_contract.json"));
    const nextPromptPath = path.join(taskPath, "NEXT_SESSION_PROMPT.md");
    const nextSessionPrompt = await exists(nextPromptPath) ? nextPromptPath : null;
    tasks.push({
      id: entry.name,
      path: taskPath,
      updatedAt: stat.mtime.toISOString(),
      status: stringOrNull(sr?.status) || stringOrNull(loop?.status_decision) || "legacy",
      objective: stringOrNull(sr?.objective) || await firstMarkdownHeading(path.join(taskPath, "task_plan.md")) || entry.name,
      lotId: stringOrNull(sr?.lot_id),
      loopStatus: stringOrNull(loop?.status_decision),
      gates: normalizeGates(sr?.gates, loop),
      verification: arrayOfStrings(sr?.verification?.commands_run).slice(0, 5),
      nextSessionPrompt
    });
  }
  return tasks.sort((a, b) => new Date(b.updatedAt) - new Date(a.updatedAt)).slice(0, 12);
}

function normalizeGates(srGates, loop) {
  const result = {};
  if (isObject(srGates)) {
    for (const [key, value] of Object.entries(srGates)) result[key] = String(value);
  }
  for (const [key, value] of Object.entries({
    lot_completion: loop?.lot_completion_gate?.status,
    propagation: loop?.propagation_gate?.status,
    verification: loop?.verification?.commands_failed?.length ? "fail" : undefined,
    context_budget: loop?.context_budget?.status
  })) {
    if (value && !result[key]) result[key] = String(value);
  }
  return result;
}

function countStatuses(lots, tasks) {
  const counts = Object.fromEntries(STATUS_KEYS.map((key) => [key, 0]));
  for (const item of lots) {
    const status = item.status || "unknown";
    counts[status] = (counts[status] || 0) + 1;
  }
  for (const task of tasks) {
    if (task.status === "repair") counts.repair += 1;
  }
  return counts;
}

function summarizeProjects(projects) {
  return {
    total: projects.length,
    srInstalled: projects.filter((project) => project.srInstalled).length,
    codexOpen: projects.filter((project) => project.codexOpen).length,
    needsSrUpgrade: projects.filter((project) => project.needsSrUpgrade).length,
    gitDirty: projects.filter((project) => project.git?.dirty).length
  };
}

async function readYamlDocument(filePath) {
  try {
    const text = await fs.readFile(filePath, "utf8");
    try {
      return {
        path: filePath,
        state: "ok",
        data: YAML.parse(text) || {},
        warnings: [],
        error: null
      };
    } catch (error) {
      try {
        return {
          path: filePath,
          state: "tolerant",
          data: YAML.parse(text, { uniqueKeys: false }) || {},
          warnings: [`strict_yaml_failed: ${firstErrorLine(error)}`],
          error: firstErrorLine(error)
        };
      } catch (tolerantError) {
        return {
          path: filePath,
          state: "invalid",
          data: {},
          warnings: [],
          error: firstErrorLine(tolerantError)
        };
      }
    }
  } catch (error) {
    if (error?.code === "ENOENT") return emptyYamlDocument(filePath);
    return {
      path: filePath,
      state: "unreadable",
      data: {},
      warnings: [],
      error: firstErrorLine(error)
    };
  }
}

function emptyYamlDocument(filePath) {
  return {
    path: filePath,
    state: "absent",
    data: {},
    warnings: [],
    error: null
  };
}

async function readJson(filePath) {
  try {
    return JSON.parse(await fs.readFile(filePath, "utf8"));
  } catch {
    return null;
  }
}

async function firstMarkdownHeading(filePath) {
  try {
    const text = await fs.readFile(filePath, "utf8");
    const line = text.split("\n").find((value) => value.trim().startsWith("#"));
    return line ? line.replace(/^#+\s*/, "").trim() : null;
  } catch {
    return null;
  }
}

async function safeReadDir(dirPath) {
  try {
    return await fs.readdir(dirPath, { withFileTypes: true });
  } catch {
    return [];
  }
}

async function safeStat(filePath) {
  try {
    return await fs.lstat(filePath);
  } catch {
    return null;
  }
}

async function safeRealpath(filePath) {
  try {
    return await fs.realpath(filePath);
  } catch {
    return filePath;
  }
}

async function mtimeIso(filePath) {
  const stat = await safeStat(filePath);
  return stat ? stat.mtime.toISOString() : null;
}

async function exists(filePath) {
  try {
    await fs.access(filePath);
    return true;
  } catch {
    return false;
  }
}

async function readProcCmdlineParts(filePath) {
  try {
    return (await fs.readFile(filePath)).toString("utf8").split("\0").filter(Boolean);
  } catch {
    return [];
  }
}

function mostRecentIso(values) {
  const timestamps = values.filter(Boolean).map((value) => new Date(value).getTime()).filter(Number.isFinite);
  if (!timestamps.length) return null;
  return new Date(Math.max(...timestamps)).toISOString();
}

function isSameOrInside(child, parent) {
  if (!child || !parent) return false;
  const relative = path.relative(path.resolve(parent), path.resolve(child));
  return relative === "" || (!relative.startsWith("..") && !path.isAbsolute(relative));
}

function compactCommand(value) {
  const text = Array.isArray(value) ? value.join(" ") : value;
  return text.replace(/\s+/g, " ").slice(0, 180);
}

export function isCodexProcess(cmdlineParts) {
  if (!Array.isArray(cmdlineParts) || !cmdlineParts.length) return false;
  const executable = path.basename(cmdlineParts[0] || "");
  return executable === "codex";
}

function summarizeSrFiles(srFiles) {
  return Object.fromEntries(Object.entries(srFiles).map(([key, value]) => [
    key,
    {
      path: value.path,
      state: value.state,
      warnings: value.warnings,
      error: value.error
    }
  ]));
}

function describeSrCompatibility(srInfo, srFiles, srInstalled) {
  if (!srInstalled) {
    return {
      supportsPasses: false,
      passesState: "not_installed",
      message: "SR non installee."
    };
  }
  const supportsPasses = srInfo.features.includes("sr_passes") || versionAtLeast(srInfo.version, "3.2.0");
  let passesState = srFiles.passes.state;
  let message = null;
  if (srFiles.passes.state === "absent") {
    passesState = supportsPasses ? "missing" : "legacy_not_supported";
    message = supportsPasses
      ? "SR_PASSES.yaml absent alors que cette version SR supporte les passes."
      : "Version SR ancienne sans SR_PASSES.yaml ; les lots sont affiches hors passe.";
  }
  return {
    supportsPasses,
    passesState,
    message
  };
}

function versionAtLeast(version, minimum) {
  if (!version) return false;
  const left = version.split(".").map((value) => Number.parseInt(value, 10) || 0);
  const right = minimum.split(".").map((value) => Number.parseInt(value, 10) || 0);
  for (let index = 0; index < Math.max(left.length, right.length); index += 1) {
    const a = left[index] || 0;
    const b = right[index] || 0;
    if (a > b) return true;
    if (a < b) return false;
  }
  return true;
}

function firstErrorLine(error) {
  return String(error?.message || error || "unknown error").split("\n")[0];
}

function isObject(value) {
  return value && typeof value === "object" && !Array.isArray(value);
}

function stringOrNull(value) {
  if (value === null || value === undefined) return null;
  const text = String(value).trim();
  return text || null;
}

function arrayOfStrings(value) {
  return Array.isArray(value) ? value.map((item) => String(item)).filter(Boolean) : [];
}
