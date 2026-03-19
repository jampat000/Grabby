# Restore and Backup Guide

This guide helps you keep your app files and chat history safe.

## What is already safe right now

- Project folder exists at `C:\Users\User\grabby`
- Local Git history is enabled in this folder
- A full backup zip was created in `C:\Users\User\grabby-backups`

## One-click backup (project + chat transcripts)

Run this any time (especially before updates/restarts):

```powershell
cd C:\Users\User\grabby
.\scripts\backup-all.ps1
```

It creates timestamped zip files in:

- `C:\Users\User\grabby-backups`

Expected output files:

- `grabby-YYYYMMDD-HHMMSS.zip`
- `grabby-transcripts-YYYYMMDD-HHMMSS.zip`

## Reopen your project after restart

1. Open Cursor
2. Open folder: `C:\Users\User\grabby`
3. Start app in dev mode if needed:

```powershell
cd C:\Users\User\grabby
.\scripts\dev-start.ps1
```

Then browse to:

- URL shown by the script (usually `http://127.0.0.1:8766`)

## Restore from backup zip

If needed, extract the newest zip from:

- `C:\Users\User\grabby-backups`

Extract back to:

- `C:\Users\User\grabby`

## Recommended extra safety

- Keep using Git commits after each work session.
- Push to a private GitHub repo for off-PC backup.
- Keep backup zips in OneDrive or an external drive too.
