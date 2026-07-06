---
name: containerization
description: Packaging applications into containers correctly — writing Dockerfiles, docker-compose, image optimization, and container best practices. Use when the user asks to containerize an app, write or fix a Dockerfile, reduce image size, set up docker-compose, debug a container that won't build or run, or prepare a container for production. Focuses on small, secure, reproducible images and correct runtime behavior — not a bloated image that "works on my machine".
---

# Containerization

A container's promise is "runs identically everywhere." You keep that promise by building images that are **small, secure, reproducible, and correct at runtime** — and break it with bloated images, root users, baked-in secrets, and processes that ignore signals. This skill is the craft of doing it right.

## Writing a good Dockerfile

### Multi-stage builds (the single biggest win)
Separate the *build* environment from the *runtime* environment. Compile/install in a fat builder stage, copy only the artifacts into a lean final stage:
```dockerfile
FROM node:20-slim AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci                      # deps cached unless lockfile changes
COPY . .
RUN npm run build

FROM node:20-slim AS runtime
WORKDIR /app
ENV NODE_ENV=production
COPY package*.json ./
RUN npm ci --omit=dev && npm cache clean --force
COPY --from=build /app/dist ./dist
USER node                       # never run as root
EXPOSE 3000
CMD ["node", "dist/server.js"]
```
This alone often cuts image size by 5–10× and removes build tools (and their attack surface) from what you ship.

### Layer caching & order
Docker caches layers; a layer rebuilds if it or anything before it changes. **Order from least- to most-frequently-changing:** copy the dependency manifest and install deps *before* copying source, so a code change doesn't bust the (slow) dependency layer. Getting this order wrong makes every build reinstall everything.

### Small base images
- Prefer `-slim` or `alpine` or **distroless** over full OS images. Smaller = faster pulls, less attack surface, fewer CVEs.
- Watch alpine's musl-libc gotchas (some native deps misbehave); distroless has no shell (great for security, harder to debug — accept the tradeoff deliberately).
- Combine `RUN` steps that install-then-clean in one layer (`apt-get update && apt-get install -y … && rm -rf /var/lib/apt/lists/*`) so the cleanup actually shrinks the layer.

### `.dockerignore`
Always add one. Exclude `.git`, `node_modules`, build output, secrets, `.env`, test data. It shrinks the build context (faster builds), keeps junk and secrets out of the image, and improves cache behavior.

## Security (containers are a security boundary — treat them like one)

- **Never run as root.** Create and switch to a non-root user (`USER`). A root process in a container is a root escalation risk if the container is breached.
- **Never bake secrets into the image.** Not in `ENV`, not `COPY`ed in — image layers are inspectable and secrets in them are permanent even if "removed" in a later layer. Inject secrets at *runtime* (env vars from a secrets manager, mounted files, build secrets via `--mount=type=secret`).
- **Pin base image versions** — `node:20.11-slim`, not `node:latest`. `latest` makes builds non-reproducible and can pull in breaking or vulnerable changes silently.
- **Scan images** for vulnerabilities (Trivy, Grype, Docker Scout) in CI; rebuild on base-image security updates.
- **Minimal footprint**: fewer packages = fewer CVEs. Don't install debug tools into production images.
- Prefer read-only root filesystem and dropped capabilities at runtime where the app allows.

## Runtime correctness (where containers surprise people)

- **One main process per container**, and it must run in the **foreground** (containers live as long as PID 1 does). Don't background your app.
- **Handle signals (PID 1 problem).** Your process runs as PID 1 and must handle `SIGTERM` for graceful shutdown — otherwise the orchestrator's stop takes the full kill-timeout every time. Use an init (`--init` / tini) if your process doesn't reap children or handle signals, or handle them in-app.
- **Health checks**: define `HEALTHCHECK` (or orchestrator liveness/readiness probes) so the platform knows if the app is actually up, not just the process running.
- **Config via environment** (12-factor): the same image runs in dev/staging/prod, configured by env vars — never build a separate image per environment.
- **Logs to stdout/stderr**, not to files inside the container. The platform collects them; files inside an ephemeral container vanish.
- **Data is ephemeral**: anything that must survive a restart goes in a **volume**, not the container's writable layer.
- Set resource requests/limits (memory especially — an unbounded container gets OOM-killed unpredictably).

## docker-compose (local dev & multi-service)

- Define the service, its dependencies (DB, cache) as services, a shared network, named volumes for persistence, and env files.
- Use `depends_on` **with health conditions** — plain `depends_on` waits for start, not for *ready*; an app that connects before the DB is accepting connections crashes on boot.
- Keep compose for local/dev and simple deployments; reach for Kubernetes/orchestration only when you actually need its scaling/scheduling (don't K8s a two-container app).

## Debugging containers

1. **Build fails**: read the failing `RUN` step's output; reproduce the command in the base image interactively (`docker run -it <base> sh`). Common causes: wrong build context, missing files (check `.dockerignore`), cache serving stale layers (`--no-cache` to confirm).
2. **Builds but won't run/exits immediately**: check `docker logs`; usually PID 1 exited (background process, crash on startup, missing env/config, wrong `CMD`). Run interactively to poke: `docker run -it --entrypoint sh <image>`.
3. **Works locally, fails deployed**: env difference (missing env var/secret, arch mismatch — build multi-arch if needed, `linux/amd64` vs `arm64`), permissions (non-root user can't write somewhere), or a dependency the slim image lacks.
4. **Huge image**: `docker history <image>` to find the fat layers; multi-stage, slimmer base, combine+clean RUN layers, `.dockerignore`.

## Deliverable

For containerizing: a multi-stage Dockerfile (small pinned base, non-root, cache-ordered, secrets at runtime), a `.dockerignore`, health check and signal handling noted, and compose for local deps if relevant. For a fix: the diagnosed cause (build context / caching / PID-1 / env / size) and the corrected file. Note the resulting image size and that it runs non-root without baked secrets.

## Rules

- Multi-stage builds; small pinned base; cache-friendly layer order; a `.dockerignore` always.
- Non-root user; no secrets in the image (inject at runtime); scan for CVEs.
- One foreground process that handles SIGTERM; health checks; logs to stdout.
- Config and secrets via environment; persistent data in volumes; same image across environments.
- Reach for orchestration only when the workload needs it.
