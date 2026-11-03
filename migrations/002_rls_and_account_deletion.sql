-- FinanceTracker v1.0.0: security hardening + account deletion
-- Run once in the Supabase SQL Editor. Safe to re-run.

-- 1) Row Level Security: each user can only touch their own rows --------
alter table public.transactions enable row level security;

-- New rows are owned by the signed-in user by default.
alter table public.transactions
  alter column user_id set default auth.uid();

drop policy if exists "transactions_select_own" on public.transactions;
drop policy if exists "transactions_insert_own" on public.transactions;
drop policy if exists "transactions_update_own" on public.transactions;
drop policy if exists "transactions_delete_own" on public.transactions;

create policy "transactions_select_own" on public.transactions
  for select to authenticated
  using (user_id = (select auth.uid()));

create policy "transactions_insert_own" on public.transactions
  for insert to authenticated
  with check (user_id = (select auth.uid()));

create policy "transactions_update_own" on public.transactions
  for update to authenticated
  using (user_id = (select auth.uid()))
  with check (user_id = (select auth.uid()));

create policy "transactions_delete_own" on public.transactions
  for delete to authenticated
  using (user_id = (select auth.uid()));

-- IMPORTANT: policies are OR-ed together. If you created older policies
-- under other names, list them and drop any that are not "own rows only":
--   select policyname, cmd, qual, with_check
--   from pg_policies where tablename = 'transactions';
--   drop policy "<old policy name>" on public.transactions;

-- Anonymous (not signed-in) visitors get no access at all.
revoke all on public.transactions from anon;

-- 2) Let a signed-in user delete their own account and data ------------
create or replace function public.delete_my_account()
returns void
language plpgsql
security definer
set search_path = public, auth
as $$
begin
  if auth.uid() is null then
    raise exception 'not authenticated';
  end if;

  delete from public.transactions where user_id = auth.uid();
  delete from auth.users where id = auth.uid();
end;
$$;

revoke all on function public.delete_my_account() from public, anon;
grant execute on function public.delete_my_account() to authenticated;
