from pydantic import BaseSettings
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware


class Settings(BaseSettings):
    origins = ["*"]

    class Rdb:
        scheme: str = "postgresql://"
        id: str = "testuser"
        pw: str = "testuser!"
        host: str = "localhost:5432"
        db_name: str = "testdb"


def initialize():
    from test_platform.config.database import Base, engine
    # RDB initialize
    # Create Tables
    Base.metadata.create_all(bind=engine)
    # Drop Tables
    Base.metadata.create_all(bind=engine)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.origins,
        allow_credentials=True,     # cookie 포함 여부를 설정한다. 기본은 False
        allow_methods=["*"],        # 허용할 method를 설정할 수 있으며, 기본값은 'GET'이다.
        allow_headers=["*"],        # 허용할 http header 목록을 설정할 수 있으며 Content-Type, Accept, Accept-Language, Content-Language은 항상 허용된다.
    )


settings = Settings()

# Fast API 초기화
app = FastAPI()
initialize()

from test_platform import api, config, entity, util
