# Changelog

This file records the release notes available in this repository. Earlier package history was not supplied, so no older changes are inferred here.

## 1.3.0-2 (display-name and artwork revision)

- Changed the package display name to **名称保护（Roothide）** in Debian metadata and the Settings bundle.
- Set the embedded PreferenceLoader icon to exactly 58 × 58 pixels.
- Kept the plugin's own `CFBundleShortVersionString` and `CFBundleVersion` at `1.3.0`.
- Added a repository icon generated from the SHGnix GitHub profile avatar during deployment.

## 1.3.0-1 (version metadata revision)

- Corrected `CFBundleShortVersionString` and `CFBundleVersion` in the Settings bundle's `Info.plist` to `1.3.0`, matching the plugin version.
- No plugin functionality or executable behavior was changed.

## 1.3.0

- Published the RootHide-native build; the package README describes support for iOS 15 and later.
- Includes the `preference-label-keeper` command-line utility and the optional PreferenceLoader Settings entry.
- Documents the `status`, `restore`, `capture`, and `refresh` commands.
- Package documentation states that Python is not required and that existing snapshots and the Settings toggle remain compatible.
