import os
import sys
import logging
import psycopg2
from flask import Flask, jsonify

from dotenv import load_dotenv

load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

def run_migrations(sql_dir: str, db_url: str):
    """
    Load all .sql files from `sql_dir` (in alphanumeric order)
    and execute them against the database specified by `db_url`.
    """
    # Gather and sort SQL files
    sql_files = sorted(
        f for f in os.listdir(sql_dir)
        if f.lower().endswith('.sql')
    )
    if not sql_files:
        logging.warning("No .sql files found in %s", sql_dir)
        return

    # Connect to the database
    try:
        conn = psycopg2.connect(db_url)
        cursor = conn.cursor()
        logging.info("Connected to database")
    except Exception as e:
        logging.error("Failed to connect to database: %s", e)
        sys.exit(1)

    # Apply each migration
    for fname in sql_files:
        path = os.path.join(sql_dir, fname)
        logging.info("Applying migration %s", fname)
        try:
            with open(path, 'r', encoding='utf-8') as f:
                sql = f.read()
            cursor.execute(sql)
            conn.commit()
            logging.info("Successfully applied %s", fname)
        except Exception as e:
            conn.rollback()
            logging.error("Error applying %s: %s", fname, e)
            cursor.close()
            conn.close()
            sys.exit(1)

    cursor.close()
    conn.close()
    logging.info("All migrations applied successfully")

def run_env_sql(db_url: str):
    """
    If the API_KEY env var is set, insert it into a table.
    Adjust the INSERT statement/table as needed.
    """
    api_key = os.getenv('API_KEY')
    project_id = os.getenv('PROJECT_ID')

    insert_sql = """
    INSERT INTO api_keys (name, api_key, search_engine_id, daily_queries)
    VALUES (%s, %s, %s, 100)
    ON CONFLICT (api_key) DO NOTHING;
    """

    try:
        conn = psycopg2.connect(db_url)
        cursor = conn.cursor()
        logging.info("Inserting API_KEY into database")
        cursor.execute(
            insert_sql,
            (api_key, api_key, project_id)
        )
        conn.commit()
        cursor.close()
        conn.close()
        logging.info("API_KEY insertion complete")
    except Exception as e:
        logging.error("Failed to insert API_KEY: %s", e)
        sys.exit(1)

def create_app() -> Flask:
    """
    Create a Flask app which provides a /health endpoint
    that verifies the database connection.
    """
    app = Flask(__name__)

    @app.route('/health', methods=['GET'])
    def healthcheck():
        try:
            return jsonify(status='healthy'), 200
        except Exception as e:
            logging.error("Healthcheck failed: %s", e)
            return jsonify(status='unhealthy', error=str(e)), 500

    return app


def main():
    # Step 1: Run migrations
    run_migrations(os.getenv("SQL_DIR", "."), os.getenv("DB_URL", "postgresql://user:pass@localhost:5432/mydb"))

    # Step2: Run env SQL
    run_env_sql(os.getenv("DB_URL", "postgresql://user:pass@localhost:5432/mydb"))

    # Step 3: Start healthcheck server
    app = create_app()
    logging.info("Starting healthcheck server on 0.0.0.0:8080")
    app.run(host="0.0.0.0", port=8080)


if __name__ == '__main__':
    main()