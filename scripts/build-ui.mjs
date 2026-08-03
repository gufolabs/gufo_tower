// ----------------------------------------------------------------------
// UI build script.
// Usage: npm run build
// ----------------------------------------------------------------------
// Copyright (C) 2015-2026 Gufo Labs
// See LICENSE for details
// ----------------------------------------------------------------------

import * as esbuild from "esbuild";
import { readFile, writeFile, mkdir, rm, cp } from "node:fs/promises";
import { resolve, join, relative } from "node:path";

const root = resolve(import.meta.dirname, "..");

const srcDir = join(root, "src", "ui");
const outDir = join(root, "build", "ui");
const assetsDir = join(outDir, "assets");

async function main() {
    console.log("Building UI");

    await rm(outDir, { recursive: true, force: true });
    await mkdir(assetsDir, { recursive: true });

    const result = await esbuild.build({
        entryPoints: [
            join(srcDir, "vendor.js"),
            join(srcDir, "main.js"),
        ],
        bundle: true,
        minify: true,
        //sourcemap: false,
        sourcemap: "linked",
        outdir: assetsDir,
        entryNames: "[name]-[hash]",
        assetNames: "[name]-[hash]",
        metafile: true,
        loader: {
            ".css": "css",
            ".png": "file",
            ".svg": "file",
            ".woff": "file",
            ".woff2": "file",
            ".ttf": "file",
            ".eot": "file",
        },
        logLevel: "info",
    });

    let vendorJs;
    let mainJs;
    let cssFile;

    for (const output of Object.keys(result.metafile.outputs)) {
        const name = relative(assetsDir, output);

        if (name.startsWith("vendor-") && name.endsWith(".js")) {
            vendorJs = name;
        }

        if (name.startsWith("main-") && name.endsWith(".js")) {
            mainJs = name;
        }

        if (name.endsWith(".css")) {
            cssFile = name;
        }
    }

    if (!vendorJs) {
        throw new Error("Vendor JavaScript bundle was not generated");
    }

    if (!mainJs) {
        throw new Error("Main JavaScript bundle was not generated");
    }

    if (!cssFile) {
        throw new Error("CSS bundle was not generated");
    }

    const template = await readFile(
        join(srcDir, "index.html"),
        "utf8",
    );

    const html = template
        .replace(
            "{{JS}}",
            [
                `<script src="assets/${vendorJs}"></script>`,
                `<script src="assets/${mainJs}"></script>`,
            ].join("\n"),
        )
        .replace(
            "{{CSS}}",
            `<link rel="stylesheet" href="assets/${cssFile}">`,
        );

    await writeFile(
        join(outDir, "index.html"),
        html,
        "utf8",
    );

    // Static resources which are not handled by imports yet.
    await cp(
        join(srcDir, "pkg", "favicon", "airport.png"),
        join(outDir, "favicon.png"),
    );

    console.log(`Vendor JS: ${vendorJs}`);
    console.log(`Main JS:   ${mainJs}`);
    console.log(`CSS:       ${cssFile}`);
    console.log("Done");
}

main().catch((err) => {
    console.error(err);
    process.exit(1);
});