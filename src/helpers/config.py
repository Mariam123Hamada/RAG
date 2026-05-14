from pydantic_settings import BaseSettings
class Settings(BaseSettings):
    POSTGRES_PASSWORD: str
    DATABASE_URL: str
    GROK_KEY: str
    EMBEDDING_MODEL_COHER: str
    GENERTION_MODEL: str
    COHERE_KEY: str
    GEMMNI_KEY : str
    EMBEDDING_MODEL_GEMMNI : str
    EMBEDDING_PROVIDER:str
    
    
    class Config:
        env_file = ".env"

get_settings = Settings()
