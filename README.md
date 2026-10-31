<div align="center">
  <img src="docs/assets/logo.svg" alt="ArthiX mark" width="76" height="76" />
  <h1>ArthiX</h1>
  <p><strong>One workspace for the work behind your business.</strong></p>
  <p>An open-source, self-hosted operations platform for growing teams.</p>
</div>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-Apache--2.0-526DDF.svg" alt="Apache 2.0 license" /></a>
  <img src="https://img.shields.io/badge/self--hosted-yes-24A789.svg" alt="Self-hosted" />
  <img src="https://img.shields.io/badge/Node.js-22%2B-43853D.svg" alt="Node.js 22 or newer" />
</p>

<p align="center"><a href="https://github.com/channallikrishnasai/ArthiX">View the source on GitHub</a></p>

ArthiX brings customer relationships, finance, team work, and day-to-day operations into one connected application. Run it on infrastructure you control, explore it with the included StrideWorks Footwear demo, and configure the modules and integrations your team needs.

## Product introduction

Watch the two-minute ArthiX overview:

<video controls playsinline preload="metadata" poster="docs/media/ArthiX_Video_Poster.png" width="100%">
  <source src="docs/media/ArthiX_Product_Introduction.mp4" type="video/mp4" />
  <a href="docs/media/ArthiX_Product_Introduction.mp4">Play or download the ArthiX product introduction (MP4)</a>
</video>

Prefer slides? Open the [10-page ArthiX product presentation](docs/media/ArthiX_Overview.pdf).

## What’s inside

| Area | What it helps with |
|---|---|
| **CRM** | Organize companies, contacts, deals, and relationship activity. |
| **Finance** | Work with invoices, expenses, budgets, and approval flows. |
| **People** | Coordinate HR, payroll, time, and team information. |
| **Projects** | Track projects, tasks, and delivery work. |
| **Service** | Manage support requests and knowledge resources. |
| **Operations** | Connect products, inventory, vendors, purchasing, and orders. |
| **Workflows** | Configure event-driven business steps and routine actions. |
| **AI assistance** | Use optional AI features when a supported provider is configured. |

The application includes a browser-based admin workspace, API, marketing site, plugin marketplace, shared packages, and official integration plugins. Available behavior depends on the version and configuration you run.

## Try the demo

The StrideWorks Footwear seed dataset provides illustrative retail records to explore the workspace. Start the database services, apply migrations, then load the sample data:

```bash
git clone https://github.com/channallikrishnasai/ArthiX.git
cd ArthiX
cp .env.example .env
docker compose up -d postgres redis
pnpm install
pnpm db:migrate
pnpm seed
pnpm dev
```

Open the local apps:

| App | URL |
|---|---|
| Admin workspace | [http://localhost:3000](http://localhost:3000) |
| API | [http://localhost:3001](http://localhost:3001) |
| Marketing site | [http://localhost:3002](http://localhost:3002) |
| Plugin marketplace | [http://localhost:3003](http://localhost:3003) |

Demo sign-in:

| Role | Email | Password |
|---|---|---|
| Administrator | `admin@strideworks.com` | `demo1234` |
| Finance | `finance@strideworks.com` | `demo1234` |
| HR | `hr@strideworks.com` | `demo1234` |
| Employee | `john@strideworks.com` | `demo1234` |

These are public demo credentials for local evaluation only. Do not use them for a deployed or internet-accessible instance. `pnpm seed:clear` removes the sample data.

## Requirements

- Node.js 22 or newer
- pnpm 9 or newer
- Docker Desktop or Docker Engine with Compose

The database compose setup uses PostgreSQL 16 with pgvector and Redis 7. See [`.env.example`](.env.example) for available environment variables. Core app use does not require an AI provider; AI-assisted features require the corresponding provider and credentials to be configured.

## Run the full stack with Docker

The root Compose file builds all four application services from this source tree. Apply database migrations before starting the API and web apps:

```bash
cp .env.example .env
pnpm install
docker compose up -d postgres redis
pnpm db:migrate
pnpm seed                 # optional: load the sample business
docker compose up -d --build
```

For local development with hot reload, the same database setup is used; start the apps on the host instead of building their containers:

```bash
pnpm install
docker compose up -d postgres redis
pnpm db:migrate
pnpm seed
pnpm dev
```

## Project structure

```text
apps/
  admin/        Next.js business workspace
  api/          Hono API on Node.js
  marketing/    Product website and documentation
  marketplace/  Plugin and integration catalog
packages/
  ai/           AI providers and agents
  core/         Business entities, data access, and services
  sdk/          Plugin authoring interfaces
  ui/           Shared interface components
plugins/
  official/     Supported integration plugins
docker/         Database initialization and deployment assets
docs/           Architecture, guides, and product media
```

## Useful commands

| Command | Purpose |
|---|---|
| `pnpm dev` | Start the development apps. |
| `pnpm build` | Build the workspace packages and apps. |
| `pnpm typecheck` | Run TypeScript checks. |
| `pnpm lint` | Run linting across the workspace. |
| `pnpm db:migrate` | Apply database migrations. |
| `pnpm seed` | Load the StrideWorks Footwear demo dataset. |
| `pnpm seed:clear` | Remove demo records. |

## Configuration and deployment

Use the included [self-hosting guide](SELF_HOSTING.md), [architecture overview](ARCHITECTURE.md), and [environment example](.env.example) when preparing a deployment. Configure strong secrets, protect database and API access, set up backups, and review enabled integrations for your environment. Keep the demo credentials confined to local evaluation.

AI assistance is optional. When enabled, configure a supported provider and its credentials through the environment. Review generated suggestions before using them in consequential business workflows.

## Contributing

Issues and pull requests are welcome. Please read [CONTRIBUTING.md](CONTRIBUTING.md) and the [Code of Conduct](CODE_OF_CONDUCT.md) before contributing. Security concerns should be reported using [SECURITY.md](SECURITY.md).

## License

ArthiX is released under the [Apache License 2.0](LICENSE).
