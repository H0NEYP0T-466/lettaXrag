from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    mongodb_uri: str = "mongodb://localhost:27017/lettaXrag"
    longcat_api_key: str
    letta_api_key: Optional[str] = None
    letta_base_url: Optional[str] = "http://localhost:8283"  # Default to local Letta server
    data_folder: str = "./data"
    history_file_path: str = "./data/history.txt"
    faiss_index_path: str = "./storage/faiss_index.bin"
    metadata_path: str = "./storage/doc_metadata.json"
    file_hash_path: str = "./storage/file_hashes.json"
    log_level: str = "DEBUG"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
