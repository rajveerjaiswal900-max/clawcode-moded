# Nexora package migration status

Last checked: 2026-10-16.

- Required Android application ID: `com.nexora.ai`.
- Local candidate APK `clawcode-moded-com.nexora.ai.apk`: manifest package verified as `com.nexora.ai`.
- Existing GitHub release asset `clawcode-moded-version.apk`: manifest package verified as `gptos.intelligence.assistant`.
- A GitHub Actions workflow at `.github/workflows/release-apk-package-check.yml` checks the release APK's ZIP integrity and requires the expected package ID on new releases and weekly.
- The workflow has been committed but its first run has not been confirmed. Because the current release has the old package ID, its package check is expected to fail until a correctly verified APK is released.
- Decompilation, Android build, installation, and runtime testing have not yet been completed. The original Android Studio source project was not available in the inspected files.

Do not rename or replace the published release asset based only on its filename. Confirm the manifest package ID and installation/runtime behavior before publishing a replacement.
