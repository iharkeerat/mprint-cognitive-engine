import sqlite3
import random

def seed_database():
    conn = sqlite3.connect("alis.db")
    cursor = conn.cursor()

    topics = ["Machine Learning", "System Design", "React", "Cyber Security", "Data Structures"]
    levels = ["Beginner", "Intermediate", "Advanced"]
    styles = ["Activist", "Reflector", "Theorist", "Pragmatist"]

    print("🌱 Seeding database with realistic user data...")

    for i in range(1, 26): # Create 25 fake sessions
        session_id = 1000 + i
        topic = random.choice(topics)
        level = random.choice(levels)
        
        # Insert Session
        cursor.execute(
            "INSERT INTO sessions (session_id, topic, target_level) VALUES (?, ?, ?)",
            (session_id, topic, level)
        )

        # Insert 3-4 fake responses for this session to simulate time tracking
        dominant_style = random.choice(styles)
        for _ in range(random.randint(3, 4)):
            # Random time between 2.5 and 12.0 seconds
            fake_time = round(random.uniform(2.5, 12.0), 2)
            cursor.execute(
                "INSERT INTO responses (session_id, style, type, time) VALUES (?, ?, ?, ?)",
                (session_id, dominant_style, "mcq", fake_time)
            )

    conn.commit()
    conn.close()
    print("✅ Database successfully seeded! Open your dashboard to see the analytics.")

if __name__ == "__main__":
    seed_database()