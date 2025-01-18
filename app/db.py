from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class DatabaseConfig:
    def __init__(self):
        self.binds = {
            "users": "sqlite:///instance/users.db",
            "global_leaderboard": "sqlite:///instance/admin/leaderboard.db",
            "questions": "sqlite:///instance/competitions/demo/questions.db",
        }

    def get_binds(self):
        """Return the database binds dictionary."""
        return self.binds

    def set_questions_db(self, competition_name):
        """Dynamically set the questions database for a specific competition."""
        self.binds["questions"] = (
            "sqlite:///instance/competitions/{}/questions.db".format(competition_name)
        )
