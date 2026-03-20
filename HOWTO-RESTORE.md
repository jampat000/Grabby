# Grabby backup & restore

Grabby stores your **settings** (Sonarr, Radarr, Emby cleaner, API keys, schedules) in a **local SQLite database** under your profile:

- **Windows:** `%LOCALAPPDATA%\Grabby\app.db` (usually `C:\Users\You\AppData\Local\Grabby\app.db`)

## One-file settings backup (recommended)

Use the **Web UI** so **Grabby** (Sonarr/Radarr) and **Cleaner** (Emby) settings are in **one JSON file** (API keys included).

1. Open Grabby in the browser (e.g. `http://127.0.0.1:8765` or dev `8766`).
2. Go to **Settings**.
3. Under **Backup & Restore**, click **Download backup**.
4. Keep the file **private** (same as a password manager export).

### Restore on a new install

1. Install/start Grabby on the new machine.
2. Open **Settings** → **Backup & Restore** → **Restore from backup**.
3. Choose the `.json` file, check the confirmation box, click **Restore from backup**.
4. **Restart the Grabby Windows service** (or the app) so the scheduler reloads.

**Note:** Import replaces **settings only** (Grabby + Cleaner). **Activity / dashboard history** is **not** in the JSON file.

## Full database copy (optional)

To clone **everything** in the database (including activity tables), **stop Grabby** (so the DB is not locked), then copy `app.db` to a safe place. To restore, stop Grabby and replace `app.db` with your copy.

## Git / source folder

Your **project folder** (clone of this repo) is separate from the **runtime database**. Backing up only the repo does **not** back up `app.db` unless you copy it separately or use the JSON export above.
