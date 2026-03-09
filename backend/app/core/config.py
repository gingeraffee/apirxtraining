from __future__ import annotations

import os


class Settings:
    app_name = "AAP Start API"
    app_version = "0.1.0"
    api_prefix = "/api/v1"
    default_cors_origins = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]

    @property
    def cors_origins(self) -> list[str]:
        raw = os.getenv("CORS_ORIGINS")
        if not raw:
            return self.default_cors_origins
        return [origin.strip() for origin in raw.split(",") if origin.strip()]


settings = Settings()
