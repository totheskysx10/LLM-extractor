from typing import Optional

import psycopg2

from config import Config


class DatabaseManager:
    def __init__(self, config: Config):
        self.dsn = config.db_dsn
        self.table_name = config.DB_TABLE
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

    def delete_by_id(self, record_id: int) -> bool:
        sql = f"DELETE FROM {self.table_name} WHERE id = %s;"
        with self._connect() as conn, conn.cursor() as cur:
            cur.execute(sql, (record_id,))
            deleted = cur.rowcount > 0
            conn.commit()
            return deleted