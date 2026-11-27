# Release and versioning procedure

Use this checklist for every new package release.

1. Keep the Debian `Package` identifier stable (`local.preference-label-keeper`) unless the package is intentionally being renamed or split.
2. Increase the Debian `Version` for every new build. Do not replace a published `.deb` with different contents while keeping the same version. Debian version ordering rules apply; use a higher version such as `1.3.1` for the next normal release.
3. Name the archive consistently, for example `pref-label-keeper_<version>_SHG_iphoneos-arm64e.deb`, and place it in `debs/`.
4. Keep older versioned `.deb` files in `debs/` when rollback availability is desired. The index is generated in multi-version mode so APT can see more than one version.
5. Add a new section to `CHANGELOG.md` using the exact version from the package control metadata. Record only changes included in that build.
6. Check that the package control metadata still has the correct `Package`, `Version`, `Architecture`, `Name`, and `Maintainer` values. Confirm that `CFBundleShortVersionString` and `CFBundleVersion` in the Settings bundle match the package version. The repository adds `Author`, `Icon`, `Depiction`, `SileoDepiction`, and `Homepage` from `metadata/packages.json` during index generation.
7. Commit the change to `main`. The GitHub Actions workflow scans all `.deb` files, enriches and validates `Packages`, creates `Packages.gz` and `Release`, and deploys GitHub Pages.
8. After the workflow succeeds, verify the published `Packages` and `Release` files, then refresh the source in Sileo and confirm the package version and depiction.

The build workflow rejects duplicate entries with the same package identifier, version, and architecture, and fails if a configured package is missing from the index.
