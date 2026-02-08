from pydantic import BaseSettings

class Config(BaseSettings):
    POSTGRES_PASSWORD:str
    
    class Config:
        env_file=".env"
        

get_settings=Config()
        