-- Used only against an in-memory SQLite fixture; no production database.
CREATE TABLE unsafe_membership (tenant TEXT NOT NULL, email TEXT NOT NULL);
CREATE TABLE safe_membership (
    tenant TEXT NOT NULL,
    email TEXT NOT NULL,
    UNIQUE (tenant, email)
);
-- App pre-checks can race: two readers observe zero, then both INSERT.
CREATE TABLE nullable_membership (
    tenant TEXT NOT NULL,
    email TEXT,
    UNIQUE (tenant, email)
);
-- The constraint exists, yet two NULL emails are not equal, so duplicates pass.
