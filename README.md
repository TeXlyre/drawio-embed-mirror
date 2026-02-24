# Draw.io Embed Mirror

Automated mirror of the Draw.io embeddable editor from https://embed.diagrams.net

## Purpose

This repository provides a self-hosted mirror of the Draw.io embed application, automatically synced via GitHub Actions. This allows applications to:

- Host Draw.io independently from diagrams.net CDN
- Control update timing
- Maintain version history
- Enable offline-first applications
- Ensure availability even if upstream is down

## Sync Schedule

- **Manual**: Can be triggered via GitHub Actions "Run workflow" button

## Usage

Replace the Draw.io CDN URL in your application:

**Before:**
```javascript
const DRAWIO_CDN = 'https://embed.diagrams.net/';
```

**After:**
```javascript
const DRAWIO_CDN = 'https://texlyre.github.io/drawio-embed-mirror/';
```

## Version Information

Current version information is available at:
- `https://texlyre.github.io/drawio-embed-mirror/VERSION.txt`
- `https://texlyre.github.io/drawio-embed-mirror/version-info.json`

## Setup Instructions

1. **Create this repository** on GitHub
2. **Enable GitHub Pages**:
   - Go to repository Settings → Pages
   - Source: GitHub Actions
3. **Run the workflow manually** for the first sync:
   - Go to Actions tab
   - Select "Sync Draw.io Embed"
   - Click "Run workflow"

## Monitoring

- Check the Actions tab for sync status
- Review commits for changes between versions
- Releases are automatically created for each version update

## License

This repository mirrors content from Draw.io (https://www.diagrams.net/), which is licensed under the Apache License 2.0.

The automation scripts in this repository are provided as-is for creating your own mirror.

## Disclaimer

This is an unofficial mirror. For the official Draw.io embed, visit https://embed.diagrams.net/
