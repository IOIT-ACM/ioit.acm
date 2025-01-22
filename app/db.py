from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()


class DatabaseConfig:
    def __init__(self):
        self.binds = {
            "users": self.get_mysql_uri("users"),
            "global_leaderboard": self.get_mysql_uri("global_leaderboard"),
            "virtual_contest_bitbyquery_jan2025": self.get_mysql_uri(
                "virtual_contest_bitbyquery_jan2025"
            ),
        }

    def get_mysql_uri(self, db_name):
        """Construct the MySQL URI."""
        db_host = os.getenv("DB_HOST", "localhost")
        db_user = os.getenv("DB_USER", "root")
        db_password = os.getenv("DB_PASSWORD", "")
        db_name = os.getenv("DB_NAME", db_name)
        return "mysql+pymysql://{}:{}@{}/{}".format(
            db_user, db_password, db_host, db_name
        )

    def get_binds(self):
        """Return the database binds dictionary."""
        return self.binds
