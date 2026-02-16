from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # These will be automatically pulled from your .env file
    POSTGRES_PASSWORD: str
    DATABASE_URL: str
    GROK_KEY:str
    
    class Config:
        env_file=".env"
        

get_settings=Settings()
        