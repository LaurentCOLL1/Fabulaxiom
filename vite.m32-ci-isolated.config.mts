import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import path from "node:path";
import fs from "node:fs";
import process from "node:process";

/**
 * GitHub Windows-CI-only Vite configuration for an EXACT staged fictional UI.
 * NOT invoked by the ordinary "npm run dev" or any Tauri launch.
 * No environment-driven host binding, normal index.html, production src/,
 * plugin-supplied aliases to application code, or publicDir exposure.
 */
function checkedStage(): string {
  if (process.env.CI?.toLowerCase() !== "true" || process.env.RUNNER_OS !== "Windows") {
    throw Error("STOP: M3.2 fictional Vite only on ephemeral Windows CI");
  }
  if ("TAURI_DEV_HOST" in process.env || "__VITE_ADDITIONAL_SERVER_ALLOWED_HOSTS" in process.env) {
    throw Error("STOP: inherited dev host or additional hosts forbidden");
  }
  const candidate = process.env.M32_CI_FIXTURE_STAGE;
  if (!candidate || !path.isAbsolute(candidate)) throw Error("STOP: missing absolute fictional stage");
  const project = path.resolve(import.meta.dirname);
  const stage = fs.realpathSync(candidate);
  if (path.dirname(stage) !== project || !path.basename(stage).startsWith(".m32-fixture-only-")) {
    throw Error("STOP: stage must be a fresh direct child of the CI checkout");
  }
  if (fs.lstatSync(candidate).isSymbolicLink()) throw Error("STOP: staging symlinks forbidden");
  if (fs.existsSync(path.join(stage, "index.html")) || fs.existsSync(path.join(stage, "src", "App.tsx"))) {
    throw Error("STOP: normal UI files detected in fixture stage");
  }
  return stage;
}

export default defineConfig(() => {
  const stage = checkedStage();
  return {
    root: stage,
    envDir: stage,
    publicDir: false,
    appType: "mpa",
    plugins: [react()],
    server: {
      host: "127.0.0.1",
      port: 14279,
      strictPort: true,
      allowedHosts: [],
      cors: false,
      // Vite dev React refresh currently injects one inline module preamble.
      // 'unsafe-inline' in script-src is a DEV-ONLY compromise: NOT a
      // production or Tauri devCsp policy, and NOT an XSS-safe runtime claim.
      headers: {
        "Content-Security-Policy": [
          "default-src 'none'",
          "script-src 'self' 'unsafe-inline'",
          "style-src 'self' 'unsafe-inline'",
          "connect-src 'self' ws://127.0.0.1:14279",
          "img-src 'self' data:",
          "font-src 'self'",
          "object-src 'none'",
          "frame-src 'none'",
          "frame-ancestors 'none'",
          "base-uri 'none'",
          "form-action 'none'",
          "worker-src 'none'",
          "manifest-src 'none'",
        ].join("; "),
        "X-Content-Type-Options": "nosniff",
        "Referrer-Policy": "no-referrer",
      },
      hmr: {
        protocol: "ws", host: "127.0.0.1", clientPort: 14279,
      },
      fs: {
        strict: true,
        allow: [stage, path.join(import.meta.dirname, "node_modules")],
        deny: [
          ".env", ".env.*", "*.{crt,pem,key,p12,pfx,cer,der}",
          ".npmrc", ".yarnrc.yml", "**/.git/**",
          "**/src/App.tsx", "**/src/main.tsx", "**/index.html",
          "**/src-tauri/**", "**/.m32-fixture-only-*/**/*.sqlite",
        ],
      },
    },
  };
});
