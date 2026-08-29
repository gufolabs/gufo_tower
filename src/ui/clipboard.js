// ----------------------------------------------------------------------
// clipboard utilities
// ----------------------------------------------------------------------
// Copyright (C) 2015-2026 Gufo Labs
// See LICENSE.md for details
// ----------------------------------------------------------------------

import { Tower } from "./lib";

export async function copyToClipboard(text) {
    if (navigator.clipboard) {
        await navigator.clipboard.writeText(text);
        Tower.msg.complete("Copied to clipboard");
        return;
    }
    const textarea = document.createElement("textarea");
    textarea.value = text;
    textarea.style.position = "fixed";
    textarea.style.opacity = "0";
    document.body.appendChild(textarea);
    textarea.select();
    try {
        if (!document.execCommand("copy")) {
            Tower.msg.failed("Failed to copy to clipboard");
            throw new Error("Copy failed");
        }
        Tower.msg.complete("Copied to clipboard");
    } finally {
        textarea.remove();
    }
}