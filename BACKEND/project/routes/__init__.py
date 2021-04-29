from .home import home_bp
from .file import file_bp
from .case import case_bp

def init_app(app):
    app.register_blueprint(home_bp)
    app.register_blueprint(file_bp, url_prefix='/file')
    app.register_blueprint(case_bp, url_prefix='/case')