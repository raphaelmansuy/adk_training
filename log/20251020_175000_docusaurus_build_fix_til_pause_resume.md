# Docusaurus Build Fix: TIL Pause & Resume Document Location

## Issue

**Error**: `npm run build` was failing with Docusaurus error:

```txt
Error: Invalid sidebar file at "sidebars.ts".
These sidebar document ids do not exist:
- til/til_pause_resume_20251020
```

The build was failing both locally and in CI/GitHub Actions.

## Root Cause

The file `til_pause_resume_20251020.md` was placed in `/docs/til/` directory
instead of the correct location `/docs/docs/til/`.

Docusaurus is configured to look for documentation files in `/docs/docs/`
directory. Since the file was one level too high in the directory hierarchy,
Docusaurus couldn't find it even though it was referenced in `sidebars.ts`.

## Solution

Moved the file from the wrong location to the correct location:

- **From**: `/docs/til/til_pause_resume_20251020.md`
- **To**: `/docs/docs/til/til_pause_resume_20251020.md`

## Verification

- ✅ Local `npm run build` now completes successfully
- ✅ No breaking changes to content or frontmatter
- ✅ Sidebar reference in `sidebars.ts` remains correct
- ✅ File move properly tracked in git

## Files Changed

- Moved: `docs/til/til_pause_resume_20251020.md` →
  `docs/docs/til/til_pause_resume_20251020.md`

## Build Status

- **Before**: ❌ Failed with "Invalid sidebar file" error
- **After**: ✅ Build completes successfully with all documents found

## Notes

- The other TIL files were already in the correct location (`docs/docs/til/`)
- This was introduced when the pause_resume TIL was first created
- Future TIL documents should be created in `/docs/docs/til/` directly
