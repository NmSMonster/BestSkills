---
name: infrastructure-as-code
description: Managing infrastructure declaratively and reproducibly with code — Terraform/OpenTofu, Pulumi, CloudFormation, and config management. Use when the user asks to write or review Terraform/IaC, provision cloud resources as code, set up reproducible environments, manage state, structure IaC modules, or move from click-ops to version-controlled infrastructure. Focuses on safe, reviewable, reproducible infrastructure changes with protected state — not one-off console clicking.
---

# Infrastructure as Code (IaC)

IaC makes infrastructure **reproducible, reviewable, and versioned** — the same code produces the same environment, changes go through review, and you can recreate everything after a disaster. The discipline that makes it safe rather than dangerous is: plan before apply, protect the state, and treat infra changes with the same rigor as production code changes (because that's what they are).

## Core principles

- **Declarative over imperative**: describe the *desired end state*; let the tool compute the diff to get there. You say "3 instances, this network, this database"; the tool figures out create/update/delete. Prefer Terraform/OpenTofu/Pulumi/CloudFormation over shell scripts that imperatively poke APIs.
- **Everything in version control**: all infra definitions in git, changed via pull requests, reviewed like code. The repo is the single source of truth — the cloud console reflects the code, never the reverse.
- **No manual drift.** Once infra is code, stop clicking in the console. Manual changes create **drift** — reality diverging from code — which the next `apply` may silently revert or clash with. If you must hotfix in the console during an incident, reconcile it back into code immediately.
- **Reproducible**: the code plus a state file recreates the environment. Someone should be able to stand up a new environment from the repo.

## The plan → review → apply loop (never skip plan)

The cardinal safety rule: **always review the plan before applying.**
1. `terraform plan` (or `pulumi preview`, change set) — shows exactly what will be created, changed, and **destroyed**. Read it, every time.
2. **Scrutinize destroys and replacements.** The dangerous line in any plan is `destroy` or `-/+ replace` — a change that looks innocent (renaming, changing an immutable attribute) can force-replace a database and delete its data. If the plan shows a destroy you didn't intend, stop and understand why before applying.
3. Apply only a reviewed plan. In CI, run `plan` on the PR (so reviewers see the diff) and `apply` on merge, gated for production.
4. Never `apply` blind, and never let anyone apply from their laptop to production — route prod changes through the pipeline.

## State — protect it like a database (because it is one)

The state file maps your code to real resources. Mishandle it and you get duplicate resources, orphaned infra, or corruption.
- **Remote, shared, locked state**: store state in a remote backend (S3+DynamoDB lock, Terraform Cloud, GCS) — never a local state file for team/production infra. Locking prevents two applies from corrupting it simultaneously.
- **State contains secrets** (DB passwords, keys can land in it) — encrypt it at rest, restrict access tightly. Never commit state to git.
- **Never hand-edit state.** Use the tool's commands (`state mv`, `import`, `taint`) for surgery. Back it up / enable versioning on the backend before risky operations.
- Separate state per environment so a staging change can't touch prod state.

## Structure & reuse

- **Modules** for reusable, composable pieces (a "web service" module, a "database" module) — parameterized, so you don't copy-paste infra. But don't over-abstract early; a module earns its existence at the second or third use.
- **Separate environments** (dev/staging/prod) via separate state and variable files or workspaces — with prod configured for real availability (multi-AZ, bigger sizes) and dev kept cheap. Keep them structurally identical so staging actually predicts prod.
- **Variables and outputs**: parameterize what differs between environments; output what other layers need (endpoints, IDs). No hardcoded environment-specific values in shared code.
- **Pin provider and module versions** — unpinned providers make applies non-reproducible and can introduce breaking changes on the next run.

## Security

- **No secrets in IaC code or state-in-git.** Reference secrets from a secrets manager / inject at apply time; mark sensitive variables `sensitive`. A password hardcoded in a `.tf` file is a password in git history forever.
- **Least-privilege everywhere**: the IAM roles you *create* should be least-privilege, and the credentials the IaC tool *runs with* should be scoped to what it manages — a Terraform runner with god-mode is a huge blast radius.
- **Policy as code** for guardrails on larger teams (OPA/Sentinel/tfsec/checkov) — scan plans for insecure configs (public buckets, open security groups, unencrypted volumes) in CI before apply.
- Scan for exposed secrets and misconfigurations as a pipeline gate.

## Safe change practice

- **Small, incremental changes** over giant ones — a huge plan is unreviewable and risky. Change a little, plan, apply, verify.
- **Understand replacements before applying**: know which attribute changes force resource replacement (and data loss). Use `create_before_destroy` where appropriate; use `prevent_destroy` on stateful resources you must never lose.
- **Import existing resources** rather than recreating when adopting IaC over existing infra.
- Test in dev/staging first; production applies are gated and reviewed.
- For stateful resources (databases), be extra deliberate — backups before changes, and never let a casual attribute tweak force-replace them.

## Deliverable

For writing IaC: modular, version-pinned, environment-parameterized code with remote locked state, secrets referenced not embedded, and least-privilege roles — plus the `plan` output reviewed and destroys explained. For a review: findings prioritized by blast radius (unprotected state, hardcoded secrets, force-replace of stateful resources, over-broad IAM, public exposure before style nits), each with the fix. Always show/summarize the plan and call out anything destructive.

## Rules

- Declarative, version-controlled, reviewed via PR — no manual console drift.
- Always read the plan before apply; scrutinize every destroy and replace; never apply blind or from a laptop to prod.
- Remote, locked, encrypted state; never commit it, never hand-edit it.
- No secrets in code or state-in-git; least-privilege for both created roles and the runner.
- Pin versions; modularize for reuse; keep environments isolated and structurally identical.
- Small reviewed changes; guard stateful resources against accidental replacement.
