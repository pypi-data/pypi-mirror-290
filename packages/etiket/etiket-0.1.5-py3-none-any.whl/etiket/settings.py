import typing

from pydantic import EmailStr
from pydantic_settings import BaseSettings, SettingsConfigDict

from sqlalchemy import URL

class Settings(BaseSettings):
    model_config = SettingsConfigDict(case_sensitive=True)

    ETIKET_NAME: str

    PROFILING: bool = False

    # root user settings
    ETIKET_ADMIN_USERNAME: str
    ETIKET_ADMIN_PASSWORD: str
    ETIKET_ADMIN_EMAIL: EmailStr

    # JWT settings
    ETIKET_TOKEN_ALGORITHM: str = "HS256"    
    ETIKET_TOKEN_SECRET_KEY: str
    ETIKET_TOKEN_EXPIRE_MINUTES: int = 30

    # database settings
    POSTGRES_HOST: str
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    # S3 settings
    S3_LOG_REPORTS_ENDPOINT: str
    S3_LOG_REPORTS_BUCKET: str
    S3_LOG_REPORTS_BUCKET_ID : int = -1 # -1 is a special value for the default bucket for log reports
    S3_LOG_REPORTS_ACCESS_KEY_ID: str
    S3_LOG_REPORTS_SECRET_ACCESS_KEY: str
    S3_LOG_REPORTS_REGION_NAME: typing.Optional[str] = None
    S3_PRESIGN_EXPIRATION_DOWNLOAD: int = 86_400 # 1 day
    S3_PRESIGN_EXPIRATION_UPLOAD: int = 86_400 # 1 day
    S3_MULTIPART_UPLOAD_PARTSIZE: int = 5_242_880 # 5 MB
    S3_MAX_FILE_SIZE : int = 107_374_182_400 # 100 GB
    
    @property
    def db_url(self) -> URL:
        return URL.create("postgresql+psycopg2",
                            username= self.POSTGRES_USER,
                            password= self.POSTGRES_PASSWORD,
                            host= self.POSTGRES_HOST,
                            port= self.POSTGRES_PORT,
                            database= self.POSTGRES_DB)

settings = Settings()
