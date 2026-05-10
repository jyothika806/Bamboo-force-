from flask import Flask

from backend.routes.detect_behavior import (
    detect_behavior_bp
)

# =========================================================
# FLASK APP
# =========================================================

app = Flask(__name__)

# =========================================================
# REGISTER BLUEPRINTS
# =========================================================

app.register_blueprint(
    detect_behavior_bp
)

# =========================================================
# HOME ROUTE
# =========================================================

@app.route("/")

def home():

    return {

        "message": "Bamboo Force Backend Running"
    }

# =========================================================
# RUN SERVER
# =========================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )