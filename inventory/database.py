import sqlite3


def create_connection(database_path):
    connection = sqlite3.connect(database_path)
    return connection


def create_tables(database_path):
    connection = create_connection(database_path)

    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS programs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            version TEXT,
            publisher TEXT,
            install_date TEXT,
            install_location TEXT,
            uninstall_string TEXT
        )
        """
    )

    connection.commit()
    connection.close()


def add_program(
    database_path,
    name,
    version,
    publisher,
    install_date,
    install_location,
    uninstall_string,
):
    connection = create_connection(database_path)

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO programs
        (
            name,
            version,
            publisher,
            install_date,
            install_location,
            uninstall_string
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            name,
            version,
            publisher,
            install_date,
            install_location,
            uninstall_string,
        ),
    )

    connection.commit()
    connection.close()


def save_programs(programs, database_path):
    for program in programs:
        add_program(
            database_path,
            program["name"],
            program["version"],
            program["publisher"],
            program["install_date"],
            program["install_location"],
            program["uninstall_string"],
        )


def get_programs(database_path):
    connection = create_connection(database_path)

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT * FROM programs
        """
    )

    programs = cursor.fetchall()

    connection.close()

    return programs