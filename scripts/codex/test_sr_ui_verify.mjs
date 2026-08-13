#!/usr/bin/env node
import test from "node:test";
import assert from "node:assert/strict";
import http from "node:http";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { spawn } from "node:child_process";

const REPO_ROOT = path.resolve(path.dirname(new URL(import.meta.url).pathname), "..", "..");
const RUNNER = path.join(REPO_ROOT, "scripts", "codex", "sr_ui_verify.mjs");

function withTempDir() {
  return fs.mkdtempSync(path.join(os.tmpdir(), "sr-ui-verify-"));
}

function writeJson(file, data) {
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, `${JSON.stringify(data, null, 2)}\n`, "utf8");
}

function baseConfig(tmp, overrides = {}) {
  return {
    enabled: true,
    base_url: { env: "PLAYWRIGHT_BASE_URL", default: "http://127.0.0.1:1" },
    viewports: [{ name: "desktop", width: 800, height: 600 }],
    auth: {
      required: false,
      mode: "none",
      storage_state: { path: path.join(tmp, "auth.json") },
      setup_command: null,
      login_detection: { url_patterns: ["/login"] },
    },
    checks: {
      screenshots: true,
      console_errors: true,
      page_errors: true,
      request_failed: "warn",
      horizontal_overflow: true,
      horizontal_overflow_tolerance_px: 2,
      unexpected_login_redirect: true,
      wait_until: "domcontentloaded",
      wait_after_ms: 350,
    },
    evidence: {
      directory: path.join(tmp, "screens"),
      report_file: path.join(tmp, "ui-verification-report.json"),
    },
    ...overrides,
  };
}

function merge(base, patch) {
  const out = { ...base };
  for (const [key, value] of Object.entries(patch)) {
    out[key] =
      value && typeof value === "object" && !Array.isArray(value) && base[key]
        ? merge(base[key], value)
        : value;
  }
  return out;
}

async function startServer() {
  const server = http.createServer((req, res) => {
    const url = req.url || "/";
    res.setHeader("content-type", "text/html; charset=utf-8");
    if (url === "/login") {
      res.end("<main>login</main>");
    } else if (url === "/dashboard") {
      res.end("<main><h1>Dashboard</h1></main>");
    } else if (url === "/settings") {
      res.end("<main><h1>Settings</h1></main>");
    } else if (url === "/protected") {
      res.end("<script>if(localStorage.getItem('auth')!=='1') location.href='/login';</script><main>Protected</main>");
    } else if (url === "/console-error") {
      res.end("<script>console.error('known ui error')</script><main>Console</main>");
    } else if (url === "/page-error") {
      res.end("<script>setTimeout(()=>{throw new Error('page boom')}, 0)</script><main>Page</main>");
    } else if (url === "/overflow") {
      res.end("<main style='width:2000px'>Overflow</main>");
    } else {
      res.end("<main><h1>Home</h1></main>");
    }
  });
  await new Promise((resolve) => server.listen(0, "127.0.0.1", resolve));
  const address = server.address();
  return { server, baseUrl: `http://127.0.0.1:${address.port}` };
}

async function runRunner(config, routes, env = {}) {
  const tmp = path.dirname(config.evidence.report_file);
  const configPath = path.join(tmp, "config.json");
  writeJson(configPath, config);
  const args = [RUNNER, "--config", configPath, "--routes", routes.join(",")];
  const proc = await new Promise((resolve) => {
    const child = spawn(process.execPath, args, {
      cwd: REPO_ROOT,
      env: { ...process.env, ...env },
      stdio: ["ignore", "pipe", "pipe"],
    });
    let stdout = "";
    let stderr = "";
    child.stdout.on("data", (chunk) => {
      stdout += chunk.toString();
    });
    child.stderr.on("data", (chunk) => {
      stderr += chunk.toString();
    });
    child.on("close", (status) => resolve({ status, stdout, stderr }));
  });
  const report = JSON.parse(fs.readFileSync(config.evidence.report_file, "utf8"));
  return { proc, report };
}

test("public application route passes and writes screenshot/report", async () => {
  const { server, baseUrl } = await startServer();
  try {
    const tmp = withTempDir();
    const config = merge(baseConfig(tmp), { base_url: { default: baseUrl } });
    const { proc, report } = await runRunner(config, ["/dashboard"]);
    assert.equal(proc.status, 0, proc.stderr || proc.stdout);
    assert.equal(report.status, "pass");
    assert.equal(report.routes[0].viewports[0].status, "pass");
    assert.ok(fs.existsSync(report.routes[0].viewports[0].screenshot));
  } finally {
    server.close();
  }
});

