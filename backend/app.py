from flask import Flask
from ai_models.face_verification.register_driver import register_bp

# =========================================================
# CREATE FLASK APP
# =========================================================

app = Flask(__name__)

# =========================================================
# REGISTER BLUEPRINTS
# =========================================================

app.register_blueprint(register_bp)

# =========================================================
# ROOT ROUTE
# =========================================================

@app.route("/")
def home():
    return {
        "success": True,
        "message": "SecureRide AI Backend Running"
    }

# =========================================================
# RUN SERVER
# =========================================================

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )