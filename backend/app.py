# =========================================================
# BAMBOO FORCE AI
# MAIN FLASK APPLICATION
# =========================================================

from flask import Flask
from flask_cors import CORS

# =========================================================
# IMPORT ROUTES
# =========================================================

from backend.routes.detect_behavior import (
    detect_behavior_bp
)

from backend.routes.ride_optimization import (
    ride_optimization_bp
)

# =========================================================
# CREATE FLASK APP
# =========================================================

app = Flask(__name__)

# =========================================================
# ENABLE CORS
# =========================================================

CORS(app)

# =========================================================
# APP CONFIGURATION
# =========================================================

app.config["JSON_SORT_KEYS"] = False

app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True

# =========================================================
# REGISTER BLUEPRINTS
# =========================================================

app.register_blueprint(

    detect_behavior_bp,

    url_prefix="/api/behavior"
)

app.register_blueprint(

    ride_optimization_bp,

    url_prefix="/api/ride"
)

# =========================================================
# HOME ROUTE
# =========================================================

@app.route("/")

def home():

    return {

        "system":
            "Bamboo Force AI",

        "status":
            "RUNNING",

        "engine":
            "Urban Mobility Optimization",

        "version":
            "1.0.0",

        "available_routes": [

            "/api/behavior",

            "/api/ride"
        ]
    }

# =========================================================
# HEALTH CHECK ROUTE
# =========================================================

@app.route("/health")

def health_check():

    return {

        "success": True,

        "server": "ONLINE",

        "backend": "ACTIVE",

        "ai_engine": "RUNNING"
    }

# =========================================================
# ERROR HANDLERS
# =========================================================

@app.errorhandler(404)

def not_found(error):

    return {

        "success": False,

        "message": "Route not found"
    }, 404

@app.errorhandler(500)

def internal_server_error(error):

    return {

        "success": False,

        "message": "Internal server error"
    }, 500

# =========================================================
# MAIN
# =========================================================

if __name__ == "__main__":

    print("\n=========================================")
    print(" BAMBOO FORCE AI BACKEND STARTED ")
    print("=========================================")
    print(" Server Running : http://127.0.0.1:5000")
    print(" Health Route   : /health")
    print("=========================================\n")

    app.run(

        debug=True,

        host="0.0.0.0",

        port=5000
    )