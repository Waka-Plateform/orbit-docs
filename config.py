from dataclasses import dataclass, field
import os


@dataclass
class Settings:
    PORT: int = 8000
    LOG_LEVEL: str = "INFO"
    GITHUB_TOKEN: str = field(
        default_factory=lambda: os.environ.get("GITHUB_TOKEN", "")
    )


settings = Settings()
