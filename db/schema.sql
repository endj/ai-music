PRAGMA foreign_keys = ON;  -- Ensure foreign key constraints are enforced

CREATE TABLE IF NOT EXISTS projects (
   id INTEGER PRIMARY KEY AUTOINCREMENT,
   project_id TEXT NOT NULL UNIQUE,
   url TEXT NOT NULL UNIQUE,
   voice TEXT NOT NULL,
   status TEXT NOT NULL,
   created_at INTEGER NOT NULL,
   updated_at INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS project_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id TEXT NOT NULL,
    status TEXT NOT NULL,
    info TEXT NOT NULL,
    created_at INTEGER NOT NULL,
    FOREIGN KEY (project_id) REFERENCES projects(project_id) ON DELETE CASCADE
);
