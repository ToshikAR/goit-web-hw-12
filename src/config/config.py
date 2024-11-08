from decouple import config as conf


class Config:
    __base = conf("POSTQ_DB")
    __user = conf("POSTQ_USER")
    __password = conf("POSTQ_PASSWORD")
    __host = conf("POSTQ_HOST")
    __port = conf("POSTQ_PORT")

    DB_URL = f"postgresql+asyncpg://{__user}:{__password}@{__host}:{__port}/{__base}"


config = Config
secret_key = conf("SECRET_KEY")
