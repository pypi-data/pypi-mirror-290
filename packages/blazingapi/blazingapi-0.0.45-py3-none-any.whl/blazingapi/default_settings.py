DEBUG = True

VIEW_FILES = [
    "blazingapi.auth.views",
    "views",
]

MODEL_FILES = [
    "blazingapi.auth.models",
    "models"
]

MIDDLEWARE_CLASSES = [
    "blazingapi.security.middleware.CorsMiddleware",
    "blazingapi.security.middleware.XFrameOptionsMiddleware",
    "blazingapi.auth.middleware.BearerAuthenticationMiddleware",
]

DB_FILE = "db.sqlite3"

DB_CONNECTION = {
    "driver": "mysql",
    "database": "dbname",
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "2004Nuno!",
}

LOGIN_ENDPOINT = "/api/auth/login"
REGISTER_ENDPOINT = "/api/auth/register"
ME_ENDPOINT = "/api/auth/me"

X_FRAME_OPTIONS = "DENY"

CORS_ALLOWED_ORIGINS = ["*"]
CORS_ALLOWED_METHODS = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
CORS_ALLOWED_HEADERS = ["Content-Type", "Authorization"]
