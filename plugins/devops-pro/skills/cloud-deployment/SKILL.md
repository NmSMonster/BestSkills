---
name: cloud-deployment
description: Deploying and running applications in the cloud — choosing the right compute, environment/config, scaling, networking, and production readiness on AWS/GCP/Azure or PaaS. Use when the user asks how to deploy an app, pick a hosting/compute option, set up environments, configure scaling or load balancing, prepare for production, or reduce cloud cost/downtime. Focuses on the right-sized, observable, recoverable deployment — not the most complex architecture.
---

# Cloud Deployment

Getting code into the cloud is easy; running it reliably, affordably, and recoverably is the skill. The two failure modes are opposite: over-engineering (Kubernetes and microservices for an app three people use) and under-engineering (a single unmonitored box with no backups holding production). The right answer is the **simplest architecture that meets the real requirements** — and you can always grow into more.

## Step 1 — Match compute to the workload

Pick the least-operational option that fits; move up the ladder only when you have a reason:
- **Static site / SPA** → static hosting + CDN (Netlify, Vercel, Cloudflare Pages, S3+CloudFront). Cheap, fast, nearly zero ops.
- **Standard web app / API** → a **PaaS** (Render, Railway, Fly.io, App Engine, App Runner, Heroku-likes) or managed containers. Handles scaling, TLS, deploys for you. **This is the right default for most apps** — don't reach past it without cause.
- **Containerized, needs orchestration at scale** → managed containers (ECS/Fargate, Cloud Run, Container Apps) before full Kubernetes. Cloud Run/Fargate give you containers without cluster ops.
- **Event-driven / spiky / low-volume** → serverless functions (Lambda, Cloud Functions) — pay per use, scale to zero. Watch cold starts and execution limits.
- **Full control / legacy / special needs** → VMs — most operational burden; justify it.
- **Kubernetes** → only when you genuinely need multi-service orchestration, complex scaling, or portability *and* have the ops capacity to run it. It is powerful and a large ongoing cost; most teams reaching for it don't need it yet.

Managed services over self-hosted for databases, queues, caches: a managed Postgres (RDS/Cloud SQL) handles backups, failover, and patching that you'd otherwise get wrong. Don't run your own stateful infra unless you must.

## Step 2 — Environments & configuration

- **Separate environments**: at least production and staging (and dev), isolated — separate credentials, databases, and ideally accounts/projects so a staging mistake can't touch prod.
- **Config via environment variables / secrets manager** (12-factor), never committed. The same artifact runs everywhere, configured per environment. Use the cloud's secrets manager (or Vault) — not `.env` files on servers, not secrets in the repo.
- **Least-privilege IAM**: each service gets only the permissions it needs; prefer role-based short-lived credentials (instance roles, workload identity, OIDC) over long-lived access keys. Over-broad IAM is the most common cloud breach vector.

## Step 3 — Networking, TLS, and the front door

- **HTTPS everywhere**, with managed certificates (ACM, managed certs, or automatic via the PaaS) — auto-renewed, never manual.
- **Load balancer** in front of multiple instances; health checks so traffic only goes to healthy instances.
- **Keep private things private**: databases and internal services in private subnets, not on the public internet. Public exposure only for what must be public, behind a security group/firewall scoped to the minimum.
- **CDN** for static assets and cacheable responses — cuts latency and origin load.
- A WAF and DDoS protection for public-facing production.

## Step 4 — Scaling & availability

- **Design stateless app instances** so you can run many behind a load balancer and scale horizontally. Push state to managed data stores, session stores, and object storage — not local disk. A stateless app is the prerequisite for every scaling and rollback strategy.
- **Autoscaling** on a real signal (CPU, request count, queue depth) with sane min/max. Set the min for your baseline, the max to cap cost.
- **Multi-AZ / redundancy** for production availability: more than one instance, across availability zones, so one failure isn't an outage. Multi-region only when the requirements (latency, DR) justify the complexity.
- Managed database with automated backups and, for production, a failover replica.

## Step 5 — Production readiness (the checklist people skip)

Before calling it production:
- [ ] **Observability**: centralized logs, metrics (latency, error rate, saturation), and alerting on symptoms users feel. You cannot operate what you cannot see. Add tracing for distributed systems.
- [ ] **Backups — and a tested restore.** Automated backups are worthless until you've *restored* one. Know your RPO/RTO.
- [ ] **Health checks & auto-recovery**: unhealthy instances are replaced automatically.
- [ ] **Rollback**: a one-step way back to the last good version (pairs with `ci-cd` deploy strategies).
- [ ] **Secrets** in a manager, not in env files on disk or the repo.
- [ ] **Cost controls**: billing alerts, right-sized instances, autoscaling caps. Cloud bills surprise teams that don't set alerts.
- [ ] **Security**: least-privilege IAM, private networking, patched images, no public database.
- [ ] **A runbook**: how to deploy, roll back, and who's paged when it breaks.

## Cost awareness

The big cloud-cost leaks: over-provisioned always-on instances (right-size; scale to zero where possible), forgotten resources (idle instances, unattached disks, old snapshots), egress bandwidth (CDN cuts it), and un-alerted growth. Set a billing alert on day one. Match spend to actual load — most cloud waste is paying for capacity you don't use.

## Deliverable

A deployment plan: the chosen compute (and *why* it's right-sized for this workload), environment/config/secrets setup, networking + TLS, the scaling and availability approach, and the production-readiness checklist status (observability, backups+restore, rollback, cost controls). For a review: what's missing for production, prioritized by risk (no backups / no monitoring / public database before minor cost tuning). Recommend the simplest thing that meets the requirement, with the growth path noted.

## Rules

- Simplest architecture that meets real requirements; PaaS/managed by default, up the ladder only with cause.
- Managed services for stateful infra (DB, cache, queue) unless you truly must self-host.
- Stateless app instances; config and secrets via environment/secrets-manager; least-privilege IAM.
- HTTPS everywhere; keep databases and internals off the public internet.
- Not production without observability, tested backups, health checks, rollback, and billing alerts.
- Set cost alerts and right-size from the start.
