-- Run ONCE as the database owner. Creates a read-only role for the research desk.
-- Replace the password before running; store the resulting URL as RESEARCH_DB_URL.

CREATE ROLE research_ro LOGIN PASSWORD 'CHANGE_ME_LONG_RANDOM';
ALTER ROLE research_ro SET default_transaction_read_only = on;
ALTER ROLE research_ro SET statement_timeout = '120s';

GRANT CONNECT ON DATABASE volatilx TO research_ro;   -- adjust db name
GRANT USAGE ON SCHEMA public TO research_ro;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO research_ro;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO research_ro;

-- Explicitly deny anything else, in case a future GRANT is too broad.
REVOKE CREATE ON SCHEMA public FROM research_ro;
REVOKE ALL ON ALL SEQUENCES IN SCHEMA public FROM research_ro;

-- Optional: hide PII tables from the desk entirely.
REVOKE SELECT ON users, user_subscriptions, subscription_usage FROM research_ro;

-- Verify (should error with "cannot execute UPDATE in a read-only transaction"):
--   psql "postgresql://research_ro:...@host/volatilx" -c "UPDATE super_agent_select_runs SET id=id WHERE 1=0"
