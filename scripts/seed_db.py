import sqlite3
import json
from pathlib import Path

# Use absolute paths so the script can be run from anywhere
DB_PATH = Path(__file__).parent.parent / "dnd5e.db"
JSON_PATH = Path(__file__).parent.parent / "data" / "items.json"

def seed_database():
    print("Seeding database...")
    conn = sqlite3.connect(DB_PATH)
    
    # 1. Create tables if they don't exist
    conn.execute('''
        CREATE TABLE IF NOT EXISTS items (
            name TEXT PRIMARY KEY,
            category TEXT NOT NULL,
            rarity TEXT NOT NULL,
            requires_attunement BOOLEAN,
            data TEXT NOT NULL
        )
    ''')
    
    # 2. Load JSON data
    with open(JSON_PATH, 'r') as f:
        items = json.load(f)

    # 3. Insert data using modern UPSERT (requires SQLite 3.24+)
    # This ensures if the item exists, we update it; if not, we insert it.
    with conn:
        for item in items:
            # Extract top-level SQL columns, leave the rest in JSON blob
            name = item.pop("name")
            category = item.pop("category", "Gear")
            rarity = item.pop("rarity", "Common")
            requires_attunement = item.pop("requires_attunement", False)
            
            conn.execute("""
                INSERT INTO items (name, category, rarity, requires_attunement, data)
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(name) DO UPDATE SET 
                    category=excluded.category,
                    rarity=excluded.rarity,
                    requires_attunement=excluded.requires_attunement,
                    data=excluded.data;
            """, (name, category, rarity, requires_attunement, json.dumps(item)))

    print(f"Successfully seeded {len(items)} items!")
    conn.close()

if __name__ == "__main__":
    seed_database()