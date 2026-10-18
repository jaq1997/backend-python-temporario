from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    RAIO_PADRAO_KM: int = 20

    model_config = {"env_file": ".env"}


settings = Settings()