test("auth required with valid storageState passes protected route", async () => {
  const { server, baseUrl } = await startServer();
  try {
    const tmp = withTempDir();
    const storageState = path.join(tmp, "auth.json");
    writeJson(storageState, {
      cookies: [],
      origins: [{ origin: baseUrl, localStorage: [{ name: "auth", value: "1" }] }],
    });
    const config = merge(baseConfig(tmp), {
      base_url: { default: baseUrl },
      auth: { required: true, mode: "storage_state", storage_state: { path: storageState } },
    });
    const { proc, report } = await runRunner(config, ["/protected"]);
    assert.equal(proc.status, 0, proc.stderr || proc.stdout);
    assert.equal(report.status, "pass");
    assert.equal(report.ui_test_readiness_gate.authentication.state_valid, true);
  } finally {
    server.close();
  }
});

test("auth required with missing storageState is blocked", async () => {
  const { server, baseUrl } = await startServer();
  try {
    const tmp = withTempDir();
    const config = merge(baseConfig(tmp), {
      base_url: { default: baseUrl },
      auth: { required: true, mode: "storage_state", storage_state: { path: path.join(tmp, "missing.json") } },
    });
    const { proc, report } = await runRunner(config, ["/protected"]);
    assert.equal(proc.status, 2, proc.stderr || proc.stdout);
    assert.equal(report.status, "blocked");
    assert.equal(report.ui_test_readiness_gate.decision, "blocked");
  } finally {
    server.close();
  }
});

test("invalid storageState causing login redirect blocks readiness", async () => {
  const { server, baseUrl } = await startServer();
  try {
    const tmp = withTempDir();
    const storageState = path.join(tmp, "auth.json");
    writeJson(storageState, { cookies: [], origins: [] });
    const config = merge(baseConfig(tmp), {
      base_url: { default: baseUrl },
      auth: { required: true, mode: "storage_state", storage_state: { path: storageState } },
    });
    const { proc, report } = await runRunner(config, ["/protected"]);
    assert.equal(proc.status, 2, proc.stderr || proc.stdout);
    assert.equal(report.ui_test_readiness_gate.decision, "blocked");
    assert.equal(report.auth.login_redirect_detected, true);
  } finally {
    server.close();
  }
});

test("console error fails visual evidence", async () => {
  const { server, baseUrl } = await startServer();
  try {
    const tmp = withTempDir();
    const config = merge(baseConfig(tmp), { base_url: { default: baseUrl } });
    const { proc, report } = await runRunner(config, ["/console-error"]);
    assert.equal(proc.status, 1, proc.stderr || proc.stdout);
    assert.equal(report.status, "fail");
    assert.equal(report.ui_visual_evidence_gate.technical_checks.console_errors, 1);
  } finally {
    server.close();
  }
});

test("pageerror fails visual evidence", async () => {
  const { server, baseUrl } = await startServer();
  try {
    const tmp = withTempDir();
    const config = merge(baseConfig(tmp), { base_url: { default: baseUrl } });
    const { proc, report } = await runRunner(config, ["/page-error"]);
    assert.equal(proc.status, 1, proc.stderr || proc.stdout);
    assert.equal(report.ui_visual_evidence_gate.technical_checks.page_errors, 1);
  } finally {
    server.close();
  }
});

test("horizontal overflow fails viewport", async () => {
  const { server, baseUrl } = await startServer();
  try {
    const tmp = withTempDir();
    const config = merge(baseConfig(tmp), { base_url: { default: baseUrl } });
    const { proc, report } = await runRunner(config, ["/overflow"]);
    assert.equal(proc.status, 1, proc.stderr || proc.stdout);
    assert.equal(report.routes[0].viewports[0].horizontal_overflow, true);
  } finally {
    server.close();
  }
});

test("multiple routes and four viewports create route x viewport evidence", async () => {
  const { server, baseUrl } = await startServer();
  try {
    const tmp = withTempDir();
    const config = merge(baseConfig(tmp), {
      base_url: { default: baseUrl },
      viewports: [
        { name: "desktop-xl", width: 1440, height: 900 },
        { name: "desktop", width: 1280, height: 800 },
        { name: "tablet", width: 768, height: 1024 },
        { name: "mobile", width: 390, height: 844 },
      ],
    });
    const { proc, report } = await runRunner(config, ["/dashboard", "/settings"]);
    assert.equal(proc.status, 0, proc.stderr || proc.stdout);
    assert.equal(report.routes.length, 2);
    assert.equal(report.routes.flatMap((route) => route.viewports).length, 8);
    assert.equal(report.ui_visual_evidence_gate.screenshots.length, 8);
  } finally {
    server.close();
  }
});
