# Changelog

## v1.0.0

### Added
- **Downloadable installers**: Windows setup (`.exe`), macOS disk image
  (`.dmg`, Apple Silicon) and a Linux archive (`.tar.gz`), built
  automatically by GitHub Actions. No terminal or Python required.
- **App icon** for the installer, taskbar/dock and window title bars.
- **Built-in backend**: official builds connect to the project's
  Supabase instance, so users no longer create a Supabase project or a
  `.env` file. (Developers can still override with a `.env`.)
- **Forgot password**: reset your password in the app with an emailed code.
- **Delete account**: permanently deletes the account and all data.
- Row Level Security policies and account-deletion function
  (`migrations/002_rls_and_account_deletion.sql`).
- Version shown on the login screen; friendly error if the app is
  misconfigured instead of a silent crash.
- Maintainer guide: `docs/SUPABASE_SETUP.md`.

### Changed
- App version now lives in `app/version.py`.

## v0.5.0

### Added
- Recurring transactions (daily, weekly, monthly, yearly, optional end date).
- Charts: income vs. expenses, spending by category, balance over time.
- Period filter, "Repeats" column, Groceries and Fuel categories.
- Migration `001_add_recurrence.sql` and unit tests.

### Fixed
- Sign-out crash, empty-notes crash, negative amount formatting.
