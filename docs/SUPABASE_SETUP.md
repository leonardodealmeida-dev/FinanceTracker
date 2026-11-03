# Supabase setup for maintainers (v1.0.0)

Official builds connect to **your** Supabase project, so users don't need
any setup. Do these steps once, before publishing a release.

## 1. Run the SQL migrations (SQL Editor, in order)

1. `migrations/001_add_recurrence.sql` — recurring transactions
2. `migrations/002_rls_and_account_deletion.sql` — Row Level Security
   policies and the `delete_my_account()` function

After running 002, check for old, looser policies (policies are OR-ed):

```sql
select policyname, cmd, qual, with_check
from pg_policies where tablename = 'transactions';
```

Only the four `transactions_*_own` policies should remain.

## 2. Test Row Level Security with two accounts

The publishable key ships inside every download, so RLS is the only
thing protecting user data.

1. Create two test accounts (A and B) and add a transaction to each.
2. Signed in as A, confirm B's transaction is not visible, can't be
   edited and can't be deleted.
3. Confirm "Delete account" removes A's account and rows but not B's.

## 3. Password reset code (email template)

The app resets passwords in-app with a one-time code. In
**Authentication → Email Templates → Reset Password**, make sure the
body shows the code, for example:

```html
<h2>Reset your password</h2>
<p>Your FinanceTracker code is: <strong>{{ .Token }}</strong></p>
```

## 4. Email delivery (important before launch)

Supabase's built-in email sender is heavily rate-limited and meant for
testing. Configure a custom SMTP provider under
**Authentication → SMTP Settings**, or signups and resets will fail once
real users arrive. Consider enabling CAPTCHA / rate limits under
**Authentication → Attack Protection**.

## 5. GitHub secrets for the release build

In the repo: **Settings → Secrets and variables → Actions → New
repository secret**

| Secret | Value |
|---|---|
| `SUPABASE_URL` | your project URL |
| `SUPABASE_KEY` | the **publishable** key (never `service_role` / `sb_secret_...`) |

The build refuses to bundle a secret key.

## 6. Publishing a release

1. Bump `__version__` in `app/version.py`, commit and push.
2. Tag and push: `git tag v1.0.0 && git push origin v1.0.0`
3. GitHub Actions builds Windows, macOS and Linux downloads and attaches
   them to a **draft** release. Download and test them on clean machines,
   edit the notes, then click **Publish**.

## Your responsibilities as the operator

Users' financial data is stored in your project. Publish a privacy
policy, keep backups, and respond to data requests (LGPD/GDPR). The
in-app "Delete account" button covers deletion requests.
