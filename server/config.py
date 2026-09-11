import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")


def _to_bool(value: str, default: bool = False) -> bool:
    if value is None:
        return default
    return value.strip().lower() == "true"


GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
OPENROUTER_BASE_URL = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "google/gemini-2.0-flash-001")
OPENROUTER_APP_NAME = os.getenv("OPENROUTER_APP_NAME", "AgriAdvisor")

AGMARKNET_API_KEY = os.getenv("AGMARKNET_API_KEY", "")
AGMARKNET_API_URL = os.getenv(
    "AGMARKNET_API_URL",
    "https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070",
)
AGMARKNET_ENABLED = _to_bool(os.getenv("AGMARKNET_ENABLED"), True)

SARVAM_API_KEY = os.getenv("SARVAM_API_KEY", "")
default_db_path = BASE_DIR / "db" / "agriadvisor.db"
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{default_db_path.as_posix()}")
IMAGE_STORAGE_PATH = os.getenv("IMAGE_STORAGE_PATH", str(BASE_DIR / "static"))
WEATHER_ENABLED = _to_bool(os.getenv("WEATHER_ENABLED"), True)
MANDI_ENABLED = _to_bool(os.getenv("MANDI_ENABLED"), True)
DEMO_CACHE_ENABLED = _to_bool(os.getenv("DEMO_CACHE_ENABLED"), True)
SERVER_HOST = os.getenv("SERVER_HOST", "0.0.0.0")
SERVER_PORT = int(os.getenv("PORT", os.getenv("SERVER_PORT", "8000")))
