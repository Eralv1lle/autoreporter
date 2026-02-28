from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    BOT_TOKEN: str
    GEMINI_API: str
    DOCS_DIRECTORY: str
    USER: str
    PASSWORD: str
    HOST: str
    PORT: int
    DATABASE: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


config = Config() # type: ignore