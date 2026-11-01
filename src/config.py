"""All settings are read from the .env file."""
import os
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env",override=True)  # override so we can run from the src/ folder


def _path(name, default):
    p = Path(os.getenv(name, default))
    return p if p.is_absolute() else ROOT / p


GROQ_API_KEY = os.getenv("GROQ_API_KEY", "").strip()
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
GROQ_TEMPERATURE = float(os.getenv("GROQ_TEMPERATURE", "0.3"))
REPLY_LANGUAGE = os.getenv("REPLY_LANGUAGE", "English")

MODEL_PATH = _path("MODEL_PATH", "models/plant_model.keras")
CLASS_NAMES_PATH = _path("CLASS_NAMES_PATH", "models/class_names.json")
IMG_SIZE = int(os.getenv("IMG_SIZE", "224"))
MIN_CONFIDENCE = float(os.getenv("MIN_CONFIDENCE", "0.6"))


def problems():
    """Return a list of setup problems (empty list means everything is fine)."""
    found = []
    if not GROQ_API_KEY or GROQ_API_KEY.startswith("paste_"):
        found.append("GROQ_API_KEY is missing. Open the .env file and paste your Groq key after GROQ_API_KEY=")
    for p in (MODEL_PATH, CLASS_NAMES_PATH):
        if not p.exists():
            found.append(f"File not found: {p}. Check MODEL_PATH / CLASS_NAMES_PATH in .env")
    return found
