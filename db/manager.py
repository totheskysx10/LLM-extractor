from typing import Optional

import psycopg2

from config import Config


class DatabaseManager:
    def __init__(self, config: Config):
        self.dsn = config.db_dsn
        self.table_name = config.DB_TABLE
        self.doc_table_name = config.DB_TABLE_DOC
        self._ensure_table()

    def _connect(self):
        return psycopg2.connect(self.dsn)

    def _ensure_table(self) -> None:
        sql = f"""
        CREATE TABLE IF NOT EXISTS {self.table_name} (
            id SERIAL PRIMARY KEY,
            document_type TEXT NOT NULL,
            field_name TEXT NOT NULL,
            learned_context TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT NOW(),
            UNIQUE (document_type, field_name)
        );
            
        CREATE TABLE IF NOT EXISTS {self.doc_table_name} (
            id serial PRIMARY KEY,
            doc_name TEXT NOT NULL,
            embedding VECTOR(4096) NOT NULL
        );
        """
        with self._connect() as conn, conn.cursor() as cur:
            cur.execute(sql)
            conn.commit()

    def save_learned_context(self, document_type: str, field_name: str, learned_context: str) -> None:
        sql = f"""
        INSERT INTO {self.table_name} (document_type, field_name, learned_context)
        VALUES (%s, %s, %s)
        ON CONFLICT (document_type, field_name)
        DO UPDATE SET
            learned_context = EXCLUDED.learned_context,
            created_at = NOW();
        """
        with self._connect() as conn, conn.cursor() as cur:
            cur.execute(sql, (document_type, field_name, learned_context))
            conn.commit()

    def get_learned_context(self, document_type: str, field_name: str) -> Optional[str]:
        sql = f"""
        SELECT learned_context FROM {self.table_name}
        WHERE document_type = %s AND field_name = %s
        """
        with self._connect() as conn, conn.cursor() as cur:
            cur.execute(sql, (document_type, field_name))
            row = cur.fetchone()
            return row[0] if row else None

    def save_document(self, doc_name, embedding):
        sql = f"""
        INSERT INTO {self.doc_table_name} (doc_name, embedding)
        VALUES (%s, %s)
        """
        with self._connect() as conn, conn.cursor() as cur:
            cur.execute(sql, (doc_name, embedding))
            conn.commit()

    def get_relevant_document(self, query_embedding):
        sql = f"""
        SELECT doc_name
        FROM {self.doc_table_name}
        WHERE embedding <=> %s::vector < 0.45
        ORDER BY embedding <=> %s::vector
        LIMIT 1
        """
        with self._connect() as conn, conn.cursor() as cur:
            cur.execute(sql, (query_embedding,query_embedding))
            row = cur.fetchone()
            return row[0] if row else None