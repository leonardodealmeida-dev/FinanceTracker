-- FinanceTracker: recurring transactions
-- Run once in the Supabase dashboard: SQL Editor -> New query -> paste -> Run.
-- Existing transactions are kept and become one-time ('once') transactions.

alter table public.transactions
  add column if not exists frequency text not null default 'once'
    check (frequency in ('once', 'daily', 'weekly', 'monthly', 'yearly')),
  add column if not exists end_date date;

-- Your existing Row Level Security policies keep working unchanged:
-- the new columns belong to the same rows, so each user still only
-- sees their own transactions.
