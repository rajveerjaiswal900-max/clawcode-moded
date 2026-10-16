# Nexora AI — Android Compatibility & Performance Plan

Status: implementation plan only. This document does not claim that the APK has been rebuilt or tested.

## Goal
Make Nexora AI work reliably across the widest practical range of Android devices, including older 32-bit devices where the app's framework and dependencies permit it, while improving startup time, responsiveness, and crash resilience.

"Every Android device" cannot be guaranteed: support depends on Android API level, CPU ABI, hardware capabilities, Google Play services, available RAM, and third-party SDK requirements. Publish an explicit tested device/API matrix.

## Required source-first workflow
1. Obtain the complete, authorized Android Studio source project and identify the actual framework (Kotlin/Java, Flutter, React Native, Capacitor, etc.). APK-only reverse engineering cannot reliably recreate original source or guarantee a maintainable build.
2. Record baseline: package ID, versionCode/versionName, minSdk/targetSdk, supported ABIs, permissions, native libraries, dependency versions, APK/AAB size, cold/warm startup, memory, crashes, and network request timing.
3. Preserve the existing release. Develop in a separate branch and produce a reproducible build.
4. Run static checks, unit tests, lint, dependency/security checks, install tests, and runtime smoke tests before release.

## Compatibility strategy
- Set minSdk based on the oldest Android version the chosen framework and every required SDK actually support; do not lower it blindly.
- Build all required native ABIs supported by dependencies: arm64-v8a and, if feasible, armeabi-v7a. Include x86/x86_64 only when supported/needed for emulator testing. A 32-bit ABI cannot be added if a mandatory native dependency has no 32-bit build.
- Use AndroidX and stable, mutually compatible dependency versions. Remove unused libraries and avoid unnecessary SDKs.
- Check API-level guards for newer APIs; provide fallbacks for older versions. Avoid assuming Google Play services or modern hardware features exist.
- Keep manifest permissions minimal. Verify cleartext traffic, exported components, network security config, and deep links.
- Handle rotation, process death, low-memory conditions, offline mode, slow/failed networks, expired sessions, and lifecycle cancellation.
- Ensure layouts adapt to small screens, display cutouts, font scaling, dark/light mode, and accessibility settings.

## Startup and responsiveness
- Keep Application/onCreate and first screen work minimal; defer nonessential initialization until needed.
- Avoid synchronous disk, database, or network work on the main thread.
- Show the first usable screen before loading optional data. Use bounded network timeouts, cancellation, caching where safe, and exponential backoff with jitter for retryable requests.
- Use lazy loading and pagination for long lists; optimize images and avoid large allocations.
- Enable R8 shrinking/obfuscation for release only after verifying keep rules and runtime reflection.
- Measure cold and warm startup before and after changes; do not claim speed improvements without repeatable measurements on low-end devices.

## Test matrix
- Oldest intended Android API and newest supported API.
- 32-bit ARM device if armeabi-v7a is shipped; 64-bit ARM device; emulator ABI as applicable.
- Low-memory/low-storage conditions, slow/offline network, background/foreground, rotation, dark mode, large font, and interrupted requests.
- Verify install, upgrade, clean launch, sign-in, core chat flow, error handling, and uninstall/reinstall.
- Validate APK signature and package ID `com.nexora.ai`; verify upgrade signing key continuity before replacing an existing installed app.

## Release gates
- Confirm manifest package ID, minSdk/targetSdk, and shipped ABI list from the built artifact.
- Install and run on real test devices; run automated smoke tests.
- Compare performance against the baseline and publish measured results.
- Generate SHA-256 checksum, maintain release notes, and keep signing credentials out of Git.
- Do not replace a release asset until the new APK is verified and install/runtime tests pass.

## Current known limitation
The inspected `clawcode-moded` repository contains release documentation/workflow but not the full Android source project. The inspected APK was reported to contain arm64-v8a native libraries only. This is a compatibility risk for 32-bit-only devices, not proof that every older phone is unsupported. The APK has not yet been fully decompiled, rebuilt, installed, or runtime-tested in this environment.

## Required next input
Provide the original source repository URL or complete source project ZIP, plus the oldest Android version/device that must be supported. Never share API keys, passwords, or signing keystores.
