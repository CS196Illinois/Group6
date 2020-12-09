CREATE TABLE user (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  email TEXT UNIQUE NOT NULL,
  profile_pic TEXT NOT NULL,
  transcripts TEXT NOT NULL,
  summaries TEXT NOT NULL
);