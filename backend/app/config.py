from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str
    RAIO_PADRAO_KM: int = 20

    model_config = {"env_file": ".env", "extra": "ignore"}


settings = Settings()
