#!python
from playhouse.migrate import BooleanField, SqliteDatabase, SqliteMigrator, migrate

my_db = SqliteDatabase("people.sqlite3")
migrator = SqliteMigrator(my_db)

# add send_feedback
migrate(
    migrator.add_column("users", "send_feedback", BooleanField(default=False)),
)
