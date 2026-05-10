from flask import Flask

from backend.routes.detect_behavior import (
    detect_behavior_bp
)

from backend.routes.ride_optimization import (
    ride_optimization_bp
)

# =========================================================
# CREATE APP
# =========================================================

app = Flask(__name__)

# =========================================================
# REGISTER BLUEPRINTS
# =========================================================

app.register_blueprint(

    detect_behavior_bp
)

app.register_blueprint(

    ride_optimization_bp
)

# =========================================================
# HOME ROUTE
# =========================================================

@app.route("/")

def home():

    return {

        "message":
            "Bamboo Force AI Backend Running"
    }

# =========================================================
# MAIN
# =========================================================

if __name__ == "__main__":

    app.run(

        debug=True,

        host="0.0.0.0",

        port=5000
    )