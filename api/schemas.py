from pydantic import BaseModel


class UrlResponse(BaseModel):
    shortUrl: str
    originalUrl: str

    # Enable ORM Mode to allow processing sqlalchemy db objects
    class Config:
        orm_mode = True


class UrlWithAnalytics(UrlResponse):
    views: int
