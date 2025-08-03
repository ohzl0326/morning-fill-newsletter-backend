#!/usr/bin/env python3
"""
The Morning Fill Newsletter API
Meridius Labs - Newsletter Backend API for Zapier Integration
"""

from flask import Flask, request, jsonify
import sqlite3
import os
from pathlib import Path
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Database configuration
DATABASE_PATH = Path("database/database.db")


def get_db_connection():
    """Create and return a database connection."""
    # Ensure database directory exists
    DATABASE_PATH.parent.mkdir(exist_ok=True)
    
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row  # This enables column access by name
    return conn


def init_database():
    """Initialize the database with tables if they don't exist."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Read and execute schema
        schema_file = Path("database/schema.sql")
        if schema_file.exists():
            with open(schema_file, 'r') as file:
                schema_sql = file.read()
            cursor.executescript(schema_sql)
            conn.commit()
            print("✓ Database initialized successfully")
        else:
            print("⚠️ Schema file not found, creating basic tables")
            # Create basic tables if schema file is not available
            cursor.execute("""
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
                )
            """)
            conn.commit()
        
        conn.close()
    except Exception as e:
        print(f"❌ Database initialization error: {e}")


@app.route('/subscribe', methods=['POST'])
def subscribe():
    """
    API endpoint to handle new subscriber data from Zapier.
    Expected JSON payload:
    {
        "email": "user@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "company_name": "Company Inc",
        "job_title": "Manager",
        "consent_given": true
    }
    """
    try:
        # Get JSON data from request
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        # Validate required fields
        if not data.get('email'):
            return jsonify({"error": "Email is required"}), 400
        
        # Extract data with defaults
        email = data['email'].strip().lower()
        first_name = data.get('first_name', '').strip()
        last_name = data.get('last_name', '').strip()
        company_name = data.get('company_name', '').strip()
        job_title = data.get('job_title', '').strip()
        consent_given = 1 if data.get('consent_given', True) else 0
        
        # Connect to database
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if email already exists
        cursor.execute("SELECT id FROM subscribers WHERE email = ?", (email,))
        existing_subscriber = cursor.fetchone()
        
        if existing_subscriber:
            return jsonify({
                "error": "Email already subscribed",
                "subscriber_id": existing_subscriber['id']
            }), 409
        
        # Insert new subscriber
        cursor.execute("""
            INSERT INTO subscribers (email, first_name, last_name, company_name, job_title, consent_given)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (email, first_name, last_name, company_name, job_title, consent_given))
        
        subscriber_id = cursor.lastrowid
        
        # Commit and close
        conn.commit()
        conn.close()
        
        logger.info(f"New subscriber added: {email} (ID: {subscriber_id})")
        
        return jsonify({
            "success": True,
            "message": "Subscriber added successfully",
            "subscriber_id": subscriber_id,
            "email": email
        }), 201
        
    except sqlite3.IntegrityError as e:
        logger.error(f"Database integrity error: {e}")
        return jsonify({"error": "Database constraint violation"}), 400
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return jsonify({"error": "Internal server error"}), 500


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for monitoring."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM subscribers")
        subscriber_count = cursor.fetchone()[0]
        conn.close()
        
        return jsonify({
            "status": "healthy",
            "database": "connected",
            "subscriber_count": subscriber_count
        }), 200
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify({"status": "unhealthy", "error": str(e)}), 500


@app.route('/', methods=['GET'])
def root():
    """Root endpoint with API information."""
    return jsonify({
        "service": "The Morning Fill Newsletter API",
        "version": "1.0.0",
        "endpoints": {
            "POST /subscribe": "Add new subscriber",
            "GET /health": "Health check",
            "GET /": "API information"
        }
    }), 200


if __name__ == '__main__':
    # Initialize database
    init_database()
    
    # Get port from environment variable (Railway) or default to 5000
    port = int(os.environ.get('PORT', 5000))
    
    print("🚀 Starting The Morning Fill Newsletter API...")
    print(f"📊 Database: {DATABASE_PATH}")
    print(f"🌐 API will be available on port: {port}")
    print("📝 Subscribe endpoint: POST /subscribe")
    
    app.run(debug=False, host='0.0.0.0', port=port) 