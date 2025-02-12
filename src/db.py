import logging
import sqlite3
import sys
import time
from contextlib import contextmanager
from dataclasses import dataclass
from typing import List
from args import ProcessJob

log = logging.getLogger(__name__)


@dataclass
class DBJob:
    project_id: str
    url: str
    models: str
    status: str
    created_at: int
    updated_at: int


def unix_millis():
    return round(time.time() * 1000)


@contextmanager
def db_connection():
    """Context manager for handling SQLite connection and cursor."""
    conn = sqlite3.connect("./../db/music.db")
    try:
        yield conn.cursor()
    finally:
        conn.commit()
        conn.close()


def migrate_db():
    try:
        with open("./../db/schema.sql") as schema:
            schema_sql = schema.read()

        with db_connection() as cursor:
            cursor.executescript(schema_sql)
            log.debug("Finished database migration")

    except Exception as e:
        log.error(f"Error during database migration: {e}")
        sys.exit(1)


def insert_job(job: ProcessJob):
    project_id = job.project_id
    url = job.url
    models = ",".join(job.models)
    status = "CREATED"
    created_at = unix_millis()
    updated_at = 0

    log.info(
        f"Inserting job (project_id: {project_id}, url: {url}, models: {models}, status: {status}, created_at: {created_at}, updated_at: {updated_at})")

    try:
        with db_connection() as cursor:
            cursor.execute("""
                INSERT INTO projects (project_id, url, models, status, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (project_id, url, models, status, created_at, updated_at))

    except sqlite3.IntegrityError as e:
        log.error(f"Failed to insert job {job} error: {e}")
        sys.exit(1)
    except sqlite3.DatabaseError as e:
        log.error(f"Database error: {e}")
        sys.exit(1)
    except Exception as e:
        log.error(f"Unexpected error: {e}")
        sys.exit(1)

def save_error(project_id: str, error: Exception):
    timestamp = unix_millis()
    with db_connection() as cursor:
        cursor.execute("""
           INSERT INTO project_events (project_id, status, info, created_at)
           VALUES (?, ?, ?, ?)
        """, (project_id, "FAILED", str(error), timestamp))
        cursor.execute("""
            UPDATE projects
            SET status = ?, updated_at = ?
            WHERE project_id = ?
        """, ("FAILED", timestamp, project_id))

def update_status(project_id: str, msg: str, status: str):
    timestamp = unix_millis()
    with db_connection() as cursor:
        cursor.execute("""
           INSERT INTO project_events (project_id, status, info, created_at)
           VALUES (?, ?, ?, ?)
        """, (project_id, status, msg, timestamp))
        cursor.execute("""
            UPDATE projects
            SET status = ?, updated_at = ?
            WHERE project_id = ?
        """, (status, timestamp, project_id))

def list_jobs() -> List[DBJob]:
    """Retrieve all jobs from the database and return them as a list of Job dataclass instances."""
    try:
        with db_connection() as cursor:
            cursor.execute("SELECT project_id, url, models, status, created_at, updated_at FROM projects")
            rows = cursor.fetchall()

            # Convert rows into a list of Job dataclass instances
            jobs = [DBJob(project_id=row[0], url=row[1], models=row[2], status=row[3],
                        created_at=row[4], updated_at=row[5]) for row in rows]

        return jobs

    except sqlite3.DatabaseError as e:
        log.error(f"Error retrieving jobs from the database: {e}")
        return []
