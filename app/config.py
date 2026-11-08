import os
from functools import lru_cache

from dotenv import load_dotenv

load_dotenv()


@lru_cache
def get_settings() -> "Settings":
    return Settings()


class Settings:
    storage_backend: str
    database_url: str | None

    def __init__(self) -> None:
        self.database_url = os.getenv("DATABASE_URL")
        backend = os.getenv("STORAGE_BACKEND", "").strip().lower()
        if backend in ("memory", "postgres"):
            self.storage_backend = backend
        elif self.database_url:
            self.storage_backend = "postgres"
        else:
            self.storage_backend = "memory"
