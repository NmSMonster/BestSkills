---
name: git-workflow
description: Git operations beyond the basics — rebasing, resolving merge conflicts, rewriting history safely, recovering lost work, bisecting, and clean branching/commit practice. Use when the user is stuck in a git mess, needs to resolve conflicts, wants to clean up commits before a PR, recover deleted commits/branches, undo a bad operation, or asks how to do a specific git task safely. Emphasizes recoverability and never losing work.
---

# Git Workflow

Git almost never truly loses committed work — it just hides it. The core discipline is: **know where you are before you act, prefer reversible operations, and know that the reflog is your undo button.** Most "I destroyed my repo" situations are a two-command recovery once you stay calm.

## Before any risky operation — orient

```
git status            # working tree state, current branch
git log --oneline -10 # recent history
git branch -vv        # branches and their upstreams
```
And before anything that rewrites history or discards changes, create an escape hatch:
```
git branch backup-before-thing     # a free, instant safety net — delete it later if unused
```
This one habit turns every scary operation into a reversible one.

## The recoverability facts (internalize these)

- **The reflog remembers everything** your HEAD pointed at for ~90 days, including commits you "lost" via reset, rebase, or amend: `git reflog` → find the SHA → `git checkout <sha>` or `git branch recovered <sha>`.
- **Committed = safe.** If work was ever committed, it's recoverable even after a hard reset. Uncommitted changes are the only ones truly at risk — which is why you commit or `git stash` before experiments.
- `git reset --hard` and `git clean -fd` are the two commands that actually destroy uncommitted work. Treat them as the only genuinely dangerous ones and double-check the working tree first.

## Common tasks, done right

### Resolving merge/rebase conflicts
1. `git status` lists conflicted files. Open each; the `<<<<<<< HEAD` / `=======` / `>>>>>>>` markers separate *your* side from *theirs*.
2. Resolve by **understanding both intents**, not by blindly keeping one side. The correct result often takes pieces of both — a conflict means two changes touched the same lines, and you must reconcile the *logic*, not just the text.
3. Remove all markers, make the code actually correct (compile/test it — resolved-but-broken is common), then `git add <file>`.
4. Continue: `git rebase --continue` / `git merge --continue`. Lost/confused? `git rebase --abort` / `git merge --abort` returns you to before the operation — no harm done.
- For a file you want entirely one side: `git checkout --ours <file>` / `--theirs <file>` (note: meanings flip between merge and rebase — verify with a diff after).

### Cleaning up commits before a PR (interactive rebase)
- `git rebase -i HEAD~N` to squash WIP commits, reword messages, reorder, or drop. Squash "fix typo"/"wip" noise into meaningful commits — a reviewer reads commits, so make them tell a story.
- **Only rewrite history that hasn't been shared** (local/your-own-branch commits). Rewriting pushed, shared history forces everyone else into a mess.
- After rewriting a branch you already pushed, use `git push --force-with-lease` (never plain `--force`) — `--force-with-lease` refuses if someone else pushed meanwhile, preventing you from clobbering their work.

### Rebase vs merge
- **Rebase** your feature branch onto updated main to keep a linear history and replay your commits on top: `git fetch && git rebase origin/main`. Cleaner history, but rewrites your branch's commits (fine if unshared).
- **Merge** to preserve exact history and when the branch is shared. Merge commits are honest about what happened.
- Team convention wins over personal preference — match the repo.

### Undoing things (pick by what you want)
| Want | Command | Note |
|---|---|---|
| Undo uncommitted changes to a file | `git restore <file>` | discards edits — gone if not stashed |
| Unstage but keep changes | `git restore --staged <file>` | |
| Undo last commit, keep changes staged | `git reset --soft HEAD~1` | safe; work preserved |
| Undo last commit, keep changes unstaged | `git reset HEAD~1` | safe |
| Undo a **pushed** commit | `git revert <sha>` | makes a new inverse commit — safe for shared history |
| Discard everything to last commit | `git reset --hard HEAD` | ⚠ destroys uncommitted work |
| Amend last commit message/content | `git commit --amend` | rewrites — only if unpushed |

Rule: on **shared/pushed** history, undo with `git revert` (adds a commit), never with `reset --hard` + force (rewrites others' base).

### Recovering lost work
- Lost commits after a bad reset/rebase: `git reflog`, find the SHA where things were good, `git branch recovered <sha>` or `git reset --hard <sha>` (on your own branch).
- Deleted branch: `git reflog` still has its tip SHA → `git branch <name> <sha>`.
- Dropped stash: `git fsck --no-reflog | grep commit` or `git stash list`; stashes are commits too.
- Accidentally `reset --hard` with **uncommitted** work: that's the one hard case — check IDE local history / editor backups; going forward, `stash` before resets.

### Finding which commit broke something
`git bisect start` → `git bisect bad` (now) → `git bisect good <old-sha>` → test each checkout, mark `good`/`bad` → git binary-searches to the culprit commit in log2(N) steps. Automate with `git bisect run <test-command>`. (This is the fastest localization tool for regressions — pairs with the `systematic-debugging` skill.)

## Good hygiene (prevents the messes above)

- **Commit small and often** with messages that say *why*: imperative summary ≤ 50 chars, blank line, body explaining reasoning. Committed work is recoverable work.
- **Branch per unit of work**; keep `main` deployable. Short-lived branches conflict less.
- `.gitignore` before the first commit (build artifacts, `.env`, secrets, deps). A secret committed is a secret leaked — rotate it, don't just `git rm`.
- **Pull with rebase** (`git pull --rebase`) on feature branches to avoid noise merge commits, if the team agrees.
- Never commit secrets or large binaries. If you did and pushed: rotate the secret immediately (history rewrite alone doesn't un-leak it).

## When helping someone out of a git mess

1. **Diagnose before touching**: `git status`, `git reflog`, `git log --oneline --all --graph -20` — understand the actual state; the user's description of what happened is often wrong.
2. **Make a backup branch/tag** at the current state before any fix.
3. Prefer the **reversible** fix (revert, new branch from reflog) over the destructive one (force-push, hard reset), unless the user explicitly wants history gone.
4. Explain what each command will do *before* running it, especially anything with `--force` or `--hard`. Confirm before destructive, shared-history operations.
