# Changelog

This file records the release notes available in this repository. Earlier package history was not supplied, so no older changes are inferred here.

## 1.3.0-1 (packaging revision)

- Corrected `CFBundleShortVersionString` and `CFBundleVersion` in the Settings bundle's `Info.plist` to `1.3.0`, matching the plugin version.
- No plugin functionality or executable behavior was changed.
- The Debian revision `-1` makes this packaging correction visible to APT/Sileo as an upgrade from `1.3.0`.

## 1.3.0

- Published the RootHide-native build; the package README describes support for iOS 15 and later.
- Includes the `preference-label-keeper` command-line utility and the optional PreferenceLoader Settings entry.
- Documents the `status`, `restore`, `capture`, and `refresh` commands.
- Package documentation states that Python is not required and that existing snapshots and the Settings toggle remain compatible.
