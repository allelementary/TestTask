from flask import Flask
import app_config


def create_app():
    app = Flask(__name__, static_folder='static')
    app.config.from_pyfile('app_config.py')
    app.secret_key = app_config.secret_key
    # import and init database
    from models.db import db
    db.app = app
    db.init_app(app)
    # import and register views
    from views.authentication import authentication_view
    from views.dashboard import dashboard_view
    from views.async_requests import async_view

    app.register_blueprint(authentication_view, url_prefix="/")
    app.register_blueprint(dashboard_view, url_prefix="/dashboard")
    app.register_blueprint(async_view, url_prefix="/async")

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
