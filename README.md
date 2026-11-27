# SHG Repo

**Repository author:** SHG  
**Repository:** <https://github.com/SHGnix/SHGnix.github.io>  
**APT source:** <https://shgnix.github.io/>

SHG Repo is a personal iOS jailbreak package repository for Sileo and RootHide-oriented packages.

## Add this source in Sileo

```text
https://shgnix.github.io/
```

The source icon (`CydiaIcon.png`) is generated from the SHGnix GitHub profile avatar during deployment.

## Available package

| Package | Package ID | Debian version | Plugin version |
|---|---|---:|---:|
| 名称保护（Roothide） | `local.preference-label-keeper` | `1.3.0-2` | `1.3.0` |

The package provides a command-line utility and an optional PreferenceLoader Settings entry. See the [package depiction](https://shgnix.github.io/depictions/local.preference-label-keeper-detail.html) for details.

## Repository layout

- `debs/` — versioned Debian packages.
- `icons/` — package icons served to package managers.
- `CydiaIcon.png` — repository icon generated from the GitHub profile avatar.
- `depictions/` — Sileo native JSON and HTML fallback descriptions.
- `metadata/packages.json` — package icon and depiction URLs.
- `scripts/rebuild-display-package.py` — creates the display-name/icon packaging revision.
- `scripts/enrich-packages.py` — injects display metadata and validates the generated APT index.
- `.github/workflows/build.yml` — builds `Packages`, `Packages.gz`, and `Release`, then publishes GitHub Pages.
- `RELEASING.md` — release and versioning procedure.

## Version information

The Debian package revision is `1.3.0-2`; the plugin's own version remains `1.3.0`. The suffix `-2` records a package metadata and artwork revision and does not indicate a plugin feature-version change.

Read [RELEASING.md](RELEASING.md) before preparing future releases.

## Author

**SHG** — repository maintainer.
