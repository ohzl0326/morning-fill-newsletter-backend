-- The Morning Fill Newsletter Database Schema
-- SQLite-compatible schema for Meridius Labs newsletter application

-- Table 1: subscribers
-- Stores information about newsletter subscribers
CREATE TABLE IF NOT EXISTS subscribers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL UNIQUE,
    first_name TEXT,
    last_name TEXT,
    company_name TEXT,
    job_title TEXT,
    subscription_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    consent_given INTEGER NOT NULL DEFAULT 1 CHECK (consent_given IN (0, 1)),
    status TEXT NOT NULL DEFAULT 'active' CHECK (status IN ('active', 'unsubscribed', 'pending'))
);

-- Table 2: newsletter_content
-- Stores generated content for each section of newsletters
CREATE TABLE IF NOT EXISTS newsletter_content (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    generation_date DATE NOT NULL,
    edition TEXT NOT NULL,
    pipeline_step TEXT NOT NULL,
    content TEXT,
    reviewed_content TEXT,
    llm_model_used TEXT,
    prompt_key TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_subscribers_email ON subscribers(email);
CREATE INDEX IF NOT EXISTS idx_subscribers_status ON subscribers(status);
CREATE INDEX IF NOT EXISTS idx_newsletter_content_date ON newsletter_content(generation_date);
CREATE INDEX IF NOT EXISTS idx_newsletter_content_edition ON newsletter_content(edition);
CREATE INDEX IF NOT EXISTS idx_newsletter_content_pipeline ON newsletter_content(pipeline_step); 