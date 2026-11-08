# Changelog

## v1.1.3

### Fixed
- Password reset no longer says "invalid or expired code" when the code was
  fine but the **new password** was rejected (same as the old one, too weak
  for the server's rules...). It now says which, and lets you try another
  password without asking for a new code.
- Spaces in the pasted code and capital letters in the email are ignored.

## v1.1.2

### Fixed
- "Forgot password" now shows the specific reason when the code can't be
  sent (timeout, too many emails, ...) and logs it to the log file.

## v1.1.1

### Fixed
- When the server times out (for example while sending the confirmation
  email), sign-up now says so instead of showing a generic error.

## v1.1.0

### Added
- **First-login tutorial**: a short, skippable 5-step walkthrough appears
  the first time an account signs in (adding transactions, recurring
  entries, charts, your data). Reopen it any time with the **Help** button.
- `tools/check_auth.py`: checks that sign-up against your Supabase project
  works and explains any failure.
- Errors are written to `~/.financetracker/financetracker.log`, so problems
  can be diagnosed even though the packaged app has no console.

### Fixed
- Sign-up and sign-in now show a **specific** message (too many emails,
  email not allowed, account already exists, weak password, no internet,
  outdated app...) instead of one generic error.

## v1.0.0

### Added
- **Plug-and-play downloads**: download, extract and open `FinanceTracker`.
  Available as a Windows `.zip` (plus an optional `.exe` installer), a
  macOS `.zip` / `.dmg` (Apple Silicon) and a Linux `.tar.gz`, built
  automatically by GitHub Actions. No terminal, Python or setup required.
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

### Dashboard floating action dock correction
- Removed the About/Settings dock from the main vertical layout so it no longer reserves a full-width footer strip.
- Repositioned the dock as a small transparent overlay anchored to the lower-left corner of the dashboard.
- The charts/transactions tab now receives the reclaimed vertical space and remains visible in normal-sized windows.

### Dashboard floating actions / footer removal
- Removed the footer/status row from the main vertical layout so it no longer reserves a full-width strip below the charts.
- Moved status feedback into the header.
- Replaced the dock container with two independent About and Settings overlay buttons, positioned separately over the dashboard content.
- Removed the bottom layout margin so the chart area reaches the bottom edge of the window.


## Transaction dialog redesign (1.1.5)
- Rebuilt the New/Edit Transaction dialog to match the website layout: title with close control, labels above inputs, two-column amount/type and date/repeats rows, and full-width description/category/notes fields.
- Removed the always-visible recurrence end-date row; it appears only when a repeating frequency is selected.
- Changed the date display to MM/DD/YYYY and removed the currency prefix from the amount field to match the web form.
- Preserved custom categories, transaction editing, recurrence, end-date validation, and notes.
