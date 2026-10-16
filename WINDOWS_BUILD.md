# Windows PC Build Guide

## Current status

A Windows `.exe` has **not** been built. The current repository contains release documentation and an Android APK, but no application source code or build configuration. An APK is an Android package, not a Windows executable, and simply renaming it to `.exe` will not work.

## What is needed before a Windows build

Provide one of the following:

1. The original app source repository (preferred), including its license and build instructions; or
2. The complete source project archive and confirmation that you have permission to build and distribute a Windows version.

The correct packaging route depends on the technology used by the source project:

- **.NET / C#**: a Windows desktop target can be published as an `.exe` if the application supports it.
- **Flutter**: enable the Windows desktop target and build the Windows runner.
- **Electron or Tauri**: package the web/desktop application for Windows using its supported build tools.
- **Android Java/Kotlin only**: this generally requires a desktop port or a supported cross-platform rewrite; the APK cannot be converted directly into a native Windows app.
- **APK only, no source**: use a compatible Android emulator to run the Android app on Windows. This is not a native `.exe` build.

## Recommended release workflow

1. Identify the source framework and confirm third-party license/redistribution rights.
2. Build and test the Windows app on Windows (or a supported Windows CI runner).
3. Test startup, network access, sign-in, file handling, and required permissions.
4. Package the output and scan it with trusted security tools.
5. Generate a SHA-256 checksum for the final installer.
6. Attach the actual Windows installer to a GitHub Release, clearly marked as a Windows build.
7. Keep the Android APK and Windows installer as separate assets, with separate compatibility notes.

## Planned release asset naming

Choose a name only after the build target is confirmed, for example:

- `Clawcode-Moded-Setup-x64.exe` for a Windows installer, or
- `Clawcode-Moded-Portable-x64.exe` for a genuinely portable build.

These are suggested names, not existing downloads.

## Next step

Share the source-code repository URL or upload the complete source project. Do not upload passwords, API keys, signing keys, or other secrets. Once the framework is known, the Windows build configuration and GitHub Actions workflow can be prepared for that project.
