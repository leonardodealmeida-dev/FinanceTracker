-- FinanceTracker: per-user custom income and expense categories
create table if not exists public.custom_categories (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users(id) on delete cascade,
  name text not null check (char_length(trim(name)) between 1 and 32),
  type text not null check (type in ('income', 'expense')),
  created_at timestamptz not null default now()
);

-- Names are unique per account and transaction type, ignoring letter case.
create unique index if not exists custom_categories_user_type_name_ci
  on public.custom_categories (user_id, type, lower(name));

alter table public.custom_categories enable row level security;

drop policy if exists "Users can read their own custom categories" on public.custom_categories;
create policy "Users can read their own custom categories"
  on public.custom_categories for select
  using (auth.uid() = user_id);

drop policy if exists "Users can create their own custom categories" on public.custom_categories;
create policy "Users can create their own custom categories"
  on public.custom_categories for insert
  with check (auth.uid() = user_id);

drop policy if exists "Users can update their own custom categories" on public.custom_categories;
create policy "Users can update their own custom categories"
  on public.custom_categories for update
  using (auth.uid() = user_id)
  with check (auth.uid() = user_id);

drop policy if exists "Users can delete their own custom categories" on public.custom_categories;
create policy "Users can delete their own custom categories"
  on public.custom_categories for delete
  using (auth.uid() = user_id);

grant select, insert, update, delete on public.custom_categories to authenticated;
