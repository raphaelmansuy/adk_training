Removed `spec/` from the repository and purged it from history.

Actions taken:
- Created backup branch `backup/remove-spec-20251212-084600` to preserve current repository state.
- Added `spec/` to `.gitignore` and committed the change.
- Removed `spec/` from the repository and committed the deletion.
- Rewrote git history using `git filter-repo --path spec --invert-paths --force` to completely remove `spec/` from history.
- Expired reflog and ran `git gc --prune=now --aggressive` to clean up removed objects.

Notes:
- The `spec/` directory (ux_audit.md) is now untracked in the working tree (file remains locally, but is ignored by git).
- If this repository is hosted remotely and you want to propagate the history rewrite, run `git push --force --all` and `git push --force --tags` on your remotes after confirming with collaborators.
- For safety, consider creating a remote backup of branch `backup/remove-spec-20251212-084600` before forcing pushes.

If you want me to force-push these changes to any remote, let me know which remote to use and I'll proceed.

Raphaël Mansuy (automated change log)
