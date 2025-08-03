#!/usr/bin/env python3
"""
Database Initialization Script for The Morning Fill Newsletter
Meridius Labs - Newsletter Backend
"""

import sqlite3
import os
from pathlib import Path


def create_database():
    """
    Initialize the SQLite database by creating the database file and tables
    based on the schema.sql file.
    """
    # Define paths
    database_dir = Path("database")
    database_file = database_dir / "database.db"
    schema_file = database_dir / "schema.sql"
    
    # Create database directory if it doesn't exist
    database_dir.mkdir(exist_ok=True)
    print(f"✓ Database directory created/verified: {database_dir}")
    
    # Connect to SQLite database (creates the file if it doesn't exist)
    try:
        conn = sqlite3.connect(database_file)
        cursor = conn.cursor()
        print(f"✓ Connected to database: {database_file}")
        
        # Read and execute the schema file
        if schema_file.exists():
            with open(schema_file, 'r') as file:
                schema_sql = file.read()
            
            # Execute the schema SQL
            cursor.executescript(schema_sql)
            print("✓ Schema executed successfully")
            
            # Verify tables were created
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            print(f"✓ Tables created: {[table[0] for table in tables]}")
            
            # Commit changes and close connection
            conn.commit()
            conn.close()
            print("✓ Database initialization completed successfully!")
            
        else:
            print(f"❌ Schema file not found: {schema_file}")
            return False
            
    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False
    
    return True


if __name__ == "__main__":
    print("🚀 Initializing The Morning Fill Newsletter Database...")
    print("=" * 50)
    
    success = create_database()
    
    if success:
        print("\n🎉 Database setup completed successfully!")
        print("You can now start using your newsletter application.")
    else:
        print("\n❌ Database setup failed. Please check the error messages above.") 