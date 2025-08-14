from flask import Flask, render_template
from flask_login import LoginManager, current_user
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from app.db import DatabaseConfig, db
from app.models import User
from sqlalchemy.exc import ProgrammingError, SQLAlchemyError, OperationalError
from dotenv import load_dotenv

load_dotenv()

database_config = DatabaseConfig()
login_manager = LoginManager()

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per hour"],
    storage_uri="memory://",
)


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "nqMt+o1BxO2Wkaj4ogmFtg=="
    app.config["SQLALCHEMY_BINDS"] = database_config.get_binds()
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SESSION_COOKIE_HTTPONLY"] = True
    app.config["SESSION_COOKIE_SECURE"] = True
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

    db.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = "auth.signin"

    limiter.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @app.context_processor
    def inject_user():
        return {"current_user": current_user}

    with app.app_context():
        db.create_all(bind=None)

    # Register blueprints
    from app.blueprints.home import home_bp
    from app.blueprints.team import team_bp
    from app.blueprints.membership import membership_bp
    from app.blueprints.join import join_bp
    from app.blueprints.feedback import feedback_bp
    from app.blueprints.gallery import gallery_bp
    from app.blueprints.events import events_bp
    from app.blueprints.about import about_bp
    from app.blueprints.projects import projects_bp
    from app.blueprints.opensource import opensource_bp
    from app.blueprints.competitions.competition import competitions_bp
    from app.blueprints.competitions.auth import auth_bp
    from app.blueprints.recruitment import recruitment_bp
    from app.blueprints.api import api_bp
    from app.blueprints.tmp import form_bp
    from app.blueprints.media_kit import media_kit_bp
    from app.blueprints.interview import interviews_bp

    limiter.limit("200 per hour")(home_bp)
    limiter.limit("200 per hour")(team_bp)
    limiter.limit("200 per hour")(membership_bp)
    limiter.limit("200 per hour")(join_bp)
    limiter.limit("200 per hour")(feedback_bp)
    limiter.limit("200 per hour")(gallery_bp)
    limiter.limit("200 per hour")(events_bp)
    limiter.limit("200 per hour")(about_bp)
    limiter.limit("200 per hour")(projects_bp)
    limiter.limit("200 per hour")(opensource_bp)
    limiter.limit("200 per hour")(competitions_bp)
    limiter.limit("100 per hour")(auth_bp)
    limiter.limit("200 per hour")(recruitment_bp)
    limiter.limit("100 per hour")(api_bp)
    limiter.limit("80 per hour")(form_bp)
    limiter.limit("200 per hour")(media_kit_bp)

    # Register blueprints
    app.register_blueprint(home_bp)
    app.register_blueprint(team_bp)
    app.register_blueprint(membership_bp)
    app.register_blueprint(join_bp)
    app.register_blueprint(feedback_bp)
    app.register_blueprint(gallery_bp)
    app.register_blueprint(events_bp)
    app.register_blueprint(about_bp)
    app.register_blueprint(projects_bp)
    app.register_blueprint(opensource_bp)
    app.register_blueprint(competitions_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(recruitment_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(form_bp)
    app.register_blueprint(media_kit_bp)
    app.register_blueprint(interviews_bp)

    # Error Handlers
    @app.errorhandler(ProgrammingError)
    def handle_programming_error(error):
        return (
            render_template(
                "errors/sql_error.html",
                message="There was an issue with the database operation.",
                details=str(error),
            ),
            500,
        )

    @app.errorhandler(ProgrammingError)
    def handle_pending_rollback_error(error):
        return (
            render_template(
                "errors/sql_error.html",
                message="A database error occurred, possibly due to a pending rollback.",
                details=str(error),
            ),
            500,
        )

    @app.errorhandler(SQLAlchemyError)
    def handle_sqlalchemy_error(error):
        return (
            render_template(
                "errors/sql_error.html",
                message="A database error occurred.",
                details=str(error),
            ),
            500,
        )

    @app.errorhandler(OperationalError)
    def handle_operational_error(error):
        return (
            render_template(
                "errors/sql_error.html",
                message="A database error occurred.",
                details=str(error),
            ),
            500,
        )

    @app.errorhandler(404)
    def page_not_found(_):
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        return render_template("errors/500.html", message=str(error)), 500

    @app.errorhandler(401)
    def unauthorized(error):
        return render_template("errors/401.html"), 401

    @app.errorhandler(403)
    def forbidden(_):
        return render_template("errors/403.html"), 403

    @app.errorhandler(400)
    def bad_request(_):
        return render_template("errors/400.html"), 400

    @app.errorhandler(429)
    def rate_limit_exceeded(e):
        return render_template("errors/429.html", error=e.description), 400

    @app.errorhandler(Exception)
    def handle_generic_exception(error):
        return (
            render_template(
                "errors/general_error.html",
                message="An unexpected error occurred.",
                details=str(error),
            ),
            500,
        )

    return app
