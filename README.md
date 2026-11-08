# FinanceTracker

A desktop personal finance app for tracking income and expenses, with recurring transactions and charts.

**Plug and play:** download, extract, open `FinanceTracker`. No Python, no terminal, no database or account setup.

## Download

Get the latest version from the
[Releases page](https://github.com/usaleonardo-ai/FinanceTracker/releases/latest).

| System | Download |
|---|---|
| Windows | `FinanceTracker-<version>-windows.zip` |
| macOS (Apple Silicon) | `FinanceTracker-<version>-macos-arm64.zip` |
| Linux (x86_64) | `FinanceTracker-<version>-linux-x86_64.tar.gz` |

### How to open it

1. **Download** the file for your system.
2. **Extract** it (right-click → *Extract All* on Windows, double-click on macOS, `tar -xzf` on Linux). Extract it fully before running; don't run it from inside the zip.
3. **Open `FinanceTracker`** (`FinanceTracker.exe` on Windows, `FinanceTracker.app` on macOS).
4. **Create an account** on the login screen and start tracking.

That's it. The app connects to its cloud service automatically.

Prefer an installer? Windows (`...-windows-setup.exe`) and macOS (`...-macos-arm64.dmg`) installers are also on the Releases page.

### If your system shows a warning

The app is not code-signed yet, so Windows and macOS may warn you the first time you open it.

- **Windows:** click **More info**, then **Run anyway**.
- **macOS:** right-click `FinanceTracker.app`, choose **Open**, then confirm.
- **Linux:** if it doesn't start, run `sudo apt install libxcb-cursor0`.

Intel Macs are not supported yet.

## Features

- **Guided start**: a short tutorial appears the first time you sign in, and you can reopen it any time with the **Help** button.
- **Accounts**: sign up and sign in with email and password. Forgot your password? Reset it in the app with a code sent to your email.
- **Transactions**: add, edit, delete and search income and expenses, with categories and notes.
- **Recurring transactions**: enter a salary, rent, gas or groceries once and mark it as daily, weekly, monthly or yearly, with an optional end date. Every occurrence is counted automatically.
- **Charts**: income vs. expenses for the last 6 months, spending by category, and your balance over time. Filter by this month, last 3 or 6 months, this year, or all time.
- **Automatic totals**: income, expenses and net balance for the selected period.
- **Private by design**: each user can only access their own data.
- **Delete your data**: permanently delete your account and all your transactions from inside the app.
- **Languages**: English and Brazilian Portuguese, chosen from your system language.

## Privacy

Your transactions are stored in the FinanceTracker cloud database. Each account can only read and change its own records, and you can delete your account and all of its data at any time from the dashboard (**Delete account**).

Don't store information you aren't comfortable keeping in a cloud service.

## Built With

Python, PySide6 (Qt), Supabase (authentication and PostgreSQL), PyInstaller and GitHub Actions.

## Roadmap

- Code signing for Windows and macOS
- Intel Mac and AppImage builds
- Monthly budgets and spending limits
- Custom transaction categories
- CSV export and reporting

## Contributing

Contributions, bug reports and feature suggestions are welcome. Please open an issue to discuss substantial changes before submitting a pull request.

## Author

**Leonardo de Almeida**

GitHub: [@usaleonardo-ai](https://github.com/usaleonardo-ai)

---

<details>
<summary><strong>For developers</strong> (running from source and publishing releases)</summary>

<br>

Regular users don't need any of this.

### Run from source

You need Python 3.10+. Official builds have the backend built in, but the keys are not part of this repository, so running from source needs a Supabase project of your own.

```bash
git clone https://github.com/usaleonardo-ai/FinanceTracker.git
cd FinanceTracker
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
python -m pip install -r requirements.txt
```

Create a `.env` file in the project root (never commit it):

```env
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_publishable_key
```

Run the SQL in `migrations/` in order (001, then 002) in the Supabase SQL Editor, then:

```bash
python main.py
```

See [`docs/SUPABASE_SETUP.md`](docs/SUPABASE_SETUP.md) for the full maintainer guide (Row Level Security, password-reset email template, SMTP, release secrets).

### Build the Linux app locally

With a `.env` in place, one command builds the standalone app (needs internet):

```bash
./build_linux.sh
```

The result is in `dist/FinanceTracker/` (run the `FinanceTracker` file) and as a `.tar.gz` ready to share. Windows and macOS builds come from the GitHub release workflow.

### Tests

```bash
python -m pytest tests
```

### Publish a release

1. Add the repository secrets `SUPABASE_URL` and `SUPABASE_KEY` (publishable key only).
2. Bump `__version__` in `app/version.py`, commit and push.
3. `git tag vX.Y.Z && git push origin vX.Y.Z`
4. GitHub Actions builds the downloads and attaches them to a **draft** release. Test them, edit the notes, then publish.

### Project structure

```text
FinanceTracker/
├── app/                  # application code (ui/, services/, analytics, recurrence, config, i18n)
├── assets/               # app icon
├── docs/                 # maintainer guide
├── migrations/           # SQL for Supabase
├── packaging/            # PyInstaller spec, Windows installer
├── tests/
├── tools/                # icon generator, build config writer
├── .github/workflows/    # release builds
├── CHANGELOG.md
└── main.py
```

</details>
