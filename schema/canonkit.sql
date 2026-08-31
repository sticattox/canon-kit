-- canon-kit SQLite shape
-- Same rules as SPEC.md. CSV packs in examples/ are the human-editable form.

PRAGMA foreign_keys = ON;

CREATE TABLE sources (
  source_id TEXT PRIMARY KEY,
  captured_at TEXT NOT NULL,
  class TEXT NOT NULL CHECK (class IN (
    'DIRECT_REPORT', 'QUOTED', 'INTERPRETATION',
    'HYPOTHESIS', 'EVIDENCE', 'CORRECTION', 'DESIGN_PRINCIPLE'
  )),
  status TEXT NOT NULL DEFAULT 'DRAFT',
  raw_text TEXT NOT NULL,
  notes TEXT
);

CREATE TABLE concepts (
  concept_id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  definition TEXT NOT NULL,
  cluster TEXT,
  status TEXT NOT NULL DEFAULT 'DRAFT',
  confidence TEXT NOT NULL DEFAULT 'MEDIUM',
  source_ids TEXT NOT NULL,
  keywords TEXT,
  notes TEXT
);

CREATE TABLE rules (
  rule_id TEXT PRIMARY KEY,
  rule TEXT NOT NULL,
  class TEXT NOT NULL,
  priority TEXT NOT NULL,
  trigger TEXT NOT NULL,
  action TEXT NOT NULL,
  verification TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'DRAFT',
  source_ids TEXT NOT NULL,
  notes TEXT
);

CREATE TABLE system_map (
  domain TEXT PRIMARY KEY,
  purpose TEXT NOT NULL,
  canonical_home TEXT NOT NULL
);

CREATE TABLE file_index (
  entry_id TEXT PRIMARY KEY,
  purpose TEXT NOT NULL,
  owner_file TEXT NOT NULL,
  keywords TEXT
);

CREATE TABLE intake_log (
  log_id TEXT PRIMARY KEY,
  captured_at TEXT NOT NULL,
  source_id TEXT NOT NULL REFERENCES sources(source_id),
  routed_to TEXT NOT NULL,
  owner_id TEXT,
  write_status TEXT NOT NULL CHECK (write_status IN (
    'ATTEMPTED', 'COMPLETED', 'VERIFIED', 'FAILED'
  )),
  verified_at TEXT,
  summary TEXT
);

CREATE INDEX idx_intake_status ON intake_log(write_status);
CREATE INDEX idx_concepts_status ON concepts(status);
CREATE INDEX idx_rules_status ON rules(status);
