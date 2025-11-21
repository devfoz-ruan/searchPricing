from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str
    secret_key: str
    port: int
    api_nota_url: str
    database_url: str

    class Config:
        env_file = ".env"  # diz de onde carregar

settings = Settings()
