class Config:
    OCR_API_KEY = ""
    OCR_BASE_URL = "https://ocrbot.ru/api/v1"

    LLM_BACK = "ollama"
    LLM_MODEL = "qwen2.5:14b-instruct-q4_K_M"
    LLM_URL = "http://localhost:11434"
    LLM_TEMPERATURE = 0.0
    LLM_MAX_TOKENS = 512
    LLM_MAX_CTX = 12248

    DB_HOST = "localhost"
    DB_PORT = 5432
    DB_NAME = "ocr"
    DB_USER = "postgres"
    DB_PASSWORD = "1"
    DB_TABLE = "llm_learned_fields"

    S3_ACCESS_KEY = ""
    S3_SECRET_KEY = ""
    S3_BUCKET = "ocr-s3"
    S3_ENDPOINT = "https://storage.yandexcloud.net"

    @property
    def db_dsn(self) -> str:
        return (
            f"dbname={self.DB_NAME} "
            f"user={self.DB_USER} "
            f"password={self.DB_PASSWORD} "
            f"host={self.DB_HOST} "
            f"port={self.DB_PORT}"
        )