# WeLiPro Learning Edition

WeLiPro Learning Edition is a Windows release package for the WeLiPro desktop application. This repository keeps the runnable learning edition build in a clean release layout so it can be downloaded, inspected, and archived consistently.

## Quick Start

1. Download or clone this repository.
2. Keep the full directory structure intact.
3. Run `微凉Pro.exe` from the repository root.

The `_internal` directory contains the runtime files, Python extension modules, OCR engine files, and other bundled dependencies required by the executable. Do not move or delete it when running the application.

## Package Layout

```text
WeLiPro/
├── 微凉Pro.exe
├── _internal/
├── unins000.exe
├── unins000.dat
├── README.md
├── .gitattributes
└── .gitignore
```

## System Requirements

- Windows 10 or later, 64-bit
- Sufficient disk space for the bundled runtime
- Permission to run local desktop applications

## Notes

- This is a release package, not a source-code project.
- Large binaries are tracked with Git LFS to keep the repository usable.
- Debug captures, temporary patch files, Python bytecode caches, and local logs are intentionally excluded from the release tree.
- If Windows SmartScreen or antivirus software asks for confirmation, review the file source and choose whether to continue according to your own security policy.

## Maintenance

When preparing a new release:

1. Replace the executable and bundled runtime files.
2. Remove local debug folders, cache folders, temporary logs, and backup files.
3. Confirm Git LFS is enabled before committing large binaries.
4. Update this README if the package layout or usage changes.

