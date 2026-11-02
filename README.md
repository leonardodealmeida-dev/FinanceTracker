# FinanceTracker

A desktop personal finance application built with Python, PySide6, and Supabase.

FinanceTracker helps users organize their personal finances by managing transactions, tracking income and expenses, and automatically calculating their financial balance.

## Features

- **User Authentication** — Create an account and sign in securely.
- **Transaction Management** — Add, edit, and delete financial transactions.
- **Automatic Calculations** — Track income, expenses, and your overall balance.
- **Cloud Database** — Store transaction data using Supabase.
- **User Data Isolation** — Use Supabase Authentication and Row Level Security (RLS) to help protect users' financial records.
- **Desktop Interface** — A graphical interface built with PySide6.
- **Localization** — Interface text supports English and Brazilian Portuguese, based on the detected system locale.

## Built With

| Technology | Purpose |
|---|---|
| Python | Application logic |
| PySide6 | Desktop graphical interface |
| Supabase | Authentication and cloud database |
| PostgreSQL | Transaction data storage |
| python-dotenv | Environment variable configuration |

## Getting Started

### Prerequisites

- Python 3
- Git
- A Supabase project

### 1. Clone the repository

```bash
git clone https://github.com/usaleonardo-ai/FinanceTracker.git
cd FinanceTracker
```

### 2. Create a virtual environment

On Linux or macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

On Windows:

```powershell
py -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
python -m pip install PySide6 supabase python-dotenv
```

### 4. Configure Supabase

Create a Supabase project and configure the required database table and authentication settings.

Create a `.env` file in the project's root directory:

```env
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_publishable_key
```

Replace the placeholder values with your own Supabase project credentials.

**Important:** Never commit your `.env` file, service-role keys, or other secrets to GitHub. Use only a publishable key in the client application and configure appropriate Row Level Security policies in Supabase.

The `transactions` table must contain the fields expected by the application, including:

- `id`
- `user_id`
- `title`
- `amount`
- `type`
- `category`
- `transaction_date`
- `notes`
- `created_at`

Enable Row Level Security and configure policies so authenticated users can access only their own records.

### 5. Run the application

```bash
python main.py
```

On Linux systems where the virtual environment is not activated, use:

```bash
source .venv/bin/activate
python main.py
```

## Project Structure

```text
FinanceTracker/
├── app/
│   ├── services/
│   │   └── supabase_service.py
│   ├── ui/
│   │   ├── login_window.py
│   │   └── dashboard.py
│   └── i18n.py
├── .env                  # Local configuration; do not commit
├── .gitignore
├── main.py
└── README.md
```

## Security

FinanceTracker uses Supabase Authentication and Row Level Security to help isolate financial records by user.

For a secure deployment:

- Keep credentials out of source control.
- Never expose a Supabase service-role key in a desktop application.
- Apply and test database access policies.
- Do not use real sensitive financial information when testing an unreviewed deployment.

## Roadmap

Potential future improvements include:

- Financial charts and spending insights
- Monthly budgets and spending limits
- Custom transaction categories
- CSV export and reporting
- Improved packaging and application distribution

## Contributing

Contributions, bug reports, and feature suggestions are welcome.

Please open an issue to discuss substantial changes before submitting a pull request.

## Author

**Leonardo de Almeida**

GitHub: [@usaleonardo-ai](https://github.com/usaleonardo-ai)

---

Built as a personal software development project.
