import sqlite3
import os


DATABASE_PATH = "database/food.db"


def get_connection():

    os.makedirs(
        "database",
        exist_ok=True
    )

    return sqlite3.connect(
        DATABASE_PATH
    )


def initialize_database():

    connection = get_connection()

    cursor = connection.cursor()


    cursor.execute("""

        CREATE TABLE IF NOT EXISTS history (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            food TEXT NOT NULL,

            mood TEXT,

            situation TEXT,

            activity TEXT,

            budget REAL,

            rating INTEGER,

            created_at TIMESTAMP
                DEFAULT CURRENT_TIMESTAMP

        )

    """)


    connection.commit()

    connection.close()


def save_history(

    food,
    mood,
    situation,
    activity,
    budget,
    rating

):

    connection = get_connection()

    cursor = connection.cursor()


    cursor.execute("""

        INSERT INTO history

        (
            food,
            mood,
            situation,
            activity,
            budget,
            rating
        )

        VALUES (?, ?, ?, ?, ?, ?)

    """, (

        food,
        mood,
        situation,
        activity,
        budget,
        rating

    ))


    connection.commit()

    connection.close()


def get_history():

    connection = get_connection()

    cursor = connection.cursor()


    cursor.execute("""

        SELECT
            id,
            food,
            mood,
            situation,
            activity,
            budget,
            rating,
            created_at

        FROM history

        ORDER BY created_at DESC

    """)


    results = cursor.fetchall()

    connection.close()


    return results