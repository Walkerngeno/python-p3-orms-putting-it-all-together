import sqlite3

# Create a SQLite database connection and cursor
CONN = sqlite3.connect('your_database_name.db')
CURSOR = CONN.cursor()

class Dog:
    def __init__(self, name, breed):
        self.name = name
        self.breed = breed
        self.id = None  # Initialize id as None for new instances

    @classmethod
    def create_table(cls):
        CREATE_TABLE_SQL = """
        CREATE TABLE IF NOT EXISTS dogs (
            id INTEGER PRIMARY KEY,
            name TEXT,
            breed TEXT
        )
        """
        CURSOR.execute(CREATE_TABLE_SQL)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        DROP_TABLE_SQL = "DROP TABLE IF EXISTS dogs"
        CURSOR.execute(DROP_TABLE_SQL)
        CONN.commit()

    def save(self):
        INSERT_DOG_SQL = "INSERT INTO dogs (name, breed) VALUES (?, ?)"
        CURSOR.execute(INSERT_DOG_SQL, (self.name, self.breed))
        CONN.commit()

    @classmethod
    def create(cls, name, breed):
        dog = cls(name, breed)
        dog.save()

        SELECT_LAST_ID_SQL = "SELECT last_insert_rowid()"
        CURSOR.execute(SELECT_LAST_ID_SQL)
        last_id = CURSOR.fetchone()[0]
        dog.id = last_id

        return dog

    @classmethod
    def new_from_db(cls, row):
        id, name, breed = row
        dog = cls(name, breed)
        dog.id = id
        return dog

    @classmethod
    def get_all(cls):
        SELECT_ALL_SQL = "SELECT * FROM dogs"
        CURSOR.execute(SELECT_ALL_SQL)
        rows = CURSOR.fetchall()
        return [cls.new_from_db(row) for row in rows]

    @classmethod
    def find_by_name(cls, name):
        SELECT_BY_NAME_SQL = "SELECT * FROM dogs WHERE name = ?"
        CURSOR.execute(SELECT_BY_NAME_SQL, (name,))
        row = CURSOR.fetchone()
        if row:
            return cls.new_from_db(row)
        else:
            return None

    @classmethod
    def find_by_id(cls, id):
        SELECT_BY_ID_SQL = "SELECT * FROM dogs WHERE id = ?"
        CURSOR.execute(SELECT_BY_ID_SQL, (id,))
        row = CURSOR.fetchone()
        if row:
            return cls.new_from_db(row)
        else:
            return None

    def update(self):
        UPDATE_DOG_SQL = "UPDATE dogs SET name = ?, breed = ? WHERE id = ?"
        CURSOR.execute(UPDATE_DOG_SQL, (self.name, self.breed, self.id))
        CONN.commit()
