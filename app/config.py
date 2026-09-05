"""
CENTRALIZED APPLICATION CONFIGURATION.

All environment variables are loaded once here and exposed via the
'settings' object so the rest of the codebase never touches
os.environ directly.
"""

import os

from dotenv import load_dotenv


load_dotenv()


class Settings:
    """Application settings loaded from environment variables."""

    # MongoDB
    MONGO_URI: str = os.getenv(
        "MONGO_URI",
        "mongodb://localhost:27017"
    )

    MONGO_DB_NAME: str = os.getenv(
        "MONGO_DB_NAME",
        "office_management_db"
    )

    # JWT
    JWT_SECRET_KEY: str = os.getenv(
        "JWT_SECRET_KEY",
        "change_me_into_creating_humanity"
    )

    JWT_ALGORITHM: str = os.getenv(
        "JWT_ALGORITHM",
        "HS256"
    )

    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
        os.getenv(
            "ACCESS_TOKEN_EXPIRE_MINUTES",
            "60"
        )
    )

    # File uploads
    UPLOAD_DIR: str = os.getenv(
        "UPLOAD_DIR",
        "uploads"
    )

    MAX_UPLOAD_SIZE_MB: int = int(
        os.getenv(
            "MAX_UPLOAD_SIZE_MB",
            "5"
        )
    )

    ALLOWED_IMAGE_EXTENSIONS: set = {
        ".jpg",
        ".jpeg",
        ".png",
        ".webp"
    }

    # CORS
    ALLOWED_ORIGINS: list = [
        origin.strip()
        for origin in os.getenv(
            "ALLOWED_ORIGINS",
            "*"
        ).split(",")
    ]


settings = Settings()


# Ensure the upload directory exists at import time
os.makedirs(
    settings.UPLOAD_DIR,
    exist_ok=True
)