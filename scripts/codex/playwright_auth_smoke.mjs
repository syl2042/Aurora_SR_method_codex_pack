#!/usr/bin/env node
import { chromium } from "playwright";
import fs from "node:fs";
import path from "node:path";
const route = process.argv.includes("--route") ? process.argv[process.argv.indexOf("--route") + 1] : "/";
const baseUrl = process.env.PLAYWRIGHT_BASE_URL || "http://localhost:3000";
const outDir = path.join(process.cwd(), "output", "playwright");
fs.mkdirSync(outDir, { recursive: true });
const browser = await chromium.launch({ headless: true });
const page = await browser.newPage();
const errors = [];
page.on("console", msg => { if (msg.type() === "error") errors.push(msg.text()); });
await page.goto(baseUrl + route, { waitUntil: "networkidle" });
await page.screenshot({ path: path.join(outDir, "smoke.png"), fullPage: true });
await browser.close();
console.log(JSON.stringify({ route, screenshot: "output/playwright/smoke.png", consoleErrors: errors.length }, null, 2));
if (errors.length) process.exit(1);
