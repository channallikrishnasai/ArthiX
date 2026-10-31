# @veska/cli

CLI for building and running [ArthiX](https://github.com/channallikrishnasai/ArthiX) plugins.

## Usage

```bash
# Scaffold a new plugin (no install needed)
npx @veska/cli create-plugin my-plugin

# Or install globally
npm install -g @veska/cli
ArthiX create-plugin my-plugin
```

## Commands

### `ArthiX create-plugin [name]`

Scaffolds a new plugin directory with:

- `ArthiX.plugin.json` — plugin manifest
- `package.json` — with `@veska/sdk` dependency
- `src/index.ts` — `onInstall` / `onUninstall` entry points
- `tsconfig.json`

### `ArthiX dev`

Starts a local ArthiX dev instance via Docker Compose and prints the service URLs.

```
ArthiX API:      http://localhost:3001
ArthiX Admin UI: http://localhost:3000
PostgreSQL:     localhost:5432
Redis:          localhost:6379
```

Use `--no-docker` to skip Docker Compose startup if services are already running.

## License

Apache 2.0
