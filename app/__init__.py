from flask import Flask, render_template


def create_app():
    app = Flask(__name__)

    # Register blueprints
    from app.blueprints.home import home_bp
    from app.blueprints.team import team_bp
    from app.blueprints.membership import membership_bp
    from app.blueprints.join import join_bp
    from app.blueprints.gallery import gallery_bp
    from app.blueprints.events import events_bp
    from app.blueprints.about import about_bp

    app.register_blueprint(home_bp)
    app.register_blueprint(team_bp)
    app.register_blueprint(membership_bp)
    app.register_blueprint(join_bp)
    app.register_blueprint(gallery_bp)
    app.register_blueprint(events_bp)
    app.register_blueprint(about_bp)

    # Error Handlers
    @app.errorhandler(404)
    def page_not_found(_):
        return render_template("404.html"), 404

    @app.errorhandler(500)
    def internal_server_error(_):
        return render_template("500.html"), 500

    @app.errorhandler(403)
    def forbidden(_):
        return render_template("403.html"), 403

    @app.errorhandler(400)
    def bad_request(_):
        return render_template("400.html"), 400

    return app
