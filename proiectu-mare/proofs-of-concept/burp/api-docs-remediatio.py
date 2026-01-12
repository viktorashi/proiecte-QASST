import os
from flask import app

if os.getenv("FLASK_ENV") == "production":
    # Disable Swagger UI
    app.config["SWAGGER_UI_DOC_EXPANSION"] = "none"
