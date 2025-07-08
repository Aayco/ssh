import aiosqlite
import os
from pathlib import Path
from typing import Optional, List, Tuple, Any

class DatabaseManager:
    def __init__(self, db_path: str = "data/profiles.db"):
        self.db_path = Path(db_path)
        os.makedirs(self.db_path.parent, exist_ok=True)

    async def Init(self):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS profiles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE,
                    host TEXT,
                    user TEXT,
                    password TEXT,
                    ssh_key TEXT
                )
            """)
            await db.execute("""
                CREATE TABLE IF NOT EXISTS history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    profile_id INTEGER,
                    command TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(profile_id) REFERENCES profiles(id)
                )
            """)
            await db.commit()

    async def SaveProfile(self, name: str, host: str, user: str,
                          password: Optional[str] = None, ssh_key: Optional[str] = None):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                INSERT OR REPLACE INTO profiles (name, host, user, password, ssh_key)
                VALUES (?, ?, ?, ?, ?)
            """, (name, host, user, password, ssh_key))
            await db.commit()

    async def GetProfiles(self) -> List[Tuple[Any, ...]]:
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute("SELECT id, name, host, user FROM profiles") as cursor:
                return await cursor.fetchall()

    async def GetProfileByName(self, name: str) -> Optional[Tuple[Any, ...]]:
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute("SELECT * FROM profiles WHERE name = ?", (name,)) as cursor:
                return await cursor.fetchone()

    async def SaveHistory(self, profile_id: int, command: str):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                INSERT INTO history (profile_id, command)
                VALUES (?, ?)
            """, (profile_id, command))
            await db.commit()

    async def GetHistory(self, profile_id: int) -> List[Tuple[str, str]]:
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute("""
                SELECT command, timestamp FROM history
                WHERE profile_id = ? ORDER BY timestamp DESC
                LIMIT 50
            """, (profile_id,)) as cursor:
                return await cursor.fetchall()
