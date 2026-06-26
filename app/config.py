import os
from pathlib import Path

# -----------------------------------------------------------------------------
# Application
# -----------------------------------------------------------------------------

APP_NAME = "The Glovebox API"
APP_VERSION = "2.0.0"

BASE_DIR = Path(__file__).resolve().parent.parent

# -----------------------------------------------------------------------------
# Database
# -----------------------------------------------------------------------------

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://siteuser:sitepass@localhost:5432/sitedb"
)

# -----------------------------------------------------------------------------
# Uploads
# -----------------------------------------------------------------------------

UPLOAD_DIR = BASE_DIR / "uploads"
CAR_UPLOAD_DIR = UPLOAD_DIR / "cars"
BLOG_UPLOAD_DIR = UPLOAD_DIR / "blog"

# -----------------------------------------------------------------------------
# Security
# -----------------------------------------------------------------------------

SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "change-this-in-production"
)

# -----------------------------------------------------------------------------
# Environment
# -----------------------------------------------------------------------------

DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# -----------------------------------------------------------------------------
# Ensure upload directories exist
# -----------------------------------------------------------------------------

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
CAR_UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
BLOG_UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

