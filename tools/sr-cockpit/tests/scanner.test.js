import test from "node:test";
import assert from "node:assert/strict";
import { mkdtemp, mkdir, writeFile, rm } from "node:fs/promises";
import path from "node:path";
import os from "node:os";
import { isCodexProcess, mapCodexSessionsToProjects, scanProjects } from "../server/scanner.js";

test("scanProjects lists apps and reads SR version, lots, passes and task gates", async () => {
  const root = await mkdtemp(path.join(os.tmpdir(), "sr-cockpit-"));
  try {
    const app = path.join(root, "Demo_App");
    await mkdir(path.join(app, "docs/codex/tasks/2026-08-04_demo"), { recursive: true });
    await writeFile(path.join(app, "docs/codex/SR_METHOD.md"), "# SR\n");
    await writeFile(path.join(app, "docs/codex/SR_PACK_VERSION.json"), JSON.stringify({ version: "3.4.0" }));
    await writeFile(path.join(app, "docs/codex/SR_LOTS.yaml"), `
lots:
  - lot_id: DEMO-001
    title: Demo lot
    status: reopened
    priority: high
    objective: Lire le lot.
`);
    await writeFile(path.join(app, "docs/codex/SR_PASSES.yaml"), `
passes:
  - pass_id: DEMO-PASS-001
    title: Demo pass
    status: validated
    lots: [DEMO-001]
    e2e_strategy:
      mode: grouped_at_pass_end
`);
    await writeFile(path.join(app, "docs/codex/SR_INBOX.yaml"), `
items:
  - id: INBOX-1
    type: feature
    priority: high
    summary: Tester inbox
`);
    await writeFile(path.join(app, "docs/codex/tasks/2026-08-04_demo/sr_contract.json"), JSON.stringify({
      status: "done",
      objective: "Demo task",
      gates: { lot_completion: "pass", propagation: "not_applicable" },
      verification: { commands_run: ["npm test"] }
    }));

    const result = await scanProjects({ appsRoot: root, codexSessions: [{ pid: 42, cwd: app, command: "codex" }] });
    assert.equal(result.totals.total, 1);
    assert.equal(result.totals.srInstalled, 1);
    assert.equal(result.totals.codexOpen, 1);
    assert.equal(result.projects[0].srVersion, "3.4.0");
    assert.equal(result.projects[0].statusCounts.reopened, 1);
    assert.equal(result.projects[0].passes[0].id, "DEMO-PASS-001");
    assert.equal(result.projects[0].passes[0].lotDetails[0].title, "Demo lot");
    assert.equal(result.projects[0].lots[0].passId, "DEMO-PASS-001");
    assert.equal(result.projects[0].inbox[0].id, "INBOX-1");
    assert.equal(result.projects[0].tasks[0].gates.lot_completion, "pass");
  } finally {
    await rm(root, { recursive: true, force: true });
  }
});

test("scanProjects reads legacy YAML with duplicate keys in tolerant mode and reports a warning", async () => {
  const root = await mkdtemp(path.join(os.tmpdir(), "sr-cockpit-"));
  try {
    const app = path.join(root, "Legacy_App");
    await mkdir(path.join(app, "docs/codex"), { recursive: true });
    await writeFile(path.join(app, "docs/codex/SR_METHOD.md"), "# SR\n");
    await writeFile(path.join(app, "docs/codex/SR_PACK_VERSION.json"), JSON.stringify({ version: "3.2.2", features: ["sr_passes"] }));
    await writeFile(path.join(app, "docs/codex/SR_LOTS.yaml"), `
lots:
  - lot_id: LEGACY-001
    title: Legacy lot
    status: user_testing
    notes:
      - first
    notes:
      - second
`);
    await writeFile(path.join(app, "docs/codex/SR_PASSES.yaml"), `
passes:
  - pass_id: LEGACY-PASS-001
    title: Legacy pass
    status: user_testing
    lots:
      - LEGACY-001
`);

    const result = await scanProjects({ appsRoot: root, codexSessions: [] });
    const project = result.projects[0];
    assert.equal(project.lots.length, 1);
    assert.equal(project.lots[0].passId, "LEGACY-PASS-001");
    assert.equal(project.srFiles.lots.state, "tolerant");
    assert.match(project.srFiles.lots.error, /Map keys must be unique/);
    assert.equal(project.passes[0].statusCounts.user_testing, 1);
  } finally {
    await rm(root, { recursive: true, force: true });
  }
});

test("scanProjects reports legacy projects without SR_PASSES as compatibility information", async () => {
  const root = await mkdtemp(path.join(os.tmpdir(), "sr-cockpit-"));
  try {
    const app = path.join(root, "Old_SR_App");
    await mkdir(path.join(app, "docs/codex"), { recursive: true });
    await writeFile(path.join(app, "docs/codex/SR_METHOD.md"), "# SR\n");
    await writeFile(path.join(app, "docs/codex/SR_PACK_VERSION.json"), JSON.stringify({ version: "3.0.4", features: ["sr_lots"] }));
    await writeFile(path.join(app, "docs/codex/SR_LOTS.yaml"), `
lots:
  - lot_id: OLD-001
    title: Old lot
    status: planned
`);

    const result = await scanProjects({ appsRoot: root, codexSessions: [] });
    const project = result.projects[0];
    assert.equal(project.lots.length, 1);
    assert.equal(project.passes.length, 0);
    assert.equal(project.unassignedLots.length, 1);
    assert.equal(project.srCompatibility.passesState, "legacy_not_supported");
  } finally {
    await rm(root, { recursive: true, force: true });
  }
});

test("mapCodexSessionsToProjects marks projects active by cwd convention", () => {
  const projects = [{ id: "A", path: "/home/ubuntu/apps/A" }, { id: "B", path: "/home/ubuntu/apps/B" }];
  const sessions = [{ pid: 10, cwd: "/home/ubuntu/apps/A/frontend", command: "codex" }];
  const result = mapCodexSessionsToProjects(projects, sessions);
  assert.equal(result[0].codexOpen, true);
  assert.equal(result[0].codexSessions.length, 1);
  assert.equal(result[1].codexOpen, false);
});

test("isCodexProcess accepts only the real codex executable", () => {
  assert.equal(isCodexProcess(["codex"]), true);
  assert.equal(isCodexProcess(["/home/ubuntu/.local/bin/codex", "exec"]), true);
  assert.equal(isCodexProcess(["systemd-inhibit", "--who", "codex", "sleep", "2147483647"]), false);
  assert.equal(isCodexProcess(["bash", "-lc", "rg codex"]), false);
});
