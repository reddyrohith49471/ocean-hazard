import os
import sys
from flask import Flask

# Add project root to sys.path
ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(ROOT_DIR, "src"))

# Import blueprints
from routes.home_routes import home_bp
from routes.post_routes import post_bp
from routes.map_routes import map_bp

# Import DB
from databases.mongo_db import MongoDB


def create_app():
    app = Flask(
        __name__,
        template_folder="../frontend/templates",
        static_folder="../frontend/static"
    )

    app.secret_key = "ocean_secret_key"

    # Attach DB
    app.db = MongoDB()

    # Register blueprints
    app.register_blueprint(home_bp)
    app.register_blueprint(post_bp)
    app.register_blueprint(map_bp)

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
