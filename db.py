"""Database management for ContentForge - AI Content Generator"""

import sqlite3
import os
from datetime import datetime
from typing import List, Dict, Any, Tuple


class Database:
    """SQLite database manager for storing generation history and templates"""

    def __init__(self, db_path: str = "content_studio.db"):
        self.db_path = db_path
        self.init_db()

    def get_connection(self) -> sqlite3.Connection:
        """Get database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def init_db(self):
        """Initialize database tables"""
        conn = self.get_connection()
        cursor = conn.cursor()

        # History table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                content_type TEXT NOT NULL,
                topic TEXT NOT NULL,
                audience TEXT,
                tone TEXT,
                style TEXT,
                model TEXT NOT NULL,
                generated_text TEXT NOT NULL,
                word_count INTEGER,
                character_count INTEGER
            )
        """
        )

        # Templates table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS templates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                content_type TEXT NOT NULL,
                description TEXT,
                template_text TEXT NOT NULL,
                created_date TEXT NOT NULL
            )
        """
        )

        # Favorites table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS favorites (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                history_id INTEGER NOT NULL,
                content TEXT NOT NULL,
                created_date TEXT NOT NULL,
                FOREIGN KEY (history_id) REFERENCES history(id)
            )
        """
        )

        conn.commit()
        conn.close()

    def add_history(
        self,
        content_type: str,
        topic: str,
        audience: str,
        tone: str,
        style: str,
        model: str,
        generated_text: str,
    ) -> int:
        """Add entry to history"""
        conn = self.get_connection()
        cursor = conn.cursor()

        word_count = len(generated_text.split())
        character_count = len(generated_text)
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute(
            """
            INSERT INTO history 
            (date, content_type, topic, audience, tone, style, model, generated_text, word_count, character_count)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                date,
                content_type,
                topic,
                audience,
                tone,
                style,
                model,
                generated_text,
                word_count,
                character_count,
            ),
        )

        conn.commit()
        history_id = cursor.lastrowid
        conn.close()

        return history_id

    def get_history(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get generation history"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT * FROM history ORDER BY date DESC LIMIT ?
        """,
            (limit,),
        )

        rows = cursor.fetchall()
        conn.close()

        return [dict(row) for row in rows]

    def search_history(
        self, content_type: str = None, topic: str = None
    ) -> List[Dict[str, Any]]:
        """Search history by content type or topic"""
        conn = self.get_connection()
        cursor = conn.cursor()

        query = "SELECT * FROM history WHERE 1=1"
        params = []

        if content_type:
            query += " AND content_type = ?"
            params.append(content_type)

        if topic:
            query += " AND topic LIKE ?"
            params.append(f"%{topic}%")

        query += " ORDER BY date DESC"

        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()

        return [dict(row) for row in rows]

    def delete_history_entry(self, entry_id: int):
        """Delete a history entry"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM history WHERE id = ?", (entry_id,))
        conn.commit()
        conn.close()

    def clear_history(self):
        """Clear all history"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM history")
        conn.commit()
        conn.close()

    def get_history_stats(self) -> Dict[str, Any]:
        """Get statistics from history"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM history")
        total_generated = cursor.fetchone()[0]

        cursor.execute("SELECT SUM(word_count) FROM history")
        total_words = cursor.fetchone()[0] or 0

        cursor.execute(
            "SELECT content_type, COUNT(*) as count FROM history GROUP BY content_type"
        )
        content_stats = cursor.fetchall()

        conn.close()

        return {
            "total_generated": total_generated,
            "total_words": total_words,
            "content_stats": [
                {"content_type": row[0], "count": row[1]} for row in content_stats
            ],
        }

    # Template methods
    def add_template(
        self, name: str, content_type: str, description: str, template_text: str
    ) -> bool:
        """Add a new template"""
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            created_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute(
                """
                INSERT INTO templates (name, content_type, description, template_text, created_date)
                VALUES (?, ?, ?, ?, ?)
            """,
                (name, content_type, description, template_text, created_date),
            )
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            conn.close()
            return False

    def get_templates(self) -> List[Dict[str, Any]]:
        """Get all templates"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM templates ORDER BY created_date DESC")

        rows = cursor.fetchall()
        conn.close()

        return [dict(row) for row in rows]

    def get_template_by_type(self, content_type: str) -> List[Dict[str, Any]]:
        """Get templates by content type"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM templates WHERE content_type = ? ORDER BY created_date DESC",
            (content_type,),
        )

        rows = cursor.fetchall()
        conn.close()

        return [dict(row) for row in rows]

    def delete_template(self, template_id: int) -> bool:
        """Delete a template"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM templates WHERE id = ?", (template_id,))
        conn.commit()
        conn.close()

        return cursor.rowcount > 0

    # Favorites methods
    def add_favorite(self, history_id: int, content: str) -> int:
        """Add to favorites"""
        conn = self.get_connection()
        cursor = conn.cursor()

        created_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute(
            """
            INSERT INTO favorites (history_id, content, created_date)
            VALUES (?, ?, ?)
        """,
            (history_id, content, created_date),
        )

        conn.commit()
        fav_id = cursor.lastrowid
        conn.close()

        return fav_id

    def get_favorites(self) -> List[Dict[str, Any]]:
        """Get all favorites"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM favorites ORDER BY created_date DESC")

        rows = cursor.fetchall()
        conn.close()

        return [dict(row) for row in rows]

    def delete_favorite(self, fav_id: int) -> bool:
        """Delete a favorite"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM favorites WHERE id = ?", (fav_id,))
        conn.commit()
        conn.close()

        return cursor.rowcount > 0
