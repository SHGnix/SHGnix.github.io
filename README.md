# SHGnix iOS Repository

**Repository author:** SHG  
**Repository:** <https://github.com/SHGnix/repo>  
**APT source:** <https://shgnix.github.io/repo/>

SHGnix is a personal iOS jailbreak package repository. The current listing is built for RootHide-oriented packages and is indexed for Sileo.

## Add this source in Sileo

```text
https://shgnix.github.io/repo/
```

## Available package

| Package | Package ID | Version | Notes |
|---|---|---:|---|
| 名称保护（RootHide 原生版） | `local.preference-label-keeper` | `1.3.0` | RootHide 原生版本，安装包说明标注 iOS 15+ |

The package provides a command-line utility. PreferenceLoader is recommended for the optional Settings entry; the command-line component is standalone. See the [package depiction](https://shgnix.github.io/repo/depictions/local.preference-label-keeper.html) for details.

## Repository layout

- `debs/` — installable Debian packages.
- `icons/` — package icons served to package managers.
- `depictions/` — Sileo native JSON and HTML fallback descriptions.
- `metadata/packages.json` — extra package-index fields such as author, icon, and depiction URLs.
- `scripts/enrich-packages.py` — injects display metadata and validates the generated APT index.
- `.github/workflows/build.yml` — builds `Packages`, `Packages.gz`, and `Release`, then publishes GitHub Pages.
- `CHANGELOG.md` — published package changes.
- `RELEASING.md` — release and versioning procedure.

## Publishing a new version

Read [RELEASING.md](RELEASING.md) before adding a new `.deb`. Keep the Debian package identifier stable, increase its version for every new build, append a factual changelog entry, and commit the package to `debs/`. GitHub Actions regenerates the repository indexes automatically.

## Author

**SHG** — repository maintainer.
